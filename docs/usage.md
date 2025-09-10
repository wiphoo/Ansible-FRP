# Usage

This page shows practical usage patterns for the `wiphoo.frp` collection. Use these examples as starting points and adapt variables to your environment.

## Basic Client

```yaml
- name: Deploy FRP Client
	hosts: clients
	become: true
	roles:
		- role: wiphoo.frp.frp_install
			vars:
				frp_install_files: ["frpc"]
				frp_server_addr: "your-server.example.com"
				frp_auth_token: "{{ vault_frp_token }}"
				frp_proxies:
					- name: "ssh"
						type: "tcp"
						local_port: 22
						remote_port: 2222
```

## Basic Server

```yaml
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

## Both Components

```yaml
- name: Hybrid node
	hosts: hybrid
	become: true
	roles:
		- role: wiphoo.frp.frp_install
			vars:
				frp_install_files: ["frps", "frpc"]
```

## Production Tips

- Pin `frp_install_version` for predictable upgrades.
- Use Ansible Vault for secrets (`frp_auth_token`, dashboard passwords).
- Enable `frp_transport_tls_enable: true` and provide TLS certs for encrypted connections.
- Use `frp_install_configure_firewall: true` to automatically allow required ports.

For templates and full variable list, see `api.md`.
