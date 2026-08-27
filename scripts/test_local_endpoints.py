import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_all_local_endpoints():
    print("============================================================")
    print("   FRESHGUARD LOCAL BACKEND PRODUCTION ENDPOINT AUDIT     ")
    print("============================================================")

    # 1. GET /health
    r1 = client.get("/health")
    print(f"GET /health: HTTP {r1.status_code} | {r1.json()}")
    assert r1.status_code == 200

    # 2. GET /api/v1/health
    r2 = client.get("/api/v1/health")
    print(f"GET /api/v1/health: HTTP {r2.status_code} | {r2.json()}")
    assert r2.status_code == 200

    # 3. GET /api/v1/scanner/vision/status
    r3 = client.get("/api/v1/scanner/vision/status")
    print(f"GET /api/v1/scanner/vision/status: HTTP {r3.status_code} | {r3.json()}")
    assert r3.status_code == 200

    # 4. POST /api/v1/scanner/vision/detect_v2 with real image
    sample_img = os.path.join(BASE_DIR, "datasets", "grocery_vision", "images", "val", "veg_val_001.jpg")
    
    if not os.path.exists(sample_img):
        val_dir = os.path.join(BASE_DIR, "datasets", "grocery_vision", "images", "val")
        if os.path.exists(val_dir):
            files = [os.path.join(val_dir, f) for f in os.listdir(val_dir) if f.endswith(".jpg")]
            if files:
                sample_img = files[0]

    print(f"\nTesting POST /api/v1/scanner/vision/detect_v2 with real image: '{sample_img}'...")
    with open(sample_img, "rb") as f:
        img_bytes = f.read()

    r4 = client.post("/api/v1/scanner/vision/detect_v2?conf=0.20", files={"file": ("test_frame.jpg", img_bytes, "image/jpeg")})
    print(f"HTTP {r4.status_code}")
    res_data = r4.json()
    print(json.dumps(res_data, indent=2))

    assert r4.status_code == 200
    assert res_data["success"] is True
    assert res_data["model"] == "grocery_yolov8_v2"
    assert "detections" in res_data
    assert "count" in res_data
    assert "inference_ms" in res_data

    print("\n[SUCCESS] ALL LOCAL ENDPOINTS EMPIRICALLY VERIFIED WITH REAL MODEL INFERENCE.")

if __name__ == "__main__":
    test_all_local_endpoints()
