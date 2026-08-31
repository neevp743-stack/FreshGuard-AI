import requests

base_url = "https://freshguard-ai-backend.onrender.com"

endpoints = ["/", "/health", "/api/v1/health", "/docs", "/openapi.json"]

print(f"Diagnosing Render URL: {base_url}")
for ep in endpoints:
    url = f"{base_url}{ep}"
    try:
        r = requests.get(url, timeout=15)
        print(f"\nGET {ep}: HTTP {r.status_code}")
        print(f"Headers: {dict(r.headers)}")
        print(f"Body snippet (first 200 chars): {r.text[:200]}")
    except Exception as ex:
        print(f"\nGET {ep}: ERROR {ex}")
