# 🚀 Ansible Collection - wiphoo.frp

[![Build & Test Collection](https://github.com/wiphoo/Ansible-FRP/actions/workflows/main.yml/badge.svg)](https://github.com/wiphoo/Ansible-FRP/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/wiphoo/Ansible-FRP/graph/badge.svg?token=3VSLLM8HB1)](https://codecov.io/gh/wiphoo/Ansible-FRP)
[![Galaxy Downloads](https://img.shields.io/ansible/collection/d/wiphoo/frp.svg)](https://galaxy.ansible.com/ui/repo/published/wiphoo/frp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Effortlessly deploy and manage [Fast Reverse Proxy (FRP)](https://github.com/fatedier/frp) with Ansible**

Production-ready Ansible collection for automated FRP deployment across multiple platforms and architectures.

## ✨ Features

- **Multi-Architecture**: x86_64, ARM64, ARMv7, RISC-V, MIPS support
- **Cross-Platform**: Ubuntu, CentOS, Debian, RHEL tested
- **Service Integration**: Native systemd with auto-start
- **TOML Configuration**: Modern config with Jinja2 templates
- **Security**: Configurable firewall rules and secure defaults
- **Enterprise Quality**: Comprehensive testing and CI/CD pipeline

## 🚀 Quick Start

**Installation:**
```bash
ansible-galaxy collection install wiphoo.frp
```

**Server Setup:**
```yaml
- hosts: frp_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ['frps']
        frp_install_server_addr: "0.0.0.0"  # Bind to all interfaces
        frp_install_server_port: 7000
        frp_install_auth_token: "your-secure-token"  # CHANGE THIS
        frp_install_configure_firewall: true
```

**Client Setup:**
```yaml
- hosts: frp_clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ['frpc']
        frp_install_client_server_addr: "your-server.example.com"
        frp_install_client_server_port: 7000
        frp_install_auth_token: "your-secure-token"  # Must match server
```

## ✨ Features

- **Full Configuration Control**: Both FRP server and client templates are fully configurable via Ansible variables
- **Secure Defaults**: Security-focused default configurations with clear upgrade paths
- **Flexible Deployment**: Install server only, client only, or both components
- **Service Management**: Automatic systemd service creation and management
- **Template Customization**: Override default TOML templates for advanced use cases
- **Firewall Integration**: Optional automatic firewall rule management
- **Comprehensive Logging**: Configurable logging levels and retention policies

## 📖 Configuration

**Key Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_version` | `0.63.0` | FRP version |
| `frp_install_files` | `['frps', 'frpc']` | Components to install |
| `frp_install_user` | `frp` | System user |
| `frp_install_dir` | `/usr/local/bin/frp` | Installation directory |
| `frp_install_configure_firewall` | `false` | Manage firewall rules |
| `frp_install_auth_method` | `token` | Authentication method |
| `frp_install_auth_token` | `changeme_default_token_123` | Authentication token |
| **Server Configuration** | | |
| `frp_install_server_addr` | `0.0.0.0` | Server bind address (bindAddr) |
| `frp_install_server_port` | `7000` | Server bind port (bindPort) |
| `frp_install_dashboard_addr` | `127.0.0.1` | Dashboard bind address |
| `frp_install_dashboard_port` | `7500` | Dashboard port |
| **Client Configuration** | | |
| `frp_install_client_server_addr` | `your-server-address.example.com` | FRP server address to connect to |
| `frp_install_client_server_port` | `7000` | FRP server port to connect to |
| `frp_install_client_webserver_enabled` | `false` | Enable client admin webServer interface |
| `frp_install_client_webserver_addr` | `127.0.0.1` | Client admin webServer bind address |
| `frp_install_client_webserver_port` | `7400` | Client admin webServer port |
| `frp_install_client_webserver_user` | `admin` | Client admin webServer username |
| `frp_install_client_webserver_password` | `admin` | Client admin webServer password |
| **Logging Configuration** | | |
| `frp_install_log_level` | `info` | Log level (trace, debug, info, warn, error) |
| `frp_install_log_max_days` | `3` | Log file retention days |
| `frp_install_log_disable_print_color` | `false` | Disable log colors |

**Advanced Example:**
```yaml
- hosts: all
  become: true
  vars:
    frp_install_version: "0.64.0"
    frp_install_auth_token: "{{ vault_frp_token }}"
    frp_install_server_addr: "0.0.0.0"  # Bind to all interfaces
    frp_install_server_port: 7000       # Custom server port
    frp_install_log_level: "debug"
    frp_install_log_max_days: 7
    frp_install_dashboard_addr: "0.0.0.0"  # Make dashboard accessible from all interfaces
    frp_install_dashboard_port: 7500
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_configure_firewall: true
        frp_server_max_clients: 100
```

**Client Configuration Example:**
```yaml
- hosts: clients
  become: true
  vars:
    frp_install_files: ['frpc']  # Install only client
    frp_install_client_server_addr: "your-frp-server.example.com"
    frp_install_client_server_port: 7000
    frp_install_client_webserver_enabled: true  # Enable client admin interface
    frp_install_client_webserver_addr: "127.0.0.1"
    frp_install_client_webserver_port: 7400
    frp_install_client_webserver_user: "admin"
    frp_install_client_webserver_password: "{{ vault_frpc_admin_password }}"
    frp_install_auth_token: "{{ vault_frp_token }}"
  roles:
    - role: wiphoo.frp.frp_install
```

## 🐛 Troubleshooting

**Service issues:**
```bash
# Check status and logs
sudo systemctl status frps
sudo journalctl -u frps -f

# Verify firewall and ports
sudo ufw status
netstat -tlnp | grep 7000
```

**Debug mode:**
```yaml
vars:
  frp_install_log_level: "debug"
  frp_install_log_max_days: 7
  frp_install_log_disable_print_color: false
```

## 🤝 Contributing

**Development setup:**
```bash
git clone https://github.com/wiphoo/Ansible-FRP.git
cd Ansible-FRP
uv sync --extra dev --extra test
pre-commit install
```

**Testing:**
```bash
uv run pytest -v --cov
cd roles/frp_install && uv run molecule test --scenario-name dev  # Fast development testing
cd roles/frp_install && uv run molecule test --scenario-name ci   # CI testing
cd roles/frp_install && uv run molecule test --scenario-name default # Full testing
```

**Local build and testing:**
```bash
# Build and install collection locally
ansible-galaxy collection build --force && ansible-galaxy collection install wiphoo-frp-0.1.0.tar.gz --force -p ~/.ansible/collections

# Test installation
ansible-galaxy collection list | grep wiphoo.frp
```

## 📊 Documentation & Links

- **📖 [Complete Documentation](docs/)** - Installation, usage, examples, API reference
- **🌌 [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/wiphoo/frp/)**
- **🐙 [GitHub Repository](https://github.com/wiphoo/Ansible-FRP)**
- **🚀 [FRP Official Project](https://github.com/fatedier/frp)**

**Quick Access:**
- [Guide](docs/guide.md) - Installation, usage, and examples
- [API Reference](docs/api.md)
- [Help](docs/help.md) - Troubleshooting and FAQ
- [Contributing Guide](docs/contributing.md)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for the Ansible community**

[⭐ Star this project](https://github.com/wiphoo/Ansible-FRP) • [🐛 Report Bug](https://github.com/wiphoo/Ansible-FRP/issues) • [💡 Request Feature](https://github.com/wiphoo/Ansible-FRP/discussions)

</div>
