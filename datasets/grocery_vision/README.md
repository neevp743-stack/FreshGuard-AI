# FreshGuard Grocery Vision Dataset Guidelines & Annotation Workflow

## 1. Image Sources & Licensing
To ensure compliance and privacy:
- **User-captured images**: Photos taken by authorized project contributors.
- **Open Datasets**: Properly licensed open-source datasets (e.g. Open Images V7, COCO, Roboflow Universe public datasets under CC-BY 4.0 or public domain).
- **Documentation Table**:
  | Dataset Source | License | Images Count | Classes Covered |
  | :--- | :--- | :--- | :--- |
  | Household Captures | Proprietary / User Consent | Pending Capture | All 15 Classes |
  | Open Images V7 (Sub-sampled) | CC-BY 4.0 | Pending Selection | Apple, Banana, Bread, Milk |

---

## 2. Dataset Quality & Realistic Variation Rules
Images must depict realistic household scenarios:
- **Environment**: Refrigerator interiors, pantry shelves, kitchen countertops.
- **Lighting**: Bright daylight, indoor warm overhead lighting, dim fridge interior light.
- **Angles & Distances**: Close-ups, medium pantry shots, top-down fridge tray views.
- **State**: Opened packaging, sealed containers, partially consumed products.

---

## 3. Bounding Box Annotation Workflow & Examples

Each image must be annotated using YOLO Darknet format: `<class_id> <x_center> <y_center> <width> <height>` (normalized 0.0 to 1.0).

Recommended local annotation tools:
- **LabelImg** (Local desktop tool: `pip install labelImg`)
- **CVAT.ai** or **Roboflow Annotate**

### Annotation Examples & Rules

#### Scenario A: Single Object
- Draw a tight bounding box around the product outer boundary.
- **Example (`fridge_001.txt`)**:
  ```text
  0 0.512 0.485 0.320 0.610   # milk
  ```

#### Scenario B: Multiple Objects
- Draw separate bounding boxes for *every* distinct object visible in the frame.
- **Example (`pantry_014.txt`)**:
  ```text
  1 0.250 0.300 0.200 0.350   # bread
  2 0.650 0.400 0.150 0.180   # apple
  3 0.800 0.450 0.180 0.220   # banana
  ```

#### Scenario C: Partially Visible / Occluded Objects
- Annotate any object that has at least 30% of its visual signature visible.
- Extend the bounding box boundary only over the visible portion of the product.
- **Example (`shelf_08.txt`)**:
  ```text
  9 0.120 0.550 0.150 0.250   # yogurt (partially hidden behind milk)
  0 0.400 0.500 0.300 0.700   # milk
  ```

#### Scenario D: Overlapping Objects
- Draw individual overlapping boxes for each product. Do **NOT** group multiple products into a single huge bounding box.
- **Example (`basket_03.txt`)**:
  ```text
  2 0.450 0.500 0.220 0.240   # apple #1
  2 0.520 0.510 0.210 0.230   # apple #2 (overlapping)
  ```

---

## 4. Anti-Leakage Split Protocol
- **Split Ratio**: 70% Train, 20% Validation, 10% Test.
- **Data Leakage Rule**: Images taken during the same burst capture session or of the same physical countertop arrangement must be placed **exclusively in one split directory** (e.g. all in `train` or all in `val`). Never split burst shots of the same item across train and test!
