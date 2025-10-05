# GitHub Copilot Instructions for Ansible-FRP Collection

## Project Overview

This is an **Ansible Collection** for deploying and managing **Fast Reverse Proxy (FRP)** on Linux systems. The collection provides production-ready automation with comprehensive testing and CI/CD pipelines.

- **Collection Name**: `wiphoo.frp`
- **Primary Role**: `frp_install`
- **Repository**: https://github.com/wiphoo/Ansible-FRP
- **Branch**: `main`
- **License**: MIT

## Tech Stack

### Core Technologies
- **Ansible Core**: >=2.15.0
- **Python**: 3.11+ (tested on 3.10, 3.12)
- **Package Manager**: `uv` (for Python package management)
- **Configuration Format**: TOML (INI support deprecated as of v0.1.0)
- **FRP Version**: 0.65.0 (default)

### Testing Framework
- **Unit Tests**: pytest 8.4.2 with pytest-ansible plugin
- **Integration Tests**: Molecule 6.0+ with Docker
- **Code Coverage**: pytest-cov (target: 85%, currently: 96.85%)
- **Linting**: ansible-lint, yamllint, ruff
- **Pre-commit**: Hooks for code quality

### CI/CD
- **Platform**: GitHub Actions
- **Workflows**: 5 workflows (main, pr-validation, docs, release, security)
- **Documentation**: MkDocs with Material theme

## Project Structure

```
wiphoo_ansible_frp/
├── roles/frp_install/          # Main Ansible role
│   ├── defaults/main.yml       # Default variables
│   ├── handlers/main.yml       # Service handlers
│   ├── tasks/                  # Role tasks
│   │   ├── main.yml           # Main task orchestration
│   │   └── configure_templates.yml  # Template configuration
│   ├── templates/              # Jinja2 templates (TOML only)
│   │   ├── frpc.toml.j2       # Client configuration
│   │   ├── frps.toml.j2       # Server configuration
│   │   ├── frpc.service.j2    # Client systemd service
│   │   └── frps.service.j2    # Server systemd service
│   └── molecule/               # Integration test scenarios
│       ├── dev/               # Fast development testing (1-2 min)
│       ├── ci/                # CI/CD testing (2-3 min)
│       ├── default/           # Production testing (3-5 min)
│       ├── config-variables/  # Configuration validation
│       └── variables/         # Full variable testing
├── tests/                      # Unit tests (pytest)
│   ├── conftest.py            # Pytest configuration
│   ├── fixtures.py            # Centralized test fixtures
│   ├── test_role.py           # Role functionality tests (99 tests)
│   └── test_variables.py      # Variable validation tests (27 tests)
├── docs/                       # MkDocs documentation
├── .github/workflows/          # GitHub Actions workflows
├── pyproject.toml             # Python project configuration
├── galaxy.yml                 # Ansible Galaxy metadata
└── ansible.cfg                # Ansible configuration
```

## Key Variables

### Installation Variables
- `frp_install_version`: FRP version (default: "0.65.0")
- `frp_install_files`: Components to install (default: ['frps', 'frpc'])
- `frp_install_create_service`: Create systemd services (default: true)
- `frp_install_user`: System user (default: "frp")
- `frp_install_group`: System group (default: "frp")
- `frp_install_auth_token`: Authentication token (required)

### Server Configuration
- `frp_install_server_addr`: Server bind address (default: "0.0.0.0")
- `frp_install_server_port`: Server bind port (default: 7000)
- `frp_install_dashboard_addr`: Dashboard address (default: "127.0.0.1")
- `frp_install_dashboard_port`: Dashboard port (default: 7500)

### Client Configuration
- `frp_install_client_server_addr`: FRP server address (required)
- `frp_install_client_server_port`: FRP server port (default: 7000)
- `frp_install_client_webserver_enabled`: Enable web UI (default: false)

### Optional Variables
Variables that don't require defaults (file paths, advanced features):
- TLS/SSL certificates: `*_tls_cert_file`, `*_tls_key_file`, `*_tls_trusted_ca_file`
- SSH keys: `ssh_tunnel_gateway`, `ssh_public_key`, `ssh_private_key`
- Advanced: `allow_ports`, `includes`, `dns_server`, OIDC configuration

