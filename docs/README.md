# 🌟 Welcome to Ansible Collection - wiphoo.frp

[![Build & Test Collection](https://github.com/wiphoo/Ansible-FRP/actions/workflows/main.yml/badge.svg)](https://github.com/wiphoo/Ansible-FRP/actions/workflows/main.yml)
[![PR Quality & Security](https://github.com/wiphoo/Ansible-FRP/actions/workflows/pr-validation.yml/badge.svg)](https://github.com/wiphoo/Ansible-FRP/actions/workflows/pr-validation.yml)
[![Security Scan](https://github.com/wiphoo/Ansible-FRP/actions/workflows/security.yml/badge.svg)](https://github.com/wiphoo/Ansible-FRP/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/wiphoo/Ansible-FRP/graph/badge.svg?token=3VSLLM8HB1)](https://codecov.io/gh/wiphoo/Ansible-FRP)
[![Ansible Galaxy](https://img.shields.io/ansible/collection/wiphoo.frp)](https://galaxy.ansible.com/ui/repo/published/wiphoo/frp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Hello there! 👋 Welcome to your gateway for effortless [Fast Reverse Proxy (FRP)](https://github.com/fatedier/frp) automation with Ansible**

We're thrilled you're here! This collection was crafted with love to make your network infrastructure deployment as smooth as silk. Whether you're a seasoned DevOps professional or just starting your automation journey, we've got everything you need to transform complex FRP deployments into simple, repeatable playbooks.

🎉 **What makes this special?** This isn't just another Ansible collection—it's your trusted companion for production-ready FRP automation, built by the community, for the community.

## 🤗 Why You'll Love This Collection

**For the Busy Professional**: Skip the manual setup headaches. Get FRP running in minutes, not hours.

**For the Security-Conscious**: Sleep well knowing your deployments follow security best practices out of the box.

**For the Scale-Minded**: Whether it's one server or a hundred, this collection grows with your infrastructure.

**For the Community**: Open source, well-documented, and continuously improved by awesome contributors like you!

## ✨ Features

### 🎯 **Production-Ready**
- **Multi-Architecture Support**: Automatic detection and deployment for x86_64, ARM64, ARMv7, ARMv6, RISC-V, and MIPS
- **Cross-Platform**: Tested on Ubuntu, CentOS, Debian, and RHEL-based systems
- **Service Integration**: Native systemd service management with auto-start capabilities
- **Security First**: Configurable firewall rules and secure defaults

### 🔧 **Flexible Configuration**
- **TOML & INI Support**: Both modern TOML and legacy INI configuration formats
- **Template-Based**: Jinja2 templates for dynamic configuration generation
- **Component Selection**: Deploy server (`frps`), client (`frpc`), or both
- **Version Management**: Pin specific FRP versions or use latest stable releases

### 🛡️ **Enterprise Quality**
- **Comprehensive Testing**: Full test coverage with pytest and Molecule
- **CI/CD Pipeline**: Automated testing, security scanning, and quality gates
- **Complete Documentation**: API docs, examples, and troubleshooting guides
- **Active Maintenance**: Regular updates and security patches

## 🚀 Quick Start

Ready to get started? Here's how easy it is:

### 1. Install the Collection

```bash
# From Ansible Galaxy (recommended)
ansible-galaxy collection install wiphoo.frp

# From source (for the latest features)
ansible-galaxy collection install git+https://github.com/wiphoo/Ansible-FRP.git
```

### 2. Basic Server Setup

```yaml
---
- name: Deploy FRP Server
  hosts: servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        frps_dashboard_user: "admin"
        frps_dashboard_password: "{{ vault_admin_password }}"
```

### 3. Basic Client Setup

```yaml
---
- name: Deploy FRP Client
  hosts: clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_server_addr: "your-server.com"
        frp_auth_token: "{{ vault_frp_token }}"
        frp_proxies:
          - name: "ssh"
            type: "tcp"
            local_port: 22
            remote_port: 2222
```

## 📚 Documentation Navigation

- **[Guide](guide.md)** - Installation, usage, and examples
- **[Role Documentation](roles/frp_install.md)** - Detailed role reference
- **[API Reference](api.md)** - Complete variable documentation
- **[Help](help.md)** - Troubleshooting and FAQ
- **[Security Guide](SECURITY.md)** - Security best practices
- **[Contributing](contributing.md)** - How to contribute to the project

## 🎯 What's Next?

1. **New to FRP?** Start with our [Guide](guide.md)
2. **Need Examples?** Check out our [Guide](guide.md) page
3. **Advanced Setup?** Dive into the [API Reference](api.md)
4. **Having Issues?** Visit our [Help](help.md) guide

---

**Happy automating!** 🎉 If you find this collection helpful, please consider starring the repository and sharing it with your team!
