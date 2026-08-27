from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Inventory, HouseholdMember, ConsumptionLog, PurchaseHistory
from app.schemas.schemas import (
    InventoryCreate, InventoryUpdate, InventoryOut, ConsumptionLogCreate,
    FromDetectionsRequest, BulkInventoryCreate, ConfirmedDetectionItem
)
from app.services.shelf_life import get_class_rule, calculate_estimated_expiry, CLASS_MAPPING_RULES

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

    rule = get_class_rule(item_in.product_name)
    category = item_in.category if item_in.category and item_in.category != "Other" else (rule["category"] if rule else "Other")
    p_date = item_in.purchase_date or datetime.utcnow()
    e_date = item_in.expiry_date or calculate_estimated_expiry(item_in.product_name, p_date)

    new_item = Inventory(
        user_id=current_user.id,
        household_id=member.household_id,
        product_name=item_in.product_name,
        brand=item_in.brand,
        category=category,
        quantity=item_in.quantity,
        unit=item_in.unit,
        storage_location=item_in.storage_location or (rule["default_location"] if rule else "Pantry"),
        purchase_date=p_date,
        expiry_date=e_date,
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

@router.post("/from-detections", response_model=List[InventoryOut])
def add_inventory_from_detections(
    payload: FromDetectionsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Converts confirmed FreshGuard Vision 35-class detections into persistent inventory items.
    Validates class IDs against official 35-class mapping (0..34).
    Rejects invalid or unknown class IDs with HTTP 400.
    """
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    if not payload.items:
        raise HTTPException(status_code=400, detail="No detection items provided")

    new_inventory_items = []
    now = datetime.utcnow()

    for item_in in payload.items:
        if item_in.class_id not in CLASS_MAPPING_RULES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid class_id: {item_in.class_id}. Must be between 0 and 34."
            )

        rule = CLASS_MAPPING_RULES[item_in.class_id]
        prod_name = item_in.name.strip().title() if item_in.name else rule["display_name"]
        category = rule["category"]
        loc = item_in.location or rule["default_location"]
        p_date = item_in.purchase_date or now
        e_date = item_in.expiry_date or (p_date + timedelta(days=rule["shelf_life_days"]))

        inv_item = Inventory(
            user_id=current_user.id,
            household_id=member.household_id,
            product_name=prod_name,
            category=category,
            quantity=max(1.0, item_in.quantity),
            unit=item_in.unit or "pcs",
            storage_location=loc,
            purchase_date=p_date,
            expiry_date=e_date,
            estimated_remaining_quantity=max(1.0, item_in.quantity),
            notes=item_in.notes
        )
        st, days = calculate_status_and_days(inv_item)
        inv_item.status = st
        db.add(inv_item)
        new_inventory_items.append(inv_item)

    db.commit()

    results = []
    for item in new_inventory_items:
        db.refresh(item)
        st, days = calculate_status_and_days(item)
        out = InventoryOut.from_orm(item)
        out.days_until_expiry = days
        results.append(out)

    return results

@router.post("/bulk", response_model=List[InventoryOut])
def add_bulk_inventory_items(
    payload: BulkInventoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atomic creation of multiple inventory items in a single request.
    """
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    created = []
    for item_in in payload.items:
        res = add_inventory_item(item_in=item_in, current_user=current_user, db=db)
        created.append(res)

    return created

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
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    item = db.query(Inventory).filter(Inventory.id == id, Inventory.household_id == member.household_id).first()
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
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    item = db.query(Inventory).filter(Inventory.id == id, Inventory.household_id == member.household_id).first()
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

@router.patch("/{id}", response_model=InventoryOut)
def patch_inventory_item(
    id: int,
    item_in: InventoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_inventory_item(id=id, item_in=item_in, current_user=current_user, db=db)

@router.delete("/{id}")
def delete_inventory_item(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    item = db.query(Inventory).filter(Inventory.id == id, Inventory.household_id == member.household_id).first()
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
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="User not assigned to a household")

    item = db.query(Inventory).filter(Inventory.id == id, Inventory.household_id == member.household_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.quantity = max(0.0, item.quantity - log_in.quantity_consumed)
    item.estimated_remaining_quantity = item.quantity
    st, days = calculate_status_and_days(item)
    item.status = st

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

@router.post("/{id}/consume")
def consume_inventory_item(
    id: int,
    log_in: ConsumptionLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return log_consumption(id=id, log_in=log_in, current_user=current_user, db=db)
