# FreshGuard Vision V5 — Model Training & ONNX Export Report

## Executive Summary
> [!IMPORTANT]
> **V5 Candidate Model Status**: **TRAINING & ONNX EXPORT COMPLETE**
> FreshGuard Vision V5 has been successfully trained and exported as an ONNX candidate in `training/v5/deployment/model.onnx`.

## Model Architecture & Vocabulary

| Attribute | V2 Production Baseline | V5 Candidate Model |
| :--- | :--- | :--- |
| **Class Vocabulary** | 35 Classes | **644 Grocery Classes** |
| **Input Shape** | `[1, 3, 640, 640]` | `[1, 3, 320, 320]` (Optimized low-latency) |
| **Output Tensor Shape** | `[1, 39, 8400]` | `[1, 648, 2100]` |
| **ONNX Model Size** | 11.7 MB | `13.49 MB` |
| **ONNX SHA-256 Hash** | `5c98003d9c68...` | `ad6550f32f07b6ee3ecf69478180ecadb30690f5746e9876b4b23fa181af189e` |

## Production Isolation Audit
- **V2 Production Model**: `grocery_yolov8_v2_web/model.onnx` (`5c98003d9c686dcc0733e095143d09fe0bd382b2a7e3b6171fd6c7d76b9dcd7a`) $\rightarrow$ **UNTOUCHED**
- **V2 Production Metadata**: `vision_models/model_metadata.json` (`85088cf442c6067f51613b2ad51b8ebbd8f53d3e08705d5cbfbcad3b21709ae0`) $\rightarrow$ **UNTOUCHED**
- **Render Backend Deployment**: **UNTOUCHED**
- **Vercel Frontend Deployment**: **UNTOUCHED**

## Candidate Deployment Location
- **ONNX Model**: `training/v5/deployment/model.onnx`
- **Metadata Config**: `training/v5/deployment/v5_classes_metadata.json`
