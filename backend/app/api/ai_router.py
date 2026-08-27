from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, HouseholdMember, Inventory, ConsumptionLog
from app.schemas.schemas import AIInsightSummary, AIRecommendationOut, ConsumptionPrediction, AIAssistantRequest, AIAssistantResponse
from app.ai.consumption import predict_item_consumption
from app.ai.reorder import generate_reorder_recommendations
from app.ai.assistant import handle_ai_assistant_query

router = APIRouter(prefix="/ai", tags=["AI Engine"])

@router.get("/insights", response_model=AIInsightSummary)
def get_ai_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="Household not assigned")

    items = db.query(Inventory).filter(Inventory.household_id == member.household_id).all()
    healthy = 0
    expiring = 0
    expired = 0
    running_low = 0

    for item in items:
        if item.status == "Healthy":
            healthy += 1
        elif item.status == "Expiring Soon":
            expiring += 1
        elif item.status == "Expired":
            expired += 1
        elif item.status == "Running Low":
            running_low += 1

    # Calculate food waste estimate
    waste_logs = db.query(ConsumptionLog).filter(
        ConsumptionLog.household_id == member.household_id,
        ConsumptionLog.log_type.in_(["wasted", "expired"])
    ).all()
    waste_val = sum(l.waste_value for l in waste_logs)

    top_cat = "Dairy"
    insight_msg = "You usually consume 1L of milk every 2 days. Based on your current stock, you may need milk tomorrow."

    return AIInsightSummary(
        healthy_count=healthy,
        expiring_soon_count=expiring,
        expired_count=expired,
        running_low_count=running_low,
        food_waste_estimate=round(waste_val, 2),
        top_consumed_category=top_cat,
        recent_insight_message=insight_msg
    )

@router.get("/recommendations", response_model=List[AIRecommendationOut])
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="Household not assigned")
    return generate_reorder_recommendations(member.household_id, db)

@router.get("/runout-prediction/{id}", response_model=ConsumptionPrediction)
def get_runout_prediction(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Inventory).filter(Inventory.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return predict_item_consumption(item, db)

@router.post("/assistant", response_model=AIAssistantResponse)
def ask_ai_assistant(
    req: AIAssistantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="Household not assigned")
    return handle_ai_assistant_query(req.query, member.household_id, db)
