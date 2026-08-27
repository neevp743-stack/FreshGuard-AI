import math
import statistics
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import Inventory, ConsumptionLog
from app.schemas.schemas import ConsumptionPrediction

def predict_item_consumption(inventory_item: Inventory, db: Session) -> ConsumptionPrediction:
    """
    AI Engine for item consumption and run-out date prediction.
    Uses historical consumption logs, Moving Average (MA), and Exponential Moving Average (EMA).
    Built in pure Python for 100% cross-platform compatibility.
    """
    item_name = inventory_item.product_name
    current_stock = inventory_item.quantity
    unit = inventory_item.unit

    # Query historical consumption logs for this household & product
    logs = db.query(ConsumptionLog).filter(
        ConsumptionLog.household_id == inventory_item.household_id,
        ConsumptionLog.product_name.ilike(f"%{item_name}%"),
        ConsumptionLog.log_type == "consumed"
    ).order_by(ConsumptionLog.date_consumed.asc()).all()

    # Rule: If insufficient data (< 2 logs), return cold start prediction
    if len(logs) < 2:
        return ConsumptionPrediction(
            product_name=item_name,
            current_quantity=current_stock,
            unit=unit,
            avg_daily_consumption=0.0,
            estimated_days_remaining=0.0,
            predicted_runout_date=None,
            confidence_score=0.0,
            status_message="Not enough data yet. Keep using FreshGuard AI and we'll learn your consumption pattern."
        )

    # Extract dates and quantities
    quantities = [log.quantity_consumed for log in logs]
    dates = [log.date_consumed for log in logs]

    first_date = dates[0]
    last_date = dates[-1]
    days_span = max((last_date - first_date).days, 1)

    total_consumed = sum(quantities)
    avg_daily = total_consumed / days_span

    # Apply Exponential Moving Average (EMA) smoothing for recent trends
    if len(quantities) >= 3:
        alpha = 0.5
        ema = quantities[0]
        for q in quantities[1:]:
            ema = alpha * q + (1 - alpha) * ema
        avg_daily = (0.4 * avg_daily) + (0.6 * (ema / max(days_span / len(quantities), 1.0)))

    # Calculate model confidence score
    confidence = min(round(len(logs) * 20.0, 1), 94.0)

    # Calculate estimated remaining days
    if avg_daily > 0:
        days_remaining = round(current_stock / avg_daily, 1)
        predicted_date = (datetime.utcnow() + timedelta(days=days_remaining)).strftime("%Y-%m-%d")
        status_msg = f"You consume ~{avg_daily:.1f} {unit}/day. Estimated to run out in {days_remaining} day(s)."
    else:
        days_remaining = 30.0
        predicted_date = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")
        status_msg = "Stock level is stable."

    return ConsumptionPrediction(
        product_name=item_name,
        current_quantity=current_stock,
        unit=unit,
        avg_daily_consumption=round(avg_daily, 2),
        estimated_days_remaining=days_remaining,
        predicted_runout_date=predicted_date,
        confidence_score=confidence,
        status_message=status_msg
    )
