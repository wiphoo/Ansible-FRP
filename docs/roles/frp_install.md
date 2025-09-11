# Role: frp_install

Automated installation and configuration of FRP (Fast Reverse Proxy) components.

## Overview

The `frp_install` role provides comprehensive automation for deploying FRP in your infrastructure. It handles everything from downloading and installing FRP binaries to creating systemd services and managing configurations.

### What This Role Does

- **Downloads** FRP binaries from official GitHub releases
- **Installs** frpc (client) and/or frps (server) components
- **Creates** dedicated system user and directories
- **Generates** configuration files from templates
- **Manages** systemd services for automatic startup
- **Configures** firewall rules (optional)
- **Verifies** checksums for security

## Requirements

- **Operating System**: Linux (Ubuntu, Debian, CentOS, RHEL, Fedora)
- **Privileges**: Root access required (`become: true`)
- **Python**: 3.11+ for Ansible execution
- **Internet Access**: To download FRP releases

## Basic Usage

### Install Client Only

```yaml
---
- name: Install FRP Client
  hosts: clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_install_server_addr: "server.example.com"
        frp_install_auth_token: "{{ vault_frp_token }}"
```

### Install Server Only

```yaml
---
- name: Install FRP Server
  hosts: servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        frp_install_configure_firewall: true
        frp_install_auth_token: "{{ vault_frp_token }}"
```

### Install Both Components

```yaml
---
- name: Install FRP Server and Client
  hosts: hybrid_nodes
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps", "frpc"]
```

## Key Variables

### Installation Control

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_version` | `"latest"` | FRP version to install |
| `frp_install_files` | `["frpc"]` | Components: frpc, frps, or both |
| `frp_install_verify_checksums` | `true` | Verify download integrity |
| `frp_install_dir` | `"/usr/local/bin"` | Binary installation directory |

### Service Management

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_create_service` | `true` | Create systemd services |
| `frp_install_service_enabled` | `true` | Enable services on boot |
| `frp_install_restart_on_change` | `true` | Restart on config changes |

### Connection Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_server_addr` | `"0.0.0.0"` | FRP server bind address |
| `frp_install_server_port` | `7000` | FRP server bind port |
| `frp_install_auth_token` | `""` | REQUIRED. Authentication token (set via vars or Vault). |
| `frp_install_dashboard_addr` | `"127.0.0.1"` | Dashboard/webServer bind address |
| `frp_install_dashboard_port` | `7500` | Dashboard/webServer port |

### Transport Settings

Performance and connection optimization variables.

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_transport_pool_count` | `5` | Client connection pool size |
| `frp_install_transport_max_pool_count` | `5` | Server maximum connection pool size |
| `frp_install_transport_tcp_mux` | `true` | Enable TCP multiplexing |
| `frp_install_transport_tcp_mux_keepalive_interval` | `60` | TCP mux keepalive interval (seconds) |

**Transport Optimization Examples:**

High-throughput deployment:
```yaml
frp_install_transport_pool_count: 20
frp_install_transport_max_pool_count: 50
frp_install_transport_tcp_mux_keepalive_interval: 30
```

Low-resource deployment:
```yaml
frp_install_transport_pool_count: 2
frp_install_transport_max_pool_count: 5
frp_install_transport_tcp_mux_keepalive_interval: 120
```

## Advanced Configuration

### Custom Paths

```yaml
frp_install_dir: "/opt/frp/bin"
frp_install_config_dir: "/opt/frp/config"
frp_install_user: "svcfrp"
frp_install_group: "svcfrp"
```

### TLS Security

TLS configuration is handled in the configuration templates. To enable TLS, you would need to customize the frp configuration files manually or extend the role templates.

### Proxy Configuration

```yaml
frp_proxies:
  - name: "ssh"
    type: "tcp"
    local_port: 22
    remote_port: 2222

  - name: "web"
    type: "http"
    local_port: 80
    custom_domains: ["app.example.com"]
```

## Examples

See the [Guide](../guide.md) for complete deployment scenarios.

## Troubleshooting

Common issues and solutions are covered in the [Help](../help.md).

## API Reference

For complete variable documentation, see the [API Reference](../api.md).
