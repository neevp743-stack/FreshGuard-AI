# FreshGuard AI Security Policy

FreshGuard AI prioritizes security, privacy, and data isolation for all users and deployment environments. This document outlines our security architecture, supported versions, security disclosure process, and production security policies.

---

## 🔒 Supported Versions

Only the latest release running on active production branches receives security updates.

| Version / Branch | Supported | Notes |
| :--- | :---: | :--- |
| `main` (Vision V3 Release) | Yes | Current production release |
| `release/v3.x` | Yes | Active maintenance releases |
| `< v3.0` | No | Legacy versions deprecated |

---

## 🛡️ Reporting Vulnerabilities

If you discover a security vulnerability in FreshGuard AI, please report it responsibly. **Do not create a public GitHub issue for security vulnerabilities.**

### Disclosure Process
1. Email our security team at `security@freshguard.ai` (or open a private security advisory on GitHub if enabled).
2. Include a detailed description of the vulnerability, proof-of-concept steps, affected components, and potential impact.
3. Our security team will acknowledge your report within **24–48 hours** and provide periodic updates regarding patch development.
4. We request that you give us at least **30 days** to remediate the vulnerability before public disclosure.

---

## 🔑 Secrets Policy

- **Zero Hardcoded Secrets**: Secrets, secret keys, JWT signing tokens, database passwords, and third-party API credentials MUST NEVER be hardcoded into the source code, committed to Git repositories, or included in documentation.
- **Environment Variables**: All production credentials must be supplied via environment variables (e.g., `SECRET_KEY`, `ALGORITHM`, `DATABASE_URL`).
- **Configuration Templates**: The repository includes `.env.example` containing non-sensitive default values for local development.

---

## 🏰 Authentication & Security Controls

1. **Password Hashing**:
   - Passwords are hashed using **PBKDF2-HMAC-SHA256** with 100,000 iterations and a cryptographically secure 16-byte random salt per user.
   - Legacy SHA-256 password hashes are automatically re-hashed to PBKDF2 upon successful user authentication.

2. **Session Authentication & Tokens**:
   - Access tokens are formatted as signed JWTs with expiration bounds.
   - Protected API routes require a valid `Authorization: Bearer <token>` HTTP header.

3. **Role-Based Access Control (RBAC)**:
   - System access levels include `USER` (standard household user) and `ADMIN` (system administrator).
   - Administrative endpoints (such as `/api/v1/admin/diagnostics`) strictly enforce `ADMIN` role checks and return `403 Forbidden` for non-admin accounts.

4. **Household & User Data Isolation**:
   - Every database query for inventory, freshness calculations, notifications, and shopping carts is strictly scoped to `user_id`.
   - Cross-user data leaks are prevented at the database service layer via explicit filtering clauses (`filter_by(user_id=...)`).

---

## ⚡ Production Security Rules

1. **Model Integrity**:
   - Vision model ONNX binaries are locked and verified via SHA-256 cryptographic hashes (`scripts/verify_model_integrity.py`).
   - Unauthorized modifications or hash mismatches halt deployment and boot sequences.

2. **Input Validation & Payload Hardening**:
   - All image uploads (OCR, barcode, multi-object vision detection) undergo payload size validation and image format verification.
   - Malformed base64 strings or corrupted images return clean error responses without crashing the backend process.

3. **CORS & Network Controls**:
   - Production FastAPI servers configure strict CORS origins (restricted to authorized domain names such as `https://fresh-guard-ai-delta.vercel.app`).
