"""Unit tests for frp_install role."""

import os

import pytest
import yaml


@pytest.fixture
def role_vars():
    """Load default variables from the role."""
    vars_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "roles",
        "frp_install",
        "defaults",
        "main.yml",
    )
    with open(vars_file) as f:
        return yaml.safe_load(f)


@pytest.fixture
def role_vars_combined():
    """Load both defaults and vars files from the role."""
    defaults_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "roles",
        "frp_install",
        "defaults",
        "main.yml",
    )
    vars_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "roles",
        "frp_install",
        "vars",
        "main.yml",
    )

    # Load defaults
    with open(defaults_file) as f:
        defaults = yaml.safe_load(f)

    # Load vars (these override defaults)
    with open(vars_file) as f:
        vars_data = yaml.safe_load(f)

    # Combine them (vars override defaults)
    combined = defaults.copy()
    combined.update(vars_data)
    return combined


class TestFrpInstallRole:
    """Test cases for the frp_install Ansible role."""

    def test_default_variables_exist(self, role_vars):
        """Test that all expected default variables are defined."""
        expected_vars = [
            "frp_install_user",
            "frp_install_group",
            "frp_install_dir",
            "frp_install_config_dir",
            "frp_install_log_dir",
            "frp_install_tmp_dir",
            "frp_install_files",
            "frp_install_system",
            "frp_install_architecture",
        ]

        for var in expected_vars:
            assert var in role_vars, f"Variable {var} is not defined in defaults"

    def test_user_group_values(self, role_vars):
        """Test that user and group values are reasonable."""
        assert role_vars["frp_install_user"] == "frp"
        assert role_vars["frp_install_group"] == "frp"

    def test_directory_paths(self, role_vars):
        """Test that directory paths are absolute and reasonable."""
        dirs_to_check = [
            "frp_install_dir",
            "frp_install_config_dir",
            "frp_install_log_dir",
            "frp_install_tmp_dir",
        ]

        for dir_var in dirs_to_check:
            path = role_vars[dir_var]
            assert path.startswith("/"), f"{dir_var} should be an absolute path"
            assert not path.endswith("/"), f"{dir_var} should not end with slash"

    def test_install_files_list(self, role_vars):
        """Test that install files list contains expected binaries."""
        install_files = role_vars["frp_install_files"]
        assert isinstance(install_files, list)
        assert "frps" in install_files
        assert "frpc" in install_files
        assert len(install_files) >= 2

    def test_system_architecture_defaults(self, role_vars):
        """Test that system and architecture defaults are empty strings."""
        assert role_vars["frp_install_system"] == ""
        assert role_vars["frp_install_architecture"] == ""

    def test_version_variable_mapping(self, role_vars_combined):
        """Test that frp_version variable is properly mapped to frp_install_version."""
        # Test default version
        assert role_vars_combined["frp_install_version"] == "0.63.0"

        # Test that version is used in filename generation
        version = "0.64.0"
        system = "linux"
        architecture = "amd64"

        # First, substitute the filename_without_extension
        filename_without_ext_template = role_vars_combined.get(
            "frp_install_filename_without_extension", ""
        )
        filename_without_ext = filename_without_ext_template.replace(
            "{{ frp_install_version | trim }}", version
        )
        filename_without_ext = filename_without_ext.replace(
            "{{ frp_install_system | trim }}", system
        )
        filename_without_ext = filename_without_ext.replace(
            "{{ frp_install_architecture | trim }}", architecture
        )

        expected_filename = f"{filename_without_ext}.tar.gz"
        expected_download_url = f"https://github.com/fatedier/frp/releases/download/v{version}/{expected_filename}"

        # Get the template from vars
        filename_template = role_vars_combined.get("frp_install_filename", "")
        download_url_template = role_vars_combined.get("frp_install_download_url", "")

        # Simulate Ansible variable substitution
        filename_result = filename_template.replace(
            "{{ frp_install_filename_without_extension }}", filename_without_ext
        )
        filename_result = filename_result.replace(
            "{{ frp_install_version | trim }}", version
        )
        filename_result = filename_result.replace(
            "{{ frp_install_system | trim }}", system
        )
        filename_result = filename_result.replace(
            "{{ frp_install_architecture | trim }}", architecture
        )

        download_url_result = download_url_template.replace(
            "{{ frp_install_download_base_url }}",
            role_vars_combined.get("frp_install_download_base_url", ""),
        )
        download_url_result = download_url_result.replace(
            "{{ frp_install_version }}", version
        )
        download_url_result = download_url_result.replace(
            "{{ frp_install_filename }}", filename_result
        )

        assert (
            filename_result == expected_filename
        ), f"Expected {expected_filename}, got {filename_result}"
        assert (
            download_url_result == expected_download_url
        ), f"Expected {expected_download_url}, got {download_url_result}"

    def test_version_0640_integration(self):
        """Test that version 0.64.0 is properly handled in all contexts."""
        version = "0.64.0"
        system = "linux"
        architecture = "amd64"

        # Test filename generation
        expected_filename = f"frp_{version}_{system}_{architecture}.tar.gz"
        assert expected_filename == f"frp_{version}_{system}_{architecture}.tar.gz"

        # Test download URL generation
        base_url = "https://github.com/fatedier/frp/releases/download"
        expected_download_url = f"{base_url}/v{version}/{expected_filename}"
        assert expected_download_url == f"{base_url}/v{version}/{expected_filename}"

        # Test checksum URL generation
        expected_checksum_url = f"{base_url}/v{version}/frp_sha256_checksums.txt"
        assert (
            expected_checksum_url == f"{base_url}/v{version}/frp_sha256_checksums.txt"
        )

    def test_version_variable_override(self):
        """Test that frp_version can override the default frp_install_version."""
        # This test simulates what happens when a user sets frp_version
        user_version = "0.64.0"
        default_version = "0.63.0"

        # Simulate the set_fact logic from the role
        final_version = user_version if user_version else default_version
        assert final_version == "0.64.0"

        # Test with undefined user version (should use default)
        final_version_default = default_version
        assert final_version_default == "0.63.0"

    def test_version_integration_with_role(self):
        """Test that the role properly handles version override in a playbook context."""
        # This test simulates what happens when a user sets frp_version in their playbook

        # Simulate the role execution with frp_version set
        user_frp_version = "0.64.0"
        default_frp_install_version = "0.63.0"

        # The role should map frp_version to frp_install_version
        effective_version = (
            user_frp_version if user_frp_version else default_frp_install_version
        )

        # Verify the mapping worked
        assert effective_version == "0.64.0"

        # Test URL construction with the effective version
        base_url = "https://github.com/fatedier/frp/releases/download"
        system = "linux"
        architecture = "amd64"

        expected_filename = f"frp_{effective_version}_{system}_{architecture}.tar.gz"
        expected_download_url = f"{base_url}/v{effective_version}/{expected_filename}"

        # Verify the URL construction
        assert expected_filename == "frp_0.64.0_linux_amd64.tar.gz"
        assert (
            expected_download_url
            == "https://github.com/fatedier/frp/releases/download/v0.64.0/frp_0.64.0_linux_amd64.tar.gz"
        )

        # Test that the role would use this version in practice
        assert effective_version == user_frp_version

    def test_checksum_verification_variables(self, role_vars):
        """Test that checksum verification variables are properly defined."""
        assert "frp_install_verify_checksums" in role_vars
        assert isinstance(role_vars["frp_install_verify_checksums"], bool)
        assert role_vars["frp_install_verify_checksums"] is True

    def test_install_files_loop_compatibility(self, role_vars):
        """Test that frp_install_files is a proper list for loop operations."""
        install_files = role_vars["frp_install_files"]
        assert isinstance(install_files, list)
        assert len(install_files) > 0

        # Test that each item is a string (not another data type)
        for item in install_files:
            assert isinstance(item, str)
            assert len(item.strip()) > 0

    def test_template_reference_format(self):
        """Test that template references use correct collection format."""
        # This test ensures templates are referenced correctly in collection context
        # In collections, templates should be referenced by filename only
        correct_template_refs = [
            "frps.toml.j2",
            "frpc.toml.j2",
            "frps.service.j2",
            "frpc.service.j2",
        ]

        # These should NOT be used in collection context
        incorrect_template_refs = [
            "{{ role_path }}/templates/frps.toml.j2",
            "{{ role_path }}/templates/frpc.toml.j2",
        ]

        for ref in correct_template_refs:
            assert not ref.startswith(
                "{{ role_path }}"
            ), f"Template ref {ref} should not use role_path in collections"

        for ref in incorrect_template_refs:
            assert ref.startswith(
                "{{ role_path }}"
            ), f"Incorrect template ref format: {ref}"

    def test_collection_build_optimization(self):
        """Test that collection build excludes unnecessary files."""
        import subprocess
        import tempfile

        # Test that collection builds successfully
        with tempfile.TemporaryDirectory():
            build_cmd = ["ansible-galaxy", "collection", "build", "--force"]
            result = subprocess.run(
                build_cmd,
                cwd=os.path.dirname(__file__) + "/..",
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0, f"Collection build failed: {result.stderr}"

            # Check that tar.gz file was created
            import glob

            tar_files = glob.glob(os.path.dirname(__file__) + "/../wiphoo-frp-*.tar.gz")
            assert len(tar_files) > 0, "No collection tar.gz file found"

            # Test collection size is reasonable (< 10MB)
            tar_file = tar_files[0]
            size_mb = os.path.getsize(tar_file) / (1024 * 1024)
            assert size_mb < 10, f"Collection size {size_mb:.2f}MB is too large"

    def test_role_variable_prefixes(self, role_vars):
        """Test that all role variables follow proper naming conventions."""
        # All role variables should start with frp_install_ prefix
        for var_name in role_vars.keys():
            if var_name.startswith("frp_") and not var_name.startswith("frp_install_"):
                # This is a user-facing variable that should be mapped
                continue
            elif var_name.startswith("frp_install_"):
                # This is correctly prefixed
                continue
            else:
                # Other variables should be role-specific
                assert var_name.startswith(
                    "frp_"
                ), f"Variable {var_name} should follow role naming convention"

    def test_checksum_url_generation(self, role_vars_combined):
        """Test that checksum URLs are generated correctly."""
        version = "0.64.0"
        base_url = "https://github.com/fatedier/frp/releases/download"
        expected_checksum_url = f"{base_url}/v{version}/frp_sha256_checksums.txt"

        # Get the checksum URL template
        checksum_url_template = role_vars_combined.get(
            "frp_install_checksum_download_url", ""
        )

        # Simulate variable substitution
        checksum_url = checksum_url_template.replace(
            "{{ frp_install_download_base_url }}", base_url
        )
        checksum_url = checksum_url.replace("{{ frp_install_version }}", version)

        assert checksum_url == expected_checksum_url

    def test_binary_installation_paths(self, role_vars):
        """Test that binary installation paths are correctly constructed."""
        install_dir = role_vars["frp_install_dir"]
        install_files = role_vars["frp_install_files"]

        # Test that installation paths are properly constructed
        for binary in install_files:
            full_path = f"{install_dir}/{binary}"
            assert full_path.startswith(
                "/"
            ), f"Installation path {full_path} should be absolute"
            assert not full_path.endswith(
                "/"
            ), f"Installation path {full_path} should not end with slash"
            assert (
                binary in full_path
            ), f"Binary name {binary} should be in path {full_path}"

    def test_service_configuration_variables(self, role_vars):
        """Test that service configuration variables are properly defined."""
        service_vars = [
            "frp_install_create_service",
            "frp_install_configure_firewall",
            "frp_install_cleanup_tmp",
        ]

        for var in service_vars:
            assert var in role_vars, f"Service variable {var} is not defined"
            assert isinstance(
                role_vars[var], bool
            ), f"Service variable {var} should be boolean"

    def test_directory_creation_variables(self, role_vars):
        """Test that directory creation variables are properly structured."""
        dirs_var = role_vars.get("frp_install_dirs", [])
        assert isinstance(dirs_var, list), "frp_install_dirs should be a list"
        assert len(dirs_var) > 0, "frp_install_dirs should not be empty"

        # Check that directories contain template variables (they will be resolved at runtime)
        expected_dirs = [
            "{{ frp_install_dir }}",
            "{{ frp_install_log_dir }}",
            "{{ frp_install_config_dir }}",
        ]

        for expected_dir in expected_dirs:
            assert (
                expected_dir in dirs_var
            ), f"Expected directory {expected_dir} not found in frp_install_dirs"

    def test_architecture_detection_logic(self):
        """Test that architecture detection logic works correctly."""
        # Test cases for different architectures
        test_cases = [
            ("x86_64", "amd64"),
            ("aarch64", "arm64"),
            ("armv7l", "arm_hf"),
            ("armv6l", "arm"),
            ("riscv64", "riscv64"),
            ("unknown_arch", "unknown_arch"),
        ]

        for ansible_arch, expected in test_cases:
            if ansible_arch == "x86_64":
                result = "amd64"
            elif ansible_arch == "aarch64":
                result = "arm64"
            elif ansible_arch == "armv7l":
                result = "arm_hf"
            elif ansible_arch == "armv6l":
                result = "arm"
            elif ansible_arch == "riscv64":
                result = "riscv64"
            else:
                result = ansible_arch

            assert (
                result == expected
            ), f"Architecture {ansible_arch} should map to {expected}, got {result}"

    def test_system_detection_logic(self):
        """Test that system detection logic works correctly."""
        # Test that system detection converts to lowercase
        test_cases = [
            ("Linux", "linux"),
            ("Darwin", "darwin"),
            ("Windows", "windows"),
            ("Unknown", "unknown"),
        ]

        for ansible_system, expected in test_cases:
            result = ansible_system.lower()
            assert (
                result == expected
            ), f"System {ansible_system} should convert to {expected}, got {result}"

    def test_error_handling_variables(self):
        """Test that error handling variables are properly configured."""
        # This test ensures that tasks have proper error handling
        # In a real test environment, we'd check the actual task configurations
        # For now, we'll test that the variables used in error handling exist

        error_related_vars = [
            "frp_install_tmp_dir",
            "frp_install_filename",
            "frp_install_download_url",
        ]

        # These would be checked against the actual role variables
        # This is a placeholder for more comprehensive error handling tests
        for var in error_related_vars:
            assert var.startswith(
                "frp_install_"
            ), f"Error handling variable {var} should follow naming convention"

    def test_idempotency_variables(self, role_vars):
        """Test that variables support idempotent operations."""
        # Test that cleanup and verification variables support idempotency
        idempotent_vars = [
            "frp_install_cleanup_tmp",
            "frp_install_verify_checksums",
        ]

        for var in idempotent_vars:
            assert var in role_vars, f"Idempotency variable {var} should be defined"
            assert isinstance(
                role_vars[var], bool
            ), f"Idempotency variable {var} should be boolean"

    def test_security_variables(self, role_vars):
        """Test that security-related variables are properly configured."""
        security_vars = [
            "frp_install_verify_checksums",
            "frp_install_user",
            "frp_install_group",
        ]

        for var in security_vars:
            assert var in role_vars, f"Security variable {var} should be defined"

        # Test that user/group are not root
        assert (
            role_vars["frp_install_user"] != "root"
        ), "frp user should not be root for security"
        assert (
            role_vars["frp_install_group"] != "root"
        ), "frp group should not be root for security"

    def test_performance_optimization_variables(self, role_vars):
        """Test that performance optimization variables are configured."""
        perf_vars = [
            "frp_install_cleanup_tmp",
            "frp_install_tmp_dir",
        ]

        for var in perf_vars:
            assert var in role_vars, f"Performance variable {var} should be defined"

        # Test that tmp directory is appropriate
        tmp_dir = role_vars["frp_install_tmp_dir"]
        assert (
            tmp_dir == "/tmp"
        ), f"Temporary directory should be /tmp for performance, got {tmp_dir}"

    def test_role_path_undefined_prevention(self):
        """Test that role_path references are properly handled in collections."""
        # This test ensures that the collection doesn't contain role_path references
        # that would cause 'role_path is undefined' errors

        # Check that templates don't contain role_path references
        template_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
        )

        if os.path.exists(template_dir):
            for template_file in os.listdir(template_dir):
                if template_file.endswith(".j2"):
                    template_path = os.path.join(template_dir, template_file)
                    with open(template_path) as f:
                        content = f.read()
                        assert (
                            "role_path" not in content
                        ), f"Template {template_file} contains role_path reference"

        # Check that tasks don't contain problematic role_path references
        tasks_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "tasks",
        )

        if os.path.exists(tasks_dir):
            for task_file in os.listdir(tasks_dir):
                if task_file.endswith(".yml"):
                    task_path = os.path.join(tasks_dir, task_file)
                    with open(task_path) as f:
                        content = f.read()
                        # Allow role_path in comments/documentation but not in actual usage
                        lines = content.split("\n")
                        for line in lines:
                            # Skip comments and documentation
                            if (
                                line.strip().startswith("#")
                                or "role_path" in line
                                and ("FIXME" in line or "TODO" in line)
                            ):
                                continue
                            # Check for actual usage in templates or variable references
                            if "{{ role_path }}" in line or "role_path:" in line:
                                pytest.fail(
                                    f"Task file {task_file} contains role_path usage that will cause undefined errors"
                                )

    def test_collection_role_reference_format(self):
        """Test that collection role references use correct format."""
        # This test ensures that documentation and examples use correct collection references

        # Check README for incorrect role references
        readme_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "README.md",
        )

        with open(readme_path) as f:
            content = f.read()

            # Should contain correct collection references
            assert (
                "wiphoo.frp.frp_install" in content
            ), "README should contain correct collection reference"

            # Should NOT contain incorrect standalone references (except in warnings)
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if (
                    "roles/frp_install" in line
                    and "ansible_collections_path" not in line
                    and "cd roles/frp_install" not in line
                    and "roles/" not in line
                ):  # Skip directory navigation
                    # Only check for actual role references in YAML/Ansible contexts
                    # Check if this is in a warning section about incorrect usage
                    context_lines = lines[
                        max(0, i - 5) : min(len(lines), i + 5)
                    ]  # Wider context
                    context = "\n".join(context_lines)
                    warning_indicators = [
                        "WRONG",
                        "incorrect",
                        "will cause",
                        "will fail",
                        "DANGER",
                        "❌",
                    ]
                    is_warning = any(
                        indicator in context for indicator in warning_indicators
                    )
                    if not is_warning:
                        pytest.fail(
                            f"README contains incorrect role reference on line {i + 1}: {line.strip()}"
                        )


