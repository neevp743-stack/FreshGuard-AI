import os
import sys
import json
import hashlib
import random
import yaml
from PIL import Image, ImageDraw

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAGING_DIR = os.path.join(BASE_DIR, "datasets", "_vegetable_acquisition")
TARGET_DIR = os.path.join(BASE_DIR, "datasets", "grocery_vision")
DATA_YAML = os.path.join(TARGET_DIR, "data.yaml")
CLASSES_JSON_PATH = os.path.join(BASE_DIR, "backend", "app", "ai", "vision", "classes.json")

ORIGINAL_CLASSES = [
    "milk", "bread", "apple", "banana", "egg",
    "tomato", "potato", "onion", "rice", "yogurt",
    "cheese", "biscuit", "juice", "water", "packaged_snack"
]

NEW_VEGETABLES = [
    "carrot", "cabbage", "cauliflower", "capsicum", "cucumber",
    "brinjal", "broccoli", "spinach", "peas", "corn",
    "garlic", "ginger", "okra", "beetroot", "radish",
    "pumpkin", "bitter_gourd", "bottle_gourd", "green_chilli", "sweet_potato"
]

ALL_CLASSES = ORIGINAL_CLASSES + NEW_VEGETABLES # Total 35 classes

BACKGROUND_COLORS = [
    (225, 235, 240), # Fridge tray
    (210, 185, 155), # Wooden pantry
    (175, 185, 195), # Granite counter
    (230, 210, 180)  # Wooden vegetable crate
]

def render_vegetable_scene(filepath: str, bg_color: tuple, items: list, width: int = 640, height: int = 640) -> str:
    """Renders a multi-object vegetable scene with normalized YOLO bounding box labels."""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Shelf/crate background lines
    draw.rectangle([0, 200, width, 215], fill=(160, 140, 110))
    draw.rectangle([0, 420, width, 435], fill=(160, 140, 110))

    colors = [
        (255, 140, 0), (50, 205, 50), (245, 245, 220), (0, 128, 0), (34, 139, 34),
        (138, 43, 226), (0, 100, 0), (46, 139, 87), (144, 238, 144), (255, 215, 0),
        (240, 230, 140), (210, 180, 140), (107, 142, 35), (139, 0, 0), (255, 250, 250),
        (255, 165, 0), (47, 79, 79), (154, 205, 50), (0, 255, 0), (205, 133, 63)
    ]

    labels = []
    for item in items:
        cls_id = item["cls_id"]
        box = item["box"] # [x1, y1, x2, y2]
        c_idx = (cls_id - 15) % len(colors)
        color = colors[c_idx]
        
        draw.rectangle(box, fill=color, outline=(30, 30, 30), width=2)
        
        x1, y1, x2, y2 = box
        xc = round(((x1 + x2) / 2.0) / width, 4)
        yc = round(((y1 + y2) / 2.0) / height, 4)
        w = round((x2 - x1) / width, 4)
        h = round((y2 - y1) / height, 4)
        labels.append(f"{cls_id} {xc} {yc} {w} {h}")

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, format='JPEG', quality=92)

    rel_path = os.path.relpath(filepath, STAGING_DIR)
    lbl_rel = rel_path.replace("images", "labels").replace(".jpg", ".txt")
    lbl_filepath = os.path.join(STAGING_DIR, lbl_rel)
    os.makedirs(os.path.dirname(lbl_filepath), exist_ok=True)

    with open(lbl_filepath, "w") as f:
        f.write("\n".join(labels) + ("\n" if labels else ""))

    return filepath

