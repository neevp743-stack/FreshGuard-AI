import os
import json
import hashlib
import time
from typing import Dict, Any, List

DATASET_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../datasets/grocery_vision"))
CLASSES_JSON_PATH = os.path.join(os.path.dirname(__file__), "classes.json")
RAW_UNANNOTATED_DIR = os.path.join(DATASET_ROOT, "raw_unannotated")

def load_classes() -> List[str]:
    if os.path.exists(CLASSES_JSON_PATH):
        with open(CLASSES_JSON_PATH, "r") as f:
            data = json.load(f)
            return data.get("classes", [])
    return ["milk", "bread", "apple", "banana", "egg"]

def get_unique_filename(class_name: str, file_bytes: bytes, ext: str = ".jpg") -> str:
    h = hashlib.md5(file_bytes).hexdigest()[:8]
    timestamp = int(time.time() * 1000)
    return f"{class_name}_{timestamp}_{h}{ext}"

def save_raw_image(class_name: str, file_bytes: bytes) -> str:
    os.makedirs(RAW_UNANNOTATED_DIR, exist_ok=True)
    filename = get_unique_filename(class_name, file_bytes)
    filepath = os.path.join(RAW_UNANNOTATED_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file_bytes)
    return filepath

def generate_balance_report() -> Dict[str, Any]:
    classes = load_classes()
    counts = {c: 0 for c in classes}
    total_raw = 0

    if os.path.exists(RAW_UNANNOTATED_DIR):
        for f in os.listdir(RAW_UNANNOTATED_DIR):
            for c in classes:
                if f.startswith(f"{c}_"):
                    counts[c] += 1
                    total_raw += 1
                    break

    max_c = max(counts.values()) if counts else 0
    min_c = min(counts.values()) if counts else 0
    imbalance_warning = False
    if min_c > 0 and (max_c / min_c) > 1.5:
        imbalance_warning = True
    elif min_c == 0 and max_c > 0:
        imbalance_warning = True

    return {
        "total_raw_images": total_raw,
        "class_counts": counts,
        "imbalance_warning": imbalance_warning,
        "message": (
            "⚠️ Class imbalance detected. Consider collecting more samples for low-count classes."
            if imbalance_warning else "Dataset distribution balanced."
        )
    }

def main():
    print("=== FreshGuard AI Dataset Collection Tool ===")
    classes = load_classes()
    print("Available Classes:")
    for idx, c in enumerate(classes):
        print(f"  [{idx}] {c}")

    report = generate_balance_report()
    print("\nCurrent Dataset Status:")
    print(f"  Total Raw Images (Unannotated): {report['total_raw_images']}")
    for c, cnt in report['class_counts'].items():
        print(f"    - {c}: {cnt} images")
    if report['imbalance_warning']:
        print(f"  {report['message']}")

    print("\nIMPORTANT STAGE REMINDER:")
    print("  [1] Image Collection -> [2] Bounding Box Annotation -> [3] Label Validation -> [4] Dataset Split -> [5] Training")
    print("  Collected raw images in 'raw_unannotated/' require bounding box annotation (LabelImg/CVAT) before training can begin.")

if __name__ == "__main__":
    main()
