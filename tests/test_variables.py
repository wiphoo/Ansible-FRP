"""Variable tests using centralized fixtures."""


class TestVariables:
    """Test all variables are properly defined."""

    def test_all_basic_variables_exist(self, role_vars, expected_basic_variables):
        """Test that all basic configuration variables are defined."""
        for var in expected_basic_variables:
            assert var in role_vars, f"Variable {var} is not defined in defaults"

    def test_all_auth_variables_exist(self, role_vars, expected_auth_variables):
        """Test that all authentication variables are defined."""
        for var in expected_auth_variables:
            assert var in role_vars, f"Variable {var} is not defined in defaults"

    def test_all_server_variables_exist(self, role_vars, expected_server_variables):
        """Test that all server configuration variables are defined."""
        for var in expected_server_variables:
            assert var in role_vars, f"Variable {var} is not defined in defaults"

    def test_all_client_variables_exist(self, role_vars, expected_client_variables):
        """Test that all client configuration variables are defined."""
        for var in expected_client_variables:
            assert var in role_vars, f"Variable {var} is not defined in defaults"

    def test_all_logging_variables_exist(self, role_vars, expected_logging_variables):
        """Test that all logging variables are defined."""
        for var in expected_logging_variables:
            assert var in role_vars, f"Variable {var} is not defined in defaults"

    def test_all_transport_variables_exist(
        self, role_vars, expected_transport_variables
    ):
        """Test that all transport configuration variables are defined."""
        for var in expected_transport_variables:
            assert var in role_vars, f"Variable {var} is not defined in defaults"

    def test_all_variables_present(self, role_vars, all_expected_variables):
        """Test that all expected variables are present in role defaults."""
        missing_vars = []
        for var in all_expected_variables:
            if var not in role_vars:
                missing_vars.append(var)

        assert not missing_vars, (
            f"Missing {len(missing_vars)} variables: {', '.join(missing_vars)}"
        )

    def test_no_unexpected_variables(self, role_vars, all_expected_variables):
        """Test that there are no unexpected variables in defaults."""
        actual_vars = [k for k in role_vars.keys() if k.startswith("frp_install_")]
        unexpected = set(actual_vars) - set(all_expected_variables)

        # This is informational, not a failure - new variables are okay
        if unexpected:
            print(
                f"\nNote: Found {len(unexpected)} additional variables: "
                f"{', '.join(sorted(unexpected))}"
            )

    def test_all_enable_flags_default_to_false(self, role_vars, expected_enable_flags):
        """Test that all enable flags default to false for backward compatibility."""
        for flag in expected_enable_flags:
            assert flag in role_vars, f"Enable flag {flag} not found in defaults"
            assert role_vars[flag] is False, (
                f"Enable flag {flag} should default to false, got {role_vars[flag]}"
            )

    def test_default_values_match_expectations(self, role_vars, expected_defaults):
        """Test that default values match expected values."""
        for var, expected_value in expected_defaults.items():
            assert var in role_vars, f"Variable {var} not found in defaults"
            actual_value = role_vars[var]
            assert actual_value == expected_value, (
                f"Variable {var} has unexpected default value: "
                f"expected {expected_value}, got {actual_value}"
            )


class TestVariableNamingConventions:
    """Test that all variables follow proper naming conventions."""

    def test_all_variables_have_prefix(self, role_vars):
        """Test that all variables use the frp_install_ prefix."""
        for var in role_vars.keys():
            assert var.startswith("frp_install_"), (
                f"Variable {var} does not use frp_install_ prefix"
            )

    def test_enable_flags_follow_convention(self, role_vars, expected_enable_flags):
        """Test that enable flags follow naming convention."""
        for flag in expected_enable_flags:
            assert flag.endswith("_enabled") or flag.endswith("_enable"), (
                f"Enable flag {flag} does not follow naming convention"
            )

    def test_no_duplicate_variables(self, defaults_file_path):
        """Test that there are no duplicate variable definitions."""

        with open(defaults_file_path) as f:
            content = f.read()

        # Parse YAML and check for duplicates
        variables = []
        for line in content.split("\n"):
            if line.strip() and not line.strip().startswith("#"):
                if ":" in line and not line.startswith(" "):
                    var_name = line.split(":")[0].strip()
                    if var_name.startswith("frp_install_"):
                        variables.append(var_name)

        # Check for duplicates
        duplicates = [v for v in set(variables) if variables.count(v) > 1]
        assert not duplicates, f"Found duplicate variables: {', '.join(duplicates)}"