## Testing Commands

### Unit Tests (pytest)
```bash
# Run all unit tests with coverage
uv run pytest tests/ -v --cov=tests

# Quick test (no verbose output)
uv run pytest tests/ --tb=no -q

# Generate HTML coverage report
uv run pytest tests/ --cov-report=html

# Run specific test file
uv run pytest tests/test_variables.py -v

# Run specific test class
uv run pytest tests/test_role.py::TestFrpInstallRole -v

# Run specific test
uv run pytest tests/test_variables.py::TestVariables::test_all_expected_variables_exist -v
```

### Integration Tests (Molecule)
```bash
# Quick development testing (1-2 min)
molecule test --scenario-name dev

# CI/CD testing with version override (2-3 min)
molecule test --scenario-name ci

# Production testing (3-5 min)
molecule test --scenario-name default

# Configuration variable testing (2-3 min)
molecule test --scenario-name config-variables

# Full variable testing (2-3 min)
molecule test --scenario-name variables

# List all scenarios
molecule list

# Run specific stages
molecule create --scenario-name dev
molecule converge --scenario-name dev
molecule verify --scenario-name dev
molecule destroy --scenario-name dev
```

### Linting & Code Quality
```bash
# Ansible linting
ansible-lint roles/frp_install/

# YAML linting
yamllint .

# Python linting with ruff
ruff check .

# Pre-commit hooks
pre-commit run --all-files
```

### Documentation
```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Collection Management
```bash
# Build collection
ansible-galaxy collection build

# Install collection locally
ansible-galaxy collection install wiphoo-frp-*.tar.gz --force

# Publish to Galaxy
ansible-galaxy collection publish wiphoo-frp-*.tar.gz
```

### Workflow Validation
```bash
# Validate GitHub Actions workflows (requires act)
act -l

