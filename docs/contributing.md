# Contributing

Thank you for contributing to the wiphoo.frp collection!

## Quick Start

**Ways to help:**
- Bug reports and feature requests
- Code contributions and documentation
- Testing and examples

**Requirements:**
- Git, Python 3.11+, Docker
- Ansible Core >=2.17.0 (automatically installed via uv)
- uv package manager for dependency management

## Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Ansible-FRP.git
cd Ansible-FRP

# Setup environment with uv (includes dev and test dependencies)
uv sync --extra dev
source .venv/bin/activate

# Install pre-commit hooks
pre-commit install

# Verify setup
uv run pytest
uv run ruff check .
uv run ruff format --check
```

## Code Standards

**Follow Ansible best practices:**
- Descriptive task names
- Proper variable naming (`frp_*`)
- Document all variables
- Use YAML formatting

**Example:**
```yaml
- name: Install FRP binary
  copy:
    src: "{{ frp_binary_path }}"
    dest: "{{ frp_install_dir }}/frpc"
    mode: '0755'
  become: true
  notify: restart frpc
```

## Testing

**Available test approaches:**

```bash
# Unit tests with pytest (126 tests, 96.85% coverage)
uv run pytest tests/ -v --cov=tests

# Quick unit tests
uv run pytest tests/ --tb=no -q

# Coverage report
uv run pytest tests/ --cov-report=html

# Code quality checks
uv run ruff check .
uv run ruff format --check
yamllint .
ansible-lint roles/frp_install/

# Molecule integration testing (5 scenarios)
cd roles/frp_install
uv run molecule test --scenario-name dev              # Fast development (1-2 min)
uv run molecule test --scenario-name ci               # CI-optimized (2-3 min)
uv run molecule test --scenario-name default          # Full production (3-5 min)
uv run molecule test --scenario-name config-variables # Config validation (2-3 min)
uv run molecule test --scenario-name variables        # Full variable test (2-3 min)
```

**Test scenarios explained:**
- **`dev`** - Fast development testing (1-2 min) - Quick iteration with instant feedback
- **`ci`** - CI/CD optimized with version override (2-3 min) - Automated testing
- **`default`** - Complete production testing (3-5 min) - Final validation before release
- **`config-variables`** - Configuration variable validation (2-3 min) - Template testing
- **`variables`** - Full variable testing (2-3 min) - Comprehensive variable validation

> **Note**: All scenarios exclude idempotence testing as the role downloads external binaries and is non-idempotent by design.

**Write tests for new features:**
```python
def test_frp_installation():
    """Test FRP installation process."""
    # Implementation
```

## Pull Requests

**Before submitting:**
1. Create issue to discuss changes
2. Write tests and update docs
3. Run full test suite
4. Test local collection build and installation
5. Update CHANGELOG.md

**PR Format:**
- Descriptive title referencing issue
- Brief description of changes
- Test results and checklist

## Documentation

**Guidelines:**
- Clear, practical examples
- Include troubleshooting tips
- Keep current with code changes

```bash
# Build and test docs
uv run mkdocs build
uv run mkdocs serve
```

## Local Collection Testing

**Build and install collection locally:**

```bash
# Build the collection
ansible-galaxy collection build --force

# Install locally for testing
ansible-galaxy collection install wiphoo-frp-0.2.0.tar.gz --force -p ~/.ansible/collections

# Verify installation
ansible-galaxy collection list | grep wiphoo.frp

# Test with a simple playbook
ansible-playbook -i localhost, docs/examples/examples.yml --connection=local
```

**Alternative installation paths:**
```bash
# Install to current directory collections/
ansible-galaxy collection install wiphoo-frp-0.2.0.tar.gz --force -p ${{ github.workspace }}/collections

# Install system-wide (requires sudo)
sudo ansible-galaxy collection install wiphoo-frp-0.2.0.tar.gz --force
```

## Dependency Management

**The project uses a streamlined dependency structure:**

- **Core dependencies**: Only `ansible-core>=2.17.0` for minimal runtime
- **Test dependencies**: All testing and molecule dependencies (`uv sync --extra test`)
- **Dev dependencies**: Includes test + development tools (`uv sync --extra dev`)

**Installation options:**
```bash
# For development (recommended)
uv sync --extra dev

# For testing only
uv sync --extra test

# Minimal runtime
uv sync
```

## Getting Help

- **Questions**: Open GitHub discussion
- **Bugs**: Create detailed issue
- **Chat**: Community channels

Thanks for contributing! 🚀
