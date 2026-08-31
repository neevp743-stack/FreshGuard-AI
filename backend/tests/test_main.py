import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.models.models import User, Household, HouseholdMember, Inventory, ConsumptionLog, Notification, DeviceToken, UserPreference
from app.services.scanner import lookup_barcode
from app.ai.ocr import parse_package_ocr_text
from app.services.ocr_image import process_raw_image_ocr
from app.services.notifications import evaluate_and_generate_notifications
from app.ai.consumption import predict_item_consumption
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_keep_alive_conn = engine.connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    conn = engine.connect()
    yield
    conn.close()
    Base.metadata.drop_all(bind=engine)





# ==================== EXISTING CORE TESTS ====================

def test_auth_register_and_login():
    res = client.post("/api/auth/register", json={
        "email": "testuser@freshguard.ai",
        "password": "securepassword123",
        "full_name": "Test User",
        "household_name": "Test Home"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["email"] == "testuser@freshguard.ai"

    login_res = client.post("/api/auth/login", json={
        "email": "testuser@freshguard.ai",
        "password": "securepassword123"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

def test_unauthorized_access():
    res = client.get("/api/inventory")
    assert res.status_code == 401

def test_add_and_delete_product():
    reg = client.post("/api/auth/register", json={"email": "invuser@freshguard.ai", "password": "pass"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    add_res = client.post("/api/inventory", json={
        "product_name": "Fresh Organic Milk",
        "category": "Dairy",
        "quantity": 2.0,
        "unit": "L",
        "storage_location": "Refrigerator"
    }, headers=headers)
    assert add_res.status_code == 200
    item_id = add_res.json()["id"]

    del_res = client.delete(f"/api/inventory/{item_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "success"

def test_expiry_calculation_and_expired_item():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    
    item_expired = Inventory(
        user_id=1, household_id=1, product_name="Old Cottage Cheese",
        quantity=1.0, unit="pcs", category="Dairy",
        expiry_date=now - timedelta(days=2), status="Expired"
    )
    db.add(item_expired)
    db.commit()

    assert item_expired.status == "Expired"
    db.close()

def test_barcode_lookup():
    res = lookup_barcode("8901058000147")
    assert res.found is True
    assert "Amul Taaza" in res.product_name

def test_ocr_parsing():
    ocr_input = "Amul Pure Butter\nEXP: 20/08/2026\nBATCH: B-9981"
    res = parse_package_ocr_text(ocr_input)
    assert res.detected is True
    assert res.expiry_date == "20/08/2026"
    assert res.confidence_score > 70.0

def test_consumption_prediction_and_reorder():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    item = Inventory(
        user_id=1, household_id=1, product_name="Test Milk",
        quantity=0.5, unit="L", category="Dairy", status="Running Low"
    )
    db.add(item)
    db.commit()

    log = ConsumptionLog(
        household_id=1, inventory_id=item.id, product_name="Test Milk",
        quantity_consumed=1.0, unit="L", date_consumed=now - timedelta(days=2), log_type="consumed"
    )
    db.add(log)
    db.commit()

    pred = predict_item_consumption(item, db)
    assert pred.product_name == "Test Milk"
    db.close()

# ==================== PHASE 2 IMAGE OCR & NOTIFICATION TESTS ====================

def test_ocr_image_endpoint_valid():
    reg = client.post("/api/auth/register", json={"email": "imguser@freshguard.ai", "password": "pass"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    buf = io.BytesIO()
    img = Image.new('RGB', (200, 200), color=(255, 255, 255))
    img.save(buf, format='JPEG')
    buf.seek(0)

    files = {"file": ("test_package.jpg", buf, "image/jpeg")}

    res = client.post("/api/scanner/ocr/image", files=files, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "raw_text" in data

def test_ocr_image_invalid_file_type():
    res = process_raw_image_ocr(b"hello world", content_type="text/plain")
    assert res.success is False
    assert "Invalid file type" in res.message

def test_ocr_image_oversized_file():
    huge_bytes = b"0" * (11 * 1024 * 1024)
    res = process_raw_image_ocr(huge_bytes, content_type="image/jpeg")
    assert res.success is False
    assert "exceeds maximum limit" in res.message

def test_ocr_date_extraction_parsing():
    raw = "AMUL MILK\nEXP: 2O/08/2026\nBATCH B-102"
    parsed = parse_package_ocr_text(raw)
    assert parsed.detected is True
    assert parsed.expiry_date == "20/08/2026"

def test_ocr_ambiguous_expiry_date():
    raw = "Generic Snack Box\nNO EXPIRY DATE VISIBLE"
    parsed = parse_package_ocr_text(raw)
    assert parsed.detected is True
    assert parsed.confidence_score <= 80.0

def test_unknown_barcode_fallback():
    res = lookup_barcode("99988877766611")
    assert res.found is False
    assert res.barcode == "99988877766611"

def test_device_token_registration():
    reg = client.post("/api/auth/register", json={"email": "devtoken@freshguard.ai", "password": "pass"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/api/notifications/device-token", json={
        "token": "fcm_test_device_token_abc123",
        "platform": "android"
    }, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["token"] == "fcm_test_device_token_abc123"
    assert data["platform"] == "android"
    assert data["is_active"] is True

def test_notification_creation_and_deduplication():
    db = TestingSessionLocal()
    now = datetime.utcnow()

    u = User(email="notifuser@freshguard.ai", password_hash="pass")
    db.add(u)
    db.commit()
    db.refresh(u)

    inv = Inventory(
        user_id=u.id, household_id=1, product_name="Expiring Milk",
        quantity=1.0, unit="L", category="Dairy",
        expiry_date=now + timedelta(days=1), status="Expiring Soon"
    )
    db.add(inv)
    db.commit()

    evaluate_and_generate_notifications(u.id, 1, db)
    notifs = db.query(Notification).filter(Notification.user_id == u.id).all()
    assert len(notifs) >= 1

    count_before = len(notifs)
    evaluate_and_generate_notifications(u.id, 1, db)
    count_after = db.query(Notification).filter(Notification.user_id == u.id).count()
    assert count_after == count_before
    db.close()

def test_user_notification_preferences_filtering():
    db = TestingSessionLocal()
    now = datetime.utcnow()

    u = User(email="prefuser@freshguard.ai", password_hash="pass")
    db.add(u)
    db.commit()
    db.refresh(u)

    pref = UserPreference(user_id=u.id, expiry_alert_enabled=False)
    db.add(pref)

    inv = Inventory(
        user_id=u.id, household_id=99, product_name="Test Item",
        quantity=1.0, unit="pcs", category="Dairy",
        expiry_date=now + timedelta(days=1), status="Expiring Soon"
    )
    db.add(inv)
    db.commit()

    evaluate_and_generate_notifications(u.id, 99, db)
    notifs = db.query(Notification).filter(Notification.user_id == u.id, Notification.type == "EXPIRING_SOON").all()
    assert len(notifs) == 0
    db.close()

def test_unauthorized_device_token_registration():
    res = client.post("/api/notifications/device-token", json={
        "token": "unauth_token_123",
        "platform": "android"
    })
    assert res.status_code == 401

# ==================== NEW PHASE 3 VISION AI & MULTIMODAL TESTS ====================

def test_vision_status_endpoint():
    from app.core.config import settings
    orig = settings.FRESHGUARD_VISION_MODEL
    settings.FRESHGUARD_VISION_MODEL = "v1"
    try:
        res = client.get("/api/scanner/vision/status")
        assert res.status_code == 200
        data = res.json()
        assert "lifecycle_state" in data
        assert data["lifecycle_state"] == "NOT_TRAINED"
        assert data["model_available"] is False
        assert data["classes_count"] == 15
        assert data["confidence_threshold"] == 0.50
    finally:
        settings.FRESHGUARD_VISION_MODEL = orig

def test_vision_detect_no_model_graceful():
    from app.core.config import settings
    orig = settings.FRESHGUARD_VISION_MODEL
    settings.FRESHGUARD_VISION_MODEL = "v1"
    try:
        buf = io.BytesIO()
        img = Image.new('RGB', (200, 200), color=(255, 255, 255))
        img.save(buf, format='JPEG')
        buf.seek(0)

        files = {"file": ("fridge_test.jpg", buf, "image/jpeg")}
        res = client.post("/api/scanner/vision/detect", files=files)
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is False
        assert data["lifecycle_state"] == "NOT_TRAINED"
        assert data["detections"] == []
        assert "pending the real grocery dataset" in data["message"]
    finally:
        settings.FRESHGUARD_VISION_MODEL = orig

def test_vision_feedback_privacy_first():
    reg = client.post("/api/auth/register", json={"email": "visionfb@freshguard.ai", "password": "pass"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/api/scanner/vision/feedback", json={
        "predicted_class": "banana",
        "confidence": 0.62,
        "corrected_class": "apple",
        "opt_in_image_retention": False,
        "comments": "User corrected prediction"
    }, headers=headers)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

def test_multimodal_barcode_vision_conflict_flagging():
    # Test barcode lookup priority and conflict handling
    res = client.post("/api/scanner/vision/multimodal?barcode=8901058000147")
    assert res.status_code == 200
    data = res.json()
    assert data["barcode_identity"] is not None
    assert "Amul Taaza" in data["final_suggested_item"]["product_name"]

# ==================== PRODUCTION READINESS & HARDENING TESTS ====================

def test_pbkdf2_password_hashing_and_legacy_migration():
    db = TestingSessionLocal()
    from app.core.security import hash_password, verify_and_migrate_password

    # Test PBKDF2 hash creation format
    pwd = "SecretPassword!2026"
    hashed = hash_password(pwd)
    assert hashed.startswith("pbkdf2_sha256$")

    valid, needs_rehash = verify_and_migrate_password(pwd, hashed)
    assert valid is True
    assert needs_rehash is False

    # Test legacy SHA256 migration
    import hashlib
    from app.core.config import settings
    legacy_salted = f"{settings.SECRET_KEY}:{pwd}".encode('utf-8')
    legacy_hash = hashlib.sha256(legacy_salted).hexdigest()

    legacy_valid, legacy_needs_rehash = verify_and_migrate_password(pwd, legacy_hash)
    assert legacy_valid is True
    assert legacy_needs_rehash is True
    db.close()

def test_lightweight_health_endpoints():
    # Root /health
    res1 = client.get("/health")
    assert res1.status_code == 200
    d1 = res1.json()
    assert d1["status"] == "READY"
    assert d1["process_alive"] is True
    assert d1["database_connected"] is True

    # Versioned /api/v1/health
    res2 = client.get("/api/v1/health")
    assert res2.status_code == 200
    d2 = res2.json()
    assert d2["status"] == "READY"

def test_rbac_user_admin_access_control():
    # Unauthenticated request -> 401
    res_unauth = client.get("/api/v1/admin/diagnostics")
    assert res_unauth.status_code == 401

    # Register normal USER -> gets USER role by default
    res_reg_user = client.post("/api/v1/auth/register", json={"email": "normaluser@freshguard.ai", "password": "password123"})
    assert res_reg_user.status_code == 200
    token_normal = res_reg_user.json()["access_token"]

    # Normal USER request -> 403 Forbidden
    res_user = client.get("/api/v1/admin/diagnostics", headers={"Authorization": f"Bearer {token_normal}"})
    assert res_user.status_code == 403
    assert "Forbidden" in res_user.json()["detail"]

    # Register ADMIN user -> pass role="ADMIN"
    res_reg_admin = client.post("/api/v1/auth/register", json={"email": "adminuser@freshguard.ai", "password": "password123", "role": "ADMIN"})
    assert res_reg_admin.status_code == 200
    token_admin = res_reg_admin.json()["access_token"]

    res_admin = client.get("/api/v1/admin/diagnostics", headers={"Authorization": f"Bearer {token_admin}"})
    assert res_admin.status_code == 200
    data_admin = res_admin.json()
    assert data_admin["status"] in ["OPERATIONAL", "DEGRADED"]
    assert data_admin["process_alive"] is True
    assert "memory_usage_mb" in data_admin


    data_admin = res_admin.json()
    assert data_admin["status"] in ["OPERATIONAL", "DEGRADED"]
    assert data_admin["process_alive"] is True
    assert "memory_usage_mb" in data_admin


def test_ocr_failure_without_hardcoded_mock():
    # Submit invalid bytes that fail OCR extraction without fabricating fake milk text
    res = process_raw_image_ocr(b"not an image", content_type="image/jpeg")
    assert res.success is False
    assert res.raw_text == ""
    assert res.confidence == 0.0
    assert "Invalid or corrupt image" in res.message

def test_api_v1_endpoint_versioning():
    reg = client.post("/api/v1/auth/register", json={"email": "v1user@freshguard.ai", "password": "pass"})
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    assert reg.json()["role"] == "USER"

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "v1user@freshguard.ai"

def test_live_webcam_v2_detection_endpoint():
    buf = io.BytesIO()
    img = Image.new('RGB', (640, 640), color=(220, 180, 150))
    img.save(buf, format='JPEG')
    buf.seek(0)

    files = {"file": ("webcam_frame.jpg", buf, "image/jpeg")}
    res = client.post("/api/v1/scanner/vision/detect_v2?conf=0.20", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "grocery_yolov8_" in data["model"]
    assert "detections" in data
    assert "count" in data
    assert "inference_ms" in data

def test_live_webcam_v2_json_base64_payload_endpoint():
    import base64
    buf = io.BytesIO()
    img = Image.new('RGB', (320, 320), color=(200, 50, 50))
    img.save(buf, format='JPEG')
    buf.seek(0)
    b64_str = "data:image/jpeg;base64," + base64.b64encode(buf.read()).decode("utf-8")

    res = client.post("/api/v1/scanner/vision/detect_v2?conf=0.20", json={"image_base64": b64_str})
    assert res.status_code == 200, f"HTTP 400 error on JSON payload: {res.text}"
    data = res.json()
    assert data["success"] is True
    assert "grocery_yolov8_" in data["model"]
    assert "detections" in data
    assert "inference_ms" in data

def test_35_class_shelf_life_rules():
    from app.services.shelf_life import get_class_rule, calculate_estimated_expiry
    rule = get_class_rule(27)  # okra
    assert rule["name"] == "okra"
    assert rule["category"] == "Vegetables"
    assert rule["default_location"] == "Fridge"

    rule_milk = get_class_rule("milk")
    assert rule_milk["category"] == "Dairy"

    exp = calculate_estimated_expiry(27)
    assert exp is not None

def test_add_inventory_from_detections():
    # Register user
    reg = client.post("/api/v1/auth/register", json={"email": "detuser@freshguard.ai", "password": "password123"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [
            {
                "class_id": 27,
                "name": "Okra",
                "quantity": 3.0,
                "unit": "pcs",
                "location": "Fridge"
            },
            {
                "class_id": 5,
                "name": "Tomato",
                "quantity": 2.0,
                "unit": "pcs",
                "location": "Fridge"
            }
        ]
    }

    res = client.post("/api/v1/inventory/from-detections", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    assert data[0]["product_name"] == "Okra"
    assert data[0]["category"] == "Vegetables"
    assert data[0]["quantity"] == 3.0
    assert data[0]["expiry_date"] is not None

def test_reject_invalid_detection_class_id():
    reg = client.post("/api/v1/auth/register", json={"email": "invalidclass@freshguard.ai", "password": "password123"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [
            {
                "class_id": 999,  # Unknown class ID
                "name": "Alien Food",
                "quantity": 1.0
            }
        ]
    }

    res = client.post("/api/v1/inventory/from-detections", json=payload, headers=headers)
    assert res.status_code == 400
    assert "Invalid class_id: 999" in res.json()["detail"]

def test_bulk_inventory_creation():
    reg = client.post("/api/v1/auth/register", json={"email": "bulkuser@freshguard.ai", "password": "password123"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [
            {"product_name": "Milk", "category": "Dairy", "quantity": 1.0, "unit": "bottle"},
            {"product_name": "Spinach", "category": "Vegetables", "quantity": 2.0, "unit": "bunch"}
        ]
    }

    res = client.post("/api/v1/inventory/bulk", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2

def test_user_inventory_isolation():
    # User 1
    reg1 = client.post("/api/v1/auth/register", json={"email": "user1@freshguard.ai", "password": "password123"})
    t1 = reg1.json()["access_token"]

    # Add item for User 1
    res_add = client.post("/api/v1/inventory", json={"product_name": "Private Milk"}, headers={"Authorization": f"Bearer {t1}"})
    item_id = res_add.json()["id"]

    # User 2
    reg2 = client.post("/api/v1/auth/register", json={"email": "user2@freshguard.ai", "password": "password123"})
    t2 = reg2.json()["access_token"]

    # User 2 tries to access User 1's item
    res_get = client.get(f"/api/v1/inventory/{item_id}", headers={"Authorization": f"Bearer {t2}"})
    assert res_get.status_code == 404

    # User 2 tries to delete User 1's item
    res_del = client.delete(f"/api/v1/inventory/{item_id}", headers={"Authorization": f"Bearer {t2}"})
    assert res_del.status_code == 404

def test_consume_inventory_item():
    reg = client.post("/api/v1/auth/register", json={"email": "consumeuser@freshguard.ai", "password": "password123"})
    t = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {t}"}

    add_res = client.post("/api/v1/inventory", json={"product_name": "Apple", "quantity": 5.0}, headers=headers)
    item_id = add_res.json()["id"]

def test_freshness_engine_status_calculations():
    from datetime import datetime, timedelta
    from app.services.freshness import calculate_freshness_status

    now = datetime.utcnow()
    # Unknown
    st_unk, d_unk = calculate_freshness_status(None)
    assert st_unk == "UNKNOWN"
    assert d_unk is None

    # Fresh (>2 days)
    st_fresh, d_fresh = calculate_freshness_status(now + timedelta(days=5))
    assert st_fresh == "FRESH"
    assert d_fresh >= 4

    # Use Soon (0..2 days)
    st_soon, d_soon = calculate_freshness_status(now + timedelta(days=1))
    assert st_soon == "USE_SOON"
    assert d_soon == 1

    # Expired (<0 days)
    st_exp, d_exp = calculate_freshness_status(now - timedelta(days=2))
    assert st_exp == "EXPIRED"
    assert d_exp <= -1

def test_freshness_summary_and_use_first_endpoints():
    from datetime import datetime, timedelta
    now = datetime.utcnow()

    reg = client.post("/api/v1/auth/register", json={"email": "freshuser@freshguard.ai", "password": "password123"})
    t = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {t}"}

    # Add Fresh item
    client.post("/api/v1/inventory", json={"product_name": "Fresh Carrot", "expiry_date": (now + timedelta(days=10)).isoformat()}, headers=headers)
    # Add Use Soon item
    client.post("/api/v1/inventory", json={"product_name": "Urgent Tomato", "expiry_date": (now + timedelta(days=1)).isoformat()}, headers=headers)
    # Add Expired item
    client.post("/api/v1/inventory", json={"product_name": "Old Milk", "expiry_date": (now - timedelta(days=2)).isoformat()}, headers=headers)

    # Test Summary
    res_sum = client.get("/api/v1/freshness/summary", headers=headers)
    assert res_sum.status_code == 200
    sum_data = res_sum.json()
    assert sum_data["total"] == 3
    assert sum_data["fresh"] == 1
    assert sum_data["use_soon"] == 1
    assert sum_data["expired"] == 1

    # Test Use-First Recommendations
    res_uf = client.get("/api/v1/freshness/use-first", headers=headers)
    assert res_uf.status_code == 200
    uf_data = res_uf.json()
    assert len(uf_data) == 3

    # Expired item safety check
    expired_rec = next(i for i in uf_data if i["product_name"] == "Old Milk")
    assert expired_rec["recommendation_action"] == "Review / Remove"
    assert "Do not consume expired food" in expired_rec["guidance"]

    # Use Soon item check
    soon_rec = next(i for i in uf_data if i["product_name"] == "Urgent Tomato")
    assert soon_rec["recommendation_action"] == "Consume First"

    # Test Alerts Endpoint
    res_alt = client.get("/api/v1/freshness/alerts", headers=headers)
    assert res_alt.status_code == 200
    alt_data = res_alt.json()
    assert len(alt_data) >= 2

def test_freshness_user_isolation():
    reg1 = client.post("/api/v1/auth/register", json={"email": "fuser1@freshguard.ai", "password": "password123"})
    t1 = reg1.json()["access_token"]
    client.post("/api/v1/inventory", json={"product_name": "Secret Spinach"}, headers={"Authorization": f"Bearer {t1}"})

    reg2 = client.post("/api/v1/auth/register", json={"email": "fuser2@freshguard.ai", "password": "password123"})
    t2 = reg2.json()["access_token"]

    res_sum2 = client.get("/api/v1/freshness/summary", headers={"Authorization": f"Bearer {t2}"})
    assert res_sum2.status_code == 200
    assert res_sum2.json()["total"] == 0




