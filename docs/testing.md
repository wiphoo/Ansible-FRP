# Molecule Testing

The FRP installation role includes **5 Molecule scenarios** for comprehensive testing needs:

- **`dev`** - Fast development testing (1-2 min) - Quick iteration with instant feedback
- **`ci`** - CI/CD optimized testing (2-3 min) - Automated testing with version override
- **`default`** - Production testing (3-5 min) - Complete validation for releases
- **`config-variables`** - Configuration validation (2-3 min) - Template variable testing
- **`variables`** - Full variable testing (2-3 min) - Comprehensive variable validation

> **Important**: This role is designed to download and install external binaries, making it non-idempotent by nature. Therefore, idempotence testing has been intentionally removed from all scenarios.

This document provides a comprehensive guide for testing the FRP installation role using Molecule.

## Quick Reference

### 1. **Quick Development Loop**:
   ```bash
   cd roles/frp_install && molecule syntax --scenario-name dev  # Check syntax
   cd roles/frp_install && molecule test --scenario-name dev    # Quick test (1-2 min)
   ```

### 2. **Full Validation**:
   ```bash
   cd roles/frp_install && molecule test --scenario-name default # Complete test (3-5 min)
   cd roles/frp_install && molecule test --scenario-name ci      # Version override test (2-3 min)
   ```

### 3. **Configuration Testing**:
   ```bash
   cd roles/frp_install && molecule test --scenario-name config-variables # Template validation (2-3 min)
   cd roles/frp_install && molecule test --scenario-name variables        # Full variable test (2-3 min)
   ```

## Prerequisites

- Docker installed and running
- Python 3.11+ environment with uv package manager
- Project dependencies installed: `uv sync --extra dev`

## Quick Start

### Using uv run (Recommended)

The recommended way to run tests is using `uv run` to ensure proper environment isolation:

```bash
# Run default scenario (full production test - 3-5 min)
cd roles/frp_install && uv run molecule test --scenario-name default

# Run dev scenario (fast development - 1-2 min)
cd roles/frp_install && uv run molecule test --scenario-name dev

# Run CI scenario (2-3 min)
cd roles/frp_install && uv run molecule test --scenario-name ci

# Run configuration variable testing (2-3 min)
cd roles/frp_install && uv run molecule test --scenario-name config-variables

# Run full variable testing (2-3 min)
cd roles/frp_install && uv run molecule test --scenario-name variables

# Run specific commands
cd roles/frp_install && uv run molecule syntax --scenario-name dev     # Just syntax check
cd roles/frp_install && uv run molecule converge --scenario-name default # Just run the role
cd roles/frp_install && uv run molecule verify --scenario-name default   # Just run verification
cd roles/frp_install && uv run molecule destroy --scenario-name default  # Clean up resources
```

### Manual Testing

You can also run molecule directly with proper environment variables:

```bash
cd roles/frp_install

# Set up environment
export MOLECULE_COLLECTIONS_PATH="/path/to/project/collections"
export MOLECULE_ROLES_PATH="/path/to/project/roles"

# Run tests
uv run molecule test --scenario-name dev
```

## Test Scenarios Explained

### 1. dev - Development Testing
- **Purpose**: Fast iteration with instant feedback during development
- **Container**: Ubuntu 22.04 with systemd
- **Features**: Binary installation and basic verification
- **Runtime**: ~1-2 minutes
- **FRP Version**: 0.65.0 (default)
- **Use case**: Feature development, bug fixes, template changes, quick validation

### 2. ci - Continuous Integration Testing
- **Purpose**: Optimized for CI/CD pipelines with version testing
- **Container**: Ubuntu 22.04 with systemd
- **Features**: Full testing with version override functionality (tests v0.64.0)
- **Runtime**: ~2-3 minutes
- **FRP Version**: 0.64.0 (tests version override)
- **Use case**: GitHub Actions, GitLab CI, automated builds, version upgrades

### 3. default - Production Testing
- **Purpose**: Complete production-ready testing with all features
- **Container**: Ubuntu 22.04 with systemd
- **Features**: Full systemd service testing, comprehensive validation
- **Runtime**: ~3-5 minutes
- **FRP Version**: 0.65.0 (default)
- **Use case**: Final validation before release, production readiness verification

### 4. config-variables - Configuration Variable Testing
- **Purpose**: Validate variable pass-through to TOML configuration files
- **Container**: Ubuntu 22.04 with systemd
- **Features**: Template variable verification, configuration validation
- **Runtime**: ~2-3 minutes
- **FRP Version**: 0.65.0 (default)
- **Use case**: Configuration changes, template modifications, variable updates

