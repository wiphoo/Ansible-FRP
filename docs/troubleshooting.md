# Troubleshooting

Common issues and troubleshooting tips for using this collection.

(Placeholder) Document known issues and debugging steps.

This page collects common issues and step-by-step debugging commands.

## Installation Issues

### Download failures

If downloads from GitHub fail, either provide a mirror or temporarily disable checksum verification:

```yaml
frp_install_download_base_url: "https://your-mirror.com/frp/releases/download"
frp_install_verify_checksums: false
```

### Permission errors

Ensure `become: true` is set and the Ansible user has proper sudo privileges.

## Service Issues

### Service won't start

Check status and follow logs:

```bash
systemctl status frpc
journalctl -u frpc -f
```

Validate config syntax where supported:

```bash
# /usr/local/bin/frpc verify -c /etc/frp/frpc.toml
```

### Connection refused or unreachable

Confirm server is listening and reachable:

```bash
ss -tlnp | grep 7000
telnet server-ip 7000
nc -zv server-ip 7000
```

## Configuration Issues

- TOML syntax: ensure string values use quotes and numbers are not quoted.
- Tokens must match between server and client. Use Ansible Vault for secrets.

## Network Issues

Check port conflicts and running processes:

```bash
lsof -i :7000
netstat -tlnp | grep 7000
```

## Debugging & Logs

- Increase logging: `frp_log_level: "debug"`
- Use `journalctl -u frpc -f` while reproducing the issue
- For SSH debug: `ssh -vvv -p 2222 user@server-ip`

If you still need help, open an issue with: steps to reproduce, logs, and relevant variable snippets (mask secrets).
