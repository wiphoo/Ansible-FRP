# API Reference

Complete variable reference for the wiphoo.frp collection.

## Configuration Format

**Important**: This collection uses **TOML configuration format only** (FRP v0.52.0+). INI format support has been deprecated and removed as of v0.1.0.

- ✅ **Supported**: TOML (frpc.toml.j2, frps.toml.j2)
- ❌ **Deprecated**: INI format (removed in v0.1.0)

## Core Installation Variables

### Basic Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_version` | `"0.65.0"` | FRP version to install |
| `frp_install_files` | `["frps", "frpc"]` | Components to install (frps, frpc, or both) |
| `frp_install_user` | `"frp"` | System user for FRP processes |
| `frp_install_group` | `"frp"` | System group for FRP processes |
| `frp_install_create_service` | `true` | Create systemd services |
| `frp_install_configure_firewall` | `true` | Automatically configure firewall rules |
| `frp_install_verify_checksums` | `true` | Verify download integrity with checksums |
| `frp_install_cleanup_tmp` | `true` | Clean up temporary files after installation |

### Directory Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_tmp_dir` | `"/tmp"` | Temporary directory for downloads |
| `frp_install_dir` | `"/usr/local/bin/frp"` | Binary installation directory |
| `frp_install_config_dir` | `"/etc/frp"` | Configuration files directory |
| `frp_install_log_dir` | `"/var/log/frp"` | Log files directory |

### System Detection

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_system` | `""` (auto) | Operating system (auto-detected if empty) |
| `frp_install_architecture` | `""` (auto) | CPU architecture (auto-detected if empty) |

## Authentication Variables

### Basic Authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_auth_method` | `"token"` | Authentication method (token or oidc) |
| `frp_install_auth_token` | `""` | **REQUIRED**. Authentication token (use Ansible Vault) |

### Additional Authentication Scopes

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_auth_additional_scopes_enabled` | `false` | Enable additional authentication scopes |
| `frp_install_auth_additional_scopes` | `["HeartBeats", "NewWorkConns"]` | Additional scopes for authentication |

### Token from File

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_auth_token_source_enabled` | `false` | Read auth token from file instead of variable |
| `frp_install_auth_token_source_type` | `"file"` | Token source type |
| `frp_install_auth_token_source_file_path` | `"/etc/frp/token"` | Path to file containing auth token |

### OIDC Authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_auth_oidc_enabled` | `false` | Enable OIDC authentication |
| `frp_install_auth_oidc_issuer` | `""` | OIDC issuer URL |
| `frp_install_auth_oidc_audience` | `""` | OIDC audience |
| `frp_install_auth_oidc_skip_expiry_check` | `false` | Skip token expiry validation |
| `frp_install_auth_oidc_skip_issuer_check` | `false` | Skip issuer validation |
| `frp_install_auth_oidc_client_id` | `""` | OIDC client ID |
| `frp_install_auth_oidc_client_secret` | `""` | OIDC client secret |
| `frp_install_auth_oidc_scope` | `""` | OIDC scope |
| `frp_install_auth_oidc_token_endpoint_url` | `""` | OIDC token endpoint URL |
| `frp_install_auth_oidc_additional_endpoint_params_enabled` | `false` | Enable additional OIDC endpoint parameters |
| `frp_install_auth_oidc_additional_endpoint_params` | `{}` | Additional OIDC endpoint parameters (dict) |

## Server Configuration Variables

### Server Binding

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_server_addr` | `"0.0.0.0"` | Server bind address (bindAddr in TOML) |
| `frp_install_server_port` | `7000` | Server bind port (bindPort in TOML) |

### Protocol Ports

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_kcp_bind_port_enabled` | `false` | Enable KCP protocol |
| `frp_install_kcp_bind_port` | `7000` | KCP protocol bind port |
| `frp_install_quic_bind_port_enabled` | `false` | Enable QUIC protocol |
| `frp_install_quic_bind_port` | `7002` | QUIC protocol bind port |

### Proxy Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_proxy_bind_addr_enabled` | `false` | Enable proxy bind address |
| `frp_install_proxy_bind_addr` | `"127.0.0.1"` | Proxy bind address |

