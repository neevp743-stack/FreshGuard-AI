from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Inventory, Recommendation, ShoppingCart, ShoppingCartItem
from app.ai.consumption import predict_item_consumption

def generate_reorder_recommendations(household_id: int, db: Session) -> List[Recommendation]:
    """
    AI Reorder Recommendation Engine.
    Evaluates current inventory stock, predicted runout dates, and expiry risks
    to auto-generate smart grocery recommendations for the household.
    """
    inventory_items = db.query(Inventory).filter(Inventory.household_id == household_id).all()
    recommendations = []

    for item in inventory_items:
        prediction = predict_item_consumption(item, db)
        now = datetime.utcnow()
        
        # Calculate days until expiry
        days_to_expiry = None
        if item.expiry_date:
            days_to_expiry = (item.expiry_date - now).days

        reason = None
        urgency = "Low"
        priority = 3

        # Rule 1: Item running low (<= 2 days remaining or quantity <= 0.5)
        if prediction.estimated_days_remaining > 0 and prediction.estimated_days_remaining <= 2:
            reason = f"Running low (Estimated {prediction.estimated_days_remaining} days remaining)"
            urgency = "High"
            priority = 1
        elif item.quantity <= 0.5:
            reason = "Stock critically low"
            urgency = "High"
            priority = 1
        # Rule 2: Item expired or expiring within 1 day
        elif days_to_expiry is not None and days_to_expiry <= 1:
            reason = "Expiring soon or expired - replacement needed"
            urgency = "Medium"
            priority = 2

        if reason:
            # Check if recommendation already exists to prevent duplicate spam
            existing = db.query(Recommendation).filter(
                Recommendation.household_id == household_id,
                Recommendation.product_name == item.product_name,
                Recommendation.added_to_cart == False
            ).first()

            if not existing:
                rec = Recommendation(
                    household_id=household_id,
                    product_name=item.product_name,
                    category=item.category,
                    suggested_quantity=1.0 if item.quantity < 1 else item.quantity,
                    unit=item.unit,
                    reason=reason,
                    urgency=urgency,
                    priority=priority
                )
                db.add(rec)
                db.commit()
                db.refresh(rec)
                recommendations.append(rec)
            else:
                recommendations.append(existing)

    return db.query(Recommendation).filter(
        Recommendation.household_id == household_id,
        Recommendation.added_to_cart == False
    ).order_by(Recommendation.priority.asc()).all()
