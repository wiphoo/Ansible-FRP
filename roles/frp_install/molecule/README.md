# Molecule Testing Scenarios

This document describes the consolidated molecule testing scenarios for the FRP Ansible role.

## 🎯 **Scenario Overview**

We have focused molecule testing scenarios with clear objectives:

### 1. **`dev` - Development Testing**
- **Purpose**: Fast development iteration with instant feedback
- **Use for**: Feature development, bug fixes, template changes, quick validation
- **Benefits**: Minimal test sequence for speed, complete basic testing
- **Test sequence**: `syntax → create → converge → verify → destroy`
- **Duration**: ~1-2 minutes
- **FRP Version**: 0.65.0 (default)

```bash
molecule test --scenario-name dev
```

### 2. **`ci` - Continuous Integration & Version Testing**
- **Purpose**: Automated CI/CD testing with version compatibility validation
- **Use for**: GitHub Actions, GitLab CI, version upgrades, automated builds
- **Benefits**: Fast CI execution, version override testing, no idempotence overhead
- **Test sequence**: Full CI sequence without idempotence
- **Duration**: ~2-3 minutes
- **FRP Version**: 0.64.0 (tests version override)

```bash
molecule test --scenario-name ci
```

### 3. **`default` - Complete Production Testing**
- **Purpose**: Comprehensive testing with full verification (no idempotence)
- **Use for**: Release testing, production readiness, comprehensive validation
- **Benefits**: Full test suite with thorough validation, production-ready testing
- **Test sequence**: Complete sequence without idempotence (role downloads by design)
- **Duration**: ~3-5 minutes
- **FRP Version**: 0.65.0 (default)

```bash
molecule test --scenario-name default
```

### 4. **`config-variables` - Configuration Variables Testing**
- **Purpose**: Validate that all configuration variables properly pass through to TOML files
- **Use for**: Testing configuration variable changes, template modifications
- **Benefits**: Comprehensive variable validation, ensures template correctness
- **Test sequence**: Full sequence with variable verification
- **Duration**: ~2-3 minutes
- **FRP Version**: 0.65.0 (default)

```bash
molecule test --scenario-name config-variables
```

### 5. **`variables` - Variables Testing**
- **Purpose**: Validate all configuration variables and enable flags
- **Use for**: Testing feature additions, advanced configuration options
- **Benefits**: Tests all enable flags, optional configurations, and advanced features
- **Test sequence**: Full sequence with comprehensive variable verification
- **Duration**: ~2-3 minutes
- **FRP Version**: 0.65.0 (default)

```bash
molecule test --scenario-name variables
```

## 🔍 **Why No Idempotence Testing?**

This role **downloads and installs** FRP binaries, making it **non-idempotent by design**:
- Always downloads the latest archive from GitHub
- Always extracts and copies binaries
- Always performs cleanup operations

Idempotence testing would fail and doesn't provide meaningful validation for this installation role.

## 📋 **Scenario Comparison**

| Scenario | Speed | Coverage | Idempotence | Version Test | Use Case |
|----------|--------|----------|-------------|---------------|----------|
| `dev`    | ⚡ Fast | Basic    | ❌ N/A      | ❌ No        | Development |
| `ci`     | 🚀 Fast | Full     | ❌ N/A      | ✅ Yes       | CI/CD Pipeline |
| `default`| 🐌 Slow | Full     | ❌ N/A      | ❌ No        | Release Testing |
| `config-variables` | 🚀 Fast | Variables | ❌ N/A | ❌ No | Config Testing |
| `variables` | 🚀 Fast | All Features | ❌ N/A | ❌ No | Full Config Testing |

> **Note**: Idempotence testing is not applicable to this role as it downloads/installs by design.

## 🚀 **Quick Commands**

```bash
# Fast development testing
molecule test --scenario-name dev

# CI pipeline testing with version validation
molecule test --scenario-name ci

# Complete production-ready testing
molecule test --scenario-name default

# Test configuration variables
molecule test --scenario-name config-variables

# Test variables and enable flags
molecule test --scenario-name variables

# Test all scenarios
for scenario in dev ci default config-variables variables; do
  echo "Testing $scenario..."
  molecule test --scenario-name $scenario
done
```

## 🔧 **Key Features**

- **Simplified Docker Setup**: All scenarios use `geerlingguy/docker-ubuntu2204-ansible:latest` with `sleep infinity`
- **No systemd Complexity**: Disabled service creation for container compatibility
- **Version Testing**: CI scenario tests version override functionality (`frp_version: "0.64.0"`)
- **Clear Objectives**: Each scenario has a distinct purpose and use case
- **Fast Execution**: Optimized test sequences for different needs

## 📦 **Removed Scenarios**

The following scenarios were consolidated to reduce complexity:

- **`quick`** → Merged into `dev` (same purpose: fast development testing)
- **`version_test`** → Merged into `ci` (version testing now part of CI validation)

This consolidation provides better clarity while maintaining full testing coverage with less maintenance overhead.
