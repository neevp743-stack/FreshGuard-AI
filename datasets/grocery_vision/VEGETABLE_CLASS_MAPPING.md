# FreshGuard AI — Vegetable Class Mapping Specification

**Dataset:** FreshGuard Grocery Vision Dataset v2 (Vegetable Expansion)  
**Target Architecture:** Ultralytics YOLOv8 (`nc: 35`)  
**Date:** August 27, 2026  

---

## 1. Class ID Specification & Mapping Matrix

### Original 15 Grocery Classes (IDs 0–14: Unchanged)
| Class ID | Target Class Name | Category | Mapping Synonyms |
|---|---|---|---|
| `0` | `milk` | Dairy | `milk`, `milk bottle`, `milk carton` |
| `1` | `bread` | Bakery | `bread`, `loaf`, `sliced bread` |
| `2` | `apple` | Produce / Fruits | `apple`, `red apple` |
| `3` | `banana` | Produce / Fruits | `banana`, `banana bunch` |
| `4` | `egg` | Dairy / Eggs | `egg`, `egg carton` |
| `5` | `tomato` | Produce / Vegetables | `tomato`, `tomatoes` |
| `6` | `potato` | Produce / Vegetables | `potato`, `potatoes` |
| `7` | `onion` | Produce / Vegetables | `onion`, `onions` |
| `8` | `rice` | Grains / Staples | `rice`, `rice bag` |
| `9` | `yogurt` | Dairy | `yogurt`, `dahi` |
| `10` | `cheese` | Dairy | `cheese`, `butter` |
| `11` | `biscuit` | Packaged Goods | `biscuit`, `cookie` |
| `12` | `juice` | Beverages | `juice`, `fruit juice` |
| `13` | `water` | Beverages | `water`, `water bottle` |
| `14` | `packaged_snack` | Packaged Goods | `packaged_snack`, `chips` |

### New Vegetable Target Classes (IDs 15–34)
| Class ID | Target Class Name | Category | Source Synonym Mappings | Semantic Inclusions |
|---|---|---|---|---|
| `15` | `carrot` | Vegetables | `carrot`, `carrots` | Fresh orange carrots (whole or sliced) |
| `16` | `cabbage` | Vegetables | `cabbage`, `green cabbage`, `red cabbage` | Whole or halved cabbage heads |
| `17` | `cauliflower` | Vegetables | `cauliflower`, `gobhi` | Cauliflower heads and florets |
| `18` | `capsicum` | Vegetables | `capsicum`, `bell pepper`, `sweet pepper` | Green, red, yellow capsicums / bell peppers |
| `19` | `cucumber` | Vegetables | `cucumber`, `cucumbers` | Fresh green salad cucumbers |
| `20` | `brinjal` | Vegetables | `brinjal`, `eggplant`, `aubergine`, `baingan` | Purple/green eggplants / brinjals |
| `21` | `broccoli` | Vegetables | `broccoli`, `broccoli floret` | Fresh green broccoli heads |
| `22` | `spinach` | Vegetables | `spinach`, `palak`, `spinach bunch` | Fresh leafy spinach bunches |
| `23` | `peas` | Vegetables | `peas`, `green peas`, `matar` | Fresh green peas or pea pods |
| `24` | `corn` | Vegetables | `corn`, `sweetcorn`, `corn cob` | Fresh corn cobs, maize |
| `25` | `garlic` | Vegetables | `garlic`, `garlic bulb` | Whole garlic bulbs and cloves |
| `26` | `ginger` | Vegetables | `ginger`, `ginger root`, `adrak` | Fresh ginger root rhizomes |
| `27` | `okra` | Vegetables | `okra`, `ladyfinger`, `bhindi` | Fresh green okra pods |
| `28` | `beetroot` | Vegetables | `beetroot`, `beet`, `beets` | Fresh red beetroots |
| `29` | `radish` | Vegetables | `radish`, `mooli`, `white radish` | Fresh white or red radishes |
| `30` | `pumpkin` | Vegetables | `pumpkin`, `squash`, `kaddu` | Whole or sliced pumpkins |
| `31` | `bitter_gourd` | Vegetables | `bitter_gourd`, `bitter melon`, `karela` | Fresh bitter gourds |
| `32` | `bottle_gourd` | Vegetables | `bottle_gourd`, `bottle melon`, `lauki` | Fresh green bottle gourds |
| `33` | `green_chilli` | Vegetables | `green_chilli`, `green chili`, `chili pepper` | Fresh raw green chillies |
| `34` | `sweet_potato` | Vegetables | `sweet_potato`, `shakarkandi` | Whole raw sweet potatoes |

---

## 2. Mapping Safety Rules

1. **Unambiguous Mapping:** `bell pepper` maps to `capsicum`, `eggplant` maps to `brinjal`, `ladyfinger` maps to `okra`.
2. **Preservation of IDs 0–14:** `tomato`, `potato`, and `onion` remain strictly mapped to IDs 5, 6, and 7 respectively.
