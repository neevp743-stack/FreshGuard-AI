# FreshGuard Vision V4 — Dataset Cleaning & Deduplication Report

## Overview
This report documents the deduplication, filtering, and alias normalization workflow performed on the Roboflow Vegetables dataset (`test-on9hk/vegetables-kacga`).

## Deduplication Metrics

| Stage | Image Count | Description |
| :--- | :--- | :--- |
| **Raw Roboflow Export** | `7952` | Total images including synthetic augmentations |
| **Augmented Variants Removed** | `6677` | Rotation/shear/crop variants filtered out |
| **Unique Base Scenes Retained** | `1275` | Primary distinct photographic capture scenes |
| **Usable Clean Images** | `1275` | Images with verified non-empty bounding box labels |
| **Usable Bounding Boxes** | `4046` | Normalized YOLO bounding box annotations |

## Class Alias Normalization Audit

| Raw Roboflow Class | Normalized FreshGuard Class | Resolution Status |
| :--- | :--- | :--- |
| `eggplant` | `brinjal` | **NORMALIZED** (Map to standard Indian produce name) |
| `rediska` / `redka` | `radish` | **NORMALIZED** (Slavic produce terms merged into `radish`) |
| `hot pepper` | `green_chilli` | **NORMALIZED** (Map to standard Indian chilli term) |
| `bell pepper` | `capsicum` | **NORMALIZED** (Map to standard Indian produce term) |
| `cayliflower` | `cauliflower` | **NORMALIZED** (Spelling typo resolved) |
| `brus capusta` | `cabbage` | **NORMALIZED** (Spelling typo resolved) |
| `vegetable marrow` | `squash-patisson` | **NORMALIZED** (Mapped to Patisson squash category) |
