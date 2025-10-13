#!/bin/bash
# SonarQube Analysis Script for wiphoo-ansible-frp
# This script runs SonarQube analysis excluding test directories

set -e

echo "🔍 Running SonarQube analysis for wiphoo-ansible-frp..."

# Check if sonar-scanner is available
if ! command -v sonar-scanner &> /dev/null; then
    echo "❌ sonar-scanner not found. Please install SonarQube Scanner CLI:"
    echo "   - Download from: https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/"
    echo "   - Or use Docker: docker run --rm -v \$(pwd):/usr/src sonarsource/sonar-scanner-cli"
    exit 1
fi

# Run analysis
sonar-scanner \
    -Dsonar.projectKey=wiphoo_Ansible-FRP \
    -Dsonar.organization=wiphoo-dev \
    -Dsonar.projectName=wiphoo-ansible-frp \
    -Dsonar.projectVersion=0.2.0 \
    -Dsonar.sources=roles,plugins,meta,scripts \
    -Dsonar.tests=tests \
    -Dsonar.test.inclusions=tests/**/*.py \
    -Dsonar.python.version=3.11,3.12 \
    -Dsonar.exclusions="**/__pycache__/**,**/htmlcov/**,**/.pytest_cache/**,**/.ruff_cache/**,**/.mypy_cache/**,**/*.pyc,**/*.pyo,**/*.pyd,**/*.tar.gz,**/collections/**,**/.ansible/**,**/.venv/**,**/.vscode/**,**/coverage.xml,**/.pre-commit-config.yaml,**/.yamllint,**/.ansible-lint,**/uv.lock,**/.nojekyll" \
    -Dsonar.coverage.exclusions=tests/**/* \
    -Dsonar.python.coverage.reportPaths=coverage.xml

echo "✅ SonarQube analysis completed!"
