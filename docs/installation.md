# Installation

This page documents practical installation steps for the wiphoo.frp Ansible collection.

## Requirements

- **Ansible Core**: 2.15+ (automatically handled by uv/pip)
- **Python**: 3.11+ for development, 3.8+ for runtime
- **Target Systems**: Linux (Ubuntu 20.04+, Debian 10+, CentOS 8+/RHEL 8+, Fedora 35+)
- **Network Access**: Internet connection to download FRP binaries (or provide local mirror)
- **Privileges**: Root access required (`become: true`) for system installation
- **Dependencies**:
  - `systemd` and `systemd-sysv` for service management (Ubuntu/Debian)
  - `systemd` package for other distributions

## Install the Collection

From Ansible Galaxy (recommended):

```bash
ansible-galaxy collection install wiphoo.frp
```

From the repository (latest source):

```bash
ansible-galaxy collection install git+https://github.com/wiphoo/Ansible-FRP.git
```

Using a requirements file:

```yaml
collections:
  - name: wiphoo.frp
    version: ">=0.1.0"
```

```bash
ansible-galaxy collection install -r requirements.yml
```

## Verify Installation

```bash
ansible-galaxy collection list wiphoo.frp
```

## Quick Start Playbook

Minimal playbook examples to install server and client components.

```yaml
- name: Install FRP Server
  hosts: frp_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        frp_install_configure_firewall: true

- name: Install FRP Client
  hosts: frp_clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_install_client_server_addr: "203.0.113.10"
        frp_install_auth_token: "{{ vault_frp_token }}"
```

## Advanced Installation Notes

- To install to a custom path, set `frp_install_dir` and `frp_install_config_dir`.
- Use `frp_install_verify_checksums: true` to validate downloaded binaries.
- For automated CI installs, pin `frp_install_version` to a tested release.

For usage patterns and examples, see `usage.md` and `guide.md`.
