import os
import sys

search_paths = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    "C:\\Users\\neevp\\OneDrive\\Desktop"
]

print("Scanning for zip archives...")
zip_files = []

for base_p in search_paths:
    if os.path.exists(base_p):
        for root, dirs, files in os.walk(base_p):
            # limit depth to prevent endless search
            depth = root.count(os.sep) - base_p.count(os.sep)
            if depth > 3:
                continue
            for f in files:
                if f.lower().endswith(".zip"):
                    fp = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(fp) / (1024 * 1024)
                        zip_files.append((fp, sz))
                    except Exception:
                        pass

print(f"Found {len(zip_files)} zip archive(s):")
for fp, sz in zip_files:
    print(f"  - {fp} ({sz:.2f} MB)")
