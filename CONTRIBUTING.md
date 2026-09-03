# Contributing to FreshGuard AI

Thank you for your interest in contributing to FreshGuard AI! We welcome open-source contributions that help make FreshGuard AI safer, faster, more reliable, and more feature-rich.

To maintain production stability and high code quality, all contributors must follow the guidelines outlined below.

---

## 🛑 Production Safety & Model Rules

> [!IMPORTANT]
> **Production Stability Policy**: FreshGuard AI is a live, production-tested platform.
> - **DO NOT alter, retrain, or overwrite production vision models** in `vision_models/` without an approved RFC and explicit model integrity update.
> - **DO NOT weaken or remove existing automated tests**.
> - **DO NOT introduce hardcoded secrets, API tokens, or mock fallback logic**.
> - **DO NOT break existing API contracts** (`/api/v1/*`).

---

## 💻 Local Development Setup

### Prerequisites
- **Python**: 3.11 or higher
- **Node.js**: 18+ (for frontend web development)
- **Git**: Latest version

### Setup Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/neevp743-stack/FreshGuard-AI.git
   cd FreshGuard-AI
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Frontend Web Setup**:
   ```bash
   cd frontend
   # Open index.html in browser or serve via static HTTP server:
   npx serve .
   ```

4. **Verify Baseline Model Integrity**:
   ```bash
   python scripts/verify_model_integrity.py
   ```

5. **Run Test Suite**:
   ```bash
   cd backend
   python -m pytest backend/tests -v
   ```
   *Verify that all 60 tests pass.*

---

## 🌿 Branch Naming Conventions

Use descriptive branch names with appropriate prefixes:

- `feat/feature-name` — New feature additions
- `fix/bug-description` — Bug fixes
- `docs/documentation-update` — Documentation improvements
- `refactor/component-name` — Code maintainability / refactoring without behavior change
- `test/test-description` — Adding or improving tests
- `chore/task-name` — Maintenance tasks, dependencies, build configurations

---

## 📝 Commit Conventions

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat(component): short description`
- `fix(component): short description`
- `docs(readme): update setup instructions`
- `test(inventory): add test for batch creation`
- `refactor(vision): improve openapi metadata`
- `chore(deps): update requirements`

### Guidelines:
- Keep commits logical and focused on a single concern.
- Do NOT create meaningless commits to inflate commit history.
- Write imperative, present-tense commit messages (e.g., `add test` not `added test`).

---

## 🧪 Testing Requirements

- All pull requests must pass the complete test suite (`python -m pytest backend/tests -v`).
- Every new feature or bug fix MUST include corresponding test coverage.
- Tests must be deterministic and isolated (using clean temporary database sessions).
- Run model integrity checks before submitting:
  ```bash
  python scripts/verify_model_integrity.py
  ```

---

## 📐 Code Quality & Formatting

- **Python**: Follow PEP 8 style guidelines. Add type hints to public methods and write clear docstrings for non-trivial logic.
- **HTML/JS/CSS**: Use clean, modern vanilla JavaScript and CSS without external bulky dependencies unless requested.
- **Error Handling**: Use explicit FastAPI exception handling with descriptive error detail payloads.

---

## 📥 Pull Request Requirements

When opening a Pull Request:

1. Use the provided [PR Template](.github/pull_request_template.md).
2. Provide a clear summary of changes and the problem being solved.
3. List the affected components and execution results of tests.
4. Include screenshots or terminal logs for UI/API updates.
5. Ensure `verify_model_integrity.py` passes without errors.
6. Ensure no merge conflicts exist with `main`.

---

## 🔒 Security Reporting

For security vulnerabilities, please refer to our [Security Policy](SECURITY.md). Do NOT report security issues via public GitHub issues.
