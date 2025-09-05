# 🚀 Ansible Collection - wiphoo.frp

[![Build & Test Collection](https://github.com/wiphoo/Ansible-FRP/actions/workflows/main.yml/badge.svg)](https://github.com/wiphoo/Ansible-FRP/actions/workflows/main.yml)
[![PR Quality & Security](https://github.com/wiphoo/Ansible-FRP/actions/workflows/pr-validation.yml/badge.svg)](https://github.com/wiphoo/Ansible-FRP/actions/workflows/pr-validation.yml)
[![Security Scan](https://github.com/wiphoo/Ansible-FRP/actions/workflows/security.yml/badge.svg)](https://github.com/wiphoo/Ansible-FRP/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/wiphoo/Ansible-FRP/graph/badge.svg?token=3VSLLM8HB1)](https://codecov.io/gh/wiphoo/Ansible-FRP)
[![Ansible Galaxy](https://img.shields.io/ansible/collection/wiphoo.frp)](https://galaxy.ansible.com/ui/repo/published/wiphoo/frp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Effortlessly deploy and manage [Fast Reverse Proxy (FRP)](https://github.com/fatedier/frp) with Ansible**

Transform your network infrastructure with this production-ready Ansible collection that automates FRP deployment, configuration, and management across multiple platforms and architectures.

## ✨ Features

### 🎯 **Production-Ready**
- **Multi-Architecture Support**: Automatic detection and deployment for x86_64, ARM64, ARMv7, ARMv6, RISC-V, and MIPS
- **Cross-Platform**: Tested on Ubuntu, CentOS, Debian, and RHEL-based systems
- **Service Integration**: Native systemd service management with auto-start capabilities
- **Security First**: Configurable firewall rules and secure defaults

### 🔧 **Flexible Configuration**
- **TOML-first**: Modern TOML configuration (INI templates planned)
- **Template-Based**: Jinja2 templates for dynamic configuration generation
- **Role Separation**: Independent server (`frps`) and client (`frpc`) role deployment
- **Version Management**: Pin specific FRP versions or use latest stable releases

### 🛡️ **Enterprise Quality**
- **[![codecov](https://codecov.io/gh/wiphoo/Ansible-FRP/graph/badge.svg?token=3VSLLM8HB1)](https://codecov.io/gh/wiphoo/Ansible-FRP) Test Coverage**: Comprehensive test suite with pytest and Molecule
- **CI/CD Pipeline**: Automated testing, security scanning, and quality gates
- **Documentation**: Complete API docs, examples, and troubleshooting guides
- **Maintenance**: Regular updates and security patches

## 🚀 Quick Start

### Installation

```bash
# Install from Ansible Galaxy
ansible-galaxy collection install wiphoo.frp

# Or install from source
ansible-galaxy collection install git+https://github.com/wiphoo/Ansible-FRP.git
```

### Basic Usage

#### Deploy FRP Server
```yaml
---
- name: Deploy FRP Server
  hosts: frp_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ['frps']
        frp_install_create_service: true
        frp_server_bind_port: 7000
        frp_server_token: "your-secure-token"
```

#### Deploy FRP Client
```yaml
---
- name: Deploy FRP Client
  hosts: frp_clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ['frpc']
        frp_install_create_service: true
        frp_server_addr: "your-server.example.com"
        frp_server_port: 7000
        frp_server_token: "your-secure-token"
```

## 📖 Comprehensive Documentation

### Core Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `frp_install_version` | `0.63.0` | FRP version to install | No |
| `frp_install_files` | `['frps', 'frpc']` | Components to install | No |
| `frp_install_create_service` | `true` | Create systemd services | No |
| `frp_install_user` | `frp` | System user for FRP | No |
| `frp_install_group` | `frp` | System group for FRP | No |
| `frp_install_dir` | `/usr/local/bin/frp` | Installation directory | No |
| `frp_install_config_dir` | `/etc/frp` | Configuration directory | No |
| `frp_install_log_dir` | `/var/log/frp` | Log directory | No |

### Server Configuration

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `frp_server_bind_port` | `7000` | Server listening port | No |
| `frp_server_token` | `""` | Authentication token | Recommended |
| `frp_server_log_level` | `info` | Logging level | No |
| `frp_server_max_clients` | `0` | Maximum client connections (0=unlimited) | No |

### Client Configuration

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `frp_server_addr` | `127.0.0.1` | FRP server address | Yes |
| `frp_server_port` | `7000` | FRP server port | Yes |
| `frp_server_token` | `""` | Authentication token | If server requires |
| `frp_client_log_level` | `info` | Logging level | No |

## 🎯 Advanced Examples

### High-Availability Server Setup
```yaml
---
- name: Deploy HA FRP Servers
  hosts: frp_servers
  become: true
  vars:
    frp_install_version: "0.64.0"
    frp_server_bind_port: 7000
    frp_server_token: "{{ vault_frp_token }}"
    frp_server_max_clients: 100
    frp_server_heartbeat_timeout: 90
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ['frps']
        frp_install_create_service: true
        frp_install_configure_firewall: true
```

### Multi-Service Client Configuration
```yaml
---
- name: Deploy Multi-Service FRP Client
  hosts: web_servers
  become: true
  vars:
    frp_install_version: "0.64.0"
    frp_server_addr: "frp.example.com"
    frp_server_port: 7000
    frp_server_token: "{{ vault_frp_token }}"
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ['frpc']
        frp_install_create_service: true
  tasks:
    - name: Configure HTTP service tunnel
      template:
        src: frpc_http.toml.j2
        dest: /etc/frp/frpc_http.conf
      vars:
        service_name: "web-http"
        local_port: 80
        remote_port: 8080
```

### Docker Environment Integration
```yaml
---
- name: FRP for Docker Services
  hosts: docker_hosts
  become: true
  vars:
    frp_install_files: ['frpc']
    frp_server_addr: "{{ hostvars['frp-server']['ansible_default_ipv4']['address'] }}"
  roles:
    - role: wiphoo.frp.frp_install
  post_tasks:
    - name: Configure container tunnels
      template:
        src: docker-frpc.toml.j2
        dest: /etc/frp/docker-services.conf
```

## 🔧 Customization & Extension

### Custom Templates
Create your own configuration templates:

```yaml
- name: Use custom FRP configuration
  template:
    src: my-custom-frpc.toml.j2
    dest: /etc/frp/frpc.toml
  notify: restart frpc
```

### Multiple Instances
Deploy multiple FRP instances on the same host:

```yaml
- include_role:
    name: wiphoo.frp.frp_install
  vars:
    frp_install_user: "frp-{{ item.name }}"
    frp_install_config_dir: "/etc/frp-{{ item.name }}"
    frp_server_bind_port: "{{ item.port }}"
  loop:
    - { name: "web", port: 7000 }
    - { name: "api", port: 7001 }
```

## 🐛 Troubleshooting

### Common Issues

**Service fails to start**
```bash
# Check service status
sudo systemctl status frps
# Check logs
sudo journalctl -u frps -f
```

**Connection refused**
```bash
# Verify firewall rules
sudo ufw status
# Check if port is listening
netstat -tlnp | grep 7000
```

**Architecture not detected**
```yaml
# Override architecture detection
vars:
  frp_install_architecture: "amd64"
  frp_install_system: "linux"
```

### Debug Mode
Enable verbose logging for troubleshooting:

```yaml
vars:
  frp_server_log_level: "debug"
  frp_client_log_level: "debug"
```

## 🤝 Contributing

We welcome contributions! This project follows industry best practices:

### Development Environment

```bash
# Clone the repository
git clone https://github.com/wiphoo/Ansible-FRP.git
cd Ansible-FRP

# Set up development environment
uv sync --extra dev

# Run pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Testing

```bash
# Run the test suite
uv run pytest tests/ -v --cov=tests --cov-report=term-missing

# Run Molecule tests
cd roles/frp_install
molecule test
```

### Code Quality

- **Pre-commit hooks**: Automatic formatting with Ruff, YAML validation, Ansible-lint
- **Testing**: [![codecov](https://codecov.io/gh/wiphoo/Ansible-FRP/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/wiphoo/Ansible-FRP) test coverage with pytest and Molecule
- **CI/CD**: Comprehensive pipeline with quality gates and security scanning
- **Documentation**: MkDocs with automatic API documentation generation

### Contribution Guidelines

1. **Fork the repository** and create a feature branch
2. **Write tests** for new functionality
3. **Follow code style**: Pre-commit hooks enforce consistency
4. **Update documentation** for user-facing changes
5. **Submit a pull request** with clear description

## 📊 Project Statistics

- 🧪 **[![codecov](https://codecov.io/gh/wiphoo/Ansible-FRP/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/wiphoo/Ansible-FRP) Test Coverage**
- 🏗️ **5 GitHub Actions Workflows**
- 🔒 **11 Pre-commit Quality Hooks**
- 📚 **Comprehensive Documentation**
- 🌟 **Production-Ready Since v1.0.0**

## 🔗 Links & Resources

- **📖 [Full Documentation](https://wiphoo.github.io/Ansible-FRP/)**
- **🐙 [GitHub Repository](https://github.com/wiphoo/Ansible-FRP)**
- **🌌 [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/wiphoo/frp/)**
- **🚀 [FRP Official Project](https://github.com/fatedier/frp)**
- **📋 [Issue Tracker](https://github.com/wiphoo/Ansible-FRP/issues)**
- **💬 [Discussions](https://github.com/wiphoo/Ansible-FRP/discussions)**

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for the Ansible community**

[⭐ Star this project](https://github.com/wiphoo/Ansible-FRP) • [🐛 Report Bug](https://github.com/wiphoo/Ansible-FRP/issues) • [💡 Request Feature](https://github.com/wiphoo/Ansible-FRP/discussions)

</div>