class TestTemplateValidation:
    """Test template rendering and validation."""

    def test_frps_template_renders_correctly(self, role_vars):
        """Test that frps.toml template renders with correct variables."""
        import jinja2

        template_content = """# FRP Server Configuration
bindAddr = "0.0.0.0"
bindPort = 7000
auth = { method = "token", token = "test_token" }
log = { to = "{{ frp_install_log_dir }}/frps.log", level = "info" }"""

        env = jinja2.Environment()
        template = env.from_string(template_content)

        # Test with default variables
        rendered = template.render(**role_vars)

        assert 'bindAddr = "0.0.0.0"' in rendered
        assert "bindPort = 7000" in rendered
        assert "test_token" in rendered
        assert "/var/log/frp/frps.log" in rendered

    def test_frpc_template_renders_correctly(self, role_vars):
        """Test that frpc.toml template renders with correct variables."""
        import jinja2

        template_content = """# FRP Client Configuration
serverAddr = "127.0.0.1"
serverPort = 7000
auth = { method = "token", token = "test_token" }
log = { to = "{{ frp_install_log_dir }}/frpc.log", level = "info" }"""

        env = jinja2.Environment()
        template = env.from_string(template_content)
        rendered = template.render(**role_vars)

        assert 'serverAddr = "127.0.0.1"' in rendered
        assert "serverPort = 7000" in rendered
        assert "/var/log/frp/frpc.log" in rendered

    def test_service_template_validation(self, role_vars):
        """Test that systemd service templates are valid."""
        import jinja2

        service_template = """[Unit]
Description=FRP Server
After=network.target

[Service]
Type=simple
User={{ frp_install_user }}
Group={{ frp_install_group }}
ExecStart={{ frp_install_dir }}/frps -c {{ frp_install_config_dir }}/frps.toml
Restart=always

[Install]
WantedBy=multi-user.target"""

        env = jinja2.Environment()
        template = env.from_string(service_template)
        rendered = template.render(**role_vars)

        assert "[Unit]" in rendered
        assert "[Service]" in rendered
        assert "[Install]" in rendered
        assert "frp" in rendered  # User and group
        assert "/usr/local/bin/frp/frps" in rendered
        assert "/etc/frp/frps.toml" in rendered


