
# Examples

Practical, real-world examples to get you started quickly.

## Home Lab Example

Deploy an FRP server and a client that exposes SSH:

```yaml
- name: Home lab FRP deployment
	hosts: all
	become: true
	tasks:
		- name: Install server on vps
			include_role:
				name: wiphoo.frp.frp_install
			vars:
				frp_install_files: ["frps"]
				frp_install_configure_firewall: true

		- name: Install client on homelab
			include_role:
				name: wiphoo.frp.frp_install
			vars:
				frp_install_files: ["frpc"]
				frp_server_addr: "203.0.113.10"
				frp_proxies:
					- name: "ssh"
						type: "tcp"
						local_port: 22
						remote_port: 2222
```

## Corporate Example (secure)

Use Vault for tokens and enable TLS:

```yaml
- hosts: corp_servers
	become: true
	vars:
		frp_auth_token: "{{ vault_corporate_token }}"
		frp_transport_tls_enable: true
	roles:
		- role: wiphoo.frp.frp_install
			vars:
				frp_install_files: ["frps"]
				frp_install_dir: "/opt/frp/bin"
				frp_install_verify_checksums: true
```

## Container Integration Example

Run frpc inside a container using the installed binary on the host:

```yaml
- hosts: container_hosts
	become: true
	roles:
		- role: wiphoo.frp.frp_install
			vars:
				frp_install_create_service: false
				frp_install_dir: "/usr/local/bin/frp"
	post_tasks:
		- name: Create Docker Compose
			copy:
				content: |
					version: '3.8'
					services:
						frpc:
							image: alpine:latest
							command: /usr/local/bin/frp/frpc -c /etc/frp/frpc.toml
							volumes:
								- /etc/frp:/etc/frp:ro
							restart: unless-stopped
				dest: /opt/frp/docker-compose.yml
```

For more scenarios, check the repository `examples/` directory and adapt variables to your environment.
