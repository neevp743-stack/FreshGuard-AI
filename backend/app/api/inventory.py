from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Inventory, HouseholdMember, ConsumptionLog, PurchaseHistory
from app.schemas.schemas import InventoryCreate, InventoryUpdate, InventoryOut, ConsumptionLogCreate

router = APIRouter(prefix="/inventory", tags=["Inventory Management"])

def calculate_status_and_days(item: Inventory) -> tuple[str, Optional[int]]:
    days = None
    status = "Healthy"
    now = datetime.utcnow()
    if item.expiry_date:
        days = (item.expiry_date - now).days
        if days < 0:
            status = "Expired"
        elif days <= 2:
            status = "Expiring Soon"
    if status == "Healthy" and item.quantity <= 0.5:
        status = "Running Low"
    return status, days

@router.get("", response_model=List[InventoryOut])
def get_inventory(
    location: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")
    
    query = db.query(Inventory).filter(Inventory.household_id == member.household_id)

    if location and location != "All":
        query = query.filter(Inventory.storage_location == location)
    if category and category != "All":
        query = query.filter(Inventory.category == category)
    if search:
        query = query.filter(Inventory.product_name.ilike(f"%{search}%"))

    items = query.order_by(Inventory.expiry_date.asc().nullslast()).all()
    results = []
    for item in items:
        st, days = calculate_status_and_days(item)
        item.status = st
        item_dict = InventoryOut.from_orm(item)
        item_dict.days_until_expiry = days
        if status and status != "All" and st != status:
            continue
        results.append(item_dict)

    return results

@router.post("", response_model=InventoryOut)
def add_inventory_item(
    item_in: InventoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    new_item = Inventory(
        user_id=current_user.id,
        household_id=member.household_id,
        product_name=item_in.product_name,
        brand=item_in.brand,
        category=item_in.category,
        quantity=item_in.quantity,
        unit=item_in.unit,
        storage_location=item_in.storage_location,
        purchase_date=item_in.purchase_date or datetime.utcnow(),
        expiry_date=item_in.expiry_date,
        opened_date=item_in.opened_date,
        estimated_remaining_quantity=item_in.quantity,
        barcode=item_in.barcode,
        image_url=item_in.image_url,
        notes=item_in.notes
    )
    st, days = calculate_status_and_days(new_item)
    new_item.status = st
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    # Record in purchase history
    history = PurchaseHistory(
        household_id=member.household_id,
        product_name=new_item.product_name,
        category=new_item.category,
        quantity=new_item.quantity,
        unit=new_item.unit,
        purchase_date=new_item.purchase_date or datetime.utcnow()
    )
    db.add(history)
    db.commit()

    out = InventoryOut.from_orm(new_item)
    out.days_until_expiry = days
    return out

@router.get("/expiring", response_model=List[InventoryOut])
def get_expiring_soon(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_inventory(status="Expiring Soon", current_user=current_user, db=db)

@router.get("/expired", response_model=List[InventoryOut])
def get_expired(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_inventory(status="Expired", current_user=current_user, db=db)

@router.get("/{id}", response_model=InventoryOut)
def get_inventory_item(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Inventory).filter(Inventory.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    st, days = calculate_status_and_days(item)
    item.status = st
    out = InventoryOut.from_orm(item)
    out.days_until_expiry = days
    return out

@router.put("/{id}", response_model=InventoryOut)
def update_inventory_item(
    id: int,
    item_in: InventoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Inventory).filter(Inventory.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_in.dict(exclude_unset=True)
    for field, val in update_data.items():
        setattr(item, field, val)

    st, days = calculate_status_and_days(item)
    item.status = st
    db.commit()
    db.refresh(item)
    out = InventoryOut.from_orm(item)
    out.days_until_expiry = days
    return out

@router.delete("/{id}")
def delete_inventory_item(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Inventory).filter(Inventory.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"status": "success", "message": "Item deleted successfully"}

@router.post("/{id}/log-consumption")
def log_consumption(
    id: int,
    log_in: ConsumptionLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Inventory).filter(Inventory.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update item quantity
    item.quantity = max(0.0, item.quantity - log_in.quantity_consumed)
    item.estimated_remaining_quantity = item.quantity
    st, days = calculate_status_and_days(item)
    item.status = st

    # Record consumption log
    log = ConsumptionLog(
        inventory_id=item.id,
        household_id=item.household_id,
        product_name=item.product_name,
        category=item.category,
        quantity_consumed=log_in.quantity_consumed,
        unit=item.unit,
        log_type=log_in.log_type,
        waste_value=log_in.waste_value or 0.0
    )
    db.add(log)
    db.commit()
    db.refresh(item)

    return {"status": "success", "remaining_quantity": item.quantity, "item_status": item.status}
