# Molecule Testing Guide for FRP Installation Role

This document provides a comprehensive guide for testing the FRP installation role using Molecule.

## Overview

The FRP installation role includes multiple Molecule scenarios for different testing needs:

- **`default`** - Complete testing with systemd services and idempotence checks
- **`ci`** - CI/CD optimized testing with full systemd support  
- **`quick`** - Fast testing without systemd services (great for development)
- **`version_test`** - Tests version override functionality

## Prerequisites

- Docker installed and running
- Python environment with uv package manager
- Project dependencies installed (`uv sync`)

## Quick Start

### Using the Test Wrapper Script

The easiest way to run tests is using the provided wrapper script:

```bash
# Run default scenario (full test)
./test-molecule.sh

# Run quick scenario (fast, no systemd)
./test-molecule.sh -s quick

# Run CI scenario
./test-molecule.sh -s ci

# Run specific commands
./test-molecule.sh -s quick -c syntax     # Just syntax check
./test-molecule.sh -s default -c converge # Just run the role
```

### Manual Testing

You can also run molecule directly with proper environment variables:

```bash
cd roles/frp_install

# Set up environment
export MOLECULE_COLLECTIONS_PATH="/path/to/project/collections"
export MOLECULE_ROLES_PATH="/path/to/project/roles"

# Run tests
uv run molecule test --scenario-name quick
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
- **Features**: Full testing but streamlined sequence
- **Runtime**: ~2 minutes
- **Use case**: Automated testing in GitHub Actions

### Quick Scenario
- **Purpose**: Fast development testing
- **Container**: Basic Ubuntu 22.04 (no systemd)
- **Features**: Binary installation, basic verification
- **Runtime**: ~30 seconds
- **Use case**: Rapid development feedback

### Version Test Scenario
- **Purpose**: Test version override functionality
- **Container**: Ubuntu 22.04 with systemd
- **Features**: Tests `frp_version` variable override
- **Runtime**: ~2 minutes
- **Use case**: Version-specific feature testing

## Test Structure

### Playbooks
- `playbook.yml` - Standard converge playbook for default/ci
- `playbook_quick.yml` - Fast converge without systemd setup
- `playbook_version_test.yml` - Version testing playbook

### Verification
- `verify.yml` - Comprehensive verification (services, files, versions)
- `verify_quick.yml` - Basic verification (binaries, directories)
- `verify_version_test.yml` - Version-specific verification

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
./test-molecule.sh -s quick -c syntax

# Create and converge only (skip verification)
./test-molecule.sh -s quick -c converge

# Run verification on existing container
./test-molecule.sh -s quick -c verify

# Clean up containers
./test-molecule.sh -s quick -c destroy

# Full test cycle
./test-molecule.sh -s quick -c test
```

## Troubleshooting

### Container Issues
If you encounter container creation issues:

```bash
# Clean up containers
docker container prune -f

# Clean up molecule state
./test-molecule.sh -s <scenario> -c destroy
```

### Permission Issues
If you see temporary directory permission errors:
- Use the `quick` scenario which doesn't require systemd
- Check Docker daemon permissions
- Ensure proper container privileges

### Path Issues
If roles/collections aren't found:
- Verify `MOLECULE_COLLECTIONS_PATH` and `MOLECULE_ROLES_PATH` are set
- Use the wrapper script which handles paths automatically
- Check that you're running from the project root

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Test with Molecule
  run: |
    cd ${{ github.workspace }}
    ./test-molecule.sh -s ci
```

The `ci` scenario is optimized for automated testing environments.

## Development Workflow

1. **Quick Development Loop**:
   ```bash
   ./test-molecule.sh -s quick -c syntax  # Check syntax
   ./test-molecule.sh -s quick -c test    # Quick test
   ```

2. **Full Validation**:
   ```bash
   ./test-molecule.sh -s default          # Complete test
   ./test-molecule.sh -s version_test     # Version override test
   ```

3. **CI Preparation**:
   ```bash
   ./test-molecule.sh -s ci               # CI-optimized test
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
| quick    | ~30 seconds    | Development |
| ci       | ~2 minutes     | CI/CD |
| default  | ~3 minutes     | Full validation |
| version_test | ~2 minutes  | Version testing |

## Best Practices

1. **Use `quick` for development** - Fast feedback loop
2. **Use `ci` for automation** - Balanced testing for CI/CD
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
4. Update the wrapper script help text

## Support

For issues with molecule testing:
1. Check the troubleshooting section above
2. Review molecule logs for detailed error information
3. Test with the `quick` scenario first for faster debugging
4. Ensure Docker is running and accessible
