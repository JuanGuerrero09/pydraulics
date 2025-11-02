# 🧠 CI/CD & Publishing Guide for *pydraulics*

A complete reference on how Continuous Integration (CI) and Continuous Deployment (CD) work for this project,  
including versioning, tags, and how to publish to **TestPyPI** and **PyPI** automatically using GitHub Actions.

---

## 📘 Overview

**CI/CD** automates the testing and publishing process of your package.

| Stage | Purpose | Workflow Trigger |
|--------|----------|------------------|
| **CI (Continuous Integration)** | Runs tests automatically on each commit or pull request | Every `push` or `pull_request` |
| **CD (Continuous Deployment)** | Publishes automatically to TestPyPI or PyPI if tests pass | Tag pushes: `test/v*` → TestPyPI, `v*` → PyPI |

---

## ⚙️ How It Works

### 1️⃣ Local Development

- Use an **editable install** to develop without reinstalling:
  ```bash
  uv pip install -e .
````

* This links your local source code (`src/pydraulics`) into the virtual environment.

### 2️⃣ GitHub Actions Workflows

Each workflow runs in a clean environment on every push or tag.

#### Common steps in all workflows

| Step                            | Purpose                                            |
| ------------------------------- | -------------------------------------------------- |
| **checkout**                    | Clones your repo into the GitHub runner            |
| **setup-uv**                    | Installs UV for dependency & build management      |
| **setup-python**                | Selects Python version (3.12)                      |
| **cache**                       | Restores cached UV dependencies (optional)         |
| **uv venv**                     | Creates a clean virtual environment                |
| **uv pip install -e .**         | Installs your package (editable)                   |
| **pytest**                      | Runs the full test suite                           |
| **uv build**                    | Builds `dist/` folder (`.tar.gz`, `.whl`)          |
| **upload-artifact**             | Saves the build to reuse in later jobs             |
| **download-artifact**           | Downloads the exact tested build before publishing |
| **pypa/gh-action-pypi-publish** | Publishes to TestPyPI or PyPI                      |

---

## 🧩 Tags and Versioning

GitHub tags trigger the workflows:

| Tag Type      | Example         | Target Registry                   | Workflow                                 |
| ------------- | --------------- | --------------------------------- | ---------------------------------------- |
| Test Release  | `test/v0.2.0a1` | [TestPyPI](https://test.pypi.org) | `.github/workflows/publish-testpypi.yml` |
| Final Release | `v0.2.0`        | [PyPI](https://pypi.org)          | `.github/workflows/publish-pypi.yml`     |

* Both workflows validate that the tag version == `project.version` in `pyproject.toml`.
* Publication happens **only if all tests pass** (`if: ${{ success() }}`).

---

## 🧮 Semantic Versioning (PEP 440)

Use [PEP 440](https://peps.python.org/pep-0440/) style versioning.

| Type                  | Example              | When to Use                     |
| --------------------- | -------------------- | ------------------------------- |
| **Stable release**    | `0.2.0`              | Final versions for PyPI         |
| **Alpha**             | `0.2.0a1`, `0.2.0a2` | First test builds to TestPyPI   |
| **Beta**              | `0.2.0b1`            | Near-final testing              |
| **Release candidate** | `0.2.0rc1`           | Pre-final validation            |
| **Post release**      | `0.2.0.post1`        | Minor hotfix after release      |
| **Dev release**       | `0.2.0.dev1`         | Optional for in-progress builds |

### 🚀 Typical release flow

```bash
# 1. Alpha build (TestPyPI)
version = "0.2.0a1"
git add pyproject.toml
git commit -m "Bump to 0.2.0a1"
git push
git tag -a test/v0.2.0a1 -m "Test 0.2.0a1"
git push origin test/v0.2.0a1
```

```bash
# 2. Final release (PyPI)
version = "0.2.0"
git add pyproject.toml
git commit -m "Release 0.2.0"
git push
git tag -a v0.2.0 -m "Release 0.2.0"
git push origin v0.2.0
```

```bash
# 3. Hotfix or patch
version = "0.2.0.post1"
git add pyproject.toml
git commit -m "Hotfix 0.2.0.post1"
git push
git tag -a v0.2.0.post1 -m "Hotfix 0.2.0.post1"
git push origin v0.2.0.post1
```

---

## 🧱 Workflows Overview

### 🧪 `publish-testpypi.yml`

Triggered by tags starting with `test/v`.

```yaml
on:
  push:
    tags:
      - "test/v*"
