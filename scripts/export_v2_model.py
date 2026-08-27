import os
import sys
import shutil
import json
from ultralytics import YOLO

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
V2_WEIGHTS = os.path.join(BASE_DIR, "vision_models", "experiments", "grocery_yolov8_v2", "weights", "best.pt")
DEPLOY_DIR = os.path.join(BASE_DIR, "vision_models", "deployment", "grocery_yolov8_v2_web")
CLASSES_PATH = os.path.join(BASE_DIR, "backend", "app", "ai", "vision", "classes.json")

def export_v2_deployment_artifact():
    print("============================================================")
    print("   FRESHGUARD YOLOV8 V2 MODEL EXPORT TO DEPLOYMENT DIR     ")
    print("============================================================")

    if not os.path.exists(V2_WEIGHTS):
        print(f"[ERROR] V2 weights not found at: {V2_WEIGHTS}")
        sys.exit(1)

    os.makedirs(DEPLOY_DIR, exist_ok=True)

    print(f"[EXPORT] Loading V2 weights from: {V2_WEIGHTS}")
    model = YOLO(V2_WEIGHTS)

    # 1. Export model to ONNX format
    try:
        onnx_path = model.export(format="onnx", imgsz=640, dynamic=False)
        target_onnx = os.path.join(DEPLOY_DIR, "model.onnx")
        if os.path.exists(onnx_path) and onnx_path != target_onnx:
            shutil.copy(onnx_path, target_onnx)
        print(f"[SUCCESS] Exported V2 ONNX model to: {target_onnx}")
    except Exception as ex:
        print(f"[WARN] ONNX export note: {ex}. Proceeding with PyTorch deployment artifact.")

    # 2. Copy best.pt weights to deployment folder
    target_pt = os.path.join(DEPLOY_DIR, "model.pt")
    shutil.copy(V2_WEIGHTS, target_pt)
    print(f"[SUCCESS] Copied V2 weights artifact to: {target_pt}")

    # 3. Save class mapping metadata
    if os.path.exists(CLASSES_PATH):
        with open(CLASSES_PATH, "r") as f:
            classes_meta = json.load(f)
        
        deploy_meta_path = os.path.join(DEPLOY_DIR, "classes_metadata.json")
        with open(deploy_meta_path, "w") as f:
            json.dump(classes_meta, f, indent=2)
        print(f"[SUCCESS] Saved 35-class metadata to: {deploy_meta_path}")

if __name__ == "__main__":
    export_v2_deployment_artifact()
