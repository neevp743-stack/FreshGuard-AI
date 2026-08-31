import os
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

all_images = []
for root, dirs, files in os.walk(DATASETS_DIR):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            all_images.append(os.path.join(root, f))

print(f"Total dataset images found: {len(all_images)}")

classes = [
    "milk", "bread", "apple", "banana", "egg", "tomato", "potato", "onion", "rice", "yogurt",
    "cheese", "biscuit", "juice", "water", "packaged_snack", "carrot", "cabbage", "cauliflower",
    "capsicum", "cucumber", "brinjal", "broccoli", "spinach", "peas", "corn", "garlic", "ginger",
    "okra", "beetroot", "radish", "pumpkin", "bitter_gourd", "bottle_gourd", "green_chilli", "sweet_potato"
]

class_image_map = {}
for cls in classes:
    matches = [img for img in all_images if cls.lower() in os.path.basename(img).lower()]
    class_image_map[cls] = matches

for cls, imgs in class_image_map.items():
    print(f"{cls:<16}: {len(imgs)} matching image(s)")
    if imgs:
        print(f"   -> Example: {os.path.basename(imgs[0])}")
