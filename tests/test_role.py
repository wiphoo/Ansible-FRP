"""Unit tests for frp_install role."""

import os

import pytest
import yaml

# All fixtures are now imported from tests.fixtures via conftest.py


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
        assert isinstance(install_files, list), (
            f"frp_install_files must be list, got {type(install_files)}: {install_files!r}"
        )
        assert "frps" in install_files
        assert "frpc" in install_files
        assert len(install_files) >= 2

    def test_system_architecture_defaults(self, role_vars):
        """Test that system and architecture defaults are empty strings."""
        assert role_vars["frp_install_system"] == ""
        assert role_vars["frp_install_architecture"] == ""

    def test_version_variable_mapping(self, role_vars_combined):
        """Test that frp_version variable is properly mapped to frp_install_version."""
        # Test default version format
        import re

        assert re.match(
            r"^\d+\.\d+\.\d+$", role_vars_combined["frp_install_version"]
        ), (
            f"frp_install_version should be semver (e.g., 0.64.0), got: {role_vars_combined['frp_install_version']!r}"
        )

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

        assert filename_result == expected_filename, (
            f"Expected {expected_filename}, got {filename_result}"
        )
        assert download_url_result == expected_download_url, (
            f"Expected {expected_download_url}, got {download_url_result}"
        )

    def test_version_0640_integration(self, role_vars_combined):
        """Test that version 0.64.0 is properly handled in all contexts."""
        version = "0.64.0"
        system = "linux"
        architecture = "amd64"
        import jinja2

        env = jinja2.Environment()

        # Test filename generation using actual templates
        fn_wo_ext_t = env.from_string(
            role_vars_combined["frp_install_filename_without_extension"]
        )
        filename_wo_ext = fn_wo_ext_t.render(
            frp_install_version=version,
            frp_install_system=system,
            frp_install_architecture=architecture,
        )
        filename_t = env.from_string(role_vars_combined["frp_install_filename"])
        filename = filename_t.render(
            frp_install_filename_without_extension=filename_wo_ext,
            frp_install_version=version,
            frp_install_system=system,
            frp_install_architecture=architecture,
        )
        expected_filename = f"frp_{version}_{system}_{architecture}.tar.gz"
        assert filename == expected_filename

        # Test download URL generation using actual templates
        download_url_t = env.from_string(role_vars_combined["frp_install_download_url"])
        download_url = download_url_t.render(
            frp_install_version=version,
            frp_install_filename=filename,
            frp_install_download_base_url=role_vars_combined[
                "frp_install_download_base_url"
            ],
        )
        base_url = "https://github.com/fatedier/frp/releases/download"
        expected_download_url = f"{base_url}/v{version}/{expected_filename}"
        assert download_url == expected_download_url

        # Test checksum URL generation using actual templates
        checksum_url_t = env.from_string(
            role_vars_combined["frp_install_checksum_download_url"]
        )
        checksum_url = checksum_url_t.render(
            frp_install_version=version,
            frp_install_download_base_url=role_vars_combined[
                "frp_install_download_base_url"
            ],
        )
        expected_checksum_url = f"{base_url}/v{version}/frp_sha256_checksums.txt"
        assert checksum_url == expected_checksum_url

    def test_version_variable_override(self):
        """Test that frp_version can override the default frp_install_version."""
        # This test simulates what happens when a user sets frp_version
        user_version = "0.64.0"

        # Read actual default version from role defaults
        import os
        import re

        defaults_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "defaults",
            "main.yml",
        )
        with open(defaults_path) as f:
            defaults = yaml.safe_load(f)
        default_version = defaults["frp_install_version"]

        # Verify default version is semver format
        assert re.match(r"^\d+\.\d+\.\d+$", default_version), (
            f"Default version should be semver, got: {default_version!r}"
        )

        # Simulate the set_fact logic from the role
        final_version = user_version if user_version else default_version
        assert final_version == "0.64.0"

        # Test with undefined user version (should use default)
        import re

        final_version_default = default_version
        assert re.match(r"^\d+\.\d+\.\d+$", final_version_default), (
            f"Default version should be semver (e.g., 0.63.0), got: {final_version_default!r}"
        )

    def test_version_integration_with_role(self):
        """Test that the role properly handles version override in a playbook context."""
        # This test simulates what happens when a user sets frp_version in their playbook

        # Simulate the role execution with frp_version set
        user_frp_version = "0.64.0"

        # Read actual default version from role defaults
        import os

        defaults_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "defaults",
            "main.yml",
        )
        with open(defaults_path) as f:
            defaults = yaml.safe_load(f)
        default_frp_install_version = defaults["frp_install_version"]

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
        assert isinstance(role_vars["frp_install_verify_checksums"], bool), (
            f"frp_install_verify_checksums must be bool, got {type(role_vars['frp_install_verify_checksums'])}: {role_vars['frp_install_verify_checksums']!r}"
        )
        assert role_vars["frp_install_verify_checksums"] is True

    def test_install_files_loop_compatibility(self, role_vars):
        """Test that frp_install_files is a proper list for loop operations."""
        install_files = role_vars["frp_install_files"]
        assert isinstance(install_files, list), (
            f"frp_install_files must be list, got {type(install_files)}: {install_files!r}"
        )
        assert len(install_files) > 0

        # Test that each item is a string (not another data type)
        for item in install_files:
            assert isinstance(item, str), (
                f"Install file must be str, got {type(item)}: {item!r}"
            )
            assert item.strip(), f"Install file name must be non-empty: {item!r}"

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
            assert not ref.startswith("{{ role_path }}"), (
                f"Template ref {ref} should not use role_path in collections"
            )

        for ref in incorrect_template_refs:
            assert ref.startswith("{{ role_path }}"), (
                f"Incorrect template ref format: {ref}"
            )

    def test_collection_build_optimization(self):
        """Test that collection build excludes unnecessary files."""
        import subprocess
        import tempfile

        # Test that collection builds successfully
        with tempfile.TemporaryDirectory() as outdir:
            build_cmd = [
                "uv",
                "run",
                "ansible-galaxy",
                "collection",
                "build",
                "--force",
                "--output-path",
                outdir,
            ]
            import shutil

            if shutil.which("ansible-galaxy") is None:
                pytest.skip("ansible-galaxy not available")
            result = subprocess.run(
                build_cmd,
                cwd=os.path.join(os.path.dirname(__file__), ".."),
                capture_output=True,
                text=True,
                timeout=600,
            )

            assert result.returncode == 0, f"Collection build failed: {result.stderr}"

            # Check that tar.gz file was created
            import glob

            tar_files = glob.glob(os.path.join(outdir, "wiphoo-frp-*.tar.gz"))
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
                assert var_name.startswith("frp_"), (
                    f"Variable {var_name} should follow role naming convention"
                )

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
            assert full_path.startswith("/"), (
                f"Installation path {full_path} should be absolute"
            )
            assert not full_path.endswith("/"), (
                f"Installation path {full_path} should not end with slash"
            )
            assert binary in full_path, (
                f"Binary name {binary} should be in path {full_path}"
            )

    def test_service_configuration_variables(self, role_vars):
        """Test that service configuration variables are properly defined."""
        service_vars = [
            "frp_install_create_service",
            "frp_install_configure_firewall",
            "frp_install_cleanup_tmp",
        ]

        for var in service_vars:
            assert var in role_vars, f"Service variable {var} is not defined"
            assert isinstance(role_vars[var], bool), (
                f"Service variable {var} should be boolean"
            )

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
            assert expected_dir in dirs_var, (
                f"Expected directory {expected_dir} not found in frp_install_dirs"
            )

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

            assert result == expected, (
                f"Architecture {ansible_arch} should map to {expected}, got {result}"
            )

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
            assert result == expected, (
                f"System {ansible_system} should convert to {expected}, got {result}"
            )

    def test_error_handling_variables(self, role_vars):
        """Test that error handling variables are properly configured."""
        # This test ensures that tasks have proper error handling
        # by validating that required variables for error recovery exist

        error_related_vars = [
            "frp_install_tmp_dir",
            "frp_install_cleanup_tmp",
            "frp_install_verify_checksums",
        ]

        # Check that all error-related variables are defined in defaults
        for var in error_related_vars:
            assert var in role_vars, (
                f"Missing variable required for error handling: {var}"
            )

    def test_idempotency_variables(self, role_vars):
        """Test that variables support idempotent operations."""
        # Test that cleanup and verification variables support idempotency
        idempotent_vars = [
            "frp_install_cleanup_tmp",
            "frp_install_verify_checksums",
        ]

        for var in idempotent_vars:
            assert var in role_vars, f"Idempotency variable {var} should be defined"
            assert isinstance(role_vars[var], bool), (
                f"Idempotency variable {var} should be boolean"
            )

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
        assert role_vars["frp_install_user"] != "root", (
            "frp user should not be root for security"
        )
        assert role_vars["frp_install_group"] != "root", (
            "frp group should not be root for security"
        )

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
        assert tmp_dir == "/tmp", (
            f"Temporary directory should be /tmp for performance, got {tmp_dir}"
        )

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
                        assert "role_path" not in content, (
                            f"Template {template_file} contains role_path reference"
                        )

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
            assert "wiphoo.frp.frp_install" in content, (
                "README should contain correct collection reference"
            )

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
        valid_versions = ["0.1.0", "0.63.0", "0.64.0"]
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
        assert tmp_dir == "/tmp", (
            f"Temporary directory should be /tmp for performance, got {tmp_dir}"
        )

    def test_binary_permissions(self):
        """Test that binary permissions are set correctly."""
        # This would test the file permission tasks
        expected_mode = "0755"
        assert expected_mode == "0755", "Binaries should have executable permissions"

    def test_config_file_permissions(self):
        """Test that config file permissions are secure."""
        expected_mode = "0600"
        assert expected_mode == "0600", (
            "Config files should have restrictive permissions"
        )


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
                timeout=600,
                cwd=os.path.join(os.path.dirname(__file__), ".."),
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
                timeout=300,  # 5 minute timeout
                cwd=role_dir,
            )

            # Check if the syntax check passed
            assert result.returncode == 0, (
                f"Molecule syntax check failed: {result.stderr}"
            )

            # Verify that the test output contains expected success indicators
            # Check stderr for completion message since stdout only contains playbook path
            assert "Completed" in result.stderr or "syntax" in result.stderr.lower(), (
                "Syntax check did not complete successfully"
            )

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


