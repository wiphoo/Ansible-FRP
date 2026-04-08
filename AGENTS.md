# Repository Guidelines

## Project Structure & Module Organization
This repository is an Ansible collection for FRP deployment. Core role code lives under `roles/frp_install/`, with defaults in `defaults/main.yml`, variables in `vars/main.yml`, task entrypoints in `tasks/`, handlers in `handlers/`, and Jinja2 templates in `templates/`. Pytest-based validation lives in `tests/`, while Molecule scenarios for integration coverage live in `roles/frp_install/molecule/`. User and maintainer docs are under `docs/`, and CI behavior is defined in `.github/workflows/`.

## Build, Test, and Development Commands
Use `uv` for environment and command execution.

```bash
uv sync --extra dev --extra test     # install development and test dependencies
uv run pytest tests/                 # run unit tests with coverage enforcement
uv run ruff check .                  # lint Python files
uv run ruff format --check .         # verify formatting
uv run ansible-lint roles/           # lint Ansible content
uv run pre-commit run --all-files    # run the full local quality gate
cd roles/frp_install && uv run molecule test --scenario-name dev
uv run mkdocs build --clean --strict # build docs
```

Prefer the `dev` Molecule scenario for quick feedback; use `default`, `ci`, `config-variables`, or `variables` when touching release behavior or template inputs.

## Coding Style & Naming Conventions
Follow Ruff defaults from `pyproject.toml`: 4-space indentation, 88-character line length, double quotes in Python, and import sorting via Ruff/isort. Keep YAML readable and compatible with `.yamllint`. For Ansible content, use descriptive task names and `frp_install_*` variable prefixes. Name pytest files `test_*.py` and keep scenario names descriptive, lowercase, and hyphenated where needed.

## Testing Guidelines
Pytest is configured with strict markers and a coverage floor of 85%. Use existing markers such as `unit`, `integration`, `template`, `config`, and `slow` where appropriate. Add or update tests in `tests/` for logic changes, and update Molecule verification playbooks when role behavior, templates, or service management changes.

## Commit & Pull Request Guidelines
Recent history mixes plain summaries and Conventional Commit prefixes, but `fix:` and `chore:` are already in use. Prefer concise, imperative commit subjects such as `fix: correct FRP template variable handling`. PRs should describe the change, list commands run, note any docs or changelog updates, and link the related issue when applicable. Include screenshots only for docs or UI-like output changes.

## Security & Configuration Tips
Do not commit real FRP tokens, passwords, or inventory secrets. Keep examples sanitized, and verify firewall, service, and template changes against the role docs in `docs/` before merging.
