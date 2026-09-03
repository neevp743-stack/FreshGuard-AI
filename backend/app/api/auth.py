import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_and_migrate_password, create_access_token, get_current_user
from app.models.models import User, Household, HouseholdMember, UserPreference
from app.schemas.schemas import UserRegister, UserLogin, TokenResponse, HouseholdOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=TokenResponse,
    summary="Register New User & Household",
    description="Registers a new user account with PBKDF2 password hashing, creates a default household and user preferences."
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if email exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Create User
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name or user_data.email.split("@")[0].title(),
        role=user_data.role or "USER"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create default User Preference
    pref = UserPreference(user_id=new_user.id)
    db.add(pref)

    # Create Household
    join_code = f"FG-{secrets.token_hex(3).upper()}"
    household_name = user_data.household_name or f"{new_user.full_name}'s Home"
    household = Household(
        name=household_name,
        join_code=join_code,
        owner_id=new_user.id
    )
    db.add(household)
    db.commit()
    db.refresh(household)

    # Add as Owner
    member = HouseholdMember(household_id=household.id, user_id=new_user.id, role="owner")
    db.add(member)
    db.commit()

    token = create_access_token({"sub": new_user.id})
    return TokenResponse(
        access_token=token,
        user_id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        role=new_user.role,
        household_id=household.id,
        household_name=household.name
    )

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate User & Issue JWT",
    description="Authenticates email and password using PBKDF2-HMAC-SHA256, transparently re-hashes legacy credentials, and returns JWT access token."
)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    is_valid, needs_rehash = verify_and_migrate_password(login_data.password, user.password_hash)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Transparently re-hash legacy SHA256 password to secure PBKDF2
    if needs_rehash:
        user.password_hash = hash_password(login_data.password)
        db.commit()
        db.refresh(user)

    # Find primary household
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == user.id).first()
    household_id = member.household_id if member else 1
    household = db.query(Household).filter(Household.id == household_id).first()
    h_name = household.name if household else "My Kitchen"

    token = create_access_token({"sub": user.id})
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role or "USER",
        household_id=household_id,
        household_name=h_name
    )

@router.get(
    "/me",
    summary="Get Authenticated User Profile",
    description="Fetches current user account details, assigned role, household ID, and join code."
)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    household = db.query(Household).filter(Household.id == member.household_id).first() if member else None
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": getattr(current_user, "role", "USER"),
        "household_id": household.id if household else None,
        "household_name": household.name if household else None,
        "join_code": household.join_code if household else None
    }

