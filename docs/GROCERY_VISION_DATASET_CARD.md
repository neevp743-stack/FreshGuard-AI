# FreshGuard AI — Grocery Vision Dataset Card

**Dataset Name:** FreshGuard Grocery Vision Dataset  
**Version:** 1.1.0  
**Release Date:** August 27, 2026  
**Format:** Ultralytics YOLO Darknet Bounding Box Format  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0) / Public Domain  

---

## 1. Dataset Overview & Intended Use

The **FreshGuard Grocery Vision Dataset** is a multi-class 2D object detection dataset designed for real-time household food tracking, inventory management, and grocery freshness monitoring.

### Intended Use Cases
- Training lightweight real-time object detection models (e.g. YOLOv8n, YOLOv9, MobileNet-SSD).
- Automated kitchen shelf, refrigerator interior, and pantry item recognition.
- Academic research in multi-object clutter detection and occlusion handling in indoor domestic settings.

---

## 2. Dataset Structure & Statistics

- **Total Images:** 178 images
- **Total Objects:** 729 bounding box annotations
- **Mean Density:** 4.10 objects per image
- **Input Resolution:** 640x640 RGB

### Directory Layout
```
datasets/grocery_vision/
├── data.yaml
├── README.md
├── CLASS_MAPPING.md
├── classes.txt
├── images/
│   ├── train/ (140 images)
│   ├── val/   (19 images)
│   └── test/  (19 images)
└── labels/
    ├── train/ (140 files)
    ├── val/   (19 files)
    └── test/  (19 files)
```

---

## 3. Supported Grocery Classes (15 Classes)

| Class ID | Class Name | Category | Object Annotations Count |
|---|---|---|---|
| `0` | `milk` | Dairy | 57 |
| `1` | `bread` | Bakery | 47 |
| `2` | `apple` | Produce / Fruits | 41 |
| `3` | `banana` | Produce / Fruits | 58 |
| `4` | `egg` | Dairy / Eggs | 50 |
| `5` | `tomato` | Produce / Vegetables | 43 |
| `6` | `potato` | Produce / Vegetables | 58 |
| `7` | `onion` | Produce / Vegetables | 49 |
| `8` | `rice` | Grains / Staples | 42 |
| `9` | `yogurt` | Dairy | 55 |
| `10` | `cheese` | Dairy | 47 |
| `11` | `biscuit` | Packaged Goods | 38 |
| `12` | `juice` | Beverages | 55 |
| `13` | `water` | Beverages | 47 |
| `14` | `packaged_snack` | Packaged Goods | 42 |

---

## 4. Collection & Annotation Methodology

1. **Annotation Format:** YOLO Darknet format (`.txt` files containing `<class_id> <x_center> <y_center> <width> <height>` normalized in `[0.0, 1.0]`).
2. **Quality Assurance:** Bounding boxes cover tight product boundaries; occluded objects are annotated if >= 30% visible.
3. **Session Isolation:** Images from identical capture sessions are kept in single split directories to prevent data leakage.

---

## 5. Licensing & Citation

Distributed under **CC BY 4.0**. You are free to share and adapt the dataset for educational, research, and commercial purposes with attribution to the FreshGuard AI Project.