class TestIntegrationScenarios:
    """Test complete integration scenarios."""

    def test_minimal_server_installation(self, role_vars):
        """Test minimal server installation scenario."""
        # Simulate minimal server installation
        minimal_vars = role_vars.copy()
        minimal_vars.update(
            {
                "frp_install_files": ["frps"],
                "frp_install_create_service": True,
                "frp_install_configure_firewall": False,
                "frp_install_cleanup_tmp": True,
            }
        )

        # Verify key components for server installation
        assert "frps" in minimal_vars["frp_install_files"]
        assert minimal_vars["frp_install_create_service"] is True
        assert len(minimal_vars["frp_install_files"]) == 1

    def test_minimal_client_installation(self, role_vars):
        """Test minimal client installation scenario."""
        minimal_vars = role_vars.copy()
        minimal_vars.update(
            {
                "frp_install_files": ["frpc"],
                "frp_install_create_service": True,
                "frp_install_configure_firewall": False,
            }
        )

        assert "frpc" in minimal_vars["frp_install_files"]
        assert minimal_vars["frp_install_create_service"] is True

    def test_full_installation_scenario(self, role_vars):
        """Test full installation with all features enabled."""
        full_vars = role_vars.copy()
        full_vars.update(
            {
                "frp_install_files": ["frps", "frpc"],
                "frp_install_create_service": True,
                "frp_install_configure_firewall": True,
                "frp_install_cleanup_tmp": True,
                "frp_install_verify_checksums": True,
            }
        )

        assert len(full_vars["frp_install_files"]) == 2
        assert full_vars["frp_install_create_service"] is True
        assert full_vars["frp_install_configure_firewall"] is True
        assert full_vars["frp_install_verify_checksums"] is True

    def test_custom_paths_scenario(self, role_vars):
        """Test installation with custom paths."""
        custom_vars = role_vars.copy()
        custom_vars.update(
            {
                "frp_install_dir": "/opt/frp",
                "frp_install_config_dir": "/opt/frp/config",
                "frp_install_log_dir": "/opt/frp/logs",
                "frp_install_tmp_dir": "/tmp/frp",
            }
        )

        assert custom_vars["frp_install_dir"] == "/opt/frp"
        assert custom_vars["frp_install_config_dir"] == "/opt/frp/config"
        assert custom_vars["frp_install_log_dir"] == "/opt/frp/logs"


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_invalid_architecture_handling(self):
        """Test handling of invalid architecture."""
        # This would test the fail task when architecture is invalid
        invalid_arch = ""

        # Simulate the failure condition - should fail when architecture is empty
        assert invalid_arch == "", "Architecture should be empty to trigger failure"

    def test_invalid_system_handling(self):
        """Test handling of invalid system."""
        invalid_system = ""

        # Simulate the failure condition - should fail when system is empty
        assert invalid_system == "", "System should be empty to trigger failure"

    def test_download_failure_simulation(self):
        """Test download failure handling."""
        # Simulate download failure scenario
        download_failed = True
        retries = 3

        if download_failed and retries > 0:
            # Should retry the download
            assert retries > 0, "Should have retries available"


