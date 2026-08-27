from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Inventory, HouseholdMember
from app.schemas.schemas import InventoryOut
from app.services.freshness import (
    calculate_freshness_status,
    get_freshness_summary,
    get_use_first_recommendations,
    get_freshness_alerts
)

router = APIRouter(prefix="/freshness", tags=["Freshness Intelligence"])

@router.get("/summary")
def freshness_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns real database-derived summary counts of user inventory:
    total, fresh, use_soon, expired, unknown
    """
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    items = db.query(Inventory).filter(Inventory.household_id == member.household_id).all()
    return get_freshness_summary(items)

@router.get("/items", response_model=List[InventoryOut])
def freshness_items(
    status: Optional[str] = Query(None, description="Filter by status: FRESH, USE_SOON, EXPIRED, UNKNOWN"),
    category: Optional[str] = None,
    location: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns inventory items with calculated freshness status and remaining days.
    """
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    query = db.query(Inventory).filter(Inventory.household_id == member.household_id)

    if category and category != "All":
        query = query.filter(Inventory.category == category)
    if location and location != "All":
        query = query.filter(Inventory.storage_location == location)

    items = query.order_by(Inventory.expiry_date.asc().nullslast()).all()
    results = []

    for item in items:
        st, days = calculate_freshness_status(item.expiry_date, item.purchase_date)
        item.status = st
        if status and status != "All" and st != status:
            continue
        out = InventoryOut.from_orm(item)
        out.days_until_expiry = days
        results.append(out)

    return results

@router.get("/use-first")
def use_first_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns prioritized list of items to consume first based on expiration dates.
    Expired items are strictly separated under 'Review / Remove'.
    """
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    items = db.query(Inventory).filter(Inventory.household_id == member.household_id).all()
    return get_use_first_recommendations(items)

@router.get("/alerts")
def freshness_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns urgent freshness alert notifications derived from the user's active inventory.
    """
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    items = db.query(Inventory).filter(Inventory.household_id == member.household_id).all()
    return get_freshness_alerts(items)