### Dashboard / Web Interface

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_dashboard_addr` | `"127.0.0.1"` | Dashboard web interface bind address |
| `frp_install_dashboard_port` | `7500` | Dashboard web interface port |
| `frp_install_dashboard_user` | `"admin"` | Dashboard username |
| `frp_install_dashboard_password` | `""` | **REQUIRED**. Dashboard password (use Ansible Vault) |
| `frp_install_dashboard_pprof_enable` | `false` | Enable pprof debugging endpoint |
| `frp_install_enable_prometheus` | `true` | Enable Prometheus metrics endpoint |
| `frp_install_dashboard_assets_dir_enabled` | `false` | Use custom dashboard assets |
| `frp_install_dashboard_assets_dir` | `"./static"` | Custom dashboard assets directory |

### Virtual Host Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_vhost_http_port_enabled` | `false` | Enable virtual host HTTP port |
| `frp_install_vhost_http_port` | `8080` | Virtual host HTTP port |
| `frp_install_vhost_https_port_enabled` | `false` | Enable virtual host HTTPS port |
| `frp_install_vhost_https_port` | `8443` | Virtual host HTTPS port |
| `frp_install_vhost_http_timeout_enabled` | `false` | Enable HTTP timeout |
| `frp_install_vhost_http_timeout` | `60` | HTTP timeout in seconds |

### TCP Multiplexing

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_tcpmux_http_connect_port_enabled` | `false` | Enable TCP multiplexing HTTP CONNECT |
| `frp_install_tcpmux_http_connect_port` | `1337` | TCP mux HTTP CONNECT port |
| `frp_install_tcpmux_passthrough_enabled` | `false` | Enable TCP mux passthrough |
| `frp_install_tcpmux_passthrough` | `false` | TCP mux passthrough setting |

### Connection Limits

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_user_conn_timeout_enabled` | `false` | Enable user connection timeout |
| `frp_install_user_conn_timeout` | `10` | User connection timeout in seconds |
| `frp_install_max_ports_per_client_enabled` | `false` | Enable port limit per client |
| `frp_install_max_ports_per_client` | `0` | Maximum ports per client (0=unlimited) |

### Subdomain Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_subdomain_host_enabled` | `false` | Enable subdomain support |
| `frp_install_subdomain_host` | `"frps.com"` | Base domain for subdomains |

### Custom Pages

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_custom_404_page_enabled` | `false` | Use custom 404 page |
| `frp_install_custom_404_page` | `"/path/to/404.html"` | Path to custom 404 page |

### SSH Tunnel Gateway

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_ssh_tunnel_gateway_enabled` | `false` | Enable SSH tunnel gateway |
| `frp_install_ssh_tunnel_gateway_bind_port` | `2200` | SSH tunnel gateway bind port |

### Detailed Error Reporting

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_detailed_errors_to_client` | `true` | Send detailed error messages to clients |

## Client Configuration Variables

### Server Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_client_user` | `"your_name"` | Client user identifier |
| `frp_install_client_server_addr` | `"your-server-address.example.com"` | **REQUIRED**. FRP server address |
| `frp_install_client_server_port` | `7000` | FRP server port |
| `frp_install_login_fail_exit` | `true` | Exit on login failure |

### NAT Hole Punching

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_nat_hole_stun_server_enabled` | `false` | Enable NAT hole punching |
| `frp_install_nat_hole_stun_server` | `"stun.easyvoip.com:3478"` | STUN server for NAT traversal |

### Client Admin WebServer

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_client_webserver_enabled` | `false` | Enable client admin web interface |
| `frp_install_client_webserver_addr` | `"127.0.0.1"` | Client admin webserver bind address |
| `frp_install_client_webserver_port` | `7400` | Client admin webserver port |
| `frp_install_client_webserver_user` | `"admin"` | Client admin webserver username |
| `frp_install_client_webserver_password` | `""` | Client admin webserver password |
| `frp_install_client_webserver_pprof_enabled` | `false` | Enable pprof debugging endpoint |

### Feature Gates

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_feature_gates_enabled` | `false` | Enable experimental features |
| `frp_install_feature_gates` | `{VirtualNet: true}` | Feature flags (dict) |

## Logging Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_log_level` | `"info"` | Log level: trace, debug, info, warn, error |
| `frp_install_log_max_days` | `3` | Log file retention in days |
| `frp_install_log_disable_print_color` | `false` | Disable colored log output |

## Transport Configuration Variables

