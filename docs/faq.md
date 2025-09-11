# FAQ

Frequently asked questions about the wiphoo.frp collection.

(Placeholder) Add Q&A items here.

## General

Q: What is FRP?

A: Fast Reverse Proxy — a tool to expose local services behind NAT/firewalls to the internet.

Q: Which operating systems are supported?

A: Ubuntu 20.04+, Debian 11+, CentOS/RHEL 8+, Fedora. Other Linux distributions may work but are untested.

## Installation

Q: Do I need root privileges?

A: Yes, installing binaries and managing systemd services requires `become: true`.

Q: Can I install both server and client on the same host?

A: Yes. Set `frp_install_files: ["frps", "frpc"]`.

## Security

Q: How should I store tokens and secrets?

A: Use Ansible Vault and reference the variables (e.g., `frp_install_auth_token: "{{ vault_frp_token }}"`).

Q: Is TLS supported?

A: Yes. Configure TLS settings in your custom templates or modify the default TOML configuration files.

## Operations

Q: How to update FRP?

A: Change `frp_install_version` and re-run the playbook. Use rolling updates with `serial` to reduce downtime.

Q: Where are logs located?

A: By default `/var/log/frp/frp.log` and `journalctl -u frpc` for systemd-managed services.

## Performance

Q: How can I optimize FRP for high throughput?

A: Increase connection pools with `frp_install_transport_pool_count` (client) and `frp_install_transport_max_pool_count` (server). Enable TCP multiplexing with `frp_install_transport_tcp_mux: true`.

Q: What transport settings should I use for many clients?

A: Increase `frp_install_transport_max_pool_count` to 50+ on the server and reduce keepalive intervals (`frp_install_transport_tcp_mux_keepalive_interval: 30`) for faster connection management.

Q: How to reduce resource usage on low-power devices?

A: Decrease pool sizes (`frp_install_transport_pool_count: 2`) and increase keepalive intervals (`frp_install_transport_tcp_mux_keepalive_interval: 120`) to reduce CPU and memory usage.

Q: Should I disable TCP multiplexing?

A: Generally no. Only disable `frp_install_transport_tcp_mux` if experiencing issues with high-latency connections (satellite/mobile) or specific network configurations that don't handle multiplexing well.

If your question isn't answered here, open an issue in the repository with relevant details.
