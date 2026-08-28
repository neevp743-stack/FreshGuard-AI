# FreshGuard Vision V3 — Training Dataset Audit Report

## Overview
- **Source Zip**: `datasets/archive.zip` (243.16 MB)
- **Extracted Location**: `training/datasets/archive/`
- **Annotation Format**: **YOLO Object Detection** (normalized `xc, yc, w, h` coordinates)
- **Total Audited Images**: 7952
- **Total Label Files**: 7952
- **Total Usable Images**: 7952
- **Total Valid Bounding Boxes**: 26436
- **Dataset Classes Count**: 26

## Split Distribution

| Split | Images | Label Files | Bounding Box Annotations |
| :--- | :--- | :--- | :--- |
| `train` | 7952 | 7952 | 26436 |
| `valid` | 0 | 0 | 0 |
| `test` | 0 | 0 | 0 |

## Data Quality & Integrity Diagnostics
- **Corrupt / Unreadable Images**: 0
- **Images Missing Label Files**: 0
- **Orphan Label Files**: 0
- **Invalid / Out-of-Bounds Bounding Boxes**: 0

## Image Resolution Profile

| Resolution (WxH) | Count | Percentage |
| :--- | :--- | :--- |
| `608x608` | 7952 | 100.0% |

## Class Breakdown & Annotation Statistics

| Dataset Class ID | Class Name | Images Count | Annotation Boxes |
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
