# frp_install Role

Installs frp (Fast Reverse Proxy) on Linux systems.

## Requirements
- Ansible >=11.10
- Ubuntu/Debian-based systems
- Internet access for downloads

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_install_version` | `"0.63.0"` | FRP version |
| `frp_install_files` | `['frps', 'frpc']` | Components to install |
| `frp_install_create_service` | `true` | Create systemd services |
| `frp_install_user` | `"frp"` | System user |
| `frp_install_group` | `"frp"` | System group |

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
