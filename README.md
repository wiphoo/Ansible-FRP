# Ansible Collection - wiphoo.frp

Fast Reverse Proxy (frp) installation and management.

## Installation

```bash
ansible-galaxy collection install wiphoo.frp
```

## Quick Start

```yaml
- hosts: servers
  become: true
  roles:
    - wiphoo.frp.frp_install
```

## Configuration

### Server
```yaml
- role: wiphoo.frp.frp_install
  vars:
    frp_install_files: ['frps']
    frp_install_create_service: true
```

### Client
```yaml
- role: wiphoo.frp.frp_install
  vars:
    frp_install_files: ['frpc']
    frp_install_create_service: true
```

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `frp_version` | `0.63.0` | FRP version |
| `frp_install_files` | `['frps', 'frpc']` | Components to install |
| `frp_install_create_service` | `true` | Create systemd services |
| `frp_install_user` | `frp` | System user |
| `frp_install_group` | `frp` | System group |

## Complete Examples

See [examples.yml](examples.yml) for detailed configurations.

## Troubleshooting

**Error: 'role_path' is undefined**

Use collection syntax: `wiphoo.frp.frp_install` instead of `roles/frp_install`

## License

MIT
