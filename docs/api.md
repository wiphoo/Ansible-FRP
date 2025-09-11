# API Reference

Complete variable reference for the wiphoo.frp collection.

## Core Installation Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_version` | `"0.63.0"` | FRP version |
| `frp_install_files` | `["frps", "frpc"]` | Components to install |
| `frp_install_user` | `"frp"` | System user |
| `frp_install_group` | `"frp"` | System group |
| `frp_install_dir` | `"/usr/local/bin/frp"` | Installation directory |
| `frp_install_create_service` | `true` | Create systemd services |
| `frp_install_configure_firewall` | `true` | Auto firewall configuration |

## Authentication Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_auth_method` | `"token"` | Authentication method |
| `frp_install_auth_token` | `""` | REQUIRED. Authentication token (set via vars or Vault). |

## Server Configuration Variables

Configure FRP server binding and dashboard settings.

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_server_addr` | `"0.0.0.0"` | Server bind address (bindAddr) |
| `frp_install_server_port` | `7000` | Server bind port (bindPort) |
| `frp_install_dashboard_addr` | `"127.0.0.1"` | Dashboard web interface bind address |
| `frp_install_dashboard_port` | `7500` | Dashboard web interface port |
| `frp_install_dashboard_user` | `"admin"` | Dashboard username |
| `frp_install_dashboard_password` | `""` | REQUIRED. Set a strong password (store in Vault). |

## Client Configuration Variables

Configure FRP client connection and admin interface.

### Server Connection Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_client_server_addr` | `"your-server-address.example.com"` | FRP server address to connect to |
| `frp_install_client_server_port` | `7000` | FRP server port to connect to |

### Client Admin WebServer Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_client_webserver_enabled` | `false` | Enable client admin webServer interface |
| `frp_install_client_webserver_addr` | `"127.0.0.1"` | Client admin webServer bind address |
| `frp_install_client_webserver_port` | `7400` | Client admin webServer port |
| `frp_install_client_webserver_user` | `"admin"` | Client admin webServer username |
| `frp_install_client_webserver_password` | `"admin"` | Client admin webServer password (CHANGE IN PRODUCTION) |
| `frp_install_client_webserver_pprof_enabled` | `false` | Enable pprof endpoint for debugging |

## Logging Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_log_level` | `"info"` | Log level (trace, debug, info, warn, error) |
| `frp_install_log_max_days` | `3` | Log file retention days |
| `frp_install_log_disable_print_color` | `false` | Disable colored log output |

## Transport Configuration Variables

Configure FRP transport layer settings for performance optimization.

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_pool_count` | `5` | Client connection pool size - increase for high throughput |
| `frp_install_transport_max_pool_count` | `5` | Server maximum connection pool size - increase for many clients |
| `frp_install_transport_tcp_mux` | `true` | Enable TCP multiplexing for better performance |
| `frp_install_transport_tcp_mux_keepalive_interval` | `60` | TCP mux keepalive interval in seconds |

### Transport Performance Tuning

**High-throughput scenarios** (many simultaneous connections):
```yaml
frp_install_transport_pool_count: 20           # Increase client pool size
frp_install_transport_max_pool_count: 50       # Increase server pool size
frp_install_transport_tcp_mux: true            # Keep multiplexing enabled
frp_install_transport_tcp_mux_keepalive_interval: 30  # More frequent keepalives
```

**Low-resource environments** (minimal resource usage):
```yaml
frp_install_transport_pool_count: 2            # Reduce pool size
frp_install_transport_max_pool_count: 5        # Conservative server limit
frp_install_transport_tcp_mux: true            # Keep for efficiency
frp_install_transport_tcp_mux_keepalive_interval: 120  # Less frequent keepalives
```

**Network with high latency** (satellite/mobile connections):
```yaml
frp_install_transport_pool_count: 10           # More connections to overcome latency
frp_install_transport_tcp_mux: false           # Disable if causing issues
frp_install_transport_tcp_mux_keepalive_interval: 180  # Longer intervals
```

## Advanced Configuration Examples

### Server Configuration Example
```yaml
- hosts: servers
  become: true
  vars:
    # Core installation
    frp_install_files: ['frps']
    frp_install_version: "0.63.0"

    # Authentication (use vault in production)
    frp_install_auth_token: "{{ vault_frp_token }}"

    # Server binding
    frp_install_server_addr: "0.0.0.0"  # Bind to all interfaces
    frp_install_server_port: 7000

    # Dashboard configuration
    frp_install_dashboard_addr: "0.0.0.0"  # Make accessible from network
    frp_install_dashboard_port: 7500
    frp_install_dashboard_user: "admin"
    frp_install_dashboard_password: "{{ vault_dashboard_password }}"

    # Logging
    frp_install_log_level: "info"
    frp_install_log_max_days: 7
  roles:
    - role: wiphoo.frp.frp_install
