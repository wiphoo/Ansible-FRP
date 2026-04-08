# Repository Guidelines

## Project Overview

This is `wiphoo.frp`, an Ansible Collection for deploying and managing [Fast Reverse Proxy (FRP)](https://github.com/fatedier/frp) on Linux systems. The single role `frp_install` handles downloading binaries, configuring TOML config files, systemd services, and firewall rules.

**Configuration format: TOML only** — INI format was deprecated in v0.1.0. All templates use `.toml.j2`.

## Commands

All Python commands must be run via `uv run` — never invoke `pytest`, `ruff`, etc. directly.

### Setup
```bash
uv sync --extra dev --extra test   # install all dev and test dependencies
pre-commit install                  # install git hooks
```

### Unit Tests
```bash
uv run pytest tests/                                                     # all tests with coverage
uv run pytest tests/test_variables.py -v                                 # single file
uv run pytest tests/test_role.py::TestFrpInstallRole::test_name -v      # single test
uv run pytest tests/ --tb=no -q                                          # quick, no verbose
uv run pytest tests/ --pdb                                               # debug on failure
```

Coverage minimum is 85% (currently ~97%). Reports are written to `htmlcov/` and `coverage.xml`.

### Integration Tests (Molecule)
```bash
# Run from roles/frp_install/ directory
cd roles/frp_install

uv run molecule test --scenario-name dev             # fast (1-2 min) — use for quick feedback
uv run molecule test --scenario-name ci              # CI testing (2-3 min)
uv run molecule test --scenario-name default         # production testing (3-5 min)
uv run molecule test --scenario-name config-variables  # for template/config changes
uv run molecule test --scenario-name variables         # for variable changes

# Individual stages
uv run molecule create --scenario-name dev
uv run molecule converge --scenario-name dev
uv run molecule verify --scenario-name dev
uv run molecule destroy --scenario-name dev
```

### Linting
```bash
uv run ruff check .                   # Python linting
uv run ruff format --check .          # formatting check
uv run ansible-lint roles/            # Ansible linting
yamllint .                            # YAML linting
uv run pre-commit run --all-files     # full quality gate
```

### Documentation
```bash
uv run mkdocs serve     # local preview at http://127.0.0.1:8000
uv run mkdocs build --clean --strict
```

### Collection Build
```bash
ansible-galaxy collection build --force
ansible-galaxy collection install wiphoo-frp-*.tar.gz --force -p ~/.ansible/collections
```

## Architecture

```
roles/frp_install/
├── defaults/main.yml          # All default variable values
├── vars/main.yml              # Computed internal variables (download URLs, filenames)
├── tasks/
│   ├── main.yml               # Task orchestration: security assertions → download → install → configure → verify
│   └── configure_templates.yml  # Template rendering tasks
├── templates/
│   ├── frps.toml.j2           # Server TOML configuration
│   ├── frpc.toml.j2           # Client TOML configuration
│   ├── frps.service.j2        # Server systemd unit
│   └── frpc.service.j2        # Client systemd unit
├── handlers/main.yml          # systemd reload/restart handlers
└── molecule/                  # Integration test scenarios (dev, ci, default, config-variables, variables)

tests/                         # pytest unit tests
├── fixtures.py                # Centralized test fixtures (all shared data here)
├── conftest.py                # Imports fixtures for pytest discovery
├── test_role.py               # Role functionality tests (~99 tests)
└── test_variables.py          # Variable validation tests (~27 tests)
```

### How Variables Flow

- `defaults/main.yml` — user-facing variables, all prefixed `frp_install_*`
- `vars/main.yml` — internal computed values (download URL assembled from version + arch + OS)
- Templates consume variables directly via Jinja2 conditionals for optional config sections

**Required variables** (role will assert and fail if missing/default):
- `frp_install_auth_token` — must be non-empty and not `changeme_default_token_123`
- `frp_install_dashboard_password` — required when frps is in `frp_install_files`

**Key installation flags:**
- `frp_install_create_config` (default: `true`) — controls TOML config file creation
- `frp_install_create_service` (default: `true`) — controls systemd unit file creation only

### Adding a New Variable

1. Add to `roles/frp_install/defaults/main.yml` (if it needs a default)
2. Update the appropriate template (`frps.toml.j2` or `frpc.toml.j2`)
3. Add to `tests/fixtures.py`
4. Add test in `tests/test_variables.py`
5. Update `docs/roles/frp_install.md` and `roles/frp_install/README.md`

## Coding Standards

### Python
- 4-space indentation, 88-character line length, double quotes — enforced by Ruff
- Import sorting via Ruff/isort (`known-first-party = ["wiphoo"]`)
- Test files: `test_*.py`, test classes: `Test*`, test functions: `test_*`

### Ansible / YAML
- 2-space indentation in YAML; quote strings containing special characters
- Always use `name:` for tasks; use descriptive task names
- Use `become: true` only when necessary; use handlers for service restarts

## Testing

Use `dev` scenario for quick feedback during development. Use `config-variables` or `variables` scenarios when modifying templates or variable defaults. Run `default` before submitting a PR.

Pytest markers: `unit`, `integration`, `template`, `config`, `slow` — `--strict-markers` is enforced so markers must be declared.

Molecule scenarios all use `frp_install_create_service: false` in Docker containers (no systemd). Config files are still written because `frp_install_create_config` defaults to `true`.

## Workflow

### Commit Messages
Use Conventional Commits: `fix:`, `feat:`, `chore:`, `docs:` prefixes with imperative subjects.
Example: `fix: correct FRP template variable handling`

### Pull Requests
PR descriptions should include: commands run to test the change, any docs or changelog updates made, and the related issue number when applicable.

Before merging: all unit tests pass, coverage ≥ 85%, at least the `dev` molecule scenario passes, and `CHANGELOG.md` is updated.

## Security

Do not commit real FRP tokens, passwords, or inventory secrets. Keep all examples and molecule test vars sanitized (use placeholder values like `test-token-12345`). Verify firewall and service changes against `docs/` before merging.
