# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-09-06

### Added
- Initial release of wiphoo.frp Ansible collection
- FRP (Fast Reverse Proxy) installation and configuration role
- Support for both FRP server (frps) and client (frpc) configurations
- Automatic architecture detection for Linux systems (x86_64, aarch64, armv7l, armv6l, riscv64, mips)
- Template-based configuration management for INI and TOML formats
- Service management with systemd integration
- Comprehensive test suite with pytest, molecule, and 94.62% test coverage
- GitHub Actions CI/CD pipeline with quality gates and security scanning
- Pre-commit hooks for code quality and consistency
- Modern Python tooling integration (uv, ruff, mypy, ansible-lint)
- Documentation with MkDocs and GitHub Pages deployment
- Security scanning with TruffleHog and GitGuardian
- Automated dependency management and updates

### Features
- Multi-architecture binary support with automatic detection
- Flexible configuration templates (frps.ini/toml, frpc.ini/toml)
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

[Unreleased]: https://github.com/wiphoo/Ansible-FRP/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/wiphoo/Ansible-FRP/releases/tag/v1.0.0
