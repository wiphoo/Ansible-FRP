# Contributing

Thank you for contributing to the wiphoo.frp collection!

## Quick Start

**Ways to help:**
- Bug reports and feature requests
- Code contributions and documentation
- Testing and examples

**Requirements:**
- Git, Python 3.11+, Ansible >=11.10, Docker

## Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Ansible-FRP.git
cd Ansible-FRP

# Setup environment with uv
uv sync --extra dev --extra test
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

```bash
# Run all tests
uv run pytest

# Linting and formatting
uv run ruff check .
uv run ruff format --check

# Integration tests
uv run molecule test
```

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
4. Update CHANGELOG.md

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

## Getting Help

- **Questions**: Open GitHub discussion
- **Bugs**: Create detailed issue
- **Chat**: Community channels

Thanks for contributing! 🚀
