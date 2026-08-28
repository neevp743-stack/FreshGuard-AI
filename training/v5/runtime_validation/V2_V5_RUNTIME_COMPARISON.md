# FreshGuard Vision — V2 vs V5 Runtime Comparison Report

| Attribute | V2 Production Model | V5 Candidate Model |
| :--- | :--- | :--- |
| **Vocabulary Size** | 35 Classes | **644 Grocery Classes** |
| **Runtime Latency** | ~45 ms | `414.5 ms` |
| **Selection Flag** | `FRESHGUARD_VISION_MODEL=v2` | `FRESHGUARD_VISION_MODEL=v5` |
| **Reversible Fallback** | Instant Baseline | Immediate Candidate |
