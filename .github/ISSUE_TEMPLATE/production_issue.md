---
name: Production Incident Report
about: Report a cloud deployment, backend latency, availability, or production regression incident.
title: '[PROD] '
labels: 'production, incident'
assignees: ''
---

### 🚨 Incident Summary
A brief description of the production incident or deployment issue.

### 🌐 Affected Deployment Environment
- **Backend Service**: Render Web Services (`https://freshguard-ai-auef.onrender.com`)
- **Frontend Service**: Vercel Edge (`https://fresh-guard-ai-delta.vercel.app`)
- **Endpoint Affected**: [e.g. `/health`, `/api/v1/vision/detect-multi`, `/api/v1/inventory`]

### ⏱️ Timestamp & Duration
- **Incident Start Time**: [UTC Timestamp]
- **Incident Duration**: [e.g. 15 minutes, Ongoing]

### 📊 Observed Symptoms & Error Codes
- **HTTP Status Code**: [e.g. 500 Internal Server Error, 503 Service Unavailable, 403 Forbidden]
- **Latency / Response Time**: [e.g. > 5000 ms]

### 📜 Server Logs / Diagnostics Output
```text
Paste Render or browser console error logs here.
```

### 🛠️ Remediation / Temporary Workaround
Any immediate action taken to mitigate the issue.
