import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.models import Inventory, Notification, DeviceToken, UserPreference, User

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK if credentials provided in environment variables
FIREBASE_INITIALIZED = False

try:
    import firebase_admin
    from firebase_admin import credentials, messaging

    cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    project_id = os.getenv("FIREBASE_PROJECT_ID")

    if cred_json:
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        FIREBASE_INITIALIZED = True
    elif project_id:
        cred_dict = {
            "type": "service_account",
            "project_id": project_id,
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL", ""),
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        FIREBASE_INITIALIZED = True
except Exception as e:
    logger.info(f"Firebase FCM Admin SDK initialized in dev mode fallback: {e}")

def send_fcm_push_notification(tokens: List[str], title: str, body: str, data_payload: Optional[dict] = None):
    """
    Dispatches native Firebase Cloud Messaging (FCM) push notifications to active device tokens.
    If Firebase credentials are not configured in environment, safely logs diagnostic message.
    """
    if not FIREBASE_INITIALIZED or not tokens:
        logger.info(f"[FCM Mock Dispatch] Title: '{title}', Body: '{body}', Device Tokens: {len(tokens)}")
        return

    try:
        from firebase_admin import messaging
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            data=data_payload or {},
            tokens=tokens,
        )
        response = messaging.send_multicast(message)
        logger.info(f"FCM Push Sent. Success count: {response.success_count}, Failure count: {response.failure_count}")
    except Exception as ex:
        logger.warning(f"Error dispatching FCM push notification: {ex}")

def evaluate_and_generate_notifications(user_id: int, household_id: int, db: Session):
    """
    Intelligent Notification Engine.
    Scans inventory for upcoming expiry or run-out events, evaluates user notification preferences,
    enqueues priority notifications, enforces 24h deduplication, and sends FCM push payloads.
    """
    # Check user preferences
    pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    expiry_enabled = pref.expiry_alert_enabled if pref else True
    runout_enabled = pref.runout_alert_enabled if pref else True
    alert_days = pref.notification_days_before if pref else 3

    items = db.query(Inventory).filter(Inventory.household_id == household_id).all()
    now = datetime.utcnow()

    new_notifications = []

    for item in items:
        # 1. Expiry Notifications
        if expiry_enabled and item.expiry_date:
            days = (item.expiry_date - now).days

            title = None
            message = None
            priority = "normal"
            notif_type = "EXPIRING_SOON"

            if days < 0:
                notif_type = "EXPIRED"
                title = f"🔴 {item.product_name} Expired"
                message = f"{item.product_name} expired {abs(days)} day(s) ago. Please check before using."
                priority = "urgent"
            elif days == 0:
                title = f"🔴 {item.product_name} Expires Today"
                message = f"{item.product_name} expires today. Consider using it in your next meal!"
                priority = "urgent"
            elif days == 1:
                title = f"🟠 {item.product_name} Expires Tomorrow"
                message = f"{item.product_name} will expire tomorrow."
                priority = "high"
            elif days == alert_days:
                title = f"🟡 {item.product_name} Expires in {alert_days} Days"
                message = f"{item.product_name} expires in {alert_days} days."
                priority = "normal"

            if title:
                # 24-hour Deduplication Check
                existing = db.query(Notification).filter(
                    Notification.user_id == user_id,
                    Notification.title == title,
                    Notification.created_at >= (now - timedelta(hours=24))
                ).first()

                if not existing:
                    notif = Notification(
                        user_id=user_id,
                        title=title,
                        message=message,
                        type=notif_type,
                        priority=priority,
                        is_read=False
                    )
                    db.add(notif)
                    new_notifications.append(notif)

        # 2. Runout Notifications
        if runout_enabled and item.status == "Running Low":
            title = f"🛒 {item.product_name} Running Low"
            message = f"Your {item.product_name} stock is low ({item.quantity} {item.unit} remaining). Add to Smart Cart?"
            existing_low = db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.title == title,
                Notification.created_at >= (now - timedelta(hours=24))
            ).first()

            if not existing_low:
                notif = Notification(
                    user_id=user_id,
                    title=title,
                    message=message,
                    type="RUNNING_LOW",
                    priority="high",
                    is_read=False
                )
                db.add(notif)
                new_notifications.append(notif)

    db.commit()

    # Send FCM push payloads if new notifications created
    if new_notifications:
        active_tokens = db.query(DeviceToken.token).filter(
            DeviceToken.user_id == user_id,
            DeviceToken.is_active == True
        ).all()
        token_list = [t[0] for t in active_tokens]

        for n in new_notifications:
            send_fcm_push_notification(token_list, n.title, n.message, {"type": n.type, "id": str(n.id)})