```

### Client Configuration Example
```yaml
- hosts: clients
  become: true
  vars:
    # Core installation - client only
    frp_install_files: ['frpc']

    # Server connection
    frp_install_client_server_addr: "your-frp-server.example.com"
    frp_install_client_server_port: 7000

    # Authentication (must match server)
    frp_install_auth_token: "{{ vault_frp_token }}"

    # Client admin interface (optional)
    frp_install_client_webserver_enabled: true
    frp_install_client_webserver_addr: "127.0.0.1"
    frp_install_client_webserver_port: 7400
    frp_install_client_webserver_user: "admin"
    frp_install_client_webserver_password: "{{ vault_client_admin_password }}"

    # Logging
    frp_install_log_level: "info"
  roles:
    - role: wiphoo.frp.frp_install
```

### Combined Server + Client Example
```yaml
- hosts: all
  become: true
  vars:
    # Install both components
    frp_install_files: ['frps', 'frpc']
    frp_install_version: "0.63.0"

    # Authentication
    frp_install_auth_token: "{{ vault_frp_token }}"

    # Server configuration
    frp_install_server_addr: "0.0.0.0"
    frp_install_server_port: 7000
    frp_install_dashboard_addr: "127.0.0.1"
    frp_install_dashboard_port: 7500

    # Client configuration
    frp_install_client_server_addr: "localhost"  # Connect to local server
    frp_install_client_server_port: 7000
    frp_install_client_webserver_enabled: true
    frp_install_client_webserver_port: 7400

    # Security
    frp_install_configure_firewall: true

    # Logging
    frp_install_log_level: "debug"
    frp_install_log_max_days: 14
  roles:
    - role: wiphoo.frp.frp_install
```

## Configuration Files Generated

The role generates TOML configuration files:

- **Server**: `/etc/frp/frps.toml` - FRP server configuration
- **Client**: `/etc/frp/frpc.toml` - FRP client configuration

Both templates are fully configurable via the variables listed above. The templates include:

- Comprehensive commenting for all options
- Example proxy configurations (commented out)
- Security best practices and warnings
- Conditional sections based on variable settings

## Template Customization

You can override the default templates by placing custom templates in your playbook:

```
playbooks/
  templates/
    frps.toml.j2    # Custom server template
    frpc.toml.j2    # Custom client template
```

## Service Management

When `frp_install_create_service: true` (default), systemd services are created:

- `frps.service` - FRP server service
- `frpc.service` - FRP client service

Services can be managed with standard systemd commands:

```bash
# Server management
sudo systemctl start frps
sudo systemctl enable frps
sudo systemctl status frps

# Client management
sudo systemctl start frpc
sudo systemctl enable frpc
sudo systemctl status frpc
```

## Security Recommendations

1. **Change default tokens**: Always use secure, unique `frp_install_auth_token`
2. **Use Ansible Vault**: Store sensitive variables in encrypted vault files
3. **Dashboard access**: Keep `frp_install_dashboard_addr` as `127.0.0.1` unless network access needed
4. **Client webserver**: Only enable `frp_install_client_webserver_enabled` when needed for debugging
5. **Firewall**: Enable `frp_install_configure_firewall` on production systems
6. **Logging**: Use `info` or `warn` log levels in production

## Supported Platforms

- **OS**: Ubuntu 20.04+, Debian 11+, CentOS/RHEL 8+, Fedora 36+
- **FRP**: Versions 0.61.x - 0.63.x
- **Architectures**: amd64, arm64, armv7

## Variable Migration

If migrating from older versions, update variable names:

| Old Variable | New Variable |
|--------------|--------------|
| `frp_server_addr` | `frp_install_client_server_addr` |
| `frp_server_port` | `frp_install_client_server_port` |
| `frp_bind_addr` | `frp_install_server_addr` |
| `frp_bind_port` | `frp_install_server_port` |
| `frp_auth_token` | `frp_install_auth_token` |

See [Guide](guide.md) for step-by-step tutorials and practical examples.
