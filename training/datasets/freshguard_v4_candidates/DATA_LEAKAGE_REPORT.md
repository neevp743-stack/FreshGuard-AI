# FreshGuard Vision V4 — Data Leakage Audit Report

## Leakage Prevention Protocol
> [!IMPORTANT]
> **Base Scene Grouping Protocol**: All images derived from the same base scene are assigned **strictly to a single split** (Train, Val, or Test).

## Split Partition Distribution

| Split | Base Scenes Count | Image Files Count | Percentage |
| :--- | :--- | :--- | :--- |
| **Train** | `1021` | `1021` | `80.1%` |
| **Val** | `127` | `127` | `10.0%` |
| **Test** | `127` | `127` | `10.0%` |

## Cross-Split Leakage Audit Findings
- **Train vs Val Base Scene Overlap**: **0 (ZERO LEAKAGE)**
- **Train vs Test Base Scene Overlap**: **0 (ZERO LEAKAGE)**
- **Val vs Test Base Scene Overlap**: **0 (ZERO LEAKAGE)**
- **Data Leakage Status**: **PASSED — ZERO CROSS-SPLIT LEAKAGE**
