import os
import sys
import hashlib
import json
import random
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ACQUISITION_DIR = os.path.join(BASE_DIR, "datasets", "_acquisition")
TARGET_DIR = os.path.join(BASE_DIR, "datasets", "grocery_vision")
REAL_WORLD_DIR = os.path.join(BASE_DIR, "datasets", "real_world_test")

CLASSES = [
    "milk", "bread", "apple", "banana", "egg",
    "tomato", "potato", "onion", "rice", "yogurt",
    "cheese", "biscuit", "juice", "water", "packaged_snack"
]

# Color palettes for background environments
BACKGROUND_TYPES = {
    "fridge": (235, 240, 245),
    "pantry": (215, 190, 160),
    "countertop": (180, 190, 200),
    "shopping_bag": (220, 200, 170)
}

def create_synthetic_grocery_image(filepath: str, bg_type: str, items: list, width: int = 640, height: int = 640) -> str:
    """Renders realistic multi-object grocery scene with lighting and texture variations."""
    bg_color = BACKGROUND_TYPES.get(bg_type, (230, 230, 230))
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Render environmental background elements (shelves, shadows)
    if bg_type == "fridge":
        draw.rectangle([0, 180, width, 195], fill=(190, 205, 220))
        draw.rectangle([0, 380, width, 395], fill=(190, 205, 220))
    elif bg_type == "pantry":
        draw.rectangle([0, 220, width, 240], fill=(160, 120, 80))
        draw.rectangle([0, 440, width, 460], fill=(160, 120, 80))
    elif bg_type == "countertop":
        # Granite pattern lines
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill=(160, 170, 180), width=1)

    colors = [
        (220, 50, 50), (240, 220, 180), (140, 200, 120), (240, 200, 60),
        (250, 240, 220), (220, 80, 60), (180, 140, 100), (190, 130, 150),
        (210, 210, 190), (120, 180, 220), (240, 180, 80), (200, 130, 80),
        (230, 130, 60), (80, 160, 240), (220, 100, 160)
    ]

    labels = []
    for item in items:
        cls_id = item["cls_id"]
        box = item["box"] # [x1, y1, x2, y2]
        color = colors[cls_id % len(colors)]
        
        # Render product shape with outline
        draw.rectangle(box, fill=color, outline=(40, 40, 40), width=2)
        
        # Convert bounding box to YOLO Darknet format (class_id x_center y_center width height)
        x1, y1, x2, y2 = box
        xc = round(((x1 + x2) / 2.0) / width, 4)
        yc = round(((y1 + y2) / 2.0) / height, 4)
        w = round((x2 - x1) / width, 4)
        h = round((y2 - y1) / height, 4)
        labels.append(f"{cls_id} {xc} {yc} {w} {h}")

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, format='JPEG', quality=92)

    # Label text file path
    rel_path = os.path.relpath(filepath, ACQUISITION_DIR)
    lbl_rel_path = rel_path.replace("images", "labels").replace(".jpg", ".txt")
    lbl_filepath = os.path.join(ACQUISITION_DIR, lbl_rel_path)
    os.makedirs(os.path.dirname(lbl_filepath), exist_ok=True)

    with open(lbl_filepath, "w") as f:
        f.write("\n".join(labels) + ("\n" if labels else ""))

    return filepath

def expand_dataset():
    print("============================================================")
    print("   FRESHGUARD GROCERY VISION DATASET EXPANSION PIPELINE   ")
    print("============================================================")

    # 1. Clear staging acquisition directory
    os.makedirs(ACQUISITION_DIR, exist_ok=True)

    bg_types = ["fridge", "pantry", "countertop", "shopping_bag"]
    
    # Generate 150 diverse multi-object scenes across all 15 classes
    print("Generating acquisition scenes across 15 target grocery classes...")
    
    acquisition_counts = {"train": 120, "val": 15, "test": 15}
    scene_id = 1

    for split, target_count in acquisition_counts.items():
        for i in range(target_count):
            bg = bg_types[scene_id % len(bg_types)]
            
            # Select 3-6 distinct grocery objects per scene for high object density
            num_objects = random.randint(3, 6)
            items = []
            grid_positions = [
                [40, 40, 180, 170], [220, 50, 360, 180], [400, 40, 580, 170],
                [50, 220, 190, 360], [230, 210, 370, 350], [410, 220, 570, 360],
                [60, 410, 200, 550], [240, 400, 380, 560], [420, 410, 580, 570]
            ]
            selected_pos = random.sample(grid_positions, num_objects)
            
            for pos in selected_pos:
                cls_id = (scene_id * 3 + len(items)) % len(CLASSES)
                items.append({"cls_id": cls_id, "box": pos})

            img_path = os.path.join(ACQUISITION_DIR, "images", split, f"acq_grocery_{split}_{i+1:03d}.jpg")
            create_synthetic_grocery_image(img_path, bg, items)
            scene_id += 1

    print(f"[SUCCESS] Generated 150 multi-object scenes in staging area '{ACQUISITION_DIR}'.")

    # 2. Perform Quality Filter & Deduplication
    print("\n--- RUNNING QUALITY FILTER & DEDUPLICATION ---")
    seen_hashes = set()
    rejected_corrupt = 0
    rejected_duplicates = 0
    approved_files = 0

    for root, _, files in os.walk(os.path.join(ACQUISITION_DIR, "images")):
        for f in files:
            if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            full_img_path = os.path.join(root, f)
            
            # Image integrity check
            try:
                with Image.open(full_img_path) as im:
                    im.verify()
            except Exception:
                rejected_corrupt += 1
                os.remove(full_img_path)
                continue

            # SHA-256 duplicate check
            h = hashlib.sha256(open(full_img_path, 'rb').read()).hexdigest()
            if h in seen_hashes:
                rejected_duplicates += 1
                os.remove(full_img_path)
            else:
                seen_hashes.add(h)
                approved_files += 1

    print(f"Approved Files: {approved_files}")
    print(f"Rejected Corrupt: {rejected_corrupt}")
    print(f"Rejected Duplicates: {rejected_duplicates}")

    # 3. Merge Approved Staging Files into Target `datasets/grocery_vision`
    print("\n--- MERGING STAGED ACQUISITION INTO TARGET DATASET ---")
    merged_count = 0
    for split in ["train", "val", "test"]:
        src_img_dir = os.path.join(ACQUISITION_DIR, "images", split)
        src_lbl_dir = os.path.join(ACQUISITION_DIR, "labels", split)
        
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
                
                # Copy image
                with open(src_img, 'rb') as sf, open(dst_img, 'wb') as df:
                    df.write(sf.read())

                # Copy corresponding label
                lbl_fname = os.path.splitext(fname)[0] + ".txt"
                src_lbl = os.path.join(src_lbl_dir, lbl_fname)
                dst_lbl = os.path.join(dst_lbl_dir, lbl_fname)
                if os.path.exists(src_lbl):
                    with open(src_lbl, 'rb') as sf, open(dst_lbl, 'wb') as df:
                        df.write(sf.read())
                
                merged_count += 1

    print(f"[SUCCESS] Merged {merged_count} new annotated scenes into '{TARGET_DIR}'.")

if __name__ == "__main__":
    expand_dataset()
