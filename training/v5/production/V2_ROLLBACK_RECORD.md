# FreshGuard Vision — Emergency V2 Rollback Reference Record

## V2 Baseline Preservation Audit
- **V2 Model File**: `grocery_yolov8_v2_web/model.onnx` (`5c98003d9c686dcc0733e095143d09fe0bd382b2a7e3b6171fd6c7d76b9dcd7a`) $\rightarrow$ **100% UNTOUCHED**
- **V2 Metadata File**: `vision_models/model_metadata.json` (`85088cf442c6067f51613b2ad51b8ebbd8f53d3e08705d5cbfbcad3b21709ae0`) $\rightarrow$ **100% UNTOUCHED**
- **Rollback Protocol**: To execute an emergency rollback to V2, set `FRESHGUARD_VISION_MODEL=v2` in environment variables or `.env`.
