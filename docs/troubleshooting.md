# Troubleshooting

Common issues and troubleshooting tips for using this collection.

(Placeholder) Document known issues and debugging steps.

This page collects common issues and step-by-step debugging commands.

## Installation Issues

### Collection dependency errors

If you see "No module named ansible_collections.community" in CI/CD:

```bash
# Ensure collections are installed with absolute paths
ansible-galaxy collection install community.general -p /absolute/path/to/collections
export ANSIBLE_COLLECTIONS_PATH=/absolute/path/to/collections
```

For GitHub Actions workflows, use:
```yaml
env:
  ANSIBLE_COLLECTIONS_PATH: ${{ github.workspace }}/collections
```

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

## Testing Issues

### Docker container build failures

If you see errors like "Package 'systemctl' has no installation candidate":

The issue is usually incorrect package names in Dockerfile templates. Ensure:
- Use `systemd` and `systemd-sysv` packages on Ubuntu/Debian
- Use `systemd` package on CentOS/RHEL/Fedora
- Never use `systemctl` as a package name (it's a command, not a package)

### Molecule test failures

If molecule tests fail due to idempotence:
- This role is designed to download external binaries and is non-idempotent by nature
- Idempotence testing has been removed from all scenarios
- Use scenarios: `dev` (fast), `ci` (CI/CD), or `default` (complete)

### Path issues in CI/CD

For consistent collections path in GitHub Actions:
```yaml
working-directory: roles/frp_install
env:
  ANSIBLE_COLLECTIONS_PATH: ${{ github.workspace }}/collections
```

## Network Issues

Check port conflicts and running processes:

```bash
lsof -i :7000
netstat -tlnp | grep 7000
```

## Debugging & Logs

- Increase logging: `frp_install_log_level: "debug"`
- Use `journalctl -u frpc -f` while reproducing the issue
- For SSH debug: `ssh -vvv -p 2222 user@server-ip`

If you still need help, open an issue with: steps to reproduce, logs, and relevant variable snippets (mask secrets).