### Connection Pool

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_pool_count` | `5` | Client connection pool size |
| `frp_install_transport_max_pool_count` | `5` | Server maximum connection pool size |

### TCP Multiplexing

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_tcp_mux` | `true` | Enable TCP multiplexing |
| `frp_install_transport_tcp_mux_keepalive_interval` | `60` | TCP mux keepalive interval (seconds) |

### Heartbeat Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_heartbeat_timeout_enabled` | `false` | Enable heartbeat timeout (server) |
| `frp_install_transport_heartbeat_timeout` | `90` | Heartbeat timeout in seconds (server) |
| `frp_install_transport_heartbeat_enabled` | `false` | Enable heartbeat (client) |
| `frp_install_transport_heartbeat_interval` | `30` | Heartbeat interval in seconds (client) |

### TCP Keepalive

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_tcp_keepalive_enabled` | `false` | Enable TCP keepalive |
| `frp_install_transport_tcp_keepalive` | `7200` | TCP keepalive interval in seconds |

### Dial Server Configuration (Client)

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_dial_server_timeout_enabled` | `false` | Enable dial server timeout |
| `frp_install_transport_dial_server_timeout` | `10` | Dial server timeout in seconds |
| `frp_install_transport_dial_server_keepalive_enabled` | `false` | Enable dial server keepalive |
| `frp_install_transport_dial_server_keepalive` | `7200` | Dial server keepalive in seconds |

### Protocol Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_protocol` | `"tcp"` | Transport protocol: tcp, kcp, quic, websocket, wss |
| `frp_install_transport_connect_server_local_ip` | `"0.0.0.0"` | Local IP for server connection |

### QUIC Protocol

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_quic_enabled` | `false` | Enable QUIC protocol options |
| `frp_install_transport_quic_keepalive_period` | `10` | QUIC keepalive period in seconds |
| `frp_install_transport_quic_max_idle_timeout` | `30` | QUIC max idle timeout in seconds |
| `frp_install_transport_quic_max_incoming_streams` | `100000` | QUIC max incoming streams |

### TLS Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_tls_enable` | `true` | Enable TLS encryption |
| `frp_install_transport_tls_force` | `false` | Force TLS for all connections (server only) |
| `frp_install_transport_tls_disable_custom_tls_first_byte_enabled` | `false` | Disable custom TLS first byte (client) |
| `frp_install_transport_tls_disable_custom_tls_first_byte` | `true` | Custom TLS first byte setting |

### UDP & NAT Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_udp_packet_size` | `1500` | UDP packet size in bytes |
| `frp_install_nathole_analysis_data_reserve_hours` | `168` | NAT hole analysis data retention (hours) |

## Optional/Advanced Variables

These variables are typically used for advanced configurations and don't have defaults. Set them only when needed.

### TLS Certificate Paths

```yaml
# Server dashboard TLS
frp_install_dashboard_tls_cert_file: "/path/to/server.crt"
frp_install_dashboard_tls_key_file: "/path/to/server.key"

# Client TLS
frp_install_client_tls_cert_file: "/path/to/client.crt"
frp_install_client_tls_key_file: "/path/to/client.key"
frp_install_client_tls_trusted_ca_file: "/path/to/ca.crt"
frp_install_client_tls_server_name: "example.com"

# Transport TLS
frp_install_transport_tls_cert_file: "/path/to/server.crt"
frp_install_transport_tls_key_file: "/path/to/server.key"
frp_install_transport_tls_trusted_ca_file: "/path/to/ca.crt"
```

### SSH Tunnel Gateway Keys

```yaml
frp_install_ssh_tunnel_gateway_private_key_file: "/home/frp-user/.ssh/id_rsa"
frp_install_ssh_tunnel_gateway_auto_gen_private_key_path: "/home/frp-user/.ssh/id_rsa_auto"
frp_install_ssh_tunnel_gateway_authorized_keys_file: "/home/frp-user/.ssh/authorized_keys"
```

### OIDC Advanced Configuration

```yaml
frp_install_auth_oidc_trusted_ca_file: "/path/to/ca.crt"
frp_install_auth_oidc_insecure_skip_verify_enabled: false
frp_install_auth_oidc_insecure_skip_verify: false
frp_install_auth_oidc_proxy_url: "http://proxy.example.com:8080"
```

### Network Configuration

