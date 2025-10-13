# Installation, Usage & Examples

Complete guide for installing, configuring, and deploying the wiphoo.frp Ansib# Transport optimization for high-throughput clients
frp_install_transport_pool_count: 20
frp_install_transport_tcp_mux: true
frp_install_transport_tcp_mux_keepalive_interval: 30

# Reduce resource usage for low-resource environments
frp_install_transport_pool_count: 2
frp_install_transport_tcp_mux_keepalive_interval: 120ction with practical examples.

## 📦 Installation

### Requirements
- Ansible Core >=2.17.0, Python >=3.11
- Linux (Ubuntu, Debian, CentOS/RHEL, Fedora)
- FRP v0.52.0+ (TOML configuration format) - default: v0.65.0
- Internet access and admin privileges

### Configuration Format
**TOML Only**: This collection uses TOML configuration format exclusively (INI support deprecated as of v0.1.0).

### Install Collection

**From Galaxy:**
```bash
ansible-galaxy collection install wiphoo.frp
```

**With requirements.yml:**
```yaml
collections:
  - name: wiphoo.frp
    version: ">=0.2.0"
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
        frp_install_client_server_addr: "203.0.113.10"
        frp_install_auth_token: "{{ vault_frp_token }}"
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
        frp_install_auth_token: "your-secure-token"
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
        frp_install_client_server_addr: "your-server.com"
        frp_install_auth_token: "your-secure-token"
        frp_proxies:
          - name: "ssh"
            type: "tcp"
            local_port: 22
            remote_port: 2222
```

### Security Configuration

**TLS Configuration:**
TLS settings are configured in the frp templates. To enable TLS, customize the configuration templates or modify them after installation.

**Using Ansible Vault:**
```yaml
frp_install_auth_token: "{{ vault_frp_token }}"
```

### Production Settings

**Server Optimization:**
```yaml
# Logging for production
frp_install_log_level: "warn"
frp_install_log_max_days: 7

# Transport optimization for high-load servers
frp_install_transport_max_pool_count: 50
frp_install_transport_tcp_mux: true
frp_install_transport_tcp_mux_keepalive_interval: 30
```

**Client Optimization:**
```yaml
# Transport optimization for high-throughput clients
frp_transport_pool_count: 20
frp_transport_tcp_mux: true
frp_transport_tcp_mux_keepalive_interval: 30

# Reduce resource usage for low-resource environments
frp_transport_pool_count: 2
frp_transport_tcp_mux_keepalive_interval: 120
```

## 🎯 Practical Examples

### Home Lab Example

Deploy an FRP server on a VPS and a client that exposes services from your home lab:

```yaml
- name: Home lab FRP deployment
  hosts: all
  become: true
  vars:
    # Secure authentication token (use Ansible Vault in production)
    frp_install_auth_token: "{{ vault_frp_token }}"
  tasks:
    - name: Install FRP server on VPS
      include_role:
        name: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        frp_install_configure_firewall: true
        frp_install_server_addr: "0.0.0.0"  # Bind to all interfaces
        frp_install_server_port: 7000
        frp_install_dashboard_addr: "127.0.0.1"  # Dashboard only on localhost
        frp_install_dashboard_port: 7500
      when: inventory_hostname in groups['vps_servers']

    - name: Install FRP client on home lab
      include_role:
        name: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_install_client_server_addr: "203.0.113.10"  # Your VPS IP
        frp_install_client_server_port: 7000
      when: inventory_hostname in groups['home_clients']
```

### Corporate Example (Secure)

Use Vault for tokens and enable logging for audit:

```yaml
- hosts: corp_servers
  become: true
  vars:
    # Use encrypted vault for sensitive data
    frp_install_auth_token: "{{ vault_corporate_token }}"
    frp_install_log_level: "info"
    frp_install_log_max_days: 30
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frps"]
        frp_install_configure_firewall: true
        frp_install_server_addr: "0.0.0.0"
        frp_install_server_port: 7000
        # Enable dashboard with authentication
        frp_install_dashboard_addr: "0.0.0.0"
        frp_install_dashboard_port: 7500
        frp_install_dashboard_user: "admin"
        frp_install_dashboard_pwd: "{{ vault_dashboard_password }}"

- hosts: corp_clients
  become: true
  vars:
    frp_install_auth_token: "{{ vault_corporate_token }}"
    frp_install_log_level: "info"
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_install_client_server_addr: "corp-frp.example.com"
        frp_install_client_server_port: 7000
```

### Container Integration Example

Deploy FRP without systemd service for container environments:

```yaml
- hosts: container_hosts
  become: true
  vars:
    frp_install_auth_token: "{{ vault_frp_token }}"
  roles:
    - role: wiphoo.frp.frp_install
      vars:
        frp_install_files: ["frpc"]
        frp_install_create_service: false  # No systemd service
        frp_install_client_server_addr: "frp-server.example.com"
        frp_install_client_server_port: 7000
  post_tasks:
    - name: Create Docker Compose for FRP Client
      copy:
        content: |
          version: '3.8'
          services:
            frpc:
              image: alpine:latest
              command: /usr/local/bin/frp/frpc -c /etc/frp/frpc.toml
              volumes:
                - /etc/frp:/etc/frp:ro
                - /var/log/frp:/var/log/frp
              restart: unless-stopped
              network_mode: host
        dest: /opt/frp/docker-compose.yml
```

## 📁 Ready-to-Use Example Files

The `docs/examples/` directory contains consolidated, production-ready examples:

### 🎯 Main Examples
- **[examples.yml](examples/examples.yml)** - **5 comprehensive scenarios** covering minimal, production, and hybrid deployments
- **[example_frpc_playbook.yml](examples/example_frpc_playbook.yml)** - **Production-ready client** with validation, error handling, and deployment notes

### ⚡ Quick Start Examples
- **[minimal_frps.yml](examples/minimal_frps.yml)** - **Minimal server** (3 variables only)
- **[minimal_frpc.yml](examples/minimal_frpc.yml)** - **Minimal client** (3 variables only)

### 🗄️ Configuration Template
- **[example_inventory.ini](examples/example_inventory.ini)** - Sample inventory with proper host grouping

### Quick Start with Examples

**For Testing:**
```bash
# Copy minimal examples (fastest way to get started)
cp docs/examples/minimal_frps.yml my-server.yml
cp docs/examples/minimal_frpc.yml my-client.yml
```

**For Production:**
```bash
# Copy production-ready example with validation
cp docs/examples/example_frpc_playbook.yml my-production-client.yml

# Or choose from 5 comprehensive scenarios
cp docs/examples/examples.yml my-deployment.yml
```

**Deploy:**
```bash
cp docs/examples/example_inventory.ini inventory/hosts.ini
# Edit inventory/hosts.ini and your playbook variables
ansible-playbook -i inventory/hosts.ini my-deployment.yml
```

## 🔧 Advanced Configuration

### Security Configuration

**TLS Configuration:**
TLS settings are configured in the frp templates. To enable TLS, customize the configuration templates or modify them after installation.

**Using Ansible Vault:**
```yaml
frp_install_auth_token: "{{ vault_frp_token }}"
```

### Production Settings

**Server Optimization:**
```yaml
frp_install_server_max_clients: 1000
frp_install_server_max_ports_per_client: 10
frp_install_log_level: "warn"
frp_install_log_max_days: 7
```

## 📚 Additional Resources

- **[API Reference](api.md)** - Complete variable documentation
- **[Security Guide](SECURITY.md)** - Security best practices and supported versions
- **[Help & Support](help.md)** - Troubleshooting and FAQ
- **[Contributing](contributing.md)** - How to contribute to the project
