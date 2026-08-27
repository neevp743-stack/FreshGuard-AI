import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_smoke_tests():
    print("============================================================")
    print("   FRESHGUARD AI — REAL PRODUCTION API SMOKE TEST MATRIX   ")
    print("============================================================")

    endpoints = [
        ("GET", "/health", None, None),
        ("GET", "/api/v1/health", None, None),
        ("POST", "/api/v1/auth/register", {"email": "smoke_user@freshguard.ai", "password": "SmokeTestPass123!", "full_name": "Smoke Tester"}, None),
        ("POST", "/api/v1/auth/login", {"email": "smoke_user@freshguard.ai", "password": "SmokeTestPass123!"}, None),
        ("GET", "/api/v1/scanner/vision/status", None, None),
    ]

    token = None
    results = []

    for method, path, payload, headers in endpoints:
        h = headers or {}
        if token and "auth" not in path:
            h["Authorization"] = f"Bearer {token}"

        t0 = time.perf_counter()
        if method == "GET":
            res = client.get(path, headers=h)
        elif method == "POST":
            res = client.post(path, json=payload, headers=h)
        t1 = time.perf_counter()

        latency_ms = round((t1 - t0) * 1000, 2)
        status_code = res.status_code

        if "login" in path and status_code == 200:
            token = res.json().get("access_token")

        results.append((method, path, status_code, latency_ms))
        print(f"[{method}] {path:<32} -> HTTP {status_code} ({latency_ms} ms)")

    # Additional Authenticated Tests
    if token:
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # /me
        t0 = time.perf_counter()
        res_me = client.get("/api/v1/auth/me", headers=auth_headers)
        t1 = time.perf_counter()
        results.append(("GET", "/api/v1/auth/me", res_me.status_code, round((t1 - t0) * 1000, 2)))
        print(f"[GET] {'/api/v1/auth/me':<32} -> HTTP {res_me.status_code} ({round((t1 - t0) * 1000, 2)} ms)")

        # USER on Admin Diagnostics (Expected 403)
        t0 = time.perf_counter()
        res_admin = client.get("/api/v1/admin/diagnostics", headers=auth_headers)
        t1 = time.perf_counter()
        results.append(("GET", "/api/v1/admin/diagnostics (USER)", res_admin.status_code, round((t1 - t0) * 1000, 2)))
        print(f"[GET] {'/api/v1/admin/diagnostics (USER)':<32} -> HTTP {res_admin.status_code} ({round((t1 - t0) * 1000, 2)} ms)")

    print("\n--- SMOKE TEST SUMMARY ---")
    print(f"Total Endpoints Tested: {len(results)}")
    all_ok = all(r[2] in [200, 403] for r in results)
    print(f"Smoke Test Status: {'PASSED' if all_ok else 'FAILED'}")
    return all_ok

if __name__ == "__main__":
    run_smoke_tests()
