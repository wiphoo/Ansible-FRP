# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-05

### Added
- Initial release of wiphoo.frp Ansible collection
- FRP (Fast Reverse Proxy) installation and configuration role
- Support for both FRP server (frps) and client (frpc) configurations
- Automatic architecture detection for Linux systems
- Template-based configuration management for INI and TOML formats
- Service management with systemd integration
- Comprehensive test suite with pytest and molecule
- GitHub Actions CI/CD pipeline with quality gates
- Pre-commit hooks for code quality and consistency

### Features
- Multi-architecture support (x86_64, aarch64, armv7l, etc.)
- Flexible configuration templates for frps.ini, frpc.ini, frps.toml, frpc.toml
- Systemd service file templates for both server and client
- Configurable installation paths and user/group settings
- Version-specific binary downloads with checksum verification
- Integration with modern Python tooling (uv, ruff, mypy)

[1.0.0]: https://github.com/wiphoo/Ansible-FRP/releases/tag/v1.0.0
