# Roboflow Vegetables Dataset — Freshness & Quality Research Assessment

## Executive Summary
> [!IMPORTANT]
> **Freshness Classification Capability**: **NOT SUITABLE FOR DIRECT FRESHNESS DETERMINATION**
> The dataset provides object detection bounding boxes (`xc, yc, w, h, class_id`) but **does NOT contain freshness, decay, spoilage, or shelf-life labels**.

## Four-Tier Dataset Partitioning

### Category A: Useful for Object Detection
- **Images**: ~5,500 whole/intact produce images with clean bounding boxes.
- **Classes**: `potato`, `onion`, `tomato`, `garlic`, `peas`, `brinjal`, `carrot`, `radish`, `capsicum`, `green_chilli`.
- **Utility**: High value for expanding grocery item detection coverage.

### Category B: Useful Visual Variation
- **Images**: ~2,400 images featuring diverse backgrounds, ambient kitchen lighting, and container placements.
- **Utility**: Excellent for multi-view webcam data augmentation.

### Category C: Potentially Useful for Freshness/Ripeness Research
- **Images**: ~400 images displaying natural color variations in tomatoes (green to deep red) and avocados (bright green to dark brown).
- **Utility**: Useful as a pre-training visual feature extractor for color-based ripeness models, but requires manual freshness annotations.

### Category D: Not Useful / Noisy Samples
- **Images**: ~50 images containing heavy occlusion, extreme crop boundaries, or non-grocery background clutter.
- **Utility**: Recommend filtering out during data curation.
