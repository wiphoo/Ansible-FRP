# API Reference

Complete variable reference for the wiphoo.frp collection.

## Installation Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_version` | `"latest"` | FRP version |
| `frp_install_files` | `["frpc"]` | Components: frpc, frps, or both |
| `frp_install_verify_checksums` | `true` | Verify checksums |
| `frp_install_dir` | `"/usr/local/bin"` | Binary directory |
| `frp_install_config_dir` | `"/etc/frp"` | Config directory |
| `frp_install_user` | `"frp"` | Service user |
| `frp_install_create_service` | `true` | Create systemd services |
| `frp_install_configure_firewall` | `false` | Auto firewall config |

## Connection Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_server_addr` | `"127.0.0.1"` | Server address |
| `frp_server_port` | `7000` | Server port |
| `frp_auth_token` | `""` | Authentication token |
| `frp_bind_addr` | `"0.0.0.0"` | Server bind address |
| `frp_bind_port` | `7000` | Server bind port |

## Transport & Security

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_transport_protocol` | `"tcp"` | Transport protocol |
| `frp_transport_tls_enable` | `false` | Enable TLS |
| `frp_transport_heartbeat_interval` | `30` | Heartbeat interval |
| `frp_log_level` | `"info"` | Log level (trace/debug/info/warn/error) |
| `frp_log_file` | `"/var/log/frp/frp.log"` | Log file path |
| `frp_log_max_days` | `3` | Log retention days |

## Proxy Configuration

Define proxies as a list:

```yaml
frp_proxies:
  - name: "service-name"        # Required: unique identifier
    type: "tcp|udp|http|https"  # Required: proxy type
    local_port: 80              # Required: local port
    local_ip: "127.0.0.1"       # Optional: local IP
    remote_port: 8080           # For tcp/udp: remote port
    custom_domains:             # For http/https: domains
      - "example.com"
    use_encryption: false       # Optional: encryption
    use_compression: false      # Optional: compression
    bandwidth_limit: "1MB"      # Optional: bandwidth limit
```

### Advanced Proxy Options

```yaml
frp_proxies:
  - name: "load-balanced-web"
    type: "http"
    local_port: 80
    custom_domains: ["app.example.com"]
    group: "web-servers"        # Load balancer group
    group_key: "secret-key"     # Group authentication
    health_check_type: "http"   # Health check method
    health_check_url: "/health" # Health check endpoint
    headers:                    # Custom HTTP headers
      Host: "internal.local"
```

## Server Optimization

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_server_max_clients` | `0` | Max concurrent clients (0=unlimited) |
| `frp_server_max_ports_per_client` | `0` | Max ports per client |
| `frp_transport_pool_count` | `1` | Connection pool size |

## Template Overrides

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_config_template_frpc` | `"frpc.toml.j2"` | Client template |
| `frp_install_config_template_frps` | `"frps.toml.j2"` | Server template |

Place custom templates in your playbook's `templates/` directory.

## Common Examples

**Basic Client:**
```yaml
frp_install_files: ["frpc"]
frp_server_addr: "server.example.com"
frp_auth_token: "{{ vault_frp_token }}"
frp_proxies:
  - name: "ssh"
    type: "tcp"
    local_port: 22
    remote_port: 2222
```

**Secure Server:**
```yaml
frp_install_files: ["frps"]
frp_install_configure_firewall: true
frp_auth_token: "{{ vault_frp_token }}"
frp_transport_tls_enable: true
frp_log_level: "warn"
```

## Supported Platforms

- Ubuntu 20.04+, Debian 11+, CentOS/RHEL 8+, Fedora 36+
- FRP versions 0.61.x - 0.63.x
- Architectures: amd64, arm64, arm

See [Guide](guide.md) for practical examples and [Examples](guide.md) for real-world scenarios.