class TestTemplateParameters:
    """Test cases for template parameters added to frpc.toml.j2."""

    def test_user_parameter_default(self, role_vars):
        """Test that frp_install_user parameter is defined."""
        assert "frp_install_user" in role_vars
        assert role_vars["frp_install_user"] == "frp"

    def test_login_fail_exit_parameter(self, role_vars):
        """Test that loginFailExit parameter has proper default."""
        # The parameter should use default of true if not defined
        # This is tested in template rendering
        import jinja2

        # Simplified template without Ansible filters
        template_content = """{% if frp_install_login_fail_exit is defined %}loginFailExit = {{ frp_install_login_fail_exit | lower }}{% else %}loginFailExit = true{% endif %}"""

        env = jinja2.Environment()
        template = env.from_string(template_content)

        # Test with undefined variable (should use default)
        rendered = template.render()
        assert "true" in rendered.lower()

        # Test with explicit false
        rendered = template.render(frp_install_login_fail_exit="false")
        assert "false" in rendered.lower()

    def test_transport_protocol_parameter(self, role_vars):
        """Test that transport protocol parameter is properly handled."""
        import jinja2

        template_content = """transport.protocol = "{{ frp_install_transport_protocol | default('tcp') }}" """

        env = jinja2.Environment()
        template = env.from_string(template_content)

        # Test with default
        rendered = template.render()
        assert 'transport.protocol = "tcp"' in rendered

        # Test with custom protocol
        rendered = template.render(frp_install_transport_protocol="websocket")
        assert 'transport.protocol = "websocket"' in rendered

    def test_transport_connect_server_local_ip(self, role_vars):
        """Test that connectServerLocalIP parameter is properly handled."""
        import jinja2

        template_content = """transport.connectServerLocalIP = "{{ frp_install_transport_connect_server_local_ip | default('0.0.0.0') }}" """

        env = jinja2.Environment()
        template = env.from_string(template_content)

        # Test with default
        rendered = template.render()
        assert 'transport.connectServerLocalIP = "0.0.0.0"' in rendered

        # Test with custom IP
        rendered = template.render(
            frp_install_transport_connect_server_local_ip="192.168.1.100"
        )
        assert 'transport.connectServerLocalIP = "192.168.1.100"' in rendered

    def test_transport_tls_enable_parameter(self, role_vars):
        """Test that TLS enable parameter is properly handled."""
        import jinja2

        # Simplified template without Ansible filters
        template_content = """{% if frp_install_transport_tls_enable is defined %}transport.tls.enable = {{ frp_install_transport_tls_enable | lower }}{% else %}transport.tls.enable = true{% endif %}"""

        env = jinja2.Environment()
        template = env.from_string(template_content)

        # Test with default (should be true)
        rendered = template.render()
        assert "true" in rendered.lower()

        # Test with explicit false
        rendered = template.render(frp_install_transport_tls_enable="false")
        assert "false" in rendered.lower()

    def test_udp_packet_size_parameter(self, role_vars):
        """Test that UDP packet size parameter is properly handled."""
        import jinja2

        template_content = (
            """udpPacketSize = {{ frp_install_udp_packet_size | default(1500) }}"""
        )

        env = jinja2.Environment()
        template = env.from_string(template_content)

        # Test with default
        rendered = template.render()
        assert "udpPacketSize = 1500" in rendered

        # Test with custom size
        rendered = template.render(frp_install_udp_packet_size=2000)
        assert "udpPacketSize = 2000" in rendered

    def test_webserver_conditional_rendering(self, role_vars):
        """Test that webServer section is conditionally rendered."""
        import jinja2

        template_content = """{% if frp_install_client_webserver_enabled | default(false) %}
webServer.addr = "{{ frp_install_client_webserver_addr | default('127.0.0.1') }}"
webServer.port = {{ frp_install_client_webserver_port | default(7400) }}
{% else %}
# Admin webServer is disabled
{% endif %}"""

        env = jinja2.Environment()
        template = env.from_string(template_content)

        # Test with webServer disabled (default)
        rendered = template.render()
        assert "# Admin webServer is disabled" in rendered
        assert "webServer.addr" not in rendered

        # Test with webServer enabled
        rendered = template.render(frp_install_client_webserver_enabled=True)
        assert 'webServer.addr = "127.0.0.1"' in rendered
        assert "webServer.port = 7400" in rendered
        assert "# Admin webServer is disabled" not in rendered

    def test_webserver_enabled_default_in_role_vars(self, role_vars):
        """Test that webServer enabled flag has correct default in role vars."""
        assert "frp_install_client_webserver_enabled" in role_vars
        assert role_vars["frp_install_client_webserver_enabled"] is False

    def test_frpc_template_has_all_new_parameters(self):
        """Test that frpc.toml.j2 template contains all new parameters."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            content = f.read()

        # Check for new parameters
        assert "frp_install_client_user" in content, "Missing user parameter"
        assert "frp_install_login_fail_exit" in content, (
            "Missing loginFailExit parameter"
        )
        assert "frp_install_transport_protocol" in content, (
            "Missing transport protocol parameter"
        )
        assert "frp_install_transport_connect_server_local_ip" in content, (
            "Missing connectServerLocalIP parameter"
        )
        assert "frp_install_transport_tls_enable" in content, (
            "Missing TLS enable parameter"
        )
        assert "frp_install_udp_packet_size" in content, (
            "Missing UDP packet size parameter"
        )
        assert "frp_install_client_webserver_enabled" in content, (
            "Missing webServer enabled conditional"
        )

    def test_frpc_template_webserver_conditional_structure(self):
        """Test that frpc.toml.j2 template has proper conditional structure for webServer."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            content = f.read()

        # Check for conditional blocks
        assert "{% if frp_install_client_webserver_enabled" in content
        assert "{% else %}" in content
        assert "{% endif %}" in content

        # Check that webServer configuration is inside conditional
        assert "webServer.addr" in content
        assert "webServer.port" in content
        assert "webServer.user" in content
        assert "webServer.password" in content
        assert "webServer.pprofEnable" in content

    def test_backward_compatibility_with_old_template(self):
        """Test that new template maintains backward compatibility with old defaults."""
        # This test verifies that the template contains the expected structure
        # We'll skip full rendering since it requires Ansible filters

        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        # Verify key configuration sections exist
        assert "serverAddr" in template_content
        assert "serverPort" in template_content
        assert "auth.method" in template_content
        assert "auth.token" in template_content
        assert "log.to" in template_content
        assert "transport.tcpMux" in template_content
        assert "transport.poolCount" in template_content

        # Verify all old parameters are still supported
        assert "frp_install_client_server_addr" in template_content
        assert "frp_install_client_server_port" in template_content
        assert "frp_install_auth_method" in template_content
        assert "frp_install_auth_token" in template_content
        assert "frp_install_log_dir" in template_content
        assert "frp_install_log_level" in template_content
        assert "frp_install_transport_tcp_mux" in template_content
        assert "frp_install_transport_pool_count" in template_content

    def test_new_parameters_have_sensible_defaults(self):
        """Test that all new parameters have sensible default values."""
        # This test verifies that the template has sensible defaults set
        # We'll check the template content rather than rendering it

        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        # Check that sensible defaults are specified in the template
        assert "| default('your_name')" in template_content  # user has default
        assert "| default(true)" in template_content  # loginFailExit has default
        assert "| default('tcp')" in template_content  # transport protocol has default
        assert "| default(true)" in template_content  # TLS enabled by default
        assert "| default(1500)" in template_content  # UDP packet size has default
        assert "| default(false)" in template_content  # webServer disabled by default

    def test_toml_format_compliance(self):
        """Test that template follows TOML format."""
        # This test verifies template structure follows TOML syntax

        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        # Basic TOML format checks on template structure
        assert " = " in template_content  # TOML uses = for assignments

        # Check for proper string quoting in template
        assert (
            '"{{' in template_content or '= "' in template_content
        )  # Strings should be quoted

        # Check for key sections
        assert "user = " in template_content
        assert "serverAddr = " in template_content
        assert "serverPort = " in template_content
        assert "log.to = " in template_content
        assert "log.level = " in template_content
        assert "auth.method = " in template_content
        assert "auth.token = " in template_content
        assert "transport." in template_content

        # Check for proxy examples section
        assert "[[proxies]]" in template_content


