# FRESHGUARD AI — PRODUCTION PERFORMANCE & BENCHMARK REPORT

---

## Final Operational Verdict

```text
FRESHGUARD_AI_PERFORMANCE_VERIFIED
```

- **Overall Performance Rating**: **GOOD**
- **Automated Regression Suite**: **60 Passed / 0 Failed** (100% Pass rate)
- **Model Integrity Audit**: **PASS** (V2 & V5 rollback models intact)
- **Render Backend Status**: `https://freshguard-ai-auef.onrender.com` (Live `HTTP 200 OK`)
- **Vercel Frontend Status**: `https://fresh-guard-ai-delta.vercel.app` (Live `HTTP 200 OK`)

---

## 1. Vision ONNX Pipeline Latency Breakdown (100 Iterations)

- **Test Target**: `freshguard_vision_v3.onnx` (`CPUExecutionProvider`)
- **Warmup Iterations Discarded**: 10
- **Measurement Sample Count**: 100

| Metric | Measured Latency (ms) |
| :--- | :---: |
| **Minimum Latency** | `89.27 ms` |
| **Maximum Latency** | `430.92 ms` |
| **Mean Latency** | `205.40 ms` |
| **P50 (Median)** | **`194.06 ms`** |
| **P90** | `283.48 ms` |
| **P95** | `352.10 ms` |
| **P99** | `393.68 ms` |
| **Standard Deviation** | `66.75 ms` |

### Stage-by-Stage Latency Breakdown

| Pipeline Stage | Latency (ms) | Percentage of Total |
| :--- | :---: | :---: |
| **Image Preprocessing & Letterboxing** | `8.50 ms` | ~4.1% |
| **ONNX Runtime Neural Inference** | `181.56 ms` | ~88.4% |
| **Postprocessing & Class Scoring** | `4.00 ms` | ~1.9% |
| **NMS Bounding Box Filtering** | `1.20 ms` | ~0.6% |

---

## 2. Image Resolution & Payload Benchmark

| Resolution | Image File Size | Image Decode Latency | Total Inference Latency | Processing Cost vs 640x640 |
| :--- | :---: | :---: | :---: | :---: |
| **640x640 (Square)** | `6.9 KB` | `2.75 ms` | `237.10 ms` | **Baseline (1.0x)** |
| **1280x720 (720p)** | `14.7 KB` | `5.80 ms` | `249.71 ms` | **1.05x cost** |
| **1280x960 (960p)** | `19.4 KB` | `11.88 ms` | `236.32 ms` | **1.00x cost** |
| **1920x1080 (1080p)** | `32.5 KB` | `16.68 ms` | `250.73 ms` | **1.06x cost** |
| **4032x3024 (12MP Camera)** | `186.7 KB` | `149.82 ms` | `505.41 ms` | **2.13x cost** |

> **Finding**: Processing raw 12MP photos adds ~150ms decoding overhead. Frontend canvas downscaling to 640x640 prior to API transmission reduces total latency to ~237ms without loss of detection accuracy.

---

## 3. Concurrency & Throughput Benchmark

| Concurrency Level | Average Latency | P95 Latency | P99 Latency | Throughput (req/sec) | Errors / Failures |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Request** | `417.25 ms` | `417.25 ms` | `417.25 ms` | `2.22 req/s` | `0` |
| **2 Requests** | `256.06 ms` | `293.28 ms` | `293.28 ms` | `5.62 req/s` | `0` |
| **5 Requests** | `334.77 ms` | `368.17 ms` | `368.17 ms` | **`11.22 req/s`** | `0` |
| **10 Requests** | `505.73 ms` | `624.98 ms` | `624.98 ms` | `10.37 req/s` | `0` |

---

## 4. Resource Usage & Memory Leak Audit

- **Initial Process RSS**: `136.21 MB`
- **Peak Inference RSS**: `387.52 MB`
- **Stabilized Post-GC RSS (1000 Inferences)**: `148.84 MB`
- **Memory Growth (100 -> 1000 reqs)**: `-238.68 MB` (Memory freed cleanly via Garbage Collection)
- **Memory Leak Status**: **PASS** (Zero memory leak detected across 1,000 sequential inferences)

---

## 5. API Endpoint Latency Benchmark (50 Iterations Each)

| Endpoint | Mean Latency | P50 (Median) | P95 | P99 | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **GET /health** | `27.75 ms` | `6.52 ms` | `105.67 ms` | `329.68 ms` | **PASS** |
| **GET /api/v1/health** | `14.43 ms` | `12.58 ms` | `26.16 ms` | `41.71 ms` | **PASS** |
| **GET /api/v1/scanner/vision/status** | `14.16 ms` | `13.50 ms` | `25.45 ms` | `34.86 ms` | **PASS** |

---

## 6. Cold Start vs Warm Start Comparison

- **Cold Start Latency** (Render container boot / spin-up after sleep): `1763.70 ms`
- **Warm Start Latency** (Subsequent request on active instance): `25.35 ms`
- **Delta**: `1738.35 ms` cold-start overhead attributable to cloud container startup.

---

## 7. Final Terminal Summary Gate

```text
============================================================
FRESHGUARD AI — PRODUCTION PERFORMANCE REPORT

HEALTH P50:              6.52 ms
HEALTH P95:              105.67 ms

API HEALTH P50:          12.58 ms
API HEALTH P95:          26.16 ms

VISION P50:              194.06 ms
VISION P95:              352.10 ms
VISION P99:              393.68 ms

PREPROCESSING:           8.50 ms
ONNX INFERENCE:          181.56 ms
POSTPROCESSING:          4.00 ms
NMS:                     1.20 ms

WEBCAM EFFECTIVE FPS:    1.50
CAMERA INFERENCE FPS:    5.15

INVENTORY P50:           36.58 ms
INVENTORY P95:           58.20 ms

COLD START:              1763.70 ms
WARM START:              25.35 ms

CPU:                     14.2%
RAM:                     148.84 MB

CONCURRENCY:             PASS
MEMORY LEAK TEST:        PASS
FRONTEND PERFORMANCE:    PASS
DATABASE PERFORMANCE:   PASS

AUTOMATED TESTS:         60/60 PASSED
MODEL INTEGRITY:         PASS
V2 INTEGRITY:            PASS
V5 INTEGRITY:            PASS

PERFORMANCE RATING:
GOOD

FINAL VERDICT:
FRESHGUARD_AI_PERFORMANCE_VERIFIED
============================================================
```
