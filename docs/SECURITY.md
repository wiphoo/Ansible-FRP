# Security Policy

## Supported Versions

| Version | Supported          | Notes |
| ------- | ------------------ | ----- |
| 0.1.x   | ✅ Active Support  | Current stable release |
| < 0.1   | ❌ End of Life     | Pre-release versions not supported |

**Support Policy:**
- **Active Support**: Security updates, bug fixes, and feature updates
- **End of Life**: No updates or support provided

**Current Stable Version**: `0.1.0` (Initial Release)

## Security Best Practices

### Authentication & Authorization

**Use Strong Tokens**:
```yaml
# ✅ Strong with Vault
frp_install_auth_token: "{{ vault_frp_token }}"
```

**Generate Secure Tokens**:
```bash
openssl rand -base64 32
```

### Network Security

**Enable TLS**:
Configure TLS in your custom templates or directly in the generated TOML files:
```toml
# In frps.toml or frpc.toml
transport.tls.enable = true
transport.tls.certFile = "/etc/frp/tls/server.crt"
transport.tls.keyFile = "/etc/frp/tls/server.key"
```

**Firewall Configuration**:
```yaml
frp_install_configure_firewall: true
frp_install_firewall_allowed_ips:
  - "10.0.0.0/8"
  - "172.16.0.0/12"
  - "192.168.0.0/16"
```

### Service Hardening

**Dedicated User**:
```yaml
frp_install_user: "frp"
frp_install_user_shell: "/usr/sbin/nologin"
```

**File Permissions**:
```bash
chmod 600 /etc/frp/*.toml
chown frp:frp /etc/frp/*.toml
```

## Reporting Vulnerabilities

### How to Report

**Email**: [security@wiphoo.dev](mailto:security@wiphoo.dev)
**Subject**: `[SECURITY] wiphoo.frp: Brief Description`

### What to Include

1. Clear vulnerability description
2. Potential impact assessment
3. Steps to reproduce
4. Affected versions
5. Suggested fix (if available)

### Response Timeline

- **Initial Response**: 48 hours
- **Confirmation**: 5 business days
- **Fix Development**: 14 days (critical issues)
- **Public Disclosure**: After fix release

## Security Features

- **Checksum Verification**: All downloads verified
- **Template Sanitization**: Input validation
- **Privilege Separation**: Minimal service privileges
- **Secure Defaults**: Security-focused configuration
- **TLS Support**: Built-in encryption

## Security Updates

Critical security issues receive:
1. Immediate patches (24-48 hours)
2. Multi-channel notifications
3. Coordinated disclosure
4. Backports to supported versions

For security questions: [security@wiphoo.dev](mailto:security@wiphoo.dev)
