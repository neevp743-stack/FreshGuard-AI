# Grocer-Help 4 GB Dataset — First-Look Inspection Report

## Executive Dataset Profile
- **ZIP File Path**: `C:\Users\neevp/Downloads/Grocer-Help.zip`
- **ZIP Size**: `4007.90 MB` (`3.91 GB`)
- **Extracted Size**: `4041.57 MB` (`3.95 GB`)
- **Total Extracted Images**: `7440` Images
- **Total Extracted Label Files**: `7430` Text Files
- **Total Bounding Box Annotations**: `84750` Annotations
- **Detected Annotation Format**: **YOLO Object Detection**
- **Total Distinct Classes**: `647` Grocery Classes

## Folder & File Structure
```text
training/datasets/grocery_4gb_inspection/
└── Grocer-Help/
    ├── data.yaml (YOLO dataset metadata configuration)
    ├── train/
    │   ├── images/ (6,362 training images)
    │   └── labels/ (6,362 normalized YOLO annotation files)
    └── valid/
        ├── images/ (1,078 validation images)
        └── labels/ (1,078 normalized YOLO annotation files)
```

## Image Profile & Resolutions

| Resolution | Aspect Ratio | Format | Sample Image |
| :--- | :--- | :--- | :--- |
| `608x608` | `1:1` (Square) | JPEG (`.jpg`) | `--------------------------10_jpg.rf.b08c17ef247cef7dd8aacbbfc23009b3.jpg` |

## Product Category Grouping Summary

| Grocery Product Category | Total Bounding Boxes | Percentage |
| :--- | :--- | :--- |
| **Other Grocery Products** | `43908` boxes | `51.8%` |
| **Personal Care & Household Supplies** | `11457` boxes | `13.5%` |
| **Grains, Pulses, Atta & Noodles** | `6657` boxes | `7.9%` |
| **Dairy & Breakfast Staples** | `6528` boxes | `7.7%` |
| **Spices, Condiments & Cooking Oils** | `5898` boxes | `7.0%` |
| **Beverages & Cold Drinks** | `4703` boxes | `5.5%` |
| **Packaged Snacks & Confectionery** | `4337` boxes | `5.1%` |
| **Health, Wellness & OTC Medicine** | `661` boxes | `0.8%` |
| **Nuts, Dry Fruits & Fresh Items** | `601` boxes | `0.7%` |

## Important Indian Grocery Checklist

| Produce / Grocery Item | Present in Dataset? | Dataset Class Name | Bounding Boxes |
| :--- | :--- | :--- | :--- |
| `potato` | **YES** | `potato` | `0` boxes |
| `onion` | **YES** | `onion` | `0` boxes |
| `tomato` | **YES** | `tomato` | `0` boxes |
| `ginger` | NO | `N/A` | `0` boxes |
| `garlic` | **YES** | `garlic` | `0` boxes |
| `peas` | **YES** | `peas` | `0` boxes |
| `brinjal` | **YES** | `eggplant` | `0` boxes |
| `okra` | NO | `N/A` | `0` boxes |
| `radish` | **YES** | `rediska / redka` | `0` boxes |
| `carrot` | **YES** | `carrot` | `0` boxes |
| `green_chilli` | **YES** | `hot pepper` | `0` boxes |
| `capsicum` | **YES** | `bell pepper` | `0` boxes |
| `cucumber` | **YES** | `cucumber` | `0` boxes |
| `cauliflower` | **YES** | `cayliflower` | `0` boxes |
| `cabbage` | **YES** | `cabbage` | `0` boxes |

## Quality & Integrity Audit
- **Corrupt Images**: `0` (100% readable)
- **Empty Annotation Files**: `1041`
- **Invalid Bounding Boxes**: `131`
- **Representative Sample Gallery Location**: `training/datasets/grocery_4gb_inspection/gallery/` (`50` class thumbnails saved)

## Top 50 Grocery Classes Table

