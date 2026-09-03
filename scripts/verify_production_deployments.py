"""
FreshGuard AI — Production Deployment Verification Script
Queries live Render backend and Vercel frontend deployments to verify operational health.
"""

import urllib.request
import urllib.error
import json
import time

RENDER_BACKEND_URL = "https://freshguard-ai.onrender.com"
VERCEL_FRONTEND_URL = "https://fresh-guard-ai-delta.vercel.app"

def verify_deployments():
    print("=========================================================================")
    print("      FRESHGUARD AI — LIVE PRODUCTION DEPLOYMENT AUDIT & VERIFICATION     ")
    print("=========================================================================")

    results = {
        "render_backend": {"status": "UNKNOWN"},
        "vercel_frontend": {"status": "UNKNOWN"},
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    }

    # 1. Test Render Backend /health
    health_url = f"{RENDER_BACKEND_URL}/health"
    print(f"\n[1/3] Querying Render Backend Health: {health_url}")
    try:
        req = urllib.request.Request(health_url, headers={"User-Agent": "FreshGuard-Prod-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            status_code = resp.status
            body = json.loads(resp.read().decode('utf-8'))
            print(f"  -> HTTP {status_code} | Health Payload: {body}")
            results["render_backend"] = {
                "status": "ONLINE" if status_code == 200 else "DEGRADED",
                "http_status": status_code,
                "payload": body
            }
    except Exception as e:
        print(f"  -> Render Backend Query Note/Warning: {e}")
        results["render_backend"] = {
            "status": "DEGRADED_OR_COLD_START",
            "error": str(e)
        }

    # 2. Test Render Backend /vision-v3-test
    v3_test_url = f"{RENDER_BACKEND_URL}/vision-v3-test"
    print(f"\n[2/3] Querying Render V3 Dedicated Test Route: {v3_test_url}")
    try:
        req = urllib.request.Request(v3_test_url, headers={"User-Agent": "FreshGuard-Prod-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"  -> HTTP {resp.status} | Content-Type: {resp.headers.get('Content-Type')}")
            results["render_backend_v3_test"] = {"status": "ONLINE", "http_status": resp.status}
    except Exception as e:
        print(f"  -> Query Note: {e}")
        results["render_backend_v3_test"] = {"status": "DEGRADED", "error": str(e)}

    # 3. Test Vercel Frontend /
    print(f"\n[3/3] Querying Vercel Frontend Root: {VERCEL_FRONTEND_URL}")
    try:
        req = urllib.request.Request(VERCEL_FRONTEND_URL, headers={"User-Agent": "FreshGuard-Prod-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"  -> HTTP {resp.status} | Content-Type: {resp.headers.get('Content-Type')}")
            results["vercel_frontend"] = {
                "status": "ONLINE" if resp.status == 200 else "DEGRADED",
                "http_status": resp.status
            }
    except Exception as e:
        print(f"  -> Vercel Query Note: {e}")
        results["vercel_frontend"] = {
            "status": "DEGRADED",
            "error": str(e)
        }

    print("\n=========================================================================")
    print("Live Production Deployment Audit Complete.")
    print("=========================================================================")
    return results

if __name__ == "__main__":
    verify_deployments()
