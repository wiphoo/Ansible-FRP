# Molecule Testing Scenarios

This document describes the consolidated molecule testing scenarios for the FRP Ansible role.

## 🎯 **Scenario Overview**

We've simplified from 5 scenarios to 3 focused scenarios with clear objectives:

### 1. **`dev` - Development Testing**
- **Purpose**: Fast development iteration with instant feedback
- **Use for**: Feature development, bug fixes, template changes, quick validation
- **Benefits**: Minimal test sequence for speed, complete basic testing
- **Test sequence**: `syntax → create → converge → verify → destroy`
- **Duration**: ~1-2 minutes
- **FRP Version**: 0.63.0 (default)

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
- **FRP Version**: 0.63.0 (default)

```bash
molecule test --scenario-name default
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

> **Note**: Idempotence testing is not applicable to this role as it downloads/installs by design.

## 🚀 **Quick Commands**

```bash
# Fast development testing
molecule test --scenario-name dev

# CI pipeline testing with version validation
molecule test --scenario-name ci

# Complete production-ready testing
molecule test --scenario-name default

# Test all scenarios
for scenario in dev ci default; do
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
