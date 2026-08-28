import os
import sys
import pytest
from fastapi.testclient import TestClient

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from main import app
from app.core.database import Base, engine, get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def get_auth_token(email="user@freshguard.com", password="password123"):
    r = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Test User",
        "household_name": "Test Household"
    })
    if r.status_code == 200:
        return r.json()["access_token"]
    r_login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return r_login.json()["access_token"]

def test_check_existing_inventory_and_duplicate_prevention():
    token = get_auth_token("unique_user_chk1@freshguard.com")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Add initial item (Tomato x3, class_id=5)
    r1 = client.post("/api/v1/inventory/from-detections", headers=headers, json={
        "items": [{
            "class_id": 5,
            "name": "tomato",
            "quantity": 3.0,
            "unit": "pcs",
            "location": "Fridge",
            "action": "add"
        }]
    })
    assert r1.status_code == 200
    assert r1.json()[0]["quantity"] == 3.0

    # 2. Check existing inventory for class_id 5 (tomato) and class_id 6 (potato)
    r2 = client.post("/api/v1/inventory/check-existing", headers=headers, json={
        "class_ids": [5, 6]
    })
    assert r2.status_code == 200
    matches = r2.json()
    assert len(matches) == 2

    match_tomato = next(m for m in matches if m["class_id"] == 5)
    assert match_tomato["already_in_inventory"] is True
    assert match_tomato["existing_quantity"] == 3.0

    match_potato = next(m for m in matches if m["class_id"] == 6)
    assert match_potato["already_in_inventory"] is False
    assert match_potato["existing_quantity"] == 0.0

def test_merge_existing_inventory_quantity():
    token = get_auth_token("unique_user_mrg2@freshguard.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Add initial item (Tomato x3)
    r1 = client.post("/api/v1/inventory/from-detections", headers=headers, json={
        "items": [{
            "class_id": 5,
            "name": "tomato",
            "quantity": 3.0,
            "unit": "pcs",
            "location": "Fridge",
            "action": "add"
        }]
    })
    item_id = r1.json()[0]["id"]

    # Merge +2 Tomatoes into existing item_id
    r2 = client.post("/api/v1/inventory/from-detections", headers=headers, json={
        "items": [{
            "class_id": 5,
            "name": "tomato",
            "quantity": 2.0,
            "unit": "pcs",
            "location": "Fridge",
            "action": "add",
            "existing_item_id": item_id
        }]
    })
    assert r2.status_code == 200
    assert r2.json()[0]["quantity"] == 5.0

def test_keep_separate_batch_creation():
    token = get_auth_token("unique_user_sep3@freshguard.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Add Batch 1 (Tomato x3)
    r1 = client.post("/api/v1/inventory/from-detections", headers=headers, json={
        "items": [{
            "class_id": 5,
            "name": "tomato",
            "quantity": 3.0,
            "unit": "pcs",
            "location": "Fridge",
            "action": "add"
        }]
    })
    assert r1.status_code == 200

    # Add Batch 2 (Tomato x2) as separate batch
    r2 = client.post("/api/v1/inventory/from-detections", headers=headers, json={
        "items": [{
            "class_id": 5,
            "name": "tomato",
            "quantity": 2.0,
            "unit": "pcs",
            "location": "Counter",
            "action": "separate_batch"
        }]
    })
    assert r2.status_code == 200

    # Query full inventory and verify 2 separate items exist
    r_list = client.get("/api/v1/inventory", headers=headers)
    assert r_list.status_code == 200
    tomatoes = [item for item in r_list.json() if item["product_name"] == "Tomato"]
    assert len(tomatoes) == 2

def test_skip_item_action():
    token = get_auth_token("unique_user_skp4@freshguard.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Submit detection payload with 1 saved item and 1 skipped item
    r = client.post("/api/v1/inventory/from-detections", headers=headers, json={
        "items": [
            {
                "class_id": 6,
                "name": "potato",
                "quantity": 2.0,
                "action": "add"
            },
            {
                "class_id": 7,
                "name": "onion",
                "quantity": 4.0,
                "action": "skip"
            }
        ]
    })
    assert r.status_code == 200
    res_items = r.json()
    assert len(res_items) == 1
    assert res_items[0]["product_name"] == "Potato"

def test_user_inventory_isolation():
    token_a = get_auth_token("unique_usera_iso5@freshguard.com")
    token_b = get_auth_token("unique_userb_iso5@freshguard.com")

    # User A adds Tomato
    client.post("/api/v1/inventory/from-detections", headers={"Authorization": f"Bearer {token_a}"}, json={
        "items": [{"class_id": 5, "name": "tomato", "quantity": 5.0, "action": "add"}]
    })

    # User B checks existing inventory for class_id 5 (tomato)
    r_check = client.post("/api/v1/inventory/check-existing", headers={"Authorization": f"Bearer {token_b}"}, json={
        "class_ids": [5]
    })
    assert r_check.status_code == 200
    # User B must NOT see User A's tomato
    assert r_check.json()[0]["already_in_inventory"] is False

def test_invalid_class_id_rejection():
    token = get_auth_token("unique_user_inv6@freshguard.com")
    r = client.post("/api/v1/inventory/from-detections", headers={"Authorization": f"Bearer {token}"}, json={
        "items": [{"class_id": 99, "name": "unknown_item", "quantity": 1.0, "action": "add"}]
    })
    assert r.status_code == 400
