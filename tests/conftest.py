"""Pytest configuration and global fixtures."""

# Import all fixtures to make them available to all test files
from fixtures import (  # noqa: F401
    all_expected_variables,
    client_template_path,
    defaults_file_path,
    expected_auth_variables,
    expected_basic_variables,
    expected_client_variables,
    expected_enable_flags,
    expected_logging_variables,
    expected_server_variables,
    expected_transport_variables,
    full_client_config,
    full_server_config,
    minimal_client_config,
    minimal_server_config,
    molecule_test_server_vars,
    role_path,
    role_vars,
    role_vars_combined,
    server_template_path,
    templates_path,
    vars_file_path,
)
