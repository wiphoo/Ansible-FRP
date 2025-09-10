# Installation

This page documents practical installation steps for the wiphoo.frp Ansible collection.

## Requirements

- Ansible Core 2.12+ (or newer)
- Python 3.6+
- Linux target hosts (Ubuntu, Debian, CentOS/RHEL, Fedora)
- Internet access to download FRP binaries (or provide a local mirror)
- `become: true` for tasks that install system files or manage services

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
				frp_server_addr: "203.0.113.10"
				frp_proxies:
					- name: "ssh"
						type: "tcp"
						local_port: 22
						remote_port: 2222
```

## Advanced Installation Notes

- To install to a custom path, set `frp_install_dir` and `frp_install_config_dir`.
- Use `frp_install_verify_checksums: true` to validate downloaded binaries.
- For automated CI installs, pin `frp_install_version` to a tested release.

For usage patterns and examples, see `usage.md` and `guide.md`.