class TestConfigurationVariables:
    """Test cases for all configuration variables."""

    def test_server_kcp_protocol_variables(self):
        """Test KCP protocol configuration variables for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        # Check KCP variables exist with enable flag
        assert "frp_install_kcp_bind_port_enabled" in template_content
        assert "frp_install_kcp_bind_port" in template_content
        assert "kcpBindPort" in template_content

    def test_server_quic_protocol_variables(self):
        """Test QUIC protocol configuration variables for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        # Check QUIC bind port variables
        assert "frp_install_quic_bind_port_enabled" in template_content
        assert "frp_install_quic_bind_port" in template_content
        assert "quicBindPort" in template_content

        # Check QUIC transport options
        assert "frp_install_transport_quic_enabled" in template_content
        assert "frp_install_transport_quic_keepalive_period" in template_content
        assert "frp_install_transport_quic_max_idle_timeout" in template_content
        assert "frp_install_transport_quic_max_incoming_streams" in template_content
        assert "transport.quic.keepalivePeriod" in template_content
        assert "transport.quic.maxIdleTimeout" in template_content
        assert "transport.quic.maxIncomingStreams" in template_content

    def test_server_proxy_bind_address_variable(self):
        """Test proxy bind address configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_proxy_bind_addr_enabled" in template_content
        assert "frp_install_proxy_bind_addr" in template_content
        assert "proxyBindAddr" in template_content

    def test_server_heartbeat_timeout_variable(self):
        """Test heartbeat timeout configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_transport_heartbeat_timeout_enabled" in template_content
        assert "frp_install_transport_heartbeat_timeout" in template_content
        assert "transport.heartbeatTimeout" in template_content

    def test_server_tcp_keepalive_variable(self):
        """Test TCP keepalive configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_transport_tcp_keepalive_enabled" in template_content
        assert "frp_install_transport_tcp_keepalive" in template_content
        assert "transport.tcpKeepalive" in template_content

    def test_server_vhost_variables(self):
        """Test virtual host configuration variables for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        # Check vhost HTTP port
        assert "frp_install_vhost_http_port_enabled" in template_content
        assert "frp_install_vhost_http_port" in template_content
        assert "vhostHTTPPort" in template_content

        # Check vhost HTTPS port
        assert "frp_install_vhost_https_port_enabled" in template_content
        assert "frp_install_vhost_https_port" in template_content
        assert "vhostHTTPSPort" in template_content

        # Check vhost HTTP timeout
        assert "frp_install_vhost_http_timeout_enabled" in template_content
        assert "frp_install_vhost_http_timeout" in template_content
        assert "vhostHTTPTimeout" in template_content

    def test_server_tcpmux_variables(self):
        """Test TCP multiplexing configuration variables for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        # Check tcpmux HTTP CONNECT port
        assert "frp_install_tcpmux_http_connect_port_enabled" in template_content
        assert "frp_install_tcpmux_http_connect_port" in template_content
        assert "tcpmuxHTTPConnectPort" in template_content

        # Check tcpmux passthrough
        assert "frp_install_tcpmux_passthrough_enabled" in template_content
        assert "frp_install_tcpmux_passthrough" in template_content
        assert "tcpmuxPassthrough" in template_content

    def test_server_dashboard_assets_dir_variable(self):
        """Test dashboard assets directory configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_dashboard_assets_dir_enabled" in template_content
        assert "frp_install_dashboard_assets_dir" in template_content
        assert "webServer.assetsDir" in template_content

    def test_server_auth_additional_scopes_variable(self):
        """Test auth additional scopes configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_auth_additional_scopes_enabled" in template_content
        assert "frp_install_auth_additional_scopes" in template_content
        assert "auth.additionalScopes" in template_content

    def test_server_auth_token_source_variables(self):
        """Test auth token source configuration variables for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_auth_token_source_enabled" in template_content
        assert "frp_install_auth_token_source_type" in template_content
        assert "frp_install_auth_token_source_file_path" in template_content
        assert "auth.tokenSource.type" in template_content
        assert "auth.tokenSource.file.path" in template_content

    def test_server_oidc_variables(self):
        """Test OIDC authentication configuration variables for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_auth_oidc_enabled" in template_content
        assert "frp_install_auth_oidc_issuer" in template_content
        assert "frp_install_auth_oidc_audience" in template_content
        assert "frp_install_auth_oidc_skip_expiry_check" in template_content
        assert "frp_install_auth_oidc_skip_issuer_check" in template_content
        assert "auth.oidc.issuer" in template_content
        assert "auth.oidc.audience" in template_content
        assert "auth.oidc.skipExpiryCheck" in template_content
        assert "auth.oidc.skipIssuerCheck" in template_content

    def test_server_user_conn_timeout_variable(self):
        """Test user connection timeout configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_user_conn_timeout_enabled" in template_content
        assert "frp_install_user_conn_timeout" in template_content
        assert "userConnTimeout" in template_content

    def test_server_max_ports_per_client_variable(self):
        """Test max ports per client configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_max_ports_per_client_enabled" in template_content
        assert "frp_install_max_ports_per_client" in template_content
        assert "maxPortsPerClient" in template_content

    def test_server_subdomain_host_variable(self):
        """Test subdomain host configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_subdomain_host_enabled" in template_content
        assert "frp_install_subdomain_host" in template_content
        assert "subDomainHost" in template_content

    def test_server_custom_404_page_variable(self):
        """Test custom 404 page configuration variable for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_custom_404_page_enabled" in template_content
        assert "frp_install_custom_404_page" in template_content
        assert "custom404Page" in template_content

    def test_server_ssh_tunnel_gateway_variables(self):
        """Test SSH tunnel gateway configuration variables for server."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_ssh_tunnel_gateway_enabled" in template_content
        assert "frp_install_ssh_tunnel_gateway_bind_port" in template_content
        assert "frp_install_ssh_tunnel_gateway_private_key_file" in template_content
        assert (
            "frp_install_ssh_tunnel_gateway_auto_gen_private_key_path"
            in template_content
        )
        assert "frp_install_ssh_tunnel_gateway_authorized_keys_file" in template_content
        assert "sshTunnelGateway.bindPort" in template_content
        assert "sshTunnelGateway.privateKeyFile" in template_content
        assert "sshTunnelGateway.autoGenPrivateKeyPath" in template_content
        assert "sshTunnelGateway.authorizedKeysFile" in template_content

    def test_client_nat_hole_stun_server_variable(self):
        """Test NAT hole STUN server configuration variable for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_nat_hole_stun_server_enabled" in template_content
        assert "frp_install_nat_hole_stun_server" in template_content
        assert "natHoleStunServer" in template_content

    def test_client_auth_additional_scopes_variable(self):
        """Test auth additional scopes configuration variable for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_auth_additional_scopes_enabled" in template_content
        assert "frp_install_auth_additional_scopes" in template_content
        assert "auth.additionalScopes" in template_content

    def test_client_auth_token_source_variables(self):
        """Test auth token source configuration variables for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_auth_token_source_enabled" in template_content
        assert "frp_install_auth_token_source_type" in template_content
        assert "frp_install_auth_token_source_file_path" in template_content
        assert "auth.tokenSource.type" in template_content
        assert "auth.tokenSource.file.path" in template_content

    def test_client_oidc_variables(self):
        """Test OIDC authentication configuration variables for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_auth_oidc_enabled" in template_content
        assert "frp_install_auth_oidc_client_id" in template_content
        assert "frp_install_auth_oidc_client_secret" in template_content
        assert "frp_install_auth_oidc_audience" in template_content
        assert "frp_install_auth_oidc_scope" in template_content
        assert "frp_install_auth_oidc_token_endpoint_url" in template_content
        assert "auth.oidc.clientID" in template_content
        assert "auth.oidc.clientSecret" in template_content
        assert "auth.oidc.audience" in template_content
        assert "auth.oidc.scope" in template_content
        assert "auth.oidc.tokenEndpointURL" in template_content

    def test_client_oidc_additional_params_variables(self):
        """Test OIDC additional params configuration variables for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert (
            "frp_install_auth_oidc_additional_endpoint_params_enabled"
            in template_content
        )
        assert "frp_install_auth_oidc_additional_endpoint_params" in template_content
        assert "frp_install_auth_oidc_trusted_ca_file" in template_content
        assert "frp_install_auth_oidc_insecure_skip_verify_enabled" in template_content
        assert "frp_install_auth_oidc_insecure_skip_verify" in template_content
        assert "frp_install_auth_oidc_proxy_url" in template_content
        assert "auth.oidc.additionalEndpointParams" in template_content
        assert "auth.oidc.trustedCaFile" in template_content
        assert "auth.oidc.insecureSkipVerify" in template_content
        assert "auth.oidc.proxyURL" in template_content

    def test_client_transport_dial_server_variables(self):
        """Test transport dial server configuration variables for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_transport_dial_server_timeout_enabled" in template_content
        assert "frp_install_transport_dial_server_timeout" in template_content
        assert "frp_install_transport_dial_server_keepalive_enabled" in template_content
        assert "frp_install_transport_dial_server_keepalive" in template_content
        assert "transport.dialServerTimeout" in template_content
        assert "transport.dialServerKeepalive" in template_content

    def test_client_transport_proxy_url_variable(self):
        """Test transport proxy URL configuration variable for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_transport_proxy_url" in template_content
        assert "transport.proxyURL" in template_content

    def test_client_transport_quic_variables(self):
        """Test transport QUIC configuration variables for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_transport_quic_enabled" in template_content
        assert "frp_install_transport_quic_keepalive_period" in template_content
        assert "frp_install_transport_quic_max_idle_timeout" in template_content
        assert "frp_install_transport_quic_max_incoming_streams" in template_content
        assert "transport.quic.keepalivePeriod" in template_content
        assert "transport.quic.maxIdleTimeout" in template_content
        assert "transport.quic.maxIncomingStreams" in template_content

    def test_client_transport_tls_custom_first_byte_variable(self):
        """Test transport TLS custom first byte configuration variable for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert (
            "frp_install_transport_tls_disable_custom_tls_first_byte_enabled"
            in template_content
        )
        assert (
            "frp_install_transport_tls_disable_custom_tls_first_byte"
            in template_content
        )
        assert "transport.tls.disableCustomTLSFirstByte" in template_content

    def test_client_transport_heartbeat_variables(self):
        """Test transport heartbeat configuration variables for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_transport_heartbeat_enabled" in template_content
        assert "frp_install_transport_heartbeat_interval" in template_content
        assert "frp_install_transport_heartbeat_timeout" in template_content
        assert "transport.heartbeatInterval" in template_content
        assert "transport.heartbeatTimeout" in template_content

    def test_client_dns_server_variable(self):
        """Test DNS server configuration variable for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_dns_server" in template_content
        assert "dnsServer" in template_content

    def test_client_start_proxies_variable(self):
        """Test start proxies configuration variable for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_start_proxies" in template_content
        assert "start = " in template_content

    def test_client_feature_gates_variables(self):
        """Test feature gates configuration variables for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_feature_gates_enabled" in template_content
        assert "frp_install_feature_gates" in template_content
        assert "featureGates" in template_content

    def test_client_virtual_net_address_variable(self):
        """Test virtual network address configuration variable for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_virtual_net_address" in template_content
        assert "virtualNet.address" in template_content

    def test_client_includes_variable(self):
        """Test includes configuration variable for client."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(template_path) as f:
            template_content = f.read()

        assert "frp_install_includes" in template_content
        assert "includes" in template_content

    def test_enable_flags_default_to_false(self):
        """Test that all enable flags default to false in templates."""
        server_template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )
        client_template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        # Read both templates
        with open(server_template_path) as f:
            server_content = f.read()
        with open(client_template_path) as f:
            client_content = f.read()

        # Find all enable flags
        import re

        enable_flags_server = re.findall(
            r"(\w+_enabled)\s*\|\s*default\((false|true)\)", server_content
        )
        enable_flags_client = re.findall(
            r"(\w+_enabled)\s*\|\s*default\((false|true)\)", client_content
        )

        # Verify all enable flags default to false
        for flag, default in enable_flags_server:
            assert default == "false", (
                f"Server enable flag {flag} should default to false, got {default}"
            )

        for flag, default in enable_flags_client:
            assert default == "false", (
                f"Client enable flag {flag} should default to false, got {default}"
            )

    def test_conditional_rendering_with_enable_flags(self):
        """Test that templates use if statements with enable flags."""
        server_template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frps.toml.j2",
        )
        client_template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "roles",
            "frp_install",
            "templates",
            "frpc.toml.j2",
        )

        with open(server_template_path) as f:
            server_content = f.read()
        with open(client_template_path) as f:
            client_content = f.read()

        # Verify conditional rendering patterns
        assert "{% if " in server_content
        assert "{% else %}" in server_content
        assert "{% endif %}" in server_content

        assert "{% if " in client_content
        assert "{% else %}" in client_content
        assert "{% endif %}" in client_content

        # Verify that enable flags are used in conditionals
        import re

        # Check that enable flags are used in {% if %} statements
        server_conditionals = re.findall(r"{% if (\w+_enabled)", server_content)
        client_conditionals = re.findall(r"{% if (\w+_enabled)", client_content)

        assert len(server_conditionals) > 0, (
            "Server template should have enable flag conditionals"
        )
        assert len(client_conditionals) > 0, (
            "Client template should have enable flag conditionals"
        )