```yaml
# DNS server
frp_install_dns_server: "8.8.8.8"

# HTTP proxy for client connections
frp_install_transport_proxy_url: "http://user:passwd@192.168.1.128:8080"

# Virtual network address
frp_install_virtual_net_address: "100.86.1.1/24"
```

### Port Restrictions

```yaml
# Server port restrictions
frp_install_allow_ports:
  - { start: 2000, end: 3000 }  # Port range
  - { single: 3001 }             # Single port
  - { start: 4000, end: 5000 }
```

### Configuration Includes

```yaml
# Include additional configuration files
frp_install_includes:
  - "./confd/*.toml"
  - "/etc/frp/custom/*.toml"
```

### Proxy Selection

```yaml
# Start specific proxies only
frp_install_start_proxies:
  - "ssh"
  - "web"
  - "database"
```

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

### Example 1: Production FRP Server with TLS and Dashboard

```yaml
---
- hosts: frp_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        # Installation
        frp_install_version: "0.65.0"
        frp_install_files: ['frps']
        frp_install_create_service: true

        # Authentication
        frp_install_auth_method: "token"
        frp_install_auth_token: "your-secure-token-here"

        # Server Configuration
        frp_install_server_addr: "0.0.0.0"
        frp_install_server_port: 7000

        # Dashboard with TLS
        frp_install_dashboard_addr: "0.0.0.0"
        frp_install_dashboard_port: 7500
        frp_install_dashboard_user: "admin"
        frp_install_dashboard_password: "admin-password"
        frp_install_dashboard_tls_cert_file: "/etc/frp/ssl/server.crt"
        frp_install_dashboard_tls_key_file: "/etc/frp/ssl/server.key"

        # Virtual Hosts
        frp_install_vhost_http_port_enabled: true
        frp_install_vhost_http_port: 80
        frp_install_vhost_https_port_enabled: true
        frp_install_vhost_https_port: 443
        frp_install_subdomain_host_enabled: true
        frp_install_subdomain_host: "frp.example.com"

        # Transport Security
        frp_install_transport_tls_enable: true
        frp_install_transport_tls_cert_file: "/etc/frp/ssl/transport.crt"
        frp_install_transport_tls_key_file: "/etc/frp/ssl/transport.key"

        # Logging
        frp_install_log_level: "info"
        frp_install_log_max_days: 7
```

### Example 2: FRP Client with Multiple Proxies

```yaml
---
- hosts: frp_clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        # Installation
        frp_install_version: "0.65.0"
        frp_install_files: ['frpc']
        frp_install_create_service: true

        # Authentication
        frp_install_auth_method: "token"
        frp_install_auth_token: "your-secure-token-here"

        # Server Connection
        frp_install_client_server_addr: "frp.example.com"
        frp_install_client_server_port: 7000

        # TLS Transport
        frp_install_transport_tls_enable: true
        frp_install_transport_tls_trusted_ca_file: "/etc/frp/ssl/ca.crt"

        # Admin Web UI
        frp_install_client_webserver_enabled: true
        frp_install_client_webserver_addr: "127.0.0.1"
        frp_install_client_webserver_port: 7400
        frp_install_client_webserver_user: "admin"
        frp_install_client_webserver_password: "admin-password"

        # Connection Pool
        frp_install_transport_pool_count: 5

        # Logging
        frp_install_log_level: "info"
        frp_install_log_max_days: 3
```

### Example 3: High-Security Setup with OIDC Authentication

```yaml
---
- hosts: frp_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        # Installation
        frp_install_version: "0.65.0"
        frp_install_files: ['frps']

        # OIDC Authentication
        frp_install_auth_method: "oidc"
        frp_install_auth_oidc_issuer: "https://auth.example.com"
        frp_install_auth_oidc_audience: "frp-server"
        frp_install_auth_oidc_skip_expiry_check: false
        frp_install_auth_oidc_skip_issuer_check: false

        # Additional OIDC Settings
        frp_install_auth_additional_scopes_enabled: true
        frp_install_auth_additional_scopes:
          - "email"
          - "profile"

        # Server Configuration
        frp_install_server_addr: "0.0.0.0"
        frp_install_server_port: 7000

        # Transport Security
        frp_install_transport_tls_enable: true
        frp_install_transport_tls_force: true
        frp_install_transport_tls_cert_file: "/etc/frp/ssl/server.crt"
        frp_install_transport_tls_key_file: "/etc/frp/ssl/server.key"

        # Dashboard with TLS
        frp_install_dashboard_addr: "127.0.0.1"
        frp_install_dashboard_port: 7500
        frp_install_dashboard_tls_cert_file: "/etc/frp/ssl/server.crt"
        frp_install_dashboard_tls_key_file: "/etc/frp/ssl/server.key"

        # Connection Limits
        frp_install_max_ports_per_client_enabled: true
        frp_install_max_ports_per_client: 10
        frp_install_user_conn_timeout_enabled: true
        frp_install_user_conn_timeout: 10
```

