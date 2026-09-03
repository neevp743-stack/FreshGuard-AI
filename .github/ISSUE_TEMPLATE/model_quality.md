---
name: Model Quality & Vision Report
about: Report a vision detection misclassification, bounding box error, or confidence policy anomaly.
title: '[VISION] '
labels: 'model-quality, vision'
assignees: ''
---

### 📷 Detection Observation
Describe the vision model behavior observed (e.g. false positive, false negative, incorrect class label, bad bounding box).

### 🏷️ Target & Predicted Class
- **Expected Item / Class**: [e.g. Tomato, Milk, Apple]
- **Predicted Class**: [e.g. Red Bell Pepper, Unknown, or None]
- **Class ID Detected**: [e.g. 0 to 34]
- **Confidence Score Reported**: [e.g. 0.42]
- **Confidence Tier**: [HIGH / MEDIUM / LOW]

### 🧪 Test Conditions
- **Input Source**: [Webcam Feed / Uploaded Image Payload / Test Script]
- **Lighting & Angle**: [Well-lit, Dim, Overlapping items, Single item]
- **Model Version**: [Vision V3 ONNX - `freshguard_vision_v3.onnx`]

### 📜 Vision API Metadata JSON
```json
{
  "class_id": 0,
  "confidence": 0.45,
  "requires_confirmation": true
}
```

### 💡 Suggested Improvement
Ideas for dataset expansion or confidence threshold adjustments.
