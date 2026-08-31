import os
import hashlib
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PROTECTED_FILES = [
    os.path.join(BASE_DIR, "vision_models", "deployment", "grocery_yolov8_v2_web", "model.onnx"),
    os.path.join(BASE_DIR, "vision_models", "deployment", "grocery_yolov8_v2_web", "classes_metadata.json"),
    os.path.join(BASE_DIR, "vision_models", "model_metadata.json")
]

v5_onnx = os.path.join(BASE_DIR, "training", "v5", "deployment", "model.onnx")
if os.path.exists(v5_onnx):
    PROTECTED_FILES.append(v5_onnx)

baseline_hashes = {}

for p in PROTECTED_FILES:
    if os.path.exists(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            h.update(f.read())
        baseline_hashes[os.path.basename(p)] = h.hexdigest()
        print(f"[BASELINE HASH] {os.path.basename(p)}: {h.hexdigest()}")

hash_file = os.path.join(BASE_DIR, "docs", "PRE_V3_MODEL_HASHES.json")
os.makedirs(os.path.dirname(hash_file), exist_ok=True)
with open(hash_file, "w", encoding="utf-8") as f:
    json.dump(baseline_hashes, f, indent=2)

print(f"\nSaved initial baseline hashes to: {hash_file}")
