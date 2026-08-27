import os
import json
import time
from app.ai.vision.validate_dataset import validate_dataset

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../docs"))
EVAL_DOC_PATH = os.path.join(DOCS_DIR, "vision_model_evaluation.md")
VISION_MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models"))
WEIGHTS_PATH = os.path.join(VISION_MODELS_DIR, "grocery_vision_v1", "weights", "best.pt")
METADATA_PATH = os.path.join(VISION_MODELS_DIR, "model_metadata.json")

def generate_evaluation_report():
    os.makedirs(DOCS_DIR, exist_ok=True)
    val_report = validate_dataset()

    # Zero False Claims Rule Check
    if not os.path.exists(WEIGHTS_PATH) or val_report["split_image_counts"]["test"] == 0:
        doc_content = """# FreshGuard Grocery Vision AI — Model Evaluation Report

## Status: Pending Dataset & Model Training
> **"Vision model training not performed because dataset is not available."**

### Current Dataset & Pipeline Status
- **Model Lifecycle State**: `NOT_TRAINED`
- **Annotated Test Images**: 0
- **Model Weights Path**: `vision_models/grocery_vision_v1/weights/best.pt` (Not Found)

### Evaluation Metrics Summary
- **Precision**: N/A (Training pending)
- **Recall**: N/A (Training pending)
- **mAP@0.5**: N/A (Training pending)
- **mAP@0.5:0.95**: N/A (Training pending)
- **Average CPU Inference Latency**: N/A (Training pending)

---
*Note: This report will automatically update upon running model training (`python -m app.ai.vision.train`) after dataset annotation.*
"""
        with open(EVAL_DOC_PATH, "w") as f:
            f.write(doc_content)
        print(f"Evaluation report written to {EVAL_DOC_PATH}")
        return

    # Evaluate trained model
    try:
        from ultralytics import YOLO
        model = YOLO(WEIGHTS_PATH)

        t0 = time.time()
        results = model.val(data=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../datasets/grocery_vision/data.yaml")), split="test")
        latency = (time.time() - t0) * 1000 / max(1, val_report["split_image_counts"]["test"])

        metrics = results.results_dict
        p = metrics.get("metrics/precision(B)", 0.0)
        r = metrics.get("metrics/recall(B)", 0.0)
        map50 = metrics.get("metrics/mAP50(B)", 0.0)
        map5095 = metrics.get("metrics/mAP50-95(B)", 0.0)

        doc_content = f"""# FreshGuard Grocery Vision AI — Model Evaluation Report

## Status: Model Evaluated on Untouched Test Set

### Performance Metrics Summary
- **Model Architecture**: Ultralytics YOLOv8n (`yolov8n.pt`)
- **Precision**: {p:.4f}
- **Recall**: {r:.4f}
- **mAP@0.5**: {map50:.4f}
- **mAP@0.5:0.95**: {map5095:.4f}
- **Average CPU Inference Latency**: {latency:.2f} ms / frame

### Test Dataset Breakdown
- **Test Images Count**: {val_report['split_image_counts']['test']}
- **Total Objects Evaluated**: {val_report['total_objects']}
"""
        with open(EVAL_DOC_PATH, "w") as f:
            f.write(doc_content)
        print(f"Evaluation report written to {EVAL_DOC_PATH}")

    except Exception as ex:
        print(f"Error during model evaluation: {ex}")

if __name__ == "__main__":
    generate_evaluation_report()