### Example 4: Development Environment with QUIC Protocol

```yaml
---
- hosts: localhost
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        # Installation
        frp_install_version: "0.65.0"
        frp_install_files: ['frps', 'frpc']
        frp_install_create_service: true

        # Basic Authentication
        frp_install_auth_method: "token"
        frp_install_auth_token: "dev-token-12345"

        # Server Configuration
        frp_install_server_addr: "127.0.0.1"
        frp_install_server_port: 7000

        # Client Configuration
        frp_install_client_server_addr: "127.0.0.1"
        frp_install_client_server_port: 7000

        # QUIC Protocol
        frp_install_transport_protocol: "quic"
        frp_install_transport_quic_enabled: true
        frp_install_transport_quic_keepalive_period: 10
        frp_install_transport_quic_max_idle_timeout: 30
        frp_install_transport_quic_max_incoming_streams: 100000

        # Development-friendly Logging
        frp_install_log_level: "debug"
        frp_install_log_max_days: 1
        frp_install_log_disable_print_color: false
```

### Example 5: SSH Tunnel Gateway with Port Restrictions

```yaml
---
- hosts: frp_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        # Installation
        frp_install_version: "0.65.0"
        frp_install_files: ['frps']

        # Authentication
        frp_install_auth_method: "token"
        frp_install_auth_token: "your-secure-token"

        # Server Configuration
        frp_install_server_addr: "0.0.0.0"
        frp_install_server_port: 7000

        # SSH Tunnel Gateway
        frp_install_ssh_tunnel_gateway_enabled: true
        frp_install_ssh_tunnel_gateway_bind_port: 2200
        frp_install_ssh_tunnel_gateway_private_key_file: "/etc/frp/ssh/id_rsa"
        frp_install_ssh_tunnel_gateway_authorized_keys_file: "/etc/frp/ssh/authorized_keys"

        # Port Restrictions
        frp_install_allow_ports:
          - { start: 2000, end: 3000 }
          - { single: 3001 }
          - { start: 8000, end: 9000 }

        # Transport Security
        frp_install_transport_tls_enable: true

        # Logging
        frp_install_log_level: "info"
```

### Example 6: Minimal Client Configuration

```yaml
---
- hosts: frp_clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_version: "0.65.0"
        frp_install_files: ['frpc']
        frp_install_auth_token: "your-token"
        frp_install_client_server_addr: "frp.example.com"
```

### Example 7: Load Balancing with Connection Pooling

```yaml
---
- hosts: frp_clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        # Installation
        frp_install_version: "0.65.0"
        frp_install_files: ['frpc']

        # Authentication
        frp_install_auth_method: "token"
        frp_install_auth_token: "your-token"

        # Server Connection
        frp_install_client_server_addr: "frp.example.com"
        frp_install_client_server_port: 7000

        # Connection Pooling
        frp_install_transport_pool_count: 10

        # TCP Multiplexing
        frp_install_transport_tcp_mux: true
        frp_install_transport_tcp_mux_keepalive_interval: 30

        # Heartbeat
        frp_install_transport_heartbeat_enabled: true
        frp_install_transport_heartbeat_interval: 15
        frp_install_transport_heartbeat_timeout: 45

        # TCP Keepalive
        frp_install_transport_tcp_keepalive_enabled: true
        frp_install_transport_tcp_keepalive: 7200
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
- **FRP**: Versions 0.52.0+ (TOML configuration format)
- **Architectures**: amd64, arm64, armv7
- **Configuration Format**: TOML (INI deprecated as of v0.1.0)

See [Guide](guide.md) for step-by-step tutorials and practical examples.
