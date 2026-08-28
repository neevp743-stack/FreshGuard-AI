# FreshGuard Vision V5 — Comprehensive Validation Report

## Executive Summary
> [!IMPORTANT]
> **V5 Candidate Model Validation**: **PASSED**
> Model integrity, ONNX Runtime session, 644-class metadata mapping, CPU latency, and produce recognition have been validated.

## Model & Benchmark Summary
- **V5 ONNX Candidate File**: `training/v5/deployment/model.onnx` (`ad6550f32f07b6ee3ecf69478180ecadb30690f5746e9876b4b23fa181af189e`)
- **Class Vocabulary**: `644` Grocery Classes
- **Input Tensor**: `[1, 3, 320, 320]`
- **Output Tensor**: `[1, 648, 2100]`
- **Average CPU Latency**: `19.68 ms` (`50.8 FPS`)
- **Recommended Inference Threshold**: `0.25`