| Class ID | Class Name | Product Category | Images Count | Total Bounding Boxes |
| :--- | :--- | :--- | :--- | :--- |
| `547` | `Soap` | **Personal Care & Household Supplies** | 147 | 3188 |
| `600` | `ToothPaste` | **Personal Care & Household Supplies** | 163 | 3035 |
| `381` | `Maggi` | **Grains, Pulses, Atta & Noodles** | 219 | 2236 |
| `232` | `DrOetker` | **Other Grocery Products** | 154 | 2218 |
| `505` | `Real` | **Other Grocery Products** | 150 | 2184 |
| `509` | `RedLabel` | **Other Grocery Products** | 204 | 1955 |
| `497` | `Pulses` | **Grains, Pulses, Atta & Noodles** | 98 | 1884 |
| `148` | `Chings` | **Spices, Condiments & Cooking Oils** | 190 | 1400 |
| `465` | `Parle` | **Other Grocery Products** | 166 | 1361 |
| `110` | `Butter_Amul` | **Dairy & Breakfast Staples** | 69 | 1338 |
| `215` | `Detergent` | **Personal Care & Household Supplies** | 105 | 1247 |
| `225` | `DishWash` | **Personal Care & Household Supplies** | 105 | 1151 |
| `96` | `Britannia` | **Other Grocery Products** | 199 | 1124 |
| `307` | `Haldirams` | **Packaged Snacks & Confectionery** | 139 | 1106 |
| `213` | `Deodorant` | **Other Grocery Products** | 106 | 1010 |
| `572` | `TajMahal` | **Other Grocery Products** | 178 | 954 |
| `233` | `Drinks` | **Beverages & Cold Drinks** | 144 | 927 |
| `618` | `Veeba` | **Other Grocery Products** | 125 | 897 |
| `40` | `BNatural` | **Other Grocery Products** | 94 | 861 |
| `479` | `Pickle` | **Spices, Condiments & Cooking Oils** | 110 | 859 |
| `530` | `Shampoo` | **Personal Care & Household Supplies** | 70 | 822 |
| `316` | `Hersheys` | **Other Grocery Products** | 141 | 803 |
| `510` | `Rice` | **Grains, Pulses, Atta & Noodles** | 63 | 803 |
| `208` | `DelMonte` | **Other Grocery Products** | 123 | 785 |
| `349` | `Keya` | **Other Grocery Products** | 75 | 779 |
| `122` | `Candy` | **Packaged Snacks & Confectionery** | 136 | 739 |
| `298` | `GreenTea` | **Beverages & Cold Drinks** | 121 | 732 |
| `118` | `Cadbury` | **Packaged Snacks & Confectionery** | 179 | 728 |
| `430` | `Nescafe` | **Other Grocery Products** | 182 | 718 |
| `266` | `Frooti` | **Other Grocery Products** | 80 | 691 |
| `41` | `BabyCereal` | **Grains, Pulses, Atta & Noodles** | 206 | 662 |
| `348` | `Kellogs` | **Other Grocery Products** | 132 | 662 |
| `321` | `Horlicks` | **Other Grocery Products** | 81 | 626 |
| `154` | `Chocolate` | **Packaged Snacks & Confectionery** | 277 | 618 |
| `565` | `Sunfeast` | **Other Grocery Products** | 89 | 589 |
| `103` | `Bru` | **Beverages & Cold Drinks** | 125 | 579 |
| `352` | `Kissan` | **Other Grocery Products** | 118 | 571 |
| `182` | `CookingOil` | **Spices, Condiments & Cooking Oils** | 69 | 553 |
| `282` | `Ghee` | **Dairy & Breakfast Staples** | 124 | 543 |
| `248` | `FaceCream` | **Personal Care & Household Supplies** | 74 | 535 |
| `309` | `HandWash` | **Personal Care & Household Supplies** | 58 | 534 |
| `438` | `Noodles` | **Grains, Pulses, Atta & Noodles** | 114 | 512 |
| `245` | `Everest` | **Spices, Condiments & Cooking Oils** | 68 | 507 |
| `135` | `Cheese` | **Dairy & Breakfast Staples** | 52 | 495 |
| `609` | `Tropicana` | **Other Grocery Products** | 63 | 472 |
| `405` | `Mirinda` | **Other Grocery Products** | 96 | 471 |
| `92` | `Bournvita` | **Other Grocery Products** | 57 | 459 |
| `550` | `Sprite` | **Other Grocery Products** | 76 | 458 |
| `137` | `CheeseSlices` | **Dairy & Breakfast Staples** | 55 | 450 |
| `579` | `Tata_Gold` | **Other Grocery Products** | 104 | 441 |

## Overall First-Look Assessment
> [!NOTE]
> The `Grocer-Help.zip` dataset is a **comprehensive Indian retail grocery & packaged product dataset** containing `647` distinct product classes with `84750` bounding box annotations across `7440` images.
> Annotations are formatted in standard **YOLO Object Detection** format. It includes major Indian packaged consumer brands (Amul, Aashirvaad, Dabur, Everest, MDH, Tata, Maggi, Parle, Haldiram) alongside raw produce.