```

* Runs all tests.
* Ensures tag matches project version.
* Builds with `uv build`.
* Publishes to **TestPyPI** via `${{ secrets.TEST_PYPI_API_TOKEN }}`.

### 🚀 `publish-pypi.yml`

Triggered by tags starting with `v`.

```yaml
on:
  push:
    tags:
      - "v*"
```

* Reuses the same logic as TestPyPI.
* Publishes to **PyPI** via `${{ secrets.PYPI_API_TOKEN }}`.

---

## 🧠 Good Practices

✅ Use **editable install** (`-e .`) in development.
✅ Use **pre-release tags** (`a`, `b`, `rc`) for testing.
✅ Never reuse a version number already uploaded.
✅ Increment versions using [Semantic Versioning](https://semver.org/).
✅ Keep a `CHANGELOG.md` to track features and fixes.
✅ Always verify the tag–version match before pushing.
✅ If a release fails after uploading, bump to `.post1` or next patch.

---

## 🔒 About Tokens

* **TestPyPI token**: stored as `TEST_PYPI_API_TOKEN` in repo secrets.
* **PyPI token**: stored as `PYPI_API_TOKEN`.
* These are used by `pypa/gh-action-pypi-publish` for authentication.

*Tip:* You can later switch to “Trusted Publishing” (OIDC) to remove token usage.

---

## 🧭 Full CI/CD Flow Diagram

```text
 ┌────────────┐        ┌───────────────┐        ┌───────────────┐        ┌───────────────┐
 │   Push /   │  --->  │    CI Tests   │  --->  │  Build dist/  │  --->  │ Upload artifact│
 │ Pull Req.  │        │ (pytest, lint)│        │ (uv build)    │        │ (cached safely)│
 └────────────┘        └───────────────┘        └───────────────┘        └───────────────┘
                                                                │
                                                                ▼
                                                      ┌──────────────────┐
                                                      │  Publish job     │
                                                      │ (TestPyPI / PyPI)│
                                                      └──────────────────┘
```

---

## 🧾 Troubleshooting

| Issue                                          | Cause                           | Fix                                       |
| ---------------------------------------------- | ------------------------------- | ----------------------------------------- |
| `ModuleNotFoundError: No module named 'utils'` | Wrong import path               | Ensure `src/` layout and editable install |
| `Version mismatch` in Actions                  | Tag and `pyproject.toml` differ | Bump version or rename tag                |
| `File already exists` on PyPI                  | Version already uploaded        | Use `0.x.y.post1` or `0.x.(y+1)`          |
| Cache warning (`pip` not found)                | UV used instead of pip          | Remove `cache: pip` from workflow         |
| Token invalid                                  | Wrong secret name or expired    | Regenerate token and re-save secret       |

---

## 🧩 Summary Table

| Step                 | Tool / Command                     | Output                        |
| -------------------- | ---------------------------------- | ----------------------------- |
| Local dev            | `uv pip install -e .`              | Editable install              |
| Tests                | `uv run -m pytest`                 | Test report                   |
| Build                | `uv build`                         | `dist/*.whl`, `dist/*.tar.gz` |
| Test publish         | tag `test/v*`                      | Published on TestPyPI         |
| Final publish        | tag `v*`                           | Published on PyPI             |
| Install user version | `uv pip install pydraulics==0.x.y` | Installed package             |

---

## ✅ Final Notes

* Use **TestPyPI** to validate that your build and metadata work correctly.
* Once confirmed, push a clean tag (`vX.Y.Z`) for PyPI.
* Each version on PyPI is **immutable** — treat it as permanent.
* The entire CI/CD pipeline ensures that only **tested, validated, and version-matched** builds reach production.

---

**Maintainer:** Juan David Guerrero
**Package:** `pydraulics`
**License:** MIT
**Python:** ≥3.12
**Tools:** UV · GitHub Actions · pytest · PyPI/TestPyPI

