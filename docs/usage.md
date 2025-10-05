# Usage

This page shows practical usage patterns for the `wiphoo.frp` collection. Use these examples as starting points and adapt variables to your environment.

## Configuration Format

**Important**: This collection uses **TOML configuration format only** (FRP v0.52.0+). INI format has been deprecated and removed as of v0.1.0.

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

- **Pin versions**: Use `frp_install_version: "0.65.0"` for predictable upgrades
- **Secure secrets**: Use Ansible Vault for `frp_install_auth_token` and dashboard passwords
- **Configuration format**: TOML only (FRP v0.52.0+), INI format deprecated
- **TLS encryption**: Configure TLS manually in frp configuration templates for encrypted connections
- **Firewall**: Use `frp_install_configure_firewall: true` to automatically allow required ports
- **Performance**: Tune transport settings (`frp_install_transport_*`) based on deployment scale and network conditions
- **Testing**: Run `uv run pytest tests/` (126 tests, 96.85% coverage) or molecule scenarios before production

For templates and full variable list, see `api.md`.
