# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-10-06

### Added
- **Expanded Templates**: Added 100+ configuration variables to TOML templates
  - KCP protocol support
  - QUIC protocol support
  - SSH tunnel gateway configuration
  - OIDC authentication support
  - Virtual host configurations
  - Advanced transport options
  - Enhanced security settings
- **Centralized Test Fixtures**: New pytest configuration with reusable test fixtures (400+ lines)
- **Variable Validation Tests**: Added 27 new tests for variable validation and naming conventions
- **Enhanced Template Tests**: Added 700+ lines of comprehensive template validation tests

### Breaking Changes
- **Minimum Ansible Core raised to 2.17.0** (was 2.15.0). Users on ansible-core 2.15.x or 2.16.x must upgrade before installing this version.
- **`frp_install_create_service` now controls only systemd unit files**. A new `frp_install_create_config` variable (default: `true`) controls TOML config file creation. Previously, setting `frp_install_create_service: false` skipped both config files and systemd units. Now it skips only systemd units; set `frp_install_create_config: false` to also skip config files.

### Changed
- **Updated Default FRP Version**: Changed default version from v0.63.0 to v0.65.0
- **TOML-Only Configuration**: Removed deprecated INI template support, now exclusively using TOML format (FRP v0.52.0+)
- **Optimized Dependencies**: Reduced collection dependencies from 3 to 1 (67% reduction)
  - Removed `ansible.posix` (not used by role)
  - Removed `community.docker` (testing only)
  - Kept only `community.general` for UFW firewall support
- **Optimized Build Artifacts**: Reduced collection size by 92% (1,250 → 98 files, ~850KB → 68KB)
  - Improved build_ignore patterns to exclude development files
  - Removed Python caches, test files, and build artifacts
- **Consistent Molecule Requirements**: Standardized all Molecule scenario dependencies

### Fixed
- **Molecule Requirements**: Fixed missing `community.docker` dependency in `variables` scenario
- **Version Constraints**: Corrected `community.docker` version constraint in `dev` scenario

### Removed
- **INI Templates**: Removed `frpc.ini.j2` and `frps.ini.j2` templates (use TOML format only)

## [0.1.0] - 2025-09-11

### Added
- **Initial Release**: First version of wiphoo.frp Ansible collection for FRP (Fast Reverse Proxy) deployment
- **Multi-Architecture Support**: Automatic detection and support for Linux systems (x86_64, aarch64, armv7l, armv6l, riscv64, mips)
- **Dual Component Installation**: Support for both FRP server (frps) and client (frpc) configurations
- **Full Template Configurability**: Made both server (frps.toml.j2) and client (frpc.toml.j2) templates fully configurable via Ansible variables
- **Comprehensive Configuration Variables**:
  - Authentication: `frp_install_auth_method` and `frp_install_auth_token` for secure connections
  - Server configuration: `frp_install_server_addr`, `frp_install_server_port` for binding
  - Dashboard: `frp_install_dashboard_*` variables for web management interface
  - Client connection: `frp_install_client_server_addr`, `frp_install_client_server_port` for server connection
  - Client webserver: `frp_install_client_webserver_*` variables with conditional rendering
  - Logging: `frp_install_log_level`, `frp_install_log_max_days`, `frp_install_log_disable_print_color`
- **Service Management**: Native systemd integration with automatic service creation and management
- **Template-Based Configuration**: Modern TOML configuration format with Jinja2 templates
- **Security Features**: Configurable firewall rules, secure defaults, and production-ready configurations
- **Comprehensive Testing**:
  - pytest unit tests with 94.62% test coverage
  - molecule integration testing with multiple scenarios (dev, ci, default, resources)
  - Invalid configuration validation tests
  - GitHub Actions CI/CD pipeline with quality gates and security scanning
- **Development Tooling**:
  - Pre-commit hooks for code quality and consistency
  - Modern Python tooling integration (uv, ruff, mypy, ansible-lint)
  - Automated documentation with MkDocs and GitHub Pages deployment
- **Documentation**: Complete documentation suite including API reference, installation guide, examples, and troubleshooting

### Features
- **Variable Naming Consistency**: Standardized all configuration variables to use `frp_install_*` prefix
- **Conditional Configuration**: Smart template rendering based on enabled features (e.g., client webserver)
- **Cross-Platform Compatibility**: Tested on Ubuntu 20.04+, Debian 11+, CentOS/RHEL 8+, Fedora 36+
- **FRP Version Support**: Compatible with FRP versions 0.61.x - 0.63.x
- **Flexible Deployment**: Install server only, client only, or both components on same system
- Pre-commit hooks for code quality and consistency
- Modern Python tooling integration (uv, ruff, mypy, ansible-lint)
- Documentation with MkDocs and GitHub Pages deployment
- Security scanning with TruffleHog and GitGuardian
- Automated dependency management and updates

### Features
- Multi-architecture binary support with automatic detection
- TOML configuration templates for modern FRP versions (v0.52.0+)
- Systemd service file templates for both server and client
- Configurable installation paths, user/group settings, and permissions
- Version-specific binary downloads with SHA256 checksum verification
- Architecture variable protection to prevent user override conflicts
- FRP configuration key fixes (localAddr→localIP) for modern FRP versions
- Collection-compatible template references (no role_path dependencies)
- Firewall configuration support with UFW integration
- Comprehensive error handling and retry mechanisms

### Infrastructure
- Complete CI/CD pipeline with 3 focused workflows (main, pr-validation, docs)
- Python 3.10-3.12 compatibility testing
- Ansible 8.7.0 and 11.9.0 support with version-specific compatibility matrix
- 53 comprehensive tests covering role functionality, templates, and integration
- Pre-commit hooks: trailing-whitespace, yaml-check, ruff, ruff-format, yamllint, ansible-lint, mypy
- Automated documentation building and deployment
- Code coverage reporting with Codecov integration
- Security scanning and PR validation workflows
- Performance optimized with uv package manager

### Configuration Management
- Centralized configuration in pyproject.toml following PEP 518 standards
- Development and test dependency separation
- Modern GitHub Actions with astral-sh/setup-uv@v6
- Template parameterization and collection-compatible structure
- Variable precedence management with conditional gates

### Bug Fixes
- Fixed FRP template parameter references for collection compatibility
- Corrected invalid FRP configuration keys (localAddr→localIP)
- Resolved CI dependency installation issues with ansible-lint
- Fixed uv command syntax for modern uv workflows
- Resolved Python/Ansible version compatibility matrix
- Fixed test-reporter permissions for PR status checks
- Applied comprehensive ruff formatting for code consistency

### Technical Debt
- Workflow optimization: reduced from 2,600+ lines to manageable structure
- Configuration consolidation from scattered files to pyproject.toml
- Template modernization with proper Jinja2 syntax and collection compatibility
- Test strengthening with comprehensive coverage and integration testing
- Security improvements with official GitHub Actions and dependency management

[Unreleased]: https://github.com/wiphoo/Ansible-FRP/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/wiphoo/Ansible-FRP/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/wiphoo/Ansible-FRP/releases/tag/v0.1.0
