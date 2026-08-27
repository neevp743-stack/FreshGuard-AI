import os
import sys
import time
import json
import yaml
import torch
from ultralytics import YOLO

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXP_DIR_V2 = os.path.join(BASE_DIR, "vision_models", "experiments", "grocery_yolov8_v2")
DATA_YAML = os.path.join(BASE_DIR, "datasets", "grocery_vision", "data.yaml")

def setup_experiment_v2():
    os.makedirs(os.path.join(EXP_DIR_V2, "weights"), exist_ok=True)
    os.makedirs(os.path.join(EXP_DIR_V2, "results"), exist_ok=True)
    os.makedirs(os.path.join(EXP_DIR_V2, "metrics"), exist_ok=True)
    os.makedirs(os.path.join(EXP_DIR_V2, "plots"), exist_ok=True)

    config = {
        "experiment_name": "grocery_yolov8_v2",
        "architecture": "YOLOv8n (yolov8n.pt)",
        "imgsz": 640,
        "epochs": 5,
        "batch_size": 8,
        "optimizer": "auto",
        "seed": 42,
        "classes_count": 35,
        "dataset_yaml": DATA_YAML
    }

    with open(os.path.join(EXP_DIR_V2, "training_config.yaml"), "w") as f:
        yaml.dump(config, f)

    print(f"[SETUP V2] Experimental directory created at: {EXP_DIR_V2}")
    return config

def train_and_eval_v2():
    print("============================================================")
    print("   FRESHGUARD EXPERIMENTAL GROCERY & VEGETABLE YOLOV8 V2   ")
    print("============================================================")

    config = setup_experiment_v2()

    # 1. Initialize YOLOv8n
    t0 = time.time()
    model = YOLO("yolov8n.pt")

    # 2. Train on 35-Class Expanded Dataset
    results = model.train(
        data=DATA_YAML,
        epochs=config["epochs"],
        imgsz=config["imgsz"],
        batch=config["batch_size"],
        seed=config["seed"],
        project=os.path.join(EXP_DIR_V2, "results"),
        name="run_v2",
        exist_ok=True,
        workers=0,
        verbose=True
    )
    t1 = time.time()
    train_duration = round(t1 - t0, 2)
    print(f"\n[V2 TRAINING COMPLETE] Duration: {train_duration} seconds.")

    # 3. Save Experimental V2 Weights
    best_src = os.path.join(EXP_DIR_V2, "results", "run_v2", "weights", "best.pt")
    exp_best = os.path.join(EXP_DIR_V2, "weights", "best.pt")
    if os.path.exists(best_src):
        with open(best_src, 'rb') as sf, open(exp_best, 'wb') as df:
            df.write(sf.read())
        print(f"[WEIGHTS V2] Experimental weights saved to: {exp_best}")

    # 4. Evaluate on Validation Set
    print("\n--- V2 EVALUATION ON VALIDATION SET ---")
    val_m = model.val(data=DATA_YAML, split="val", imgsz=640, project=os.path.join(EXP_DIR_V2, "metrics"), name="val_eval", exist_ok=True)

    val_map50 = round(float(val_m.box.map50), 4)
    val_map50_95 = round(float(val_m.box.map), 4)
    val_mp = round(float(val_m.box.mp), 4)
    val_mr = round(float(val_m.box.mr), 4)

    # 5. Evaluate on Unseen Test Set
    print("\n--- V2 EVALUATION ON UNSEEN TEST SET ---")
    test_m = model.val(data=DATA_YAML, split="test", imgsz=640, project=os.path.join(EXP_DIR_V2, "metrics"), name="test_eval", exist_ok=True)

    test_map50 = round(float(test_m.box.map50), 4)
    test_map50_95 = round(float(test_m.box.map), 4)
    test_mp = round(float(test_m.box.mp), 4)
    test_mr = round(float(test_m.box.mr), 4)

    # 6. Inference Speed Benchmark
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

    print(f"\nV2 CPU Inference Speed: {avg_latency} ms ({approx_fps} FPS)")

    # 7. Write EXPERIMENT_INFO.md for V2
    v2_info_path = os.path.join(EXP_DIR_V2, "EXPERIMENT_INFO.md")
    with open(v2_info_path, "w") as f:
        f.write(f"""# Experimental Model Information — grocery_yolov8_v2

- **Experiment Name:** grocery_yolov8_v2
- **Architecture:** Ultralytics YOLOv8n (`yolov8n.pt`)
- **Dataset Version:** FreshGuard Grocery & Vegetable Vision Dataset v2 (328 images, 1,345 objects)
- **Target Classes:** 35 Target Classes (15 Grocery + 20 Vegetables)
- **Training Epochs:** 5
- **Batch Size:** 8
- **Hardware:** CPU Mode (PyTorch 2.13.0)
- **Training Duration:** {train_duration} s
- **Validation mAP@50:** {val_map50}
- **Validation mAP@50-95:** {val_map50_95}
- **Unseen Test mAP@50:** {test_map50}
- **Unseen Test mAP@50-95:** {test_map50_95}
- **Inference Speed:** {avg_latency} ms / frame ({approx_fps} FPS)
- **Status:** EXPERIMENTAL (Not deployed to production)
""")

    print(f"[SUCCESS] Wrote V2 experiment info to '{v2_info_path}'.")

if __name__ == "__main__":
    train_and_eval_v2()