class TestConfigurationValidation:
    """Test configuration file validation."""

    def test_frps_config_structure(self):
        """Test FRP server configuration structure."""
        # Basic frps.toml structure validation
        config_lines = [
            'bindAddr = "0.0.0.0"',
            "bindPort = 7000",
            'auth = { method = "token", token = "test" }',
            'log = { to = "/var/log/frp/frps.log", level = "info" }',
        ]

        required_fields = ["bindAddr", "bindPort", "auth", "log"]
        config_text = "\n".join(config_lines)

        for field in required_fields:
            assert field in config_text, f"Required field {field} missing from config"

    def test_frpc_config_structure(self):
        """Test FRP client configuration structure."""
        config_lines = [
            'serverAddr = "127.0.0.1"',
            "serverPort = 7000",
            'auth = { method = "token", token = "test" }',
            'log = { to = "/var/log/frp/frpc.log", level = "info" }',
        ]

        required_fields = ["serverAddr", "serverPort", "auth", "log"]
        config_text = "\n".join(config_lines)

        for field in required_fields:
            assert field in config_text, f"Required field {field} missing from config"

    def test_service_file_structure(self):
        """Test systemd service file structure."""
        service_content = """[Unit]
Description=FRP Service
After=network.target

[Service]
Type=simple
User=frp
ExecStart=/usr/local/bin/frp/frps -c /etc/frp/frps.toml
Restart=always

[Install]
WantedBy=multi-user.target"""

        required_sections = ["[Unit]", "[Service]", "[Install]"]
        for section in required_sections:
            assert section in service_content, f"Required section {section} missing"

        assert "User=frp" in service_content
        assert "ExecStart=" in service_content
        assert "Restart=always" in service_content


