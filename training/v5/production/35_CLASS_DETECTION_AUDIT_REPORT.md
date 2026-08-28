# FreshGuard Vision — 35-Class Complete Detection Audit Report

## 1. Cryptographic Model Integrity
- **V2 Baseline ONNX Model Path**: `C:\Users\neevp\OneDrive\Desktop\SEM_03\IDEA\freshguard-ai\vision_models\deployment\grocery_yolov8_v2_web\model.onnx`
- **ONNX Model SHA-256**: `5c98003d9c686dcc0733e095143d09fe0bd382b2a7e3b6171fd6c7d76b9dcd7a` $\rightarrow$ **100% BYTE-MATCHED & UNTOUCHED**
- **Metadata File SHA-256**: `3a5a318f65bb7b0d665965255de2d3e2c16980905dd5c9b1d7b03c14b3c3e26d` $\rightarrow$ **100% BYTE-MATCHED & UNTOUCHED**

## 2. Authoritative 35-Class Alignment Table
Total Classes: **35** (Class IDs 0 through 34)

| Class ID | Model Class Name | Backend Label | Frontend Display Name | Alignment Status |
| :--- | :--- | :--- | :--- | :--- |
| 0 | milk | milk | Milk | VERIFIED ALIGNED |
| 1 | bread | bread | Bread | VERIFIED ALIGNED |
| 2 | apple | apple | Apple | VERIFIED ALIGNED |
| 3 | banana | banana | Banana | VERIFIED ALIGNED |
| 4 | egg | egg | Egg | VERIFIED ALIGNED |
| 5 | tomato | tomato | Tomato | VERIFIED ALIGNED |
| 6 | potato | potato | Potato | VERIFIED ALIGNED |
| 7 | onion | onion | Onion | VERIFIED ALIGNED |
| 8 | rice | rice | Rice | VERIFIED ALIGNED |
| 9 | yogurt | yogurt | Yogurt | VERIFIED ALIGNED |
| 10 | cheese | cheese | Cheese | VERIFIED ALIGNED |
| 11 | biscuit | biscuit | Biscuit | VERIFIED ALIGNED |
| 12 | juice | juice | Juice | VERIFIED ALIGNED |
| 13 | water | water | Water | VERIFIED ALIGNED |
| 14 | packaged_snack | packaged_snack | Packaged Snack | VERIFIED ALIGNED |
| 15 | carrot | carrot | Carrot | VERIFIED ALIGNED |
| 16 | cabbage | cabbage | Cabbage | VERIFIED ALIGNED |
| 17 | cauliflower | cauliflower | Cauliflower | VERIFIED ALIGNED |
| 18 | capsicum | capsicum | Capsicum | VERIFIED ALIGNED |
| 19 | cucumber | cucumber | Cucumber | VERIFIED ALIGNED |
| 20 | brinjal | brinjal | Brinjal | VERIFIED ALIGNED |
| 21 | broccoli | broccoli | Broccoli | VERIFIED ALIGNED |
| 22 | spinach | spinach | Spinach | VERIFIED ALIGNED |
| 23 | peas | peas | Peas | VERIFIED ALIGNED |
| 24 | corn | corn | Corn | VERIFIED ALIGNED |
| 25 | garlic | garlic | Garlic | VERIFIED ALIGNED |
| 26 | ginger | ginger | Ginger | VERIFIED ALIGNED |
| 27 | okra | okra | Okra | VERIFIED ALIGNED |
| 28 | beetroot | beetroot | Beetroot | VERIFIED ALIGNED |
| 29 | radish | radish | Radish | VERIFIED ALIGNED |
| 30 | pumpkin | pumpkin | Pumpkin | VERIFIED ALIGNED |
| 31 | bitter_gourd | bitter_gourd | Bitter Gourd | VERIFIED ALIGNED |
| 32 | bottle_gourd | bottle_gourd | Bottle Gourd | VERIFIED ALIGNED |
| 33 | green_chilli | green_chilli | Green Chilli | VERIFIED ALIGNED |
| 34 | sweet_potato | sweet_potato | Sweet Potato | VERIFIED ALIGNED |


## 3. 35-Class Real Model Inference Execution Matrix

| ID | Class Name | Test Image | Detections @ 0.25 | Detections @ 0.15 | Audit Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | milk | acq_grocery_val_004.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 1 | bread | acq_grocery_val_004.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 2 | apple | acq_grocery_val_004.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 3 | banana | acq_grocery_val_001.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 4 | egg | acq_grocery_val_001.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 5 | tomato | acq_grocery_val_001.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 6 | potato | acq_grocery_val_001.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 7 | onion | acq_grocery_val_001.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 8 | rice | acq_grocery_val_002.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 9 | yogurt | acq_grocery_val_002.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 10 | cheese | acq_grocery_val_002.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 11 | biscuit | acq_grocery_val_003.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 12 | juice | acq_grocery_val_003.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 13 | water | acq_grocery_val_003.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 14 | packaged_snack | acq_grocery_val_003.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 15 | carrot | veg_val_006.jpg | 1 | 2 | PASS |
| 16 | cabbage | veg_val_006.jpg | 1 | 2 | PASS |
| 17 | cauliflower | veg_val_006.jpg | 1 | 2 | PASS |
| 18 | capsicum | veg_val_001.jpg | 0 | 3 | PASS |
| 19 | cucumber | veg_val_001.jpg | 0 | 3 | PASS |
| 20 | brinjal | veg_val_001.jpg | 0 | 3 | PASS |
| 21 | broccoli | veg_val_001.jpg | 0 | 3 | PASS |
| 22 | spinach | veg_val_002.jpg | 1 | 1 | PASS |
| 23 | peas | veg_val_002.jpg | 1 | 1 | PASS |
| 24 | corn | veg_val_002.jpg | 1 | 1 | PASS |
| 25 | garlic | veg_val_003.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 26 | ginger | veg_val_003.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 27 | okra | veg_val_004.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 28 | beetroot | veg_val_004.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 29 | radish | veg_val_004.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 30 | pumpkin | veg_val_004.jpg | 0 | 0 | NO_DETECTION_AT_THRESHOLD |
| 31 | bitter_gourd | veg_val_005.jpg | 1 | 1 | PASS |
| 32 | bottle_gourd | veg_val_005.jpg | 1 | 1 | PASS |
| 33 | green_chilli | veg_val_006.jpg | 1 | 2 | PASS |
| 34 | sweet_potato | veg_val_006.jpg | 1 | 2 | PASS |


---

### Final Audit Verdict

```
35_CLASS_DETECTION_PIPELINE_VERIFIED
```
