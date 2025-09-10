# frp_install Role

Installs frp (Fast Reverse Proxy) on Linux systems.

## Requirements
- Ansible Core >=2.15.0
- Ubuntu/Debian-based systems
- Internet access for downloads

## Variables

### Core Installation Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_version` | `"0.63.0"` | FRP version |
| `frp_install_files` | `['frps', 'frpc']` | Components to install |
| `frp_install_create_service` | `true` | Create systemd services |
| `frp_install_user` | `"frp"` | System user |
| `frp_install_group` | `"frp"` | System group |
| `frp_install_auth_token` | `changeme_default_token_123` | Authentication token |

### Server Configuration Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_server_addr` | `"0.0.0.0"` | Server bind address (bindAddr) |
| `frp_install_server_port` | `7000` | Server bind port (bindPort) |
| `frp_install_dashboard_addr` | `"127.0.0.1"` | Dashboard bind address |
| `frp_install_dashboard_port` | `7500` | Dashboard port |

### Client Configuration Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_client_server_addr` | `"your-server-address.example.com"` | FRP server address to connect to |
| `frp_install_client_server_port` | `7000` | FRP server port to connect to |
| `frp_install_client_webserver_enabled` | `false` | Enable client admin webServer interface |
| `frp_install_client_webserver_addr` | `"127.0.0.1"` | Client admin webServer bind address |
| `frp_install_client_webserver_port` | `7400` | Client admin webServer port |
| `frp_install_client_webserver_user` | `"admin"` | Client admin webServer username |
| `frp_install_client_webserver_password` | `"admin"` | Client admin webServer password |

### Logging Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_log_level` | `"info"` | Log level (trace, debug, info, warn, error) |
| `frp_install_log_max_days` | `3` | Log file retention days |
| `frp_install_log_disable_print_color` | `false` | Disable log colors |

## Usage

### Basic Installation
```yaml
- hosts: servers
  roles:
    - wiphoo.frp.frp_install
```

### Server Only
```yaml
- role: wiphoo.frp.frp_install
  vars:
    frp_install_files: ['frps']
    frp_install_create_service: true
```

### Client Only
```yaml
- role: wiphoo.frp.frp_install
  vars:
    frp_install_files: ['frpc']
    frp_install_create_service: true
    frp_install_client_server_addr: "your-frp-server.example.com"
    frp_install_client_server_port: 7000
    frp_install_client_webserver_enabled: true
    frp_install_client_webserver_port: 7400
```

## What Gets Installed

- FRP binaries (`frps`, `frpc`)
- Systemd services (if enabled)
- Configuration files (`/etc/frp/*.toml`)
- Dedicated system user/group
- Firewall rules (if enabled)

## Post-Installation

1. Edit `/etc/frp/frps.toml` or `/etc/frp/frpc.toml`
2. Start services: `sudo systemctl start frps` or `sudo systemctl start frpc`
3. Enable on boot: `sudo systemctl enable frps` or `sudo systemctl enable frpc`
