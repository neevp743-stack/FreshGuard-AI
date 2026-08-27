from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, HouseholdMember, ShoppingCart, ShoppingCartItem, Recommendation
from app.schemas.schemas import CartOut, CartItemCreate, CartItemOut
from app.services.grocery_provider import MockGroceryProvider

router = APIRouter(prefix="/cart", tags=["Smart Grocery Cart"])
provider = MockGroceryProvider()

def get_or_create_cart(household_id: int, db: Session) -> ShoppingCart:
    cart = db.query(ShoppingCart).filter(
        ShoppingCart.household_id == household_id,
        ShoppingCart.status == "active"
    ).first()
    if not cart:
        cart = ShoppingCart(household_id=household_id, status="active", total_estimated_price=0.0)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.get("", response_model=CartOut)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="Household not assigned")
    cart = get_or_create_cart(member.household_id, db)

    # Recalculate total estimated price
    total = sum(item.estimated_price * item.quantity for item in cart.items)
    cart.total_estimated_price = round(total, 2)
    db.commit()
    return cart

@router.post("/items", response_model=CartItemOut)
def add_cart_item(
    item_in: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    cart = get_or_create_cart(member.household_id, db)

    price = item_in.estimated_price or provider.get_price(item_in.product_name)

    item = ShoppingCartItem(
        cart_id=cart.id,
        product_name=item_in.product_name,
        quantity=item_in.quantity,
        unit=item_in.unit,
        estimated_price=price,
        reason=item_in.reason or "Smart Cart Recommendation",
        priority=item_in.priority or "Normal"
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/items/{id}")
def delete_cart_item(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(ShoppingCartItem).filter(ShoppingCartItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return {"status": "success", "message": "Item removed from cart"}

@router.post("/confirm")
def confirm_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Explicit User Confirmation endpoint.
    Performs user-approved mock checkout.
    """
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    cart = db.query(ShoppingCart).filter(
        ShoppingCart.household_id == member.household_id,
        ShoppingCart.status == "active"
    ).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    mock_res = provider.checkout(f"H{member.household_id}")

    # Mark cart as confirmed and create new active cart
    cart.status = "confirmed"
    for item in cart.items:
        item.confirmed = True

    # Clear recommendations marked as added_to_cart
    db.query(Recommendation).filter(Recommendation.household_id == member.household_id).update({"added_to_cart": True})

    db.commit()

    # Create fresh active cart
    get_or_create_cart(member.household_id, db)

    return {
        "status": "success",
        "message": "Order confirmed by user!",
        "order_details": mock_res
    }
