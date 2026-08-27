import os
import sys
import time
import json
import yaml
import torch
from ultralytics import YOLO

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXP_DIR = os.path.join(BASE_DIR, "vision_models", "experiments", "grocery_yolov8_v1")
DATA_YAML = os.path.join(BASE_DIR, "datasets", "grocery_vision", "data.yaml")

def setup_experiment_directory():
    os.makedirs(os.path.join(EXP_DIR, "weights"), exist_ok=True)
    os.makedirs(os.path.join(EXP_DIR, "results"), exist_ok=True)
    os.makedirs(os.path.join(EXP_DIR, "metrics"), exist_ok=True)
    os.makedirs(os.path.join(EXP_DIR, "plots"), exist_ok=True)

    config = {
        "experiment_name": "grocery_yolov8_v1",
        "architecture": "YOLOv8n (yolov8n.pt)",
        "imgsz": 640,
        "epochs": 5,
        "batch_size": 8,
        "optimizer": "auto",
        "lr0": 0.01,
        "seed": 42,
        "device": "cpu",
        "dataset_yaml": DATA_YAML
    }

    config_path = os.path.join(EXP_DIR, "training_config.yaml")
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    print(f"[SETUP] Created experiment directory structure at: {EXP_DIR}")
    return config

def run_training_experiment():
    print("============================================================")
    print("   FRESHGUARD EXPERIMENTAL GROCERY VISION MODEL TRAINING    ")
    print("============================================================")
    
    config = setup_experiment_directory()

    # 1. Initialize YOLOv8n Pretrained Model
    t0 = time.time()
    model = YOLO("yolov8n.pt")

    # 2. Train Model on FreshGuard Grocery Vision Dataset
    results = model.train(
        data=DATA_YAML,
        epochs=config["epochs"],
        imgsz=config["imgsz"],
        batch=config["batch_size"],
        seed=config["seed"],
        project=os.path.join(EXP_DIR, "results"),
        name="run_1",
        exist_ok=True,
        workers=0,
        verbose=True
    )
    t1 = time.time()
    train_duration = round(t1 - t0, 2)
    print(f"\n[TRAINING COMPLETE] Duration: {train_duration} seconds.")

    # 3. Save Experimental Model Weights
    best_weight_src = os.path.join(EXP_DIR, "results", "run_1", "weights", "best.pt")
    exp_best_weight = os.path.join(EXP_DIR, "weights", "best.pt")
    
    if os.path.exists(best_weight_src):
        with open(best_weight_src, 'rb') as fsrc, open(exp_best_weight, 'wb') as fdst:
            fdst.write(fsrc.read())
        print(f"[WEIGHTS] Experimental weights saved to: {exp_best_weight}")

    # 4. Evaluate on Validation Set
    print("\n--- EVALUATING ON VALIDATION SET ---")
    val_metrics = model.val(data=DATA_YAML, split="val", imgsz=640, project=os.path.join(EXP_DIR, "metrics"), name="val_eval", exist_ok=True)
    
    val_map50 = round(float(val_metrics.box.map50), 4)
    val_map50_95 = round(float(val_metrics.box.map), 4)
    val_mp = round(float(val_metrics.box.mp), 4)
    val_mr = round(float(val_metrics.box.mr), 4)

    print(f"Validation mAP@50: {val_map50}")
    print(f"Validation mAP@50-95: {val_map50_95}")
    print(f"Validation Precision: {val_mp}")
    print(f"Validation Recall: {val_mr}")

    # 5. Evaluate on Unseen Test Set
    print("\n--- EVALUATING ON UNSEEN TEST SET ---")
    test_metrics = model.val(data=DATA_YAML, split="test", imgsz=640, project=os.path.join(EXP_DIR, "metrics"), name="test_eval", exist_ok=True)

    test_map50 = round(float(test_metrics.box.map50), 4)
    test_map50_95 = round(float(test_metrics.box.map), 4)
    test_mp = round(float(test_metrics.box.mp), 4)
    test_mr = round(float(test_metrics.box.mr), 4)

    print(f"Test mAP@50: {test_map50}")
    print(f"Test mAP@50-95: {test_map50_95}")
    print(f"Test Precision: {test_mp}")
    print(f"Test Recall: {test_mr}")

    # 6. Benchmark Inference Latency & Speed
    print("\n--- BENCHMARKING INFERENCE SPEED ---")
    test_img_dir = os.path.join(BASE_DIR, "datasets", "grocery_vision", "images", "test")
    sample_images = [os.path.join(test_img_dir, f) for f in os.listdir(test_img_dir) if f.endswith(".jpg")][:5]
    
    latencies = []
    for img_p in sample_images:
        t_start = time.perf_counter()
        pred = model.predict(img_p, imgsz=640, verbose=False)
        t_end = time.perf_counter()
        latencies.append((t_end - t_start) * 1000)

    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0.0
    approx_fps = round(1000.0 / avg_latency, 2) if avg_latency > 0 else 0.0

    print(f"Average CPU Inference Latency: {avg_latency} ms ({approx_fps} FPS)")

    # 7. Write EXPERIMENT_INFO.md
    exp_info_path = os.path.join(EXP_DIR, "EXPERIMENT_INFO.md")
    with open(exp_info_path, "w") as f:
        f.write(f"""# Experimental Model Information — grocery_yolov8_v1

- **Experiment Name:** grocery_yolov8_v1
- **Architecture:** Ultralytics YOLOv8n (`yolov8n.pt`)
- **Dataset Version:** FreshGuard Grocery Vision Dataset v1 (178 images, 729 objects)
- **Target Classes:** 15 Target Grocery Classes
- **Training Epochs:** 5
- **Batch Size:** 8
- **Hardware:** CPU (Intel/AMD x86_64, PyTorch 2.13.0)
- **Training Duration:** {train_duration} s
- **Validation mAP@50:** {val_map50}
- **Validation mAP@50-95:** {val_map50_95}
- **Unseen Test mAP@50:** {test_map50}
- **Unseen Test mAP@50-95:** {test_map50_95}
- **Inference Speed:** {avg_latency} ms / frame ({approx_fps} FPS)
- **Status:** EXPERIMENTAL (Not deployed to production)
""")

    print(f"[SUCCESS] Wrote experiment metadata to '{exp_info_path}'.")
    return {
        "train_duration": train_duration,
        "val_map50": val_map50,
        "val_map50_95": val_map50_95,
        "val_mp": val_mp,
        "val_mr": val_mr,
        "test_map50": test_map50,
        "test_map50_95": test_map50_95,
        "test_mp": test_mp,
        "test_mr": test_mr,
        "avg_latency": avg_latency,
        "approx_fps": approx_fps
    }

if __name__ == "__main__":
    run_training_experiment()
