# FreshGuard AI — Invalid Annotation Audit Report

## 1. Executive Summary
This report details the granular breakdown of invalid or unsafe annotations discovered in the raw 4.2 GB dataset.

All invalid annotations have been **EXCLUDED** from the clean dataset (`datasets/freshguard_35_clean`) to ensure zero label corruption during training.

---

## 2. Invalid Annotation Categories & Counts

| Category | Description | Count | Action Taken |
| :--- | :--- | :--- | :--- |
| **Malformed Row** | Wrong number of columns or non-numeric tokens | `13369` | Excluded |
| **Invalid Class ID** | Class ID out of dataset range | `0` | Excluded |
| **Coordinate Out of Range** | Bounding box center coordinates $<0.0$ or $>1.0$ | `0` | Excluded |
| **Zero or Negative Size** | Bounding box width or height $\le 0.0$ | `3` | Excluded |
| **Duplicate BBox** | Identical bounding box coordinates in same file | `0` | Deduplicated |

**Total Invalid Bounding Box Instances**: `13372`
