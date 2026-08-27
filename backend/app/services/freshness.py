"""
FreshGuard AI — Centralized Freshness Calculation Engine & Use-First Recommendation Intelligence.
All freshness determinations are date-based and derived from user/manufacturer expiry dates
or estimated shelf-life rules.
"""

from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
from app.models.models import Inventory

def calculate_freshness_status(expiry_date: Optional[datetime], purchase_date: Optional[datetime] = None) -> Tuple[str, Optional[int]]:
    """
    Calculates timezone-safe freshness status and remaining days until expiration.
    Returns tuple: (status, days_until_expiry)
    Status options: "FRESH", "USE_SOON", "EXPIRED", "UNKNOWN"
    """
    if not expiry_date:
        return "UNKNOWN", None

    today = datetime.utcnow().date()
    exp_date = expiry_date.date() if isinstance(expiry_date, datetime) else expiry_date
    days = (exp_date - today).days

    if days < 0:
        return "EXPIRED", days
    elif days <= 2:
        return "USE_SOON", days
    else:
        return "FRESH", days

def get_freshness_summary(items: List[Inventory]) -> Dict[str, int]:
    """
    Calculates summary metrics derived directly from real inventory items.
    Returns: {"total": N, "fresh": N, "use_soon": N, "expired": N, "unknown": N}
    """
    summary = {"total": len(items), "fresh": 0, "use_soon": 0, "expired": 0, "unknown": 0}

    for item in items:
        status, _ = calculate_freshness_status(item.expiry_date, item.purchase_date)
        if status == "FRESH":
            summary["fresh"] += 1
        elif status == "USE_SOON":
            summary["use_soon"] += 1
        elif status == "EXPIRED":
            summary["expired"] += 1
        else:
            summary["unknown"] += 1

    return summary

def get_use_first_recommendations(items: List[Inventory]) -> List[Dict[str, Any]]:
    """
    Determines consumption priority recommendations.
    EXPIRED items are separated into 'Review / Remove' (NEVER recommended to eat).
    USE_SOON and FRESH items are sorted by nearest expiration date.
    """
    active_items = [i for i in items if i.quantity > 0]
    results = []

    for item in active_items:
        status, days = calculate_freshness_status(item.expiry_date, item.purchase_date)

        if status == "EXPIRED":
            recommendation_action = "Review / Remove"
            guidance = f"Item expired {abs(days)} day(s) ago. Inspect for spoilage before discarding or composting. Do not consume expired food."
            priority_score = 1
        elif status == "USE_SOON":
            recommendation_action = "Consume First"
            if days == 0:
                guidance = "Expires today! Prioritize consuming this item today."
            elif days == 1:
                guidance = "Expires tomorrow! Use in your next meal."
            else:
                guidance = f"Expires in {days} days. Consume soon."
            priority_score = 2
        elif status == "FRESH":
            recommendation_action = "Use Next"
            guidance = f"Fresh. Estimated {days} days of remaining shelf life."
            priority_score = 3
        else:
            recommendation_action = "Add Expiry Date"
            guidance = "Expiry date is currently unknown. Add an expiry date to enable freshness tracking."
            priority_score = 4

        results.append({
            "id": item.id,
            "product_name": item.product_name,
            "category": item.category,
            "quantity": item.quantity,
            "unit": item.unit,
            "storage_location": item.storage_location,
            "purchase_date": item.purchase_date.isoformat() if item.purchase_date else None,
            "expiry_date": item.expiry_date.isoformat() if item.expiry_date else None,
            "status": status,
            "days_until_expiry": days,
            "recommendation_action": recommendation_action,
            "guidance": guidance,
            "priority_score": priority_score,
            "is_expiry_estimated": item.notes and "estimated" in item.notes.lower()
        })

    # Sort: Expiry review first, then nearest expiry date
    results.sort(key=lambda x: (x["priority_score"], x["days_until_expiry"] if x["days_until_expiry"] is not None else 9999))
    return results

def get_freshness_alerts(items: List[Inventory]) -> List[Dict[str, Any]]:
    """
    Identifies urgent freshness alert objects for dashboard notifications.
    Categorizes: EXPIRED, EXPIRES_TODAY, EXPIRES_TOMORROW, EXPIRING_SOON
    """
    alerts = []

    for item in items:
        if item.quantity <= 0:
            continue
        status, days = calculate_freshness_status(item.expiry_date, item.purchase_date)

        if status == "EXPIRED":
            alerts.append({
                "type": "EXPIRED",
                "item_id": item.id,
                "item": item.product_name,
                "days_remaining": days,
                "severity": "high",
                "message": f"🔴 {item.product_name} expired {abs(days)} day(s) ago — Review / Remove"
            })
        elif status == "USE_SOON":
            if days == 0:
                alerts.append({
                    "type": "EXPIRES_TODAY",
                    "item_id": item.id,
                    "item": item.product_name,
                    "days_remaining": 0,
                    "severity": "high",
                    "message": f"⚠️ {item.product_name} expires today — Use First!"
                })
            elif days == 1:
                alerts.append({
                    "type": "EXPIRES_TOMORROW",
                    "item_id": item.id,
                    "item": item.product_name,
                    "days_remaining": 1,
                    "severity": "medium",
                    "message": f"⚠️ {item.product_name} expires tomorrow — Use First!"
                })
            else:
                alerts.append({
                    "type": "EXPIRING_SOON",
                    "item_id": item.id,
                    "item": item.product_name,
                    "days_remaining": days,
                    "severity": "medium",
                    "message": f"⚠️ {item.product_name} expires in {days} days"
                })

    alerts.sort(key=lambda a: a["days_remaining"])
    return alerts