### 5. variables - Full Variable Testing
- **Purpose**: Comprehensive testing of all variables and enable flags
- **Container**: Ubuntu 22.04 with systemd
- **Features**: Complete variable validation, all configuration options
- **Runtime**: ~2-3 minutes
- **FRP Version**: 0.65.0 (default)
- **Use case**: Feature additions, advanced configurations, variable validation

> **Note**: Idempotence testing has been removed from all scenarios because this role downloads external binaries and is inherently non-idempotent by design.

## Test Structure

### Playbooks
- `playbook.yml` - Standard converge playbook for default scenario
- `playbook_version_test.yml` - Version testing playbook for ci scenario

### Verification
- `verify.yml` - Comprehensive verification (services, files, versions) for default
- `verify_version_test.yml` - Version-specific verification for ci scenario

## Environment Configuration

The molecule configurations use environment variables for portable paths:

```yaml
collections_path: "$MOLECULE_COLLECTIONS_PATH"
roles_path: "$MOLECULE_ROLES_PATH"
```

These are automatically set by the wrapper script or can be set manually.

## Common Commands

```bash
# Syntax check only
cd roles/frp_install && uv run molecule syntax --scenario-name dev

# Create and converge only (skip verification)
cd roles/frp_install && uv run molecule converge --scenario-name dev

# Run verification on existing container
cd roles/frp_install && uv run molecule verify --scenario-name dev

# Clean up containers
cd roles/frp_install && uv run molecule destroy --scenario-name dev

# Full test cycle
cd roles/frp_install && uv run molecule test --scenario-name dev
```

## Troubleshooting

### Container Issues
If you encounter container creation issues:

```bash
# Clean up containers
docker container prune -f

# Clean up molecule state
cd roles/frp_install && uv run molecule destroy --scenario-name <scenario>
```

### Permission Issues
If you see temporary directory permission errors:
- Use the `dev` scenario which doesn't require systemd
- Check Docker daemon permissions
- Ensure proper container privileges

### Path Issues
If roles/collections aren't found:
- Verify `MOLECULE_COLLECTIONS_PATH` and `MOLECULE_ROLES_PATH` are set
- Run commands from the roles/frp_install directory
- Check that you're running from the project root

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Test with Molecule
  working-directory: roles/frp_install
  run: |
    uv run molecule test --scenario-name ci
  env:
    ANSIBLE_COLLECTIONS_PATH: ${{ github.workspace }}/collections
```

The `ci` scenario is optimized for automated testing environments. Note the use of `working-directory` and absolute path for collections to ensure proper path resolution in CI/CD pipelines.

## Development Workflow

1. **Quick Development Loop**:
   ```bash
   cd roles/frp_install && uv run molecule syntax --scenario-name dev  # Check syntax
   cd roles/frp_install && uv run molecule test --scenario-name dev    # Quick test
   ```

2. **Full Validation**:
   ```bash
   cd roles/frp_install && uv run molecule test --scenario-name default # Complete test
   cd roles/frp_install && uv run molecule test --scenario-name ci      # Version override test
   ```

3. **CI Preparation**:
   ```bash
   cd roles/frp_install && uv run molecule test --scenario-name ci      # CI-optimized test
   ```

## Test Coverage

The molecule tests cover:

- ✅ Ansible syntax validation
- ✅ Role execution (converge)
- ✅ Binary installation verification
- ✅ File and directory creation
- ✅ User and group creation
- ✅ Version verification
- ✅ Service file creation (systemd scenarios)
- ✅ Executable permissions
- ✅ Configuration file templating

> **Note**: Idempotence testing is intentionally excluded as this role downloads external binaries and creates new resources by design, making it non-idempotent.

## Performance

| Scenario | Typical Runtime | Use Case |
|----------|----------------|----------|
| dev      | ~30 seconds    | Development |
| ci       | ~2 minutes     | CI/CD & Version testing |
| default  | ~3 minutes     | Full validation |

## Best Practices

1. **Use `dev` for development** - Fast feedback loop
2. **Use `ci` for automation** - Balanced testing for CI/CD with version override
3. **Use `default` for releases** - Comprehensive validation
4. **Clean up between tests** - Use destroy to avoid conflicts
5. **Check syntax first** - Quick validation before longer tests

## Configuration Customization

You can customize test variables in each scenario's molecule.yml:

```yaml
inventory:
  group_vars:
    all:
      frp_install_version: "0.65.0"
      frp_install_user: "custom_user"
      # ... other variables
```

## Extending Tests

To add new scenarios:

1. Create new directory: `molecule/my_scenario/`
2. Add `molecule.yml` configuration
3. Create corresponding playbooks in `resources/`
4. Test with `uv run molecule test --scenario-name my_scenario`

## Support

For issues with molecule testing:
1. Check the troubleshooting section above
2. Review molecule logs for detailed error information
3. Test with the `dev` scenario first for faster debugging
4. Ensure Docker is running and accessible
