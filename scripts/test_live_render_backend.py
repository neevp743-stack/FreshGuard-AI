import os
import sys
import time
import json
import requests

LIVE_URL = "https://freshguard-ai-auef.onrender.com"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_live_render_backend():
    print("============================================================")
    print(f"   FRESHGUARD LIVE RENDER BACKEND PRODUCTION AUDIT          ")
    print(f"   Target URL: {LIVE_URL}")
    print("============================================================")

    results = {}

    # 1. GET /health
    url_health = f"{LIVE_URL}/health"
    print(f"\n1. Testing GET {url_health}...")
    t0 = time.perf_counter()
    try:
        r1 = requests.get(url_health, timeout=120)
        t1 = time.perf_counter()
        lat1 = round((t1 - t0) * 1000, 2)
        print(f"   HTTP {r1.status_code} | Latency: {lat1} ms")
        print(f"   Body: {r1.json()}")
        results["health"] = {"url": url_health, "status": r1.status_code, "latency_ms": lat1, "body": r1.json()}
    except Exception as ex:
        print(f"   [ERROR] Failed to reach {url_health}: {ex}")
        results["health"] = {"url": url_health, "status": 0, "error": str(ex)}

    # 2. GET /api/v1/health
    url_v1_health = f"{LIVE_URL}/api/v1/health"
    print(f"\n2. Testing GET {url_v1_health}...")
    t0 = time.perf_counter()
    try:
        r2 = requests.get(url_v1_health, timeout=60)
        t1 = time.perf_counter()
        lat2 = round((t1 - t0) * 1000, 2)
        print(f"   HTTP {r2.status_code} | Latency: {lat2} ms")
        print(f"   Body: {r2.json()}")
        results["v1_health"] = {"url": url_v1_health, "status": r2.status_code, "latency_ms": lat2, "body": r2.json()}
    except Exception as ex:
        print(f"   [ERROR] Failed to reach {url_v1_health}: {ex}")
        results["v1_health"] = {"url": url_v1_health, "status": 0, "error": str(ex)}

    # 3. GET /api/v1/scanner/vision/status
    url_vision_status = f"{LIVE_URL}/api/v1/scanner/vision/status"
    print(f"\n3. Testing GET {url_vision_status}...")
    t0 = time.perf_counter()
    try:
        r3 = requests.get(url_vision_status, timeout=60)
        t1 = time.perf_counter()
        lat3 = round((t1 - t0) * 1000, 2)
        print(f"   HTTP {r3.status_code} | Latency: {lat3} ms")
        print(f"   Body: {r3.json()}")
        results["vision_status"] = {"url": url_vision_status, "status": r3.status_code, "latency_ms": lat3, "body": r3.json()}
    except Exception as ex:
        print(f"   [ERROR] Failed to reach {url_vision_status}: {ex}")
        results["vision_status"] = {"url": url_vision_status, "status": 0, "error": str(ex)}

    # 4. POST /api/v1/scanner/vision/detect_v2
    url_detect_v2 = f"{LIVE_URL}/api/v1/scanner/vision/detect_v2?conf=0.20"
    print(f"\n4. Testing POST {url_detect_v2} with real image...")
    sample_img = os.path.join(BASE_DIR, "datasets", "grocery_vision", "images", "val", "veg_val_001.jpg")
    
    if not os.path.exists(sample_img):
        val_dir = os.path.join(BASE_DIR, "datasets", "grocery_vision", "images", "val")
        if os.path.exists(val_dir):
            files = [os.path.join(val_dir, f) for f in os.listdir(val_dir) if f.endswith(".jpg")]
            if files:
                sample_img = files[0]

    print(f"   Image Path: {sample_img}")
    try:
        with open(sample_img, "rb") as f:
            img_bytes = f.read()

        t0 = time.perf_counter()
        r4 = requests.post(url_detect_v2, files={"file": ("veg_val_001.jpg", img_bytes, "image/jpeg")}, timeout=90)
        t1 = time.perf_counter()
        lat4 = round((t1 - t0) * 1000, 2)
        print(f"   HTTP {r4.status_code} | Latency: {lat4} ms")
        res_data = r4.json()
        print(f"   Response Body:\n{json.dumps(res_data, indent=2)}")
        results["detect_v2"] = {"url": url_detect_v2, "status": r4.status_code, "latency_ms": lat4, "body": res_data}
    except Exception as ex:
        print(f"   [ERROR] Failed to post to {url_detect_v2}: {ex}")
        results["detect_v2"] = {"url": url_detect_v2, "status": 0, "error": str(ex)}

    # 5. OPTIONS CORS Verification
    print(f"\n5. Testing OPTIONS CORS headers on {url_detect_v2}...")
    headers_cors = {
        "Origin": "https://freshguard-ai.vercel.app",
        "Access-Control-Request-Method": "POST"
    }
    try:
        r5 = requests.options(url_detect_v2, headers=headers_cors, timeout=15)
        print(f"   HTTP {r5.status_code}")
        print(f"   Access-Control-Allow-Origin: {r5.headers.get('Access-Control-Allow-Origin', 'NOT_SET')}")
        results["cors"] = {
            "status": r5.status_code,
            "allow_origin": r5.headers.get('Access-Control-Allow-Origin', 'NOT_SET')
        }
    except Exception as ex:
        print(f"   [ERROR] CORS check failed: {ex}")
        results["cors"] = {"status": 0, "error": str(ex)}

    # Save verification JSON results
    out_file = os.path.join(BASE_DIR, "live_render_verification.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n============================================================")
    print(f"Verification results saved to '{out_file}'.")

if __name__ == "__main__":
    test_live_render_backend()
