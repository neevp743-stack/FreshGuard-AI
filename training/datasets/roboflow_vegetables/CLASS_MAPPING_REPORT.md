# Roboflow Vegetables Dataset — Class Mapping & Compatibility Report

## Overview
This report details the exact alignment between the 26 classes in `test-on9hk/vegetables-kacga` and the FreshGuard V3 42-class production vocabulary.

## Class Mapping Matrix

| Dataset Class ID | Dataset Class Name | FreshGuard V3 ID | FreshGuard V3 Class Name | Match Type | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `avocado` | `35` | `avocado` | **Match (Direct)** | Map to V3 Class ID 35 ('avocado') |
| `1` | `beans` | `36` | `beans` | **Match (Direct)** | Map to V3 Class ID 36 ('beans') |
| `2` | `beet` | `37` | `beet` | **Match (Direct)** | Map to V3 Class ID 37 ('beet') |
| `3` | `bell pepper` | `18` | `capsicum` | **Partial Match (Alias: 'bell pepper' -> 'capsicum')** | Map to V3 Class ID 18 ('capsicum') |
| `4` | `broccoli` | `21` | `broccoli` | **Match (Direct)** | Map to V3 Class ID 21 ('broccoli') |
| `5` | `brus capusta` | `16` | `cabbage` | **Partial Match (Alias: 'brus capusta' -> 'cabbage')** | Map to V3 Class ID 16 ('cabbage') |
| `6` | `cabbage` | `16` | `cabbage` | **Match (Direct)** | Map to V3 Class ID 16 ('cabbage') |
| `7` | `carrot` | `15` | `carrot` | **Match (Direct)** | Map to V3 Class ID 15 ('carrot') |
| `8` | `cayliflower` | `17` | `cauliflower` | **Partial Match (Alias: 'cayliflower' -> 'cauliflower')** | Map to V3 Class ID 17 ('cauliflower') |
| `9` | `celery` | `38` | `celery` | **Match (Direct)** | Map to V3 Class ID 38 ('celery') |
| `10` | `corn` | `24` | `corn` | **Match (Direct)** | Map to V3 Class ID 24 ('corn') |
| `11` | `cucumber` | `19` | `cucumber` | **Match (Direct)** | Map to V3 Class ID 19 ('cucumber') |
| `12` | `eggplant` | `20` | `brinjal` | **Partial Match (Alias: 'eggplant' -> 'brinjal')** | Map to V3 Class ID 20 ('brinjal') |
| `13` | `fasol` | `39` | `fasol` | **Match (Direct)** | Map to V3 Class ID 39 ('fasol') |
| `14` | `garlic` | `25` | `garlic` | **Match (Direct)** | Map to V3 Class ID 25 ('garlic') |
| `15` | `hot pepper` | `33` | `green_chilli` | **Partial Match (Alias: 'hot pepper' -> 'green_chilli')** | Map to V3 Class ID 33 ('green_chilli') |
| `16` | `onion` | `7` | `onion` | **Match (Direct)** | Map to V3 Class ID 7 ('onion') |
| `17` | `peas` | `23` | `peas` | **Match (Direct)** | Map to V3 Class ID 23 ('peas') |
| `18` | `potato` | `6` | `potato` | **Match (Direct)** | Map to V3 Class ID 6 ('potato') |
| `19` | `pumpkin` | `30` | `pumpkin` | **Match (Direct)** | Map to V3 Class ID 30 ('pumpkin') |
| `20` | `rediska` | `29` | `radish` | **Partial Match (Alias: 'rediska' -> 'radish')** | Map to V3 Class ID 29 ('radish') |
| `21` | `redka` | `29` | `radish` | **Partial Match (Alias: 'redka' -> 'radish')** | Map to V3 Class ID 29 ('radish') |
| `22` | `salad` | `40` | `salad` | **Match (Direct)** | Map to V3 Class ID 40 ('salad') |
| `23` | `squash-patisson` | `41` | `squash-patisson` | **Match (Direct)** | Map to V3 Class ID 41 ('squash-patisson') |
| `24` | `tomato` | `5` | `tomato` | **Match (Direct)** | Map to V3 Class ID 5 ('tomato') |
| `25` | `vegetable marrow` | `41` | `squash-patisson` | **Partial Match (Alias: 'vegetable marrow' -> 'squash-patisson')** | Map to V3 Class ID 41 ('squash-patisson') |

## Overlapping Produce Verification

| Overlapping Produce | Extracted Bounding Boxes | FreshGuard V3 ID | Semantic Verification Findings |
| :--- | :--- | :--- | :--- |
| `potato` | `989` boxes | `6` (`potato`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `tomato` | `2298` boxes | `5` (`tomato`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `onion` | `1253` boxes | `7` (`onion`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `garlic` | `1586` boxes | `25` (`garlic`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `peas` | `1025` boxes | `23` (`peas`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `eggplant` | `900` boxes | `20` (`brinjal`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `rediska` | `1179` boxes | `29` (`radish`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `carrot` | `1375` boxes | `15` (`carrot`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `hot pepper` | `1322` boxes | `33` (`green_chilli`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `bell pepper` | `1303` boxes | `18` (`capsicum`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `cucumber` | `1199` boxes | `19` (`cucumber`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `cayliflower` | `758` boxes | `17` (`cauliflower`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
| `cabbage` | `663` boxes | `16` (`cabbage`) | **VERIFIED**: Valid object bounding boxes matching raw grocery items. |
