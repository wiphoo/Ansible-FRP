# Molecule Testing Guide for FRP Installation Role

This document provides a comprehensive guide for testing the FRP installation role using Molecule.

## Ov1. **Quick Development Loop**:
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
   ```installation role includes three Molecule scenarios for different testing needs:

- **`default`** - Complete testing with systemd services and idempotence checks
- **`ci`** - CI/CD optimized testing with full systemd support and version override functionality  
- **`dev`** - Fast development testing without systemd services (great for rapid iteration)

## Prerequisites

- Docker installed and running
- Python 3.11+ environment with uv package manager
- Project dependencies installed: `uv sync --extra dev`

## Quick Start

### Using Direct Molecule Commands

The recommended way to run tests is using molecule directly:

```bash
# Run default scenario (full test)
cd roles/frp_install && uv run molecule test --scenario-name default

# Run dev scenario (fast, no systemd)
cd roles/frp_install && uv run molecule test --scenario-name dev

# Run CI scenario
cd roles/frp_install && uv run molecule test --scenario-name ci

# Run specific commands
cd roles/frp_install && uv run molecule syntax --scenario-name dev     # Just syntax check
cd roles/frp_install && uv run molecule converge --scenario-name default # Just run the role
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

### Default Scenario
- **Purpose**: Complete role testing with all features
- **Container**: Ubuntu 22.04 with systemd
- **Features**: Full systemd service testing, idempotence checks
- **Runtime**: ~2-3 minutes
- **Use case**: Final validation before release

### CI Scenario  
- **Purpose**: Optimized for CI/CD pipelines
- **Container**: Ubuntu 22.04 with systemd
- **Features**: Full testing with version override functionality, streamlined sequence
- **Runtime**: ~2 minutes
- **Use case**: Automated testing in GitHub Actions

### Dev Scenario
- **Purpose**: Fast development testing
- **Container**: Basic Ubuntu 22.04 (no systemd)
- **Features**: Binary installation, basic verification
- **Runtime**: ~30 seconds
- **Use case**: Rapid development feedback

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
  run: |
    cd ${{ github.workspace }}/roles/frp_install
    uv run molecule test --scenario-name ci
```

The `ci` scenario is optimized for automated testing environments.

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
- ✅ Idempotence testing (default scenario)
- ✅ Binary installation verification
- ✅ File and directory creation
- ✅ User and group creation
- ✅ Version verification
- ✅ Service file creation (systemd scenarios)
- ✅ Executable permissions
- ✅ Configuration file templating

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
      frp_install_version: "0.63.0"
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
