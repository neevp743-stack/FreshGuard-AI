# FreshGuard AI — Vision Class Mapping Specification

**Dataset:** FreshGuard Grocery Vision Dataset v1  
**Target Architecture:** Ultralytics YOLOv8 (`nc: 15`)  
**Date:** August 27, 2026  

---

## 1. Class Mapping Matrix

| Target Class ID | FreshGuard Target Class | Category | Accepted Source Class Names / Synonyms | Semantic Boundaries & Inclusions | Exclusions |
|---|---|---|---|---|---|
| `0` | `milk` | Dairy | `milk`, `milk bottle`, `milk carton`, `milk pouch`, `dairy milk` | Fluid cow/plant milk in cartons, bottles, or pouches | Milk powder, condensed milk cans |
| `1` | `bread` | Bakery | `bread`, `loaf`, `sliced bread`, `sandwich bread`, `bun`, `toast` | Baked loaves, sliced bread packages, burger buns | Pastries, cakes, biscuits |
| `2` | `apple` | Produce / Fruits | `apple`, `red apple`, `green apple` | Whole fresh apples | Apple pie, apple juice bottles |
| `3` | `banana` | Produce / Fruits | `banana`, `bananas`, `banana bunch` | Whole fresh bananas (single or bunch) | Banana chips, plantain snacks |
| `4` | `egg` | Dairy / Eggs | `egg`, `eggs`, `egg carton`, `egg tray` | Fresh poultry eggs (single or in cartons) | Fried/cooked egg dishes |
| `5` | `tomato` | Produce / Vegetables | `tomato`, `tomatoes`, `cherry tomato` | Fresh raw tomatoes | Tomato ketchup, canned paste |
| `6` | `potato` | Produce / Vegetables | `potato`, `potatoes`, `raw potato` | Fresh raw potatoes | Potato chips, french fries |
| `7` | `onion` | Produce / Vegetables | `onion`, `onions`, `red onion`, `yellow onion` | Fresh raw onions | Fried onion rings |
| `8` | `rice` | Grains / Staples | `rice`, `rice bag`, `rice packet`, `basmati` | Uncooked rice bags, pouches, or grain packets | Cooked rice meals |
| `9` | `yogurt` | Dairy | `yogurt`, `yoghurt`, `dahi`, `curd` | Yogurt cups, tubs, Greek yogurt containers | Frozen yogurt ice cream |
| `10` | `cheese` | Dairy | `cheese`, `cheese block`, `cheese slice`, `butter` | Dairy cheese blocks, slices, butter tubs | Mac and cheese boxes |
| `11` | `biscuit` | Packaged Goods | `biscuit`, `biscuits`, `cookie`, `cookies`, `cracker` | Packaged biscuits, cookies, crackers | Sliced bread, cakes |
| `12` | `juice` | Beverages | `juice`, `fruit juice`, `orange juice`, `juice box` | Packaged fruit juices, juice cartons, juice bottles | Soda, plain water |
| `13` | `water` | Beverages | `water`, `water bottle`, `mineral water` | Bottled drinking water | Flavored sodas, juice boxes |
| `14` | `packaged_snack` | Packaged Goods | `packaged_snack`, `chips`, `snack bag`, `crisps` | Sealed snack pouches, potato chips, corn chips | Fresh unpackaged fruit |

---

## 2. Mapping Safety Protocol

1. **Semantic Rigor:** Only map source labels to target classes when the visual and physical properties match (e.g. `water bottle` -> `water`, `cookie` -> `biscuit`).
2. **Ambiguity Prevention:** Unmapped or out-of-scope classes (e.g., `soda can`, `cooking oil`, `dish soap`) are filtered out during acquisition.
3. **Index Ordering:** Target class IDs are strictly enforced in integer range `[0, 14]` corresponding to `data.yaml`.