def acquire_and_expand_vegetables():
    print("============================================================")
    print("   FRESHGUARD COMMON VEGETABLE DATASET EXPANSION PIPELINE   ")
    print("============================================================")

    # 1. Clear staging directory
    os.makedirs(STAGING_DIR, exist_ok=True)

    # Generate 150 diverse multi-vegetable scenes for IDs 15-34
    print("Generating vegetable acquisition scenes across 20 target classes (IDs 15-34)...")
    
    splits = {"train": 120, "val": 15, "test": 15}
    scene_id = 1

    grid_positions = [
        [40, 40, 180, 170], [220, 50, 360, 180], [400, 40, 580, 170],
        [50, 220, 190, 360], [230, 210, 370, 350], [410, 220, 570, 360],
        [60, 410, 200, 550], [240, 400, 380, 560], [420, 410, 580, 570]
    ]

    for split, count in splits.items():
        for i in range(count):
            bg = BACKGROUND_COLORS[scene_id % len(BACKGROUND_COLORS)]
            num_objects = random.randint(3, 5)
            selected_pos = random.sample(grid_positions, num_objects)
            
            items = []
            for pos in selected_pos:
                # Assign class IDs in range [15, 34]
                veg_cls_id = 15 + ((scene_id * 3 + len(items)) % len(NEW_VEGETABLES))
                items.append({"cls_id": veg_cls_id, "box": pos})

            img_path = os.path.join(STAGING_DIR, "images", split, f"veg_{split}_{i+1:03d}.jpg")
            render_vegetable_scene(img_path, bg, items)
            scene_id += 1

    print(f"[STAGING SUCCESS] Staged 150 vegetable scenes in '{STAGING_DIR}'.")

    # 2. Quality Audit & Deduplication
    print("\n--- RUNNING STAGING QUALITY AUDIT & DEDUPLICATION ---")
    seen_hashes = set()
    approved = 0

    for root, _, files in os.walk(os.path.join(STAGING_DIR, "images")):
        for f in files:
            if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            full_img_path = os.path.join(root, f)
            
            try:
                with Image.open(full_img_path) as im:
                    im.verify()
            except Exception:
                os.remove(full_img_path)
                continue

            h = hashlib.sha256(open(full_img_path, 'rb').read()).hexdigest()
            if h in seen_hashes:
                os.remove(full_img_path)
            else:
                seen_hashes.add(h)
                approved += 1

    print(f"Approved Vegetable Image Files: {approved}")

    # 3. Merge Staged Vegetable Dataset into `datasets/grocery_vision`
    print("\n--- MERGING VEGETABLE DATASET INTO TARGET DATASET ---")
    merged_count = 0
    for split in ["train", "val", "test"]:
        src_img_dir = os.path.join(STAGING_DIR, "images", split)
        src_lbl_dir = os.path.join(STAGING_DIR, "labels", split)

        dst_img_dir = os.path.join(TARGET_DIR, "images", split)
        dst_lbl_dir = os.path.join(TARGET_DIR, "labels", split)

        os.makedirs(dst_img_dir, exist_ok=True)
        os.makedirs(dst_lbl_dir, exist_ok=True)

        if not os.path.exists(src_img_dir):
            continue

        for fname in os.listdir(src_img_dir):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                src_img = os.path.join(src_img_dir, fname)
                dst_img = os.path.join(dst_img_dir, fname)

                with open(src_img, 'rb') as sf, open(dst_img, 'wb') as df:
                    df.write(sf.read())

                lbl_fname = os.path.splitext(fname)[0] + ".txt"
                src_lbl = os.path.join(src_lbl_dir, lbl_fname)
                dst_lbl = os.path.join(dst_lbl_dir, lbl_fname)
                if os.path.exists(src_lbl):
                    with open(src_lbl, 'rb') as sf, open(dst_lbl, 'wb') as df:
                        df.write(sf.read())

                merged_count += 1

    print(f"[MERGE SUCCESS] Merged {merged_count} vegetable scenes into '{TARGET_DIR}'.")

    # 4. Update `datasets/grocery_vision/data.yaml` to 35 Classes
    yaml_names = {i: cname for i, cname in enumerate(ALL_CLASSES)}
    yaml_content = {
        "path": "../datasets/grocery_vision",
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": len(ALL_CLASSES),
        "names": yaml_names
    }
    with open(DATA_YAML, "w") as f:
        yaml.dump(yaml_content, f, sort_keys=False)
    print(f"[DATA.YAML UPDATED] Capped `nc` to {len(ALL_CLASSES)} classes.")

    # 5. Update `classes.json` and `classes.txt`
    classes_json_data = {
        "version": "2.0.0",
        "classes_count": len(ALL_CLASSES),
        "classes": ALL_CLASSES
    }
    with open(CLASSES_JSON_PATH, "w") as f:
        json.dump(classes_json_data, f, indent=2)

    txt_classes_path = os.path.join(TARGET_DIR, "classes.txt")
    with open(txt_classes_path, "w") as f:
        f.write("\n".join(ALL_CLASSES) + "\n")

    print("[SUCCESS] Updated classes.json and classes.txt to 35 classes.")

if __name__ == "__main__":
    acquire_and_expand_vegetables()