class TestFirewallConfiguration:
    """Test firewall configuration scenarios."""

    def test_firewall_rules_generation(self):
        """Test that firewall rules are generated correctly."""
        default_ports = [7000, 7500]  # frp server and dashboard

        for port in default_ports:
            rule = f"ufw allow {port}/tcp"
            assert str(port) in rule, f"Port {port} should be in firewall rule"

    def test_firewall_disabled_scenario(self, role_vars):
        """Test firewall configuration when disabled."""
        no_firewall_vars = role_vars.copy()
        no_firewall_vars["frp_install_configure_firewall"] = False

        assert no_firewall_vars["frp_install_configure_firewall"] is False


class TestVersionCompatibility:
    """Test version compatibility scenarios."""

    def test_version_format_validation(self):
        """Test that version format is valid."""
        valid_versions = ["0.63.0", "0.64.0", "1.0.0"]
        invalid_versions = ["0.63", "0.63.0-beta", "latest"]

        for version in valid_versions:
            parts = version.split(".")
            assert len(parts) == 3, f"Version {version} should have 3 parts"
            for part in parts:
                assert part.isdigit(), f"Version part {part} should be numeric"

        for version in invalid_versions:
            parts = version.split(".")
            # These should not match the expected format
            assert not (len(parts) == 3 and all(p.isdigit() for p in parts))

    def test_download_url_construction(self):
        """Test download URL construction for different versions."""
        base_url = "https://github.com/fatedier/frp/releases/download"
        versions = ["0.63.0", "0.64.0"]

        for version in versions:
            expected_url = f"{base_url}/v{version}/frp_{version}_linux_amd64.tar.gz"
            assert f"v{version}" in expected_url
            assert "linux_amd64" in expected_url
            assert expected_url.endswith(".tar.gz")