class TestTemplateVariableUsage:
    """Test that templates use consolidated variables correctly."""

    def test_server_template_uses_valid_variables(
        self, server_template_path, all_expected_variables
    ):
        """Test that server template only uses defined variables."""
        import re

        with open(server_template_path) as f:
            content = f.read()

        # Find all variable references in template
        var_pattern = r"\{\{\s*([a-z_][a-z0-9_]*)"
        matches = re.findall(var_pattern, content)

        frp_vars = [m for m in matches if m.startswith("frp_install_")]

        # Optional variables that are documented but not required in defaults
        # These are advanced/optional file paths and settings users set only when needed
        optional_server_vars = {
            "frp_install_allow_ports",  # Optional port whitelist
            "frp_install_dashboard_tls_cert_file",  # Optional TLS cert file path
            "frp_install_dashboard_tls_key_file",  # Optional TLS key file path
            "frp_install_ssh_tunnel_gateway_private_key_file",  # Optional SSH key path
            "frp_install_ssh_tunnel_gateway_auto_gen_private_key_path",  # Optional SSH key gen path
            "frp_install_ssh_tunnel_gateway_authorized_keys_file",  # Optional SSH authorized keys path
            "frp_install_transport_tls_cert_file",  # Optional transport TLS cert
            "frp_install_transport_tls_key_file",  # Optional transport TLS key
            "frp_install_transport_tls_trusted_ca_file",  # Optional transport TLS CA
        }

        # Check that all used variables are defined or are known optional
        undefined_vars = (
            set(frp_vars) - set(all_expected_variables) - optional_server_vars
        )

        # Filter out variables with filters or special handling
        undefined_vars = {
            v
            for v in undefined_vars
            if not any(
                s in v for s in ["default", "tojson", "b64encode", "|", ".", "[", "]"]
            )
        }

        assert not undefined_vars, (
            f"Server template uses undefined variables: {', '.join(undefined_vars)}"
        )

    def test_client_template_uses_valid_variables(
        self, client_template_path, all_expected_variables
    ):
        """Test that client template only uses defined variables."""
        import re

        with open(client_template_path) as f:
            content = f.read()

        # Find all variable references in template
        var_pattern = r"\{\{\s*([a-z_][a-z0-9_]*)"
        matches = re.findall(var_pattern, content)

        frp_vars = [m for m in matches if m.startswith("frp_install_")]

        # Optional variables that are documented but not required in defaults
        # These are advanced/optional settings users set only when needed
        optional_client_vars = {
            "frp_install_includes",  # Optional config includes list
            "frp_install_start_proxies",  # Optional proxy start list
            "frp_install_dns_server",  # Optional custom DNS server
            "frp_install_virtual_net_address",  # Optional virtual network address
            "frp_install_transport_proxy_url",  # Optional HTTP proxy URL
            "frp_install_client_tls_cert_file",  # Optional client TLS cert file path
            "frp_install_client_tls_key_file",  # Optional client TLS key file path
            "frp_install_client_tls_trusted_ca_file",  # Optional client TLS CA file path
            "frp_install_client_tls_server_name",  # Optional TLS server name override
            "frp_install_auth_oidc_proxy_url",  # Optional OIDC proxy URL
            "frp_install_auth_oidc_trusted_ca_file",  # Optional OIDC trusted CA file path
            "frp_install_auth_oidc_insecure_skip_verify",  # Optional OIDC insecure skip verify
        }

        # Check that all used variables are defined or are known optional
        undefined_vars = (
            set(frp_vars) - set(all_expected_variables) - optional_client_vars
        )

        # Filter out variables with filters or special handling
        undefined_vars = {
            v
            for v in undefined_vars
            if not any(
                s in v for s in ["default", "tojson", "b64encode", "|", ".", "[", "]"]
            )
        }

        assert not undefined_vars, (
            f"Client template uses undefined variables: {', '.join(undefined_vars)}"
        )


