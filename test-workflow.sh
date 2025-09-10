#!/bin/bash
set -e

echo "🧪 Testing GitHub Actions workflow logic locally..."

# Set up environment
export ANSIBLE_COLLECTIONS_PATH="$PWD/collections"

echo "📦 Installing collection dependencies..."
uv run ansible-galaxy collection install community.general --force -p ./collections
uv run ansible-galaxy collection install community.docker --force -p ./collections

echo "🔍 Running ansible-lint..."
uv run ansible-lint roles/

echo "✅ Running pre-commit hooks..."
uv run pre-commit run --all-files --show-diff-on-failure

echo "🏗️  Building collection..."
uv run ansible-galaxy collection build

echo "📦 Testing collection installation..."
uv run ansible-galaxy collection install wiphoo-frp-*.tar.gz --force -p ./collections
uv run ansible-galaxy collection list -p ./collections | grep -q '^wiphoo\.frp\s'
echo "✅ wiphoo.frp collection is installed successfully"

echo "🧪 Running pytest tests..."
uv run pytest tests/ -v --cov=tests --cov-report=xml --cov-report=term-missing --junitxml=test-results.xml

echo "📊 Checking test coverage..."
uv run coverage report --fail-under=85

echo "🎉 All workflow steps completed successfully!"
