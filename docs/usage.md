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
        frp_install_client_server_addr: "your-server.example.com"
        frp_install_auth_token: "{{ vault_frp_token }}"
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
        frp_install_dashboard_user: "admin"
        frp_install_dashboard_password: "{{ vault_admin_password }}"
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

## Performance Tuning

### High-Throughput Server
```yaml
- name: High-performance FRP server
  hosts: servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        # Standard server config
        frp_install_dashboard_user: "admin"
        frp_install_dashboard_password: "{{ vault_admin_password }}"
        # Transport optimization for many clients
        frp_install_transport_max_pool_count: 50
        frp_install_transport_tcp_mux: true
        frp_install_transport_tcp_mux_keepalive_interval: 30
```

### Optimized Client
```yaml
- name: Performance-optimized client
  hosts: clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_install_client_server_addr: "your-server.example.com"
        frp_install_auth_token: "{{ vault_frp_token }}"
        # Transport optimization for high throughput
        frp_install_transport_pool_count: 20
        frp_install_transport_tcp_mux: true
        frp_install_transport_tcp_mux_keepalive_interval: 30
```

## Production Tips

- Pin `frp_install_version` for predictable upgrades.
- Use Ansible Vault for secrets (`frp_install_auth_token`, dashboard passwords).
- Configure TLS manually in frp configuration templates for encrypted connections.
- Use `frp_install_configure_firewall: true` to automatically allow required ports.
- Tune transport settings (`frp_install_transport_*`) based on your deployment scale and network conditions.

For templates and full variable list, see `api.md`.
