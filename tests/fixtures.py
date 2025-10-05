"""Test fixtures and shared test data for FRP Install Role tests."""

import os

import pytest
import yaml

# ==========================================
# File Path Fixtures
# ==========================================


@pytest.fixture
def role_path():
    """Return the absolute path to the role directory."""
    return os.path.join(
        os.path.dirname(__file__),
        "..",
        "roles",
        "frp_install",
    )


@pytest.fixture
def defaults_file_path(role_path):
    """Return the path to defaults/main.yml."""
    return os.path.join(role_path, "defaults", "main.yml")


@pytest.fixture
def vars_file_path(role_path):
    """Return the path to vars/main.yml."""
    return os.path.join(role_path, "vars", "main.yml")


@pytest.fixture
def templates_path(role_path):
    """Return the path to templates directory."""
    return os.path.join(role_path, "templates")


# ==========================================
# Variable Loading Fixtures
# ==========================================


@pytest.fixture
def role_vars(defaults_file_path):
    """Load default variables from the role."""
    with open(defaults_file_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def role_vars_combined(defaults_file_path, vars_file_path):
    """Load both defaults and vars files from the role."""
    # Load defaults
    with open(defaults_file_path) as f:
        defaults = yaml.safe_load(f)

    # Load vars (these override defaults)
    with open(vars_file_path) as f:
        vars_data = yaml.safe_load(f)

    # Combine them (vars override defaults)
    combined = defaults.copy()
    combined.update(vars_data)
    return combined


# ==========================================
# Expected Variable Lists
# ==========================================


@pytest.fixture
def expected_basic_variables():
    """List of expected basic configuration variables."""
    return [
        "frp_install_user",
        "frp_install_group",
        "frp_install_tmp_dir",
        "frp_install_dir",
        "frp_install_config_dir",
        "frp_install_log_dir",
        "frp_install_version",
        "frp_install_files",
        "frp_install_system",
        "frp_install_architecture",
        "frp_install_cleanup_tmp",
        "frp_install_create_service",
        "frp_install_configure_firewall",
        "frp_install_verify_checksums",
    ]


@pytest.fixture
def expected_auth_variables():
    """List of expected authentication variables."""
    return [
        "frp_install_auth_method",
        "frp_install_auth_token",
        "frp_install_auth_additional_scopes_enabled",
        "frp_install_auth_additional_scopes",
        "frp_install_auth_token_source_enabled",
        "frp_install_auth_token_source_type",
        "frp_install_auth_token_source_file_path",
        "frp_install_auth_oidc_enabled",
        "frp_install_auth_oidc_issuer",
        "frp_install_auth_oidc_audience",
        "frp_install_auth_oidc_skip_expiry_check",
        "frp_install_auth_oidc_skip_issuer_check",
        "frp_install_auth_oidc_client_id",
        "frp_install_auth_oidc_client_secret",
        "frp_install_auth_oidc_scope",
        "frp_install_auth_oidc_token_endpoint_url",
    ]


@pytest.fixture
def expected_server_variables():
    """List of expected server configuration variables."""
    return [
        "frp_install_server_addr",
        "frp_install_server_port",
        "frp_install_kcp_bind_port_enabled",
        "frp_install_kcp_bind_port",
        "frp_install_quic_bind_port_enabled",
        "frp_install_quic_bind_port",
        "frp_install_proxy_bind_addr_enabled",
        "frp_install_proxy_bind_addr",
        "frp_install_dashboard_addr",
        "frp_install_dashboard_port",
        "frp_install_dashboard_user",
        "frp_install_dashboard_password",
        "frp_install_dashboard_pprof_enable",
        "frp_install_enable_prometheus",
        "frp_install_dashboard_assets_dir_enabled",
        "frp_install_dashboard_assets_dir",
        "frp_install_vhost_http_port_enabled",
        "frp_install_vhost_http_port",
        "frp_install_vhost_https_port_enabled",
        "frp_install_vhost_https_port",
        "frp_install_vhost_http_timeout_enabled",
        "frp_install_vhost_http_timeout",
        "frp_install_tcpmux_http_connect_port_enabled",
        "frp_install_tcpmux_http_connect_port",
        "frp_install_tcpmux_passthrough_enabled",
        "frp_install_tcpmux_passthrough",
        "frp_install_user_conn_timeout_enabled",
        "frp_install_user_conn_timeout",
        "frp_install_max_ports_per_client_enabled",
        "frp_install_max_ports_per_client",
        "frp_install_subdomain_host_enabled",
        "frp_install_subdomain_host",
        "frp_install_custom_404_page_enabled",
        "frp_install_custom_404_page",
        "frp_install_ssh_tunnel_gateway_enabled",
        "frp_install_ssh_tunnel_gateway_bind_port",
    ]


@pytest.fixture
def expected_client_variables():
    """List of expected client configuration variables."""
    return [
        "frp_install_client_user",
        "frp_install_client_server_addr",
        "frp_install_client_server_port",
        "frp_install_login_fail_exit",
        "frp_install_nat_hole_stun_server_enabled",
        "frp_install_nat_hole_stun_server",
        "frp_install_client_webserver_enabled",
        "frp_install_client_webserver_addr",
        "frp_install_client_webserver_port",
        "frp_install_client_webserver_user",
        "frp_install_client_webserver_password",
        "frp_install_client_webserver_pprof_enabled",
        "frp_install_feature_gates_enabled",
        "frp_install_feature_gates",
    ]


@pytest.fixture
def expected_logging_variables():
    """List of expected logging variables."""
    return [
        "frp_install_log_level",
        "frp_install_log_max_days",
        "frp_install_log_disable_print_color",
        "frp_install_detailed_errors_to_client",
    ]


@pytest.fixture
def expected_transport_variables():
    """List of expected transport configuration variables."""
    return [
        "frp_install_transport_pool_count",
        "frp_install_transport_max_pool_count",
        "frp_install_transport_tcp_mux",
        "frp_install_transport_tcp_mux_keepalive_interval",
        "frp_install_transport_heartbeat_timeout_enabled",
        "frp_install_transport_heartbeat_timeout",
        "frp_install_transport_heartbeat_enabled",
        "frp_install_transport_heartbeat_interval",
        "frp_install_transport_tcp_keepalive_enabled",
        "frp_install_transport_tcp_keepalive",
        "frp_install_transport_dial_server_timeout_enabled",
        "frp_install_transport_dial_server_timeout",
        "frp_install_transport_dial_server_keepalive_enabled",
        "frp_install_transport_dial_server_keepalive",
        "frp_install_transport_protocol",
        "frp_install_transport_connect_server_local_ip",
        "frp_install_transport_quic_enabled",
        "frp_install_transport_quic_keepalive_period",
        "frp_install_transport_quic_max_idle_timeout",
        "frp_install_transport_quic_max_incoming_streams",
        "frp_install_transport_tls_enable",
        "frp_install_transport_tls_force",
        "frp_install_transport_tls_disable_custom_tls_first_byte_enabled",
        "frp_install_transport_tls_disable_custom_tls_first_byte",
        "frp_install_udp_packet_size",
        "frp_install_nathole_analysis_data_reserve_hours",
    ]


@pytest.fixture
def all_expected_variables(
    expected_basic_variables,
    expected_auth_variables,
    expected_server_variables,
    expected_client_variables,
    expected_logging_variables,
    expected_transport_variables,
):
    """Combined list of all expected variables."""
    return (
        expected_basic_variables
        + expected_auth_variables
        + expected_server_variables
        + expected_client_variables
        + expected_logging_variables
        + expected_transport_variables
    )


# ==========================================
# Enable Flag Variables
# ==========================================


@pytest.fixture
def expected_enable_flags():
    """List of all enable flag variables that should default to false."""
    return [
        "frp_install_auth_additional_scopes_enabled",
        "frp_install_auth_token_source_enabled",
        "frp_install_auth_oidc_enabled",
        "frp_install_kcp_bind_port_enabled",
        "frp_install_quic_bind_port_enabled",
        "frp_install_proxy_bind_addr_enabled",
        "frp_install_dashboard_assets_dir_enabled",
        "frp_install_vhost_http_port_enabled",
        "frp_install_vhost_https_port_enabled",
        "frp_install_vhost_http_timeout_enabled",
        "frp_install_tcpmux_http_connect_port_enabled",
        "frp_install_tcpmux_passthrough_enabled",
        "frp_install_user_conn_timeout_enabled",
        "frp_install_max_ports_per_client_enabled",
        "frp_install_subdomain_host_enabled",
        "frp_install_custom_404_page_enabled",
        "frp_install_ssh_tunnel_gateway_enabled",
        "frp_install_nat_hole_stun_server_enabled",
        "frp_install_client_webserver_enabled",
        "frp_install_feature_gates_enabled",
        "frp_install_transport_heartbeat_timeout_enabled",
        "frp_install_transport_heartbeat_enabled",
        "frp_install_transport_tcp_keepalive_enabled",
        "frp_install_transport_dial_server_timeout_enabled",
        "frp_install_transport_dial_server_keepalive_enabled",
        "frp_install_transport_quic_enabled",
        "frp_install_transport_tls_disable_custom_tls_first_byte_enabled",
        "frp_install_client_webserver_pprof_enabled",
        "frp_install_dashboard_pprof_enable",
    ]


# ==========================================
# Template Test Data
# ==========================================


@pytest.fixture
def server_template_path(templates_path):
    """Return the path to server TOML template."""
    return os.path.join(templates_path, "frps.toml.j2")


@pytest.fixture
def client_template_path(templates_path):
    """Return the path to client TOML template."""
    return os.path.join(templates_path, "frpc.toml.j2")


@pytest.fixture
def minimal_server_config():
    """Minimal valid server configuration for testing."""
    return {
        "frp_install_auth_token": "test_token_12345",
        "frp_install_dashboard_password": "test_password",
    }


@pytest.fixture
def minimal_client_config():
    """Minimal valid client configuration for testing."""
    return {
        "frp_install_client_user": "test_user",
        "frp_install_client_server_addr": "test.example.com",
        "frp_install_auth_token": "test_token_12345",
    }


@pytest.fixture
def full_server_config():
    """Full server configuration with all optional features enabled."""
    return {
        "frp_install_auth_token": "test_token_12345",
        "frp_install_dashboard_password": "test_password",
        "frp_install_kcp_bind_port_enabled": True,
        "frp_install_kcp_bind_port": 7001,
        "frp_install_quic_bind_port_enabled": True,
        "frp_install_quic_bind_port": 7002,
        "frp_install_vhost_http_port_enabled": True,
        "frp_install_vhost_http_port": 8080,
        "frp_install_vhost_https_port_enabled": True,
        "frp_install_vhost_https_port": 8443,
        "frp_install_ssh_tunnel_gateway_enabled": True,
        "frp_install_ssh_tunnel_gateway_bind_port": 2200,
    }


@pytest.fixture
def full_client_config():
    """Full client configuration with all optional features enabled."""
    return {
        "frp_install_client_user": "test_user",
        "frp_install_client_server_addr": "test.example.com",
        "frp_install_auth_token": "test_token_12345",
        "frp_install_nat_hole_stun_server_enabled": True,
        "frp_install_nat_hole_stun_server": "stun.l.google.com:19302",
        "frp_install_client_webserver_enabled": True,
        "frp_install_client_webserver_addr": "127.0.0.1",
        "frp_install_client_webserver_port": 7400,
        "frp_install_client_webserver_user": "admin",
        "frp_install_client_webserver_password": "admin",
        "frp_install_transport_quic_enabled": True,
        "frp_install_transport_quic_keepalive_period": 15,
        "frp_install_transport_quic_max_idle_timeout": 45,
        "frp_install_feature_gates_enabled": True,
        "frp_install_feature_gates": {"VirtualNet": True},
    }


# ==========================================
# Integration Test Variables
# ==========================================


@pytest.fixture
def molecule_test_server_vars():
    """Variables for molecule server integration tests."""
    return {
        "frp_install_version": "0.65.0",
        "frp_install_files": ["frps"],
        "frp_install_auth_token": "molecule_test_token",
        "frp_install_dashboard_password": "molecule_dashboard_pwd",
        "frp_install_kcp_bind_port_enabled": True,
        "frp_install_kcp_bind_port": 7000,
        "frp_install_quic_bind_port_enabled": True,
        "frp_install_quic_bind_port": 7002,
        "frp_install_proxy_bind_addr_enabled": True,
        "frp_install_proxy_bind_addr": "0.0.0.0",
        "frp_install_transport_heartbeat_timeout_enabled": True,
        "frp_install_transport_heartbeat_timeout": 120,
        "frp_install_transport_tcp_keepalive_enabled": True,
        "frp_install_transport_tcp_keepalive": 3600,
        "frp_install_vhost_http_port_enabled": True,
        "frp_install_vhost_http_port": 8080,
        "frp_install_vhost_https_port_enabled": True,
        "frp_install_vhost_https_port": 8443,
        "frp_install_vhost_http_timeout_enabled": True,
        "frp_install_vhost_http_timeout": 90,
        "frp_install_tcpmux_http_connect_port_enabled": True,
        "frp_install_tcpmux_http_connect_port": 1337,
        "frp_install_dashboard_assets_dir_enabled": True,
        "frp_install_dashboard_assets_dir": "/var/www/frp",
        "frp_install_auth_additional_scopes_enabled": True,
        "frp_install_auth_additional_scopes": ["HeartBeats", "NewWorkConns"],
        "frp_install_subdomain_host_enabled": True,
        "frp_install_subdomain_host": "frps.test.local",
        "frp_install_custom_404_page_enabled": True,
        "frp_install_custom_404_page": "/etc/frp/404.html",
        "frp_install_ssh_tunnel_gateway_enabled": True,
        "frp_install_ssh_tunnel_gateway_bind_port": 2200,
        "frp_install_transport_quic_enabled": True,
        "frp_install_transport_quic_keepalive_period": 15,
        "frp_install_transport_quic_max_idle_timeout": 45,
        "frp_install_transport_quic_max_incoming_streams": 200000,
    }


@pytest.fixture
def molecule_test_client_vars():
    """Variables for molecule client integration tests."""
    return {
        "frp_install_version": "0.65.0",
        "frp_install_files": ["frpc"],
        "frp_install_client_user": "molecule_test_user",
        "frp_install_client_server_addr": "frps.test.local",
        "frp_install_client_server_port": 7000,
        "frp_install_auth_token": "molecule_test_token",
        "frp_install_nat_hole_stun_server_enabled": True,
        "frp_install_nat_hole_stun_server": "stun.test.local:3478",
        "frp_install_client_webserver_enabled": True,
        "frp_install_client_webserver_addr": "127.0.0.1",
        "frp_install_client_webserver_port": 7400,
        "frp_install_client_webserver_user": "molecule_admin",
        "frp_install_client_webserver_password": "molecule_pwd",
        "frp_install_transport_dial_server_timeout_enabled": True,
        "frp_install_transport_dial_server_timeout": 15,
        "frp_install_transport_dial_server_keepalive_enabled": True,
        "frp_install_transport_dial_server_keepalive": 3600,
        "frp_install_transport_quic_enabled": True,
        "frp_install_transport_quic_keepalive_period": 15,
        "frp_install_transport_quic_max_idle_timeout": 45,
        "frp_install_transport_quic_max_incoming_streams": 200000,
        "frp_install_transport_heartbeat_enabled": True,
        "frp_install_transport_heartbeat_interval": 45,
        "frp_install_feature_gates_enabled": True,
        "frp_install_feature_gates": {"VirtualNet": True},
    }


# ==========================================
# Default Value Expectations
# ==========================================


@pytest.fixture
def expected_defaults():
    """Expected default values for key variables."""
    return {
        "frp_install_user": "frp",
        "frp_install_group": "frp",
        "frp_install_version": "0.65.0",
        "frp_install_dir": "/usr/local/bin/frp",
        "frp_install_config_dir": "/etc/frp",
        "frp_install_log_dir": "/var/log/frp",
        "frp_install_tmp_dir": "/tmp",
        "frp_install_files": ["frps", "frpc"],
        "frp_install_system": "",
        "frp_install_architecture": "",
        "frp_install_cleanup_tmp": True,
        "frp_install_create_service": True,
        "frp_install_configure_firewall": True,
        "frp_install_verify_checksums": True,
        "frp_install_auth_method": "token",
        "frp_install_server_addr": "0.0.0.0",
        "frp_install_server_port": 7000,
        "frp_install_dashboard_addr": "127.0.0.1",
        "frp_install_dashboard_port": 7500,
        "frp_install_dashboard_user": "admin",
        "frp_install_enable_prometheus": True,
        "frp_install_client_server_port": 7000,
        "frp_install_login_fail_exit": True,
        "frp_install_log_level": "info",
        "frp_install_log_max_days": 3,
        "frp_install_log_disable_print_color": False,
        "frp_install_detailed_errors_to_client": True,
        "frp_install_transport_pool_count": 5,
        "frp_install_transport_max_pool_count": 5,
        "frp_install_transport_tcp_mux": True,
        "frp_install_transport_tcp_mux_keepalive_interval": 60,
        "frp_install_transport_protocol": "tcp",
        "frp_install_transport_connect_server_local_ip": "0.0.0.0",
        "frp_install_transport_tls_enable": True,
        "frp_install_transport_tls_force": False,
        "frp_install_udp_packet_size": 1500,
        "frp_install_nathole_analysis_data_reserve_hours": 168,
    }
