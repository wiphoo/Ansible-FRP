# Installation, Usage & Examples

Complete guide for installing, configuring, and deploying the wiphoo.frp Ansible collection.

## Installation

### Requirements
- Ansible >=11.10, Python >=3.11
- Linux (Ubuntu, Debian, CentOS/RHEL, Fedora)
- Internet access and admin privileges

### Install Collection

**From Galaxy:**
```bash
ansible-galaxy collection install wiphoo.frp
```

**With requirements.yml:**
```yaml
collections:
  - name: wiphoo.frp
    version: ">=1.0.0"
```
```bash
ansible-galaxy collection install -r requirements.yml
```

**Verify installation:**
```bash
ansible-galaxy collection list wiphoo.frp
```

**Quick Start Playbook:**
```yaml
- name: Install FRP Server
  hosts: frp_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        frp_install_configure_firewall: true

- name: Install FRP Client
  hosts: frp_clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_server_addr: "203.0.113.10"
        frp_proxies:
          - name: "ssh"
            type: "tcp"
            local_port: 22
            remote_port: 2222
```

## Usage Patterns

### Server Configuration
```yaml
- hosts: vps_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        frp_auth_token: "your-secure-token"
        frp_install_configure_firewall: true
```

### Client Configuration
```yaml
- hosts: clients
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_server_addr: "your-server.com"
        frp_auth_token: "your-secure-token"
        frp_proxies:
          - name: "ssh"
            type: "tcp"
            local_port: 22
            remote_port: 2222
```

### Security Configuration

**With TLS:**
```yaml
frp_transport_tls_enable: true
frp_transport_tls_cert_file: "/path/to/cert.pem"
frp_transport_tls_key_file: "/path/to/key.pem"
```

**Using Ansible Vault:**
```yaml
frp_auth_token: "{{ vault_frp_token }}"
```

### Production Settings

**Server Optimization:**
```yaml
frp_server_max_clients: 1000
frp_server_max_ports_per_client: 10
frp_log_level: "warn"
frp_log_max_days: 7
```

## Real-World Examples

### Home Lab Setup
```yaml
- hosts: vps_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        frp_install_configure_firewall: true

- hosts: homelab
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_server_addr: "203.0.113.10"
        frp_proxies:
          - name: "ssh"
            type: "tcp"
            local_port: 22
            remote_port: 2222
          - name: "homeassistant"
            type: "http"
            local_port: 8123
            custom_domains: ["home.example.com"]
```

### Corporate Environment
```yaml
- hosts: all
  become: true
  vars:
    frp_auth_token: "{{ vault_corporate_token }}"
    frp_transport_tls_enable: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_user: "svcfrp"
        frp_install_dir: "/opt/frp/bin"
        frp_install_verify_checksums: true
        frp_install_configure_firewall: true
```

### Load Balanced Services
```yaml
- hosts: web_servers
  become: true
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_server_addr: "lb.example.com"
        frp_proxies:
          - name: "web-{{ inventory_hostname }}"
            type: "http"
            local_port: 80
            custom_domains: ["app.example.com"]
            group: "web-cluster"
            group_key: "{{ vault_lb_key }}"
            health_check_type: "http"
            health_check_url: "/health"
```

### Container Integration
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

For detailed variable reference, see [API Documentation](api.md).
For help with issues, see [Help & Support](help.md).
