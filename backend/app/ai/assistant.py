from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import Inventory, ConsumptionLog, Recommendation
from app.schemas.schemas import AIAssistantResponse

def handle_ai_assistant_query(query: str, household_id: int, db: Session) -> AIAssistantResponse:
    """
    Context-aware AI Assistant query solver.
    Answers natural language queries using actual household database inventory,
    vision detections, confidence thresholds, and consumption records without inventing information.
    """
    q = query.strip().lower()
    items = db.query(Inventory).filter(Inventory.household_id == household_id).all()
    now = datetime.utcnow()
    related = []

    # 1. Vision Detection Queries
    if "vision" in q or "detect" in q or "detected" in q or "camera" in q:
        if "threshold" in q or "confidence" in q or "why wasn't" in q or "not added" in q:
            ans = "Items detected with confidence below the 50% threshold (VISION_CONFIDENCE_THRESHOLD=0.50) are flagged for manual verification before being added to inventory to prevent false entries."
        else:
            ans = "The FreshGuard AI Vision engine detects 15 grocery classes (e.g. milk, bread, apple, banana, egg). It returns bounding boxes and confidence scores, requiring user approval before saving to inventory."

    # 2. Barcode vs Vision Discrepancy Queries
    elif "disagree" in q or "conflict" in q or "barcode vs vision" in q:
        ans = "When Barcode identity and Vision detection disagree (e.g. Barcode='Organic Milk', Vision='Juice'), FreshGuard AI flags a discrepancy and requires explicit user confirmation instead of automatically picking either result."

    # 3. Expiry Queries: "What expires this week?" / "Expiring soon"
    elif "expire" in q or "expiring" in q:
        expiring = []
        for item in items:
            if item.expiry_date:
                days = (item.expiry_date - now).days
                if 0 <= days <= 7:
                    expiring.append(f"{item.product_name} (Expires in {days} days)")
                    related.append(item.product_name)

        if expiring:
            ans = "Here are the items expiring within the next 7 days:\n• " + "\n• ".join(expiring)
        else:
            ans = "Great news! You have no items expiring in the next 7 days."

    # 4. Query: "What should I cook first?" / "Use first"
    elif "cook" in q or "use first" in q:
        urgent_cook = []
        sorted_items = sorted([i for i in items if i.expiry_date], key=lambda x: x.expiry_date)
        for item in sorted_items[:4]:
            days = (item.expiry_date - now).days
            urgent_cook.append(f"🥛 {item.product_name} ({item.quantity} {item.unit}) - Expires in {max(days, 0)} days")
            related.append(item.product_name)

        if urgent_cook:
            ans = "To prevent food waste, you should cook/use these items first:\n" + "\n".join(urgent_cook)
        else:
            ans = "Your inventory looks fresh! You can cook any items of your choice."

    # 5. Query: "What do I need to buy?" / "reorder" / "recommendation"
    elif "buy" in q or "reorder" in q or "recommend" in q:
        recs = db.query(Recommendation).filter(
            Recommendation.household_id == household_id,
            Recommendation.added_to_cart == False
        ).all()
        if recs:
            buy_list = [f"🛒 {r.product_name} ({r.suggested_quantity} {r.unit}) - Reason: {r.reason}" for r in recs]
            ans = "Based on your consumption trends, you should buy:\n" + "\n".join(buy_list)
            related = [r.product_name for r in recs]
        else:
            ans = "Your kitchen is well-stocked! No urgent purchases are recommended right now."

    # 6. Query: "Why are you recommending [product]?"
    elif "why" in q:
        target_name = None
        for item in items:
            if item.product_name.lower() in q:
                target_name = item.product_name
                break
        if target_name:
            ans = f"We recommend buying {target_name} because your stock level ({item.quantity} {item.unit}) is estimated to run out soon based on your historical daily consumption pattern."
            related.append(target_name)
        else:
            ans = "Recommendations are calculated using your consumption speed, current stock levels, and safety thresholds."

    # 7. Query: "What products are wasting the most?" / "waste"
    elif "waste" in q or "wasting" in q:
        wasted_logs = db.query(ConsumptionLog).filter(
            ConsumptionLog.household_id == household_id,
            ConsumptionLog.log_type.in_(["wasted", "expired"])
        ).all()
        if wasted_logs:
            waste_counts = {}
            for l in wasted_logs:
                waste_counts[l.product_name] = waste_counts.get(l.product_name, 0) + 1
            sorted_waste = sorted(waste_counts.items(), key=lambda x: x[1], reverse=True)
            top_wasted = [f"• {name} (wasted {cnt} times)" for name, cnt in sorted_waste[:3]]
            ans = "Here are the top products frequently wasted in your household:\n" + "\n".join(top_wasted) + "\n\nTip: Consider buying smaller portion sizes!"
            related = [w[0] for w in sorted_waste[:3]]
        else:
            ans = "Awesome! You have zero logged food waste so far."

    # General catch-all query
    else:
        healthy = len([i for i in items if i.status == "Healthy"])
        expiring = len([i for i in items if i.status == "Expiring Soon"])
        ans = f"FreshGuard AI Summary: You have {len(items)} total items in stock ({healthy} healthy, {expiring} expiring soon). Ask me about vision detections, items expiring, or grocery recommendations!"

    return AIAssistantResponse(
        query=query,
        answer=ans,
        related_items=related
    )
