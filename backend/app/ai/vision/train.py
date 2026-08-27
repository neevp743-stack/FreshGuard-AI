import os
import json
from datetime import datetime
from app.ai.vision.validate_dataset import validate_dataset

VISION_MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models"))
METADATA_PATH = os.path.join(VISION_MODELS_DIR, "model_metadata.json")
DATA_YAML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../datasets/grocery_vision/data.yaml"))

def update_metadata(state: str, metrics: dict = None, message: str = None):
    os.makedirs(VISION_MODELS_DIR, exist_ok=True)
    meta = {
        "model_name": "FreshGuard Grocery Vision",
        "version": "0.1.0",
        "lifecycle_state": state,
        "classes_count": 15,
        "training_dataset_version": "v1",
        "created_at": datetime.utcnow().isoformat(),
        "model_architecture": "Ultralytics YOLOv8n (yolov8n.pt)",
        "framework": "PyTorch / Ultralytics 8.1.24",
        "metrics": metrics or {},
        "message": message or f"Model state updated to {state}."
    }
    with open(METADATA_PATH, "w") as f:
        json.dump(meta, f, indent=2)

def train_model(epochs: int = 25, imgsz: int = 640):
    print("=== FreshGuard AI Vision Training Pipeline ===")

    # 1. Dataset Pre-training Validation Check
    val_report = validate_dataset()
    if not val_report["is_valid"] or val_report["annotated_images"] == 0:
        print("\n❌ CANNOT START TRAINING: Dataset is missing, unannotated, or invalid.")
        print(f"Annotated Images Count: {val_report['annotated_images']}")
        update_metadata(
            state="NOT_TRAINED",
            message="Vision model integration is ready; training is pending the real grocery dataset."
        )
        return False

    print("\n✅ Dataset Validation Passed! Transitioning model state to TRAINING...")
    update_metadata(state="TRAINING", message="Training in progress...")

    try:
        from ultralytics import YOLO

        # Load Pinned Ultralytics YOLOv8n Base Weights
        model = YOLO("yolov8n.pt")

        # Train Model
        results = model.train(
            data=DATA_YAML_PATH,
            epochs=epochs,
            imgsz=imgsz,
            project=VISION_MODELS_DIR,
            name="grocery_vision_v1",
            exist_ok=True,
            fliplr=0.5,
            hsv_h=0.015,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=10.0,
            translate=0.1,
            scale=0.5,
        )

        metrics = {
            "mAP50": getattr(results, "results_dict", {}).get("metrics/mAP50(B)", 0.0),
            "mAP50-95": getattr(results, "results_dict", {}).get("metrics/mAP50-95(B)", 0.0),
        }

        print("\n🎉 Training completed successfully! Transitioning model state to READY.")
        update_metadata(state="READY", metrics=metrics, message="Trained model weights ready for inference.")
        return True

    except Exception as ex:
        print(f"\n❌ Model Training Failed: {ex}")
        update_metadata(state="FAILED", message=f"Training failed: {ex}")
        return False

if __name__ == "__main__":
    train_model()