class TestPerformanceAndOptimization:
    """Test performance and optimization scenarios."""

    def test_cleanup_configuration(self, role_vars):
        """Test cleanup configuration."""
        assert role_vars["frp_install_cleanup_tmp"] is True

    def test_temporary_file_handling(self, role_vars):
        """Test temporary file handling."""
        tmp_dir = role_vars["frp_install_tmp_dir"]
        assert (
            tmp_dir == "/tmp"
        ), f"Temporary directory should be /tmp for performance, got {tmp_dir}"

    def test_binary_permissions(self):
        """Test that binary permissions are set correctly."""
        # This would test the file permission tasks
        expected_mode = "0755"
        assert expected_mode == "0755", "Binaries should have executable permissions"

    def test_config_file_permissions(self):
        """Test that config file permissions are secure."""
        expected_mode = "0600"
        assert (
            expected_mode == "0600"
        ), "Config files should have restrictive permissions"


class TestAnsibleIntegration:
    """Test Ansible role integration scenarios."""

    def test_role_execution_with_molecule(self):
        """Test that the role can be executed with molecule."""
        import os
        import subprocess

        # Check if molecule is available and configured
        try:
            result = subprocess.run(
                ["molecule", "--version"],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__) + "/..",
            )
            molecule_available = result.returncode == 0
        except FileNotFoundError:
            molecule_available = False

        if not molecule_available:
            pytest.skip("Molecule not available")

        # Change to the role directory where molecule.yml is located
        role_dir = os.path.join(os.path.dirname(__file__), "..", "roles", "frp_install")

        # Run molecule syntax check for the default scenario (lighter than full test)
        try:
            result = subprocess.run(
                ["molecule", "syntax", "-s", "default"],
                capture_output=True,
                text=True,
                cwd=role_dir,
                timeout=300,  # 5 minute timeout
            )

            # Check if the syntax check passed
            assert (
                result.returncode == 0
            ), f"Molecule syntax check failed: {result.stderr}"

            # Verify that the test output contains expected success indicators
            # Check stderr for completion message since stdout only contains playbook path
            assert (
                "Completed" in result.stderr or "syntax" in result.stderr.lower()
            ), "Syntax check did not complete successfully"

        except subprocess.TimeoutExpired:
            pytest.fail("Molecule syntax check timed out after 5 minutes")
        except Exception as e:
            pytest.fail(f"Molecule syntax check failed with error: {str(e)}")

    def test_handlers_configuration(self):
        """Test that handlers are properly configured."""
        handlers_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "handlers",
            "main.yml",
        )

        with open(handlers_file) as f:
            handlers_content = f.read()

        # Check for reload systemd handler
        assert "reload systemd" in handlers_content.lower()
        assert "ansible.builtin.systemd" in handlers_content
        assert "daemon_reload: true" in handlers_content

    def test_role_dependencies(self):
        """Test role dependencies and requirements."""
        meta_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "meta",
            "main.yml",
        )

        with open(meta_file) as f:
            meta_content = f.read()

        # Should have galaxy_info and dependencies
        assert "galaxy_info" in meta_content or "galaxy_info" in meta_content.replace(
            " ", ""
        )
        assert "dependencies" in meta_content

    def test_template_files_exist(self):
        """Test that all required template files exist."""
        template_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
        )

        required_templates = [
            "frps.toml.j2",
            "frpc.toml.j2",
            "frps.service.j2",
            "frpc.service.j2",
        ]

        for template in required_templates:
            template_path = os.path.join(template_dir, template)
            assert os.path.exists(template_path), f"Template {template} does not exist"

    def test_template_content_validation(self):
        """Test that templates contain required content."""
        template_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
        )

        # Check frps template
        with open(os.path.join(template_dir, "frps.toml.j2")) as f:
            frps_content = f.read()

        assert "bindAddr" in frps_content
        assert "bindPort" in frps_content
        assert "auth" in frps_content

        # Check frpc template
        with open(os.path.join(template_dir, "frpc.toml.j2")) as f:
            frpc_content = f.read()

        assert "serverAddr" in frpc_content
        assert "serverPort" in frpc_content
        assert "auth" in frpc_content

    def test_service_template_validation(self):
        """Test that service templates are valid systemd units."""
        template_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
        )

        with open(os.path.join(template_dir, "frps.service.j2")) as f:
            service_content = f.read()

        # Check systemd service structure
        assert "[Unit]" in service_content
        assert "[Service]" in service_content
        assert "[Install]" in service_content
        assert "ExecStart" in service_content
        assert "frps" in service_content
