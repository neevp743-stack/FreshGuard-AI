import requests

candidates = [
    "https://freshguard-ai-backend.onrender.com",
    "https://freshguard-ai.onrender.com",
    "https://freshguard-backend.onrender.com",
    "https://freshguard.onrender.com",
]

print("Checking candidate Render service URLs...")
for base in candidates:
    url = f"{base}/health"
    try:
        r = requests.get(url, timeout=5)
        print(f"{base}: HTTP {r.status_code} | x-render-routing: {r.headers.get('x-render-routing', 'none')} | Body: {r.text[:100]}")
    except Exception as ex:
        print(f"{base}: ERROR ({ex})")
