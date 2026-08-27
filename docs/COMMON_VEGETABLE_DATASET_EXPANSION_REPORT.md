# FreshGuard AI — Common Vegetable Dataset Expansion Report

**Project:** FreshGuard AI  
**Report Title:** Common Vegetable Dataset Expansion Report  
**Date:** August 27, 2026  
**Final Status:** **VALIDATED [35 CLASSES]**  

---

## 1. Executive Summary

The FreshGuard AI Vision dataset has been expanded from 15 grocery classes to **35 multi-modal household grocery and vegetable target classes**.

- **Previous Image Count:** 178 images
- **New Images Added:** 150 images
- **Final Image Count:** **328 images** (+84.3% increase)
- **Previous Object Count:** 729 objects
- **New Objects Added:** 616 objects
- **Final Object Count:** **1,345 objects** (+84.5% increase)
- **Classes Supported:** **35 / 35 Classes** (IDs 0–14 preserved; IDs 15–34 added)

---

## 2. Quantitative Dataset Expansion Matrix

| Metric | Before Vegetable Expansion | After Vegetable Expansion | Change | Status |
|---|---|---|---|---|
| **Total Supported Classes** | 15 classes | **35 classes** | +20 classes | **VERIFIED** |
| **Total Images** | 178 | **328** | +150 images | **VERIFIED** |
| **Total Bounding Box Objects** | 729 | **1,345** | +616 objects | **VERIFIED** |
| **Training Split (`train`)** | 140 images | **260 images (79.3%)** | +120 images | **VERIFIED** |
| **Validation Split (`val`)** | 19 images | **34 images (10.4%)** | +15 images | **VERIFIED** |
| **Test Split (`test`)** | 19 images | **34 images (10.4%)** | +15 images | **VERIFIED** |
| **Invalid Label Files** | 0 | **0** | 0 errors | **VERIFIED** |
| **Corrupt Image Files** | 0 | **0** | 0 corrupt | **VERIFIED** |
| **Cross-Split Data Leakage** | 0 | **0** | 0 leakage | **VERIFIED** |

---

## 3. Supported Vegetable Classes Breakdown (IDs 15–34)

| Class ID | Target Class Name | Category | Object Annotations Count |
|---|---|---|---|
| `15` | `carrot` | Vegetables | 32 |
| `16` | `cabbage` | Vegetables | 30 |
| `17` | `cauliflower` | Vegetables | 34 |
| `18` | `capsicum` | Vegetables | 33 |
| `19` | `cucumber` | Vegetables | 32 |
| `20` | `brinjal` | Vegetables | 30 |
| `21` | `broccoli` | Vegetables | 31 |
| `22` | `spinach` | Vegetables | 28 |
| `23` | `peas` | Vegetables | 26 |
| `24` | `corn` | Vegetables | 29 |
| `25` | `garlic` | Vegetables | 32 |
| `26` | `ginger` | Vegetables | 32 |
| `27` | `okra` | Vegetables | 33 |
| `28` | `beetroot` | Vegetables | 31 |
| `29` | `radish` | Vegetables | 30 |
| `30` | `pumpkin` | Vegetables | 33 |
| `31` | `bitter_gourd` | Vegetables | 30 |
| `32` | `bottle_gourd` | Vegetables | 31 |
| `33` | `green_chilli` | Vegetables | 29 |
| `34` | `sweet_potato` | Vegetables | 30 |

---

## 4. Anti-Leakage & Quality Audit

- Staged acquisition directory `datasets/_vegetable_acquisition/` passed exact SHA-256 duplicate image hash check.
- Multi-frame burst captures from single camera sessions remain strictly isolated within single split directories.
- 0 cross-split image collisions detected between `train`, `val`, and `test`.
