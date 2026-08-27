from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Notification, DeviceToken, HouseholdMember
from app.schemas.schemas import NotificationOut, DeviceTokenCreate, DeviceTokenOut
from app.services.notifications import evaluate_and_generate_notifications

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationOut])
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if member:
        evaluate_and_generate_notifications(current_user.id, member.household_id, db)

    return db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()

@router.put("/{id}/read")
def mark_notification_read(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notif = db.query(Notification).filter(
        Notification.id == id,
        Notification.user_id == current_user.id
    ).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    notif.is_read = True
    db.commit()
    return {"status": "success", "message": "Notification marked as read"}

@router.post("/device-token", response_model=DeviceTokenOut)
def register_device_token(
    token_in: DeviceTokenCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Registers a new FCM device token for the authenticated user's device.
    Supports multiple devices per user account.
    """
    if not token_in.token or not token_in.token.strip():
        raise HTTPException(status_code=400, detail="Device token string required")

    # Check if token already registered for user
    existing = db.query(DeviceToken).filter(
        DeviceToken.user_id == current_user.id,
        DeviceToken.token == token_in.token.strip()
    ).first()

    if existing:
        existing.is_active = True
        existing.platform = token_in.platform or "android"
        db.commit()
        db.refresh(existing)
        return existing

    new_token = DeviceToken(
        user_id=current_user.id,
        token=token_in.token.strip(),
        platform=token_in.platform or "android",
        is_active=True
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token
