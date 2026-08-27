# FreshGuard AI — Dataset Requirements & Vision Model Specification

**Repository:** FreshGuard-AI  
**Task Type:** Multi-Class Grocery Object Detection (YOLOv8 Bounding Box Annotation)  
**Date:** August 27, 2026  

---

## 1. Objective & Target Detection Scope

The FreshGuard AI Vision module performs real-time multi-object grocery detection to identify, count, and classify household food items in kitchen, refrigerator, and pantry settings.

---

## 2. Model Architecture & Pipeline Specifications

- **Framework:** PyTorch / Ultralytics YOLOv8 (`yolov8n.pt`).
- **Task Type:** **Object Detection** (2D Bounding Boxes).
- **Target Resolution:** 640x640 pixels (RGB).
- **Supported Image Formats:** `.jpg`, `.jpeg`, `.png`, `.webp`.
- **Annotation Format:** YOLO Darknet Format (`.txt` files containing `<class_id> <x_center> <y_center> <width> <height>` normalized between 0.0 and 1.0).

---

## 3. Supported Grocery Classes (15 Classes)

| Class ID | Class Name | Category | Description / Sample Products |
|---|---|---|---|
| `0` | `milk` | Dairy | Fluid milk cartons, bottles, pouches |
| `1` | `bread` | Bakery | Sliced bread loaves, buns, bakery loaves |
| `2` | `apple` | Produce / Fruits | Fresh apples (red, green, yellow) |
| `3` | `banana` | Produce / Fruits | Fresh bananas (single or bunch) |
| `4` | `egg` | Dairy / Eggs | Individual eggs or egg cartons |
| `5` | `tomato` | Produce / Vegetables | Fresh tomatoes |
| `6` | `potato` | Produce / Vegetables | Fresh raw potatoes |
| `7` | `onion` | Produce / Vegetables | Fresh raw onions |
| `8` | `rice` | Grains / Staples | Rice bags, grain packets |
| `9` | `yogurt` | Dairy | Yogurt cups, tubs, dahi containers |
| `10` | `cheese` | Dairy | Cheese blocks, slices, butter/cheese tubs |
| `11` | `biscuit` | Packaged Goods | Biscuit / cookie packs |
| `12` | `juice` | Beverages | Fruit juice cartons or bottles |
| `13` | `water` | Beverages | Water bottles |
| `14` | `packaged_snack` | Packaged Goods | Chips, snack bags, packaged items |

---

## 4. Expected Dataset Directory Structure

```
datasets/grocery_vision/
├── data.yaml
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

### `data.yaml` Configuration Specification
```yaml
path: ../datasets/grocery_vision
train: images/train
val: images/val
test: images/test

nc: 15
names:
  0: milk
  1: bread
  2: apple
  3: banana
  4: egg
  5: tomato
  6: potato
  7: onion
  8: rice
  9: yogurt
  10: cheese
  11: biscuit
  12: juice
  13: water
  14: packaged_snack
```

---

## 5. Quality & Environmental Criteria

1. **Environment Variation:** Realistic household settings (refrigerator shelves, pantry racks, kitchen countertops).
2. **Lighting Conditions:** High contrast, ambient kitchen light, dim fridge interior illumination.
3. **Occlusion & Clutter:** Multi-object clutter, partially hidden products (>= 30% visibility).
4. **Anti-Leakage Protocol:** Burst shots or images from the same camera session must belong exclusively to a single split directory (`train`, `val`, or `test`).
