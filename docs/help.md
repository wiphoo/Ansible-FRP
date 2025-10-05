# Help & Support

Comprehensive FAQ and troubleshooting guide for the wiphoo.frp collection.

## Frequently Asked Questions

### General

**Q: What is FRP?**
A: Fast Reverse Proxy - exposes local services behind NAT/firewalls to the internet.

**Q: Supported OS?**
A: Ubuntu 20.04+, Debian 11+, CentOS/RHEL 8+, Fedora.

**Q: Which FRP versions?**
A: FRP v0.52.0+ (TOML configuration format). Default version: v0.65.0. Pin versions in production with `frp_install_version: "0.65.0"`.

**Q: Configuration format?**
A: TOML only (FRP v0.52.0+). INI format deprecated and removed as of v0.1.0.

### Installation

**Q: Need root privileges?**
A: Yes, requires `become: true` for system installation and service management.

**Q: Install both client and server?**
A: `frp_install_files: ["frps", "frpc"]`

**Q: Custom paths?**
A: Use `frp_install_dir`, `frp_install_config_dir`, `frp_install_user`.

**Q: Custom templates?**
A: Override with `frp_install_config_template_frpc: "custom.toml.j2"` in your templates directory.

### Security

**Q: Secure tokens?**
A: Use Ansible Vault:
```bash
ansible-vault encrypt_string 'token' --name 'vault_frp_token'
```
```yaml
frp_install_auth_token: "{{ vault_frp_token }}"
```

**Q: Firewall configuration?**
A: Set `frp_install_configure_firewall: true`

### Operations

**Q: Update FRP?**
A: Change `frp_install_version` and re-run playbook.

**Q: Rolling updates?**
A: Use `serial: "25%"` and `max_fail_percentage` in playbook.

**Q: Monitor services?**
A: `systemctl status frpc` or `journalctl -u frpc`

### Performance

**Q: Connection limits?**
A: 100-500 (small), 1000-5000 (medium), 10000+ (large, requires tuning).

**Q: Optimize performance?**
A: Edit frp configuration manually or create custom templates. Transport settings are hardcoded in templates (poolCount: 5, tcpMux: true).

## Troubleshooting

### Installation Issues

**Download Failures:**
```yaml
# Use custom mirror
frp_install_download_base_url: "https://your-mirror.com/frp/releases/download"
# Or disable checksums temporarily
frp_install_verify_checksums: false
```

**Permission Errors:** Ensure `become: true` and proper sudo access.

### Service Issues

**Won't Start:**
```bash
# Check status and logs
systemctl status frpc
journalctl -u frpc -f
# Validate config
/usr/local/bin/frpc verify -c /etc/frp/frpc.toml
```

**Connection Refused:**
```bash
# Check server port
netstat -tlnp | grep 7000
# Test connectivity
telnet server-ip 7000
```

### Configuration Issues

**TOML Configuration Format:**
- This collection uses TOML format only (FRP v0.52.0+)
- INI format has been deprecated and removed
- Ensure proper TOML syntax (strings quoted, numbers unquoted)

**TOML Syntax Validation:**
```bash
# Validate configuration
/usr/local/bin/frpc verify -c /etc/frp/frpc.toml
/usr/local/bin/frps verify -c /etc/frp/frps.toml
```
```toml
serverAddr = "203.0.113.10"  # Quotes for strings
serverPort = 7000            # No quotes for numbers
```

**Authentication:** Verify matching tokens, use `ansible-vault` for secrets.

### Network Issues

**Port Conflicts:**
```bash
# Find conflicting process
lsof -i :7000
netstat -tlnp | grep 7000
```

**Proxy Failures:** Verify local service is running and accessible.

### Performance Issues

**High Memory:** Reduce `transport.poolCount` and disable `transport.tcpMux`.

**Slow Connections:** Enable `useCompression` and consider `transport.protocol = "kcp"`.

### Debug Mode

**Enable Verbose Logging:**
```yaml
frp_install_log_level: "debug"
```

**Test Commands:**
```bash
# Config validation
/usr/local/bin/frpc verify -c /etc/frp/frpc.toml
# Connection test
nc -zv server-ip 7000
# SSH debug
ssh -vvv -p 2222 user@server-ip
```

## Getting Additional Help

Need more assistance?
- Check [Installation & Usage Guide](guide.md) for setup examples
- Review [API Reference](api.md) for complete variable documentation
- Visit [GitHub Issues](https://github.com/wiphoo/Ansible-FRP/issues) to report problems or request features
