# 📁 Example Files

This directory contains practical examples for deploying FRP (Fast Reverse Proxy) using the wiphoo.frp Ansible collection.

# � FRP Examples Directory

This directory contains practical, ready-to-use examples for deploying FRP (Fast Reverse Proxy) using the wiphoo.frp Ansible collection.

## 📋 Available Examples

### 🎯 Main Examples File
- **[examples.yml](examples.yml)** - **Comprehensive examples** with 5 different deployment scenarios:
  1. Minimal FRP Server
  2. Minimal FRP Client
  3. Production FRP Server (with dashboard, logging, firewall)
  4. Production FRP Client (with admin interface, validation)
  5. Combined Server + Client Setup

### ⚡ Quick Start Examples
- **[minimal_frps.yml](minimal_frps.yml)** - **Minimal server deployment** (3 variables only)
- **[minimal_frpc.yml](minimal_frpc.yml)** - **Minimal client deployment** (3 variables only)

### 🚀 Production Ready Example
- **[example_frpc_playbook.yml](example_frpc_playbook.yml)** - **Complete client deployment** with:
  - Pre-deployment validation
  - Connectivity testing
  - Error handling
  - Post-deployment verification
  - Detailed comments and deployment notes

### 🗄️ Configuration Template
- **[example_inventory.ini](example_inventory.ini)** - **Sample inventory** showing proper host grouping and variables

## 🚀 Quick Start Guide

## 🚀 Quick Start Guide

### 1. **Choose Your Deployment Type**

**For Testing/Learning:**
```bash
# Server (minimal - 3 variables only)
cp docs/examples/minimal_frps.yml my-server.yml

# Client (minimal - 3 variables only)
cp docs/examples/minimal_frpc.yml my-client.yml
```

**For Production:**
```bash
# Client with full error handling and validation
cp docs/examples/example_frpc_playbook.yml my-production-client.yml

# Or choose from 5 comprehensive scenarios
cp docs/examples/examples.yml my-deployment.yml
```

### 2. **Customize Variables**
Edit your copied files and update the key variables:
- `frp_install_auth_token` - Your secure authentication token
- `frp_install_client_server_addr` - Your FRP server address (clients only)
- Host groups in your inventory file

### 3. **Create Inventory**
```bash
cp docs/examples/example_inventory.ini inventory/hosts.ini
# Edit inventory/hosts.ini with your server addresses
```

### 4. **Deploy**
```bash
# Test connectivity
ansible all -i inventory/hosts.ini -m ping

# Deploy (minimal examples)
ansible-playbook -i inventory/hosts.ini my-server.yml
ansible-playbook -i inventory/hosts.ini my-client.yml

# Deploy (production with vault)
ansible-playbook -i inventory/hosts.ini my-production-client.yml --ask-vault-pass
```

## 🔒 Security Best Practices

When using these examples in production:

1. **Use Ansible Vault** for sensitive values:
   ```bash
   ansible-vault encrypt_string 'your-secret-token' --name 'frp_install_auth_token'
   ```

2. **Generate Strong Tokens**:
   ```bash
   openssl rand -base64 32
   ```

3. **Review Variables**: Check all variables match your environment before deployment

## 📚 Related Documentation

- **[Installation Guide](../installation.md)** - How to install the collection
- **[API Reference](../api.md)** - Complete variable documentation
- **[Security Guide](../SECURITY.md)** - Security best practices
- **[Troubleshooting](../troubleshooting.md)** - Common issues and solutions

## 🆘 Need Help?

- Check the **[Help documentation](../help.md)** for common questions
- Review **[troubleshooting](../troubleshooting.md)** for deployment issues
- Open an issue on GitHub for bugs or feature requests