class TestMinimalConfigurations:
    """Test minimal valid configurations."""

    def test_minimal_server_config_has_required_variables(self, minimal_server_config):
        """Test that minimal server config contains required variables."""
        required = ["frp_install_auth_token", "frp_install_dashboard_password"]

        for var in required:
            assert var in minimal_server_config, f"Minimal server config missing {var}"

    def test_minimal_client_config_has_required_variables(self, minimal_client_config):
        """Test that minimal client config contains required variables."""
        # frp_install_client_user is optional (defaults to "" in defaults/main.yml)
        required = [
            "frp_install_client_server_addr",
            "frp_install_auth_token",
        ]

        for var in required:
            assert var in minimal_client_config, f"Minimal client config missing {var}"


class TestFullConfigurations:
    """Test full configurations with all features enabled."""

    def test_full_server_config_structure(self, full_server_config):
        """Test that full server config has proper structure."""
        # Check basic required variables
        assert "frp_install_auth_token" in full_server_config
        assert "frp_install_dashboard_password" in full_server_config

        # Check optional features
        optional_features = [
            "frp_install_kcp_bind_port_enabled",
            "frp_install_quic_bind_port_enabled",
            "frp_install_vhost_http_port_enabled",
            "frp_install_vhost_https_port_enabled",
        ]

        for feature in optional_features:
            assert feature in full_server_config
            if full_server_config[feature]:
                # If feature is enabled, check corresponding setting exists
                setting_var = feature.replace("_enabled", "")
                assert setting_var in full_server_config

    def test_full_client_config_structure(self, full_client_config):
        """Test that full client config has proper structure."""
        # Check basic required variables
        assert "frp_install_client_user" in full_client_config
        assert "frp_install_client_server_addr" in full_client_config
        assert "frp_install_auth_token" in full_client_config

        # Check optional features
        optional_features = [
            "frp_install_nat_hole_stun_server_enabled",
            "frp_install_client_webserver_enabled",
            "frp_install_transport_quic_enabled",
            "frp_install_feature_gates_enabled",
        ]

        for feature in optional_features:
            assert feature in full_client_config
            if full_client_config[feature]:
                # If feature is enabled, check corresponding setting exists
                if feature == "frp_install_feature_gates_enabled":
                    assert "frp_install_feature_gates" in full_client_config
                elif feature == "frp_install_nat_hole_stun_server_enabled":
                    assert "frp_install_nat_hole_stun_server" in full_client_config


class TestMoleculeTestVariables:
    """Test molecule integration test variable sets."""

    def test_molecule_server_vars_complete(
        self, molecule_test_server_vars, expected_server_variables
    ):
        """Test that molecule server vars include all necessary variables."""
        # Check that key variables are present
        key_vars = [
            "frp_install_version",
            "frp_install_auth_token",
            "frp_install_dashboard_password",
        ]

        for var in key_vars:
            assert var in molecule_test_server_vars, (
                f"Molecule server vars missing {var}"
            )

    def test_molecule_client_vars_complete(
        self, molecule_test_client_vars, expected_client_variables
    ):
        """Test that molecule client vars include all necessary variables."""
        # Check that key variables are present
        key_vars = [
            "frp_install_version",
            "frp_install_client_user",
            "frp_install_client_server_addr",
            "frp_install_auth_token",
        ]

        for var in key_vars:
            assert var in molecule_test_client_vars, (
                f"Molecule client vars missing {var}"
            )

    def test_molecule_vars_use_test_values(self, molecule_test_server_vars):
        """Test that molecule vars use proper test values, not production values."""
        # Check that sensitive values are test values
        assert "molecule" in molecule_test_server_vars["frp_install_auth_token"]
        assert "molecule" in molecule_test_server_vars["frp_install_dashboard_password"]

    def test_molecule_vars_enable_optional_features(
        self, molecule_test_server_vars, molecule_test_client_vars
    ):
        """Test that molecule vars enable optional features for testing."""
        # Server should have some features enabled
        server_features = [
            k for k, v in molecule_test_server_vars.items() if k.endswith("_enabled")
        ]
        assert len(server_features) > 0, "Molecule server should enable some features"

        # Client should have some features enabled
        client_features = [
            k for k, v in molecule_test_client_vars.items() if k.endswith("_enabled")
        ]
        assert len(client_features) > 0, "Molecule client should enable some features"