# Test specific workflow locally
act -j test
```

## Coding Standards

### Ansible Best Practices
1. **YAML Formatting**:
   - Use 2-space indentation
   - Quote strings containing special characters
   - Use YAML lists (with `-`) not inline lists
   - Always use `name:` for tasks

2. **Variable Naming**:
   - Prefix all role variables with `frp_install_`
   - Use snake_case for variable names
   - Use descriptive names (e.g., `frp_install_client_server_addr` not `frp_server`)

3. **Templates**:
   - Use TOML format only (INI deprecated)
   - Template files end with `.j2`
   - Use Jinja2 conditionals for optional configurations
   - Preserve indentation and formatting

4. **Tasks**:
   - Use `become: true` only when necessary
   - Add `check_mode: yes` for validation tasks
   - Use handlers for service restarts
   - Tag tasks appropriately

### Python/Pytest Standards
1. **Test Organization**:
   - Use class-based test organization (TestClass pattern)
   - Centralize fixtures in `tests/fixtures.py`
   - Import fixtures via `tests/conftest.py`
   - Descriptive test names: `test_<what>_<expected_result>`

2. **Fixtures**:
   - Define reusable fixtures in `fixtures.py`
   - Use pytest scope (session, module, function) appropriately
   - Document fixture purpose with docstrings

3. **Assertions**:
   - Use descriptive assertion messages
   - Test one concept per test method
   - Use pytest's built-in assertions

4. **Coverage**:
   - Maintain minimum 85% code coverage
   - Cover happy paths and error conditions
   - Test edge cases

### Documentation Standards
1. **README Files**:
   - Include usage examples
   - Document all variables
   - Provide troubleshooting guidance
   - Keep up-to-date with code changes

2. **Code Comments**:
   - Comment complex logic
   - Explain "why" not "what"
   - Use YAML comments for task explanations

3. **Changelog**:
   - Follow semantic versioning
   - Document breaking changes
   - Include migration guides

## Development Workflow

### Making Changes
1. Create feature branch from `main`
2. Make changes with descriptive commits
3. Run tests: `uv run pytest tests/`
4. Run linting: `ansible-lint`, `yamllint`, `ruff check`
5. Update documentation if needed
6. Run integration tests: `molecule test --scenario-name dev`
7. Submit PR with clear description

### Testing Strategy
1. **Unit Tests First**: Run `uv run pytest tests/` after code changes
2. **Quick Integration**: Run `molecule test --scenario-name dev` for fast feedback
3. **Full Integration**: Run `molecule test --scenario-name default` before PR
4. **CI Validation**: Ensure all GitHub Actions pass

### Version Updates
When updating FRP version:
1. Update `frp_install_version` in `roles/frp_install/defaults/main.yml`
2. Update version in test fixtures (`tests/fixtures.py`)
3. Update documentation
4. Run full test suite
5. Update CHANGELOG.md

## Important Notes

### Configuration Format
- **TOML ONLY**: INI format deprecated as of v0.1.0
- Templates: `frpc.toml.j2`, `frps.toml.j2`
- FRP v0.52.0+ uses TOML by default

### Test Expectations
- Unit tests: 126 tests (should all pass)
- Coverage target: 85% minimum (currently 96.85%)
- Integration tests: 5 scenarios configured
- Test duration: Unit (~15s), Integration (1-5 min per scenario)

### Optional Variables
Some variables are optional (file paths, advanced features) and don't need defaults:
- TLS certificate paths
- SSH key paths
- Advanced authentication (OIDC)
- Network restrictions (`allow_ports`)
- Configuration includes

### Command Runner
Always use `uv run` prefix for Python commands:
- ✅ `uv run pytest tests/`
- ✅ `uv run mkdocs serve`
- ✅ `uv run ruff check`
- ❌ `pytest tests/` (don't use)

### Molecule Scenarios
- `dev`: Fast development (1-2 min) - use for quick testing
- `ci`: CI/CD testing (2-3 min) - for automated testing
- `default`: Production testing (3-5 min) - before releases
- `config-variables`: Config validation (2-3 min) - for template changes
- `variables`: Full variable testing (2-3 min) - for variable changes

## Common Tasks

### Add New Variable
1. Add to `roles/frp_install/defaults/main.yml` (if required)
2. Update template: `roles/frp_install/templates/frp*.toml.j2`
3. Add to fixtures: `tests/fixtures.py`
4. Add test: `tests/test_variables.py`
5. Update documentation: `roles/frp_install/README.md`
6. Run tests: `uv run pytest tests/`

### Add New Test
1. Add to appropriate test file (`test_role.py` or `test_variables.py`)
2. Use existing fixtures from `tests/fixtures.py`
3. Follow naming: `test_<feature>_<expected_outcome>`
4. Ensure coverage: `uv run pytest tests/ --cov=tests`

### Fix Test Failure
1. Review test output: `uv run pytest tests/ -v`
2. Check specific test: `uv run pytest tests/test_file.py::TestClass::test_name -v`
3. Use `--pdb` for debugging: `uv run pytest tests/ --pdb`
4. Fix code or update test
5. Verify: `uv run pytest tests/`

### Update Documentation
1. Edit Markdown files in `docs/`
2. Test locally: `mkdocs serve` (http://127.0.0.1:8000)
3. Build: `mkdocs build`
4. Commit changes

## Quality Gates

### Before Committing
- ✅ Unit tests pass: `uv run pytest tests/`
- ✅ Linting passes: `ansible-lint`, `yamllint`, `ruff check`
- ✅ Pre-commit hooks pass: `pre-commit run --all-files`

### Before PR
- ✅ All unit tests pass (126/126)
- ✅ Coverage ≥85% (current: 96.85%)
- ✅ Integration test passes: `molecule test --scenario-name dev`
- ✅ Documentation updated
- ✅ CHANGELOG.md updated

### Before Release
- ✅ All workflows pass on GitHub Actions
- ✅ Full integration test: `molecule test --scenario-name default`
- ✅ Version bumped in `galaxy.yml`
- ✅ Git tag created
- ✅ Release notes prepared

## Resources

- **FRP Official Docs**: https://github.com/fatedier/frp
- **Ansible Docs**: https://docs.ansible.com/
- **Molecule Docs**: https://molecule.readthedocs.io/
- **Pytest Docs**: https://docs.pytest.org/
- **Project Docs**: https://wiphoo.github.io/Ansible-FRP/

## Status

- **Current Version**: 0.1.0
- **FRP Version**: 0.65.0
- **Test Status**: ✅ 126/126 passing
- **Coverage**: 96.85%
- **Quality**: Production Ready ✨
