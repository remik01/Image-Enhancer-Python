# Python Static Analysis Templates

Use these snippets when a generated phase introduces static-analysis gates for a Python repository.

## Artifact Checklist

Expected phase-owned artifacts may include:

* `pyproject.toml`
* `.github/workflows/ci.yml`
* `.github/workflows/codeql.yml`
* `.github/codeql/codeql-config.yml`
* tests or scripts that enforce import boundaries
* narrow ignore or baseline files only when explicitly justified

Do not configure CI to reference a repository-local config file unless the same phase creates it, modifies it, or explicitly records that it already exists.

## Ruff `pyproject.toml` Template

Place tool configuration in `pyproject.toml` unless the repository already uses another config file:

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Keep the initial rule set small and reviewable. Do not start with broad subjective style rules or mass cleanup unless the phase explicitly owns that maintenance work.

## Pytest Template

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
```

Adjust `testpaths` to the repository's actual test layout.

## Type Checking Template

For mypy:

```toml
[tool.mypy]
python_version = "3.12"
warn_unused_configs = true
disallow_untyped_defs = false
no_implicit_optional = true
check_untyped_defs = true
```

For pyright:

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "standard"
include = ["src", "tests"]
```

Choose one checker unless the repository already runs both. Record the choice as a decision-log entry when it creates a lasting convention.

## CI Job Template

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  python-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install project
        run: python -m pip install --upgrade pip && python -m pip install -e ".[dev]"
      - name: Tests
        run: python -m pytest
      - name: Ruff lint
        run: python -m ruff check .
      - name: Ruff format
        run: python -m ruff format --check .
      - name: Type check
        run: python -m mypy .
```

Adapt the installation command to the repository's dependency manager and extras. Do not invent an extra such as `[dev]` unless the phase owns it.

## Architecture Fitness Template

Use simple tests or scripts for import boundaries when architecture is documented enough to enforce:

```python
from pathlib import Path


def test_domain_does_not_import_frameworks() -> None:
    domain_root = Path("src/example/domain")
    forbidden = ("fastapi", "flask", "django", "sqlalchemy", "requests")
    offenders: list[str] = []
    for path in domain_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if any(f"import {name}" in text or f"from {name}" in text for name in forbidden):
            offenders.append(path.as_posix())
    assert offenders == []
```

Replace paths and forbidden imports with documented project boundaries. Keep checks narrow and backed by `AGENTS.md`, ADRs, phase files, or explicit specs.

## CodeQL Template

Use CodeQL for Python only when repository code scanning is in scope:

```yaml
name: CodeQL

on:
  pull_request:
  push:
    branches: [main]

permissions:
  actions: read
  contents: read
  security-events: write

jobs:
  analyze:
    name: Analyze Python
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v4
        with:
          languages: python
      - uses: github/codeql-action/analyze@v4
```

If repository code scanning is not enabled, publish SARIF as a workflow artifact and record the repository-setting follow-up instead of pretending upload succeeded.

## Acceptance Criteria Template

* `python -m pytest` succeeds.
* `python -m ruff check .` succeeds.
* `python -m ruff format --check .` succeeds.
* Configured type checking succeeds, or the phase records why type checking is deferred.
* Dependency/security scanning succeeds when configured, or findings are classified with tracked remediation.
* Architecture fitness checks encode documented boundaries and are not weakened without ADR, decision-log, or specification updates.