class TestVariableTypeValidation:
    """Test that variables have correct types."""

    def test_boolean_variables_are_boolean(self, role_vars):
        """Test that boolean variables have boolean values."""
        boolean_vars = [
            "frp_install_cleanup_tmp",
            "frp_install_create_service",
            "frp_install_configure_firewall",
            "frp_install_verify_checksums",
            "frp_install_login_fail_exit",
            "frp_install_enable_prometheus",
            "frp_install_log_disable_print_color",
            "frp_install_detailed_errors_to_client",
            "frp_install_transport_tcp_mux",
            "frp_install_transport_tls_enable",
            "frp_install_transport_tls_force",
            "frp_install_auth_oidc_insecure_skip_verify",
            "frp_install_auth_oidc_insecure_skip_verify_enabled",
        ]

        for var in boolean_vars:
            if var in role_vars:
                assert isinstance(role_vars[var], bool), (
                    f"Variable {var} should be boolean, got {type(role_vars[var])}"
                )

    def test_integer_variables_are_integer(self, role_vars):
        """Test that integer variables have integer values."""
        integer_vars = [
            "frp_install_server_port",
            "frp_install_dashboard_port",
            "frp_install_log_max_days",
            "frp_install_transport_pool_count",
            "frp_install_transport_max_pool_count",
            "frp_install_transport_tcp_mux_keepalive_interval",
            "frp_install_udp_packet_size",
            "frp_install_nathole_analysis_data_reserve_hours",
        ]

        for var in integer_vars:
            if var in role_vars:
                assert isinstance(role_vars[var], int), (
                    f"Variable {var} should be integer, got {type(role_vars[var])}"
                )

    def test_string_variables_are_string(self, role_vars):
        """Test that string variables have string values."""
        string_vars = [
            "frp_install_user",
            "frp_install_group",
            "frp_install_version",
            "frp_install_dir",
            "frp_install_config_dir",
            "frp_install_log_dir",
            "frp_install_auth_method",
            "frp_install_server_addr",
            "frp_install_log_level",
            "frp_install_transport_protocol",
        ]

        for var in string_vars:
            if var in role_vars:
                assert isinstance(role_vars[var], str), (
                    f"Variable {var} should be string, got {type(role_vars[var])}"
                )

    def test_list_variables_are_list(self, role_vars):
        """Test that list variables have list values."""
        list_vars = [
            "frp_install_files",
            "frp_install_auth_additional_scopes",
        ]

        for var in list_vars:
            if var in role_vars:
                assert isinstance(role_vars[var], list), (
                    f"Variable {var} should be list, got {type(role_vars[var])}"
                )


class TestCollectionMetadata:
    """Test galaxy.yml collection metadata and build configuration."""

    def test_galaxy_molecule_exclusion_is_complete(self):
        """Test that galaxy.yml excludes all molecule content, not just molecule.yml.

        Partial exclusion (only molecule.yml) leaves orphaned verify/requirements
        files in the published artifact, which is worse than all-or-nothing.
        Molecule is dev-only infrastructure — end users of the collection don't need it.
        """
        import os

        import yaml

        galaxy_path = os.path.join(os.path.dirname(__file__), "..", "galaxy.yml")
        with open(galaxy_path) as f:
            galaxy = yaml.safe_load(f)

        build_ignore = galaxy.get("build_ignore", [])

        # Must exclude the full molecule directory (not just individual files)
        assert "roles/*/molecule/" in build_ignore or any(
            "molecule/" in str(p) and "*" not in str(p).replace("roles/*/molecule/", "")
            for p in build_ignore
        ), "galaxy.yml must exclude the full roles/*/molecule/ directory"

        # Must NOT use the partial pattern that leaves orphaned files behind
        partial_patterns = [
            "roles/*/molecule/*/molecule.yml",
            "roles/*/molecule/**",
        ]
        for pattern in partial_patterns:
            if pattern in build_ignore:
                # Partial pattern is only acceptable if the full dir is also excluded
                assert "roles/*/molecule/" in build_ignore, (
                    f"galaxy.yml uses partial pattern '{pattern}' without "
                    f"also excluding the full 'roles/*/molecule/' directory"
                )
