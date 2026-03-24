# Releasing c3-invoke

## Workflows Overview

| Workflow | Trigger | Target |
|----------|---------|--------|
| `ci.yml` | Push/PR to `main` | Runs tests + build verification |
| `test-publish.yml` | Manual (workflow_dispatch) | Publishes to TestPyPI |
| `publish.yml` | GitHub Release published | Publishes to PyPI |

## Prerequisites

- Trusted publisher configured on [PyPI](https://pypi.org/manage/account/publishing/) and [TestPyPI](https://test.pypi.org/manage/account/publishing/) for this repo
- GitHub environments `pypi` and `testpypi` created in repo Settings > Environments

## Step-by-Step Release Process

### 1. Test publish to TestPyPI

Run the test publish workflow first to verify everything works:

1. Go to **Actions** > **Test Publish to TestPyPI** > **Run workflow**
2. Optionally enter a PEP 440 version suffix (e.g. `.dev1`, `rc1`, `a1`)
3. Click **Run workflow**
4. Verify installation:
   ```bash
   pip install -i https://test.pypi.org/simple/ c3-invoke
   ```

### 2. Bump version

Update the version in `pyproject.toml`:

```toml
version = "X.Y.Z"
```

Commit and push:

```bash
git add pyproject.toml
git commit -m "Bump version to X.Y.Z"
git push origin main
```

### 3. Create a tag and release

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

Then create a GitHub Release:

1. Go to **Releases** > **Draft a new release**
2. Select the tag `vX.Y.Z`
3. Set title to `vX.Y.Z`
4. Add release notes
5. Click **Publish release**

This triggers the `publish.yml` workflow which runs tests, builds, and publishes to PyPI.

### 4. Verify

```bash
pip install c3-invoke==X.Y.Z
python -c "from c3_invoke import get_provider, list_providers; print('OK')"
```

## Version Suffixes (TestPyPI only)

When running the test publish workflow, you can append a suffix to avoid version conflicts:

| Suffix | Result | Use case |
|--------|--------|----------|
| (empty) | `0.1.1` | Exact version test |
| `.dev1` | `0.1.1.dev1` | Development snapshot |
| `rc1` | `0.1.1rc1` | Release candidate |
| `a1` | `0.1.1a1` | Alpha |
| `b1` | `0.1.1b1` | Beta |

## Troubleshooting

### 400 Bad Request from TestPyPI/PyPI
- The version already exists — use a different suffix or bump the version
- Trusted publisher not configured — set it up on PyPI/TestPyPI account settings

### Node.js deprecation warnings
- Update action versions in workflow files (checkout, setup-python, upload-artifact, download-artifact)
