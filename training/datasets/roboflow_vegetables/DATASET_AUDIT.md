# Roboflow Vegetables Dataset (test-on9hk) — Dataset Audit Report

## Dataset Profile
- **Dataset Source**: Roboflow Universe (`https://universe.roboflow.com/test-on9hk/vegetables-kacga/dataset/5`)
- **Publication Date**: 2022-07-15
- **License**: CC BY 4.0
- **Total Audited Images**: `7952` (Unique Base Scenes: `1275`, Augmented Variants: `6677`)
- **Total Label Files**: `7952`
- **Total Bounding Box Annotations**: `26436`
- **Annotation Format**: **YOLO Object Detection** (normalized `xc, yc, w, h` coordinates)
- **Dataset Class Count**: `26` Classes

## Data Quality & Integrity Diagnostics
- **Corrupt / Unreadable Images**: `0`
- **Images Missing Annotations**: `0`
- **Orphan Label Files**: `0`
- **Invalid Bounding Boxes**: `0`

## Produce Visual State Distribution

| Visual Presentation State | Estimated Count | Percentage | Utility for FreshGuard |
| :--- | :--- | :--- | :--- |
| **Whole / Intact Vegetables** | `7952` | `100.0%` | **HIGH** (Primary grocery checkout & pantry use-case) |
| **Sliced / Cut Vegetables** | `0` | `0.0%` | **MEDIUM** (Useful for meal-prep scanning) |
| **Chopped / Diced Vegetables** | `0` | `0.0%` | **LOW** (Ambiguous boundary recognition) |
| **Cooked / Prepared Dishes** | `0` | `0.0%` | **NONE** (Outside grocery item vocabulary) |

## Image Resolution Profile

| Resolution (WxH) | Image Count | Percentage |
| :--- | :--- | :--- |
| `608x608` | 7952 | 100.0% |

## Class Breakdown & Annotation Statistics

| Class ID | Class Name | Images Count | Annotation Boxes |
| :--- | :--- | :--- | :--- |
| `0` | `avocado` | 359 | 1265 |
| `1` | `beans` | 248 | 520 |
| `2` | `beet` | 326 | 1041 |
| `3` | `bell pepper` | 357 | 1303 |
| `4` | `broccoli` | 325 | 671 |
| `5` | `brus capusta` | 254 | 626 |
| `6` | `cabbage` | 297 | 663 |
| `7` | `carrot` | 411 | 1375 |
| `8` | `cayliflower` | 311 | 758 |
| `9` | `celery` | 196 | 440 |
| `10` | `corn` | 352 | 1255 |
| `11` | `cucumber` | 386 | 1199 |
| `12` | `eggplant` | 334 | 900 |
| `13` | `fasol` | 322 | 479 |
| `14` | `garlic` | 452 | 1586 |
| `15` | `hot pepper` | 303 | 1322 |
| `16` | `onion` | 411 | 1253 |
| `17` | `peas` | 306 | 1025 |
| `18` | `potato` | 369 | 989 |
| `19` | `pumpkin` | 354 | 1209 |
| `20` | `rediska` | 306 | 1179 |
| `21` | `redka` | 220 | 757 |
| `22` | `salad` | 251 | 401 |
| `23` | `squash-patisson` | 295 | 1079 |
| `24` | `tomato` | 486 | 2298 |
| `25` | `vegetable marrow` | 302 | 843 |
