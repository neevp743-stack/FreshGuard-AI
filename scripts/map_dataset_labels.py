import os
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

classes = [
    "milk", "bread", "apple", "banana", "egg", "tomato", "potato", "onion", "rice", "yogurt",
    "cheese", "biscuit", "juice", "water", "packaged_snack", "carrot", "cabbage", "cauliflower",
    "capsicum", "cucumber", "brinjal", "broccoli", "spinach", "peas", "corn", "garlic", "ginger",
    "okra", "beetroot", "radish", "pumpkin", "bitter_gourd", "bottle_gourd", "green_chilli", "sweet_potato"
]

class_to_image = {cls_id: None for cls_id in range(len(classes))}

label_files = glob.glob(os.path.join(DATASETS_DIR, "**", "labels", "*", "*.txt"), recursive=True) + \
              glob.glob(os.path.join(DATASETS_DIR, "**", "labels", "*.txt"), recursive=True)

print(f"Total dataset label files found: {len(label_files)}")

for lbl in label_files:
    try:
        with open(lbl, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if parts:
                cls_id = int(parts[0])
                if cls_id in class_to_image and class_to_image[cls_id] is None:
                    # Find corresponding image file
                    base_name = os.path.splitext(os.path.basename(lbl))[0]
                    lbl_dir = os.path.dirname(lbl)
                    img_dir = lbl_dir.replace("labels", "images")
                    for ext in [".jpg", ".png", ".jpeg"]:
                        cand = os.path.join(img_dir, base_name + ext)
                        if os.path.exists(cand):
                            class_to_image[cls_id] = cand
                            break
    except Exception:
        pass

print("\n--- CLASS TO REAL DATASET IMAGE MAPPING ---")
for cls_id, name in enumerate(classes):
    img = class_to_image[cls_id]
    if img:
        print(f"ID {cls_id:<2} | {name:<16}: {os.path.basename(img)}")
    else:
        print(f"ID {cls_id:<2} | {name:<16}: [NO LABEL FILE MATCH]")
