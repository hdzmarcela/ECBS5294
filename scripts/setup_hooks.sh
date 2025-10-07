#!/bin/bash
#
# Setup Git Hooks for ECBS5294
#
# This script installs the pre-commit hook that prevents
# accidental commits of unencrypted solution files.
#
# Usage: ./scripts/setup_hooks.sh
#

set -e

echo "Setting up git hooks for ECBS5294..."
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "   Run this script from the repository root"
    exit 1
fi

# Check if hook file exists in scripts directory
if [ ! -f ".git/hooks/pre-commit" ]; then
    echo "❌ Error: Pre-commit hook not found at .git/hooks/pre-commit"
    echo "   The hook should have been created already"
    exit 1
fi

# Make hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed and activated"
echo ""
echo "What this hook does:"
echo "  ✅ Blocks commits of *_solution.ipynb files"
echo "  ✅ Blocks commits of *_solution.py files"
echo "  ✅ Allows commits of encrypted solutions-*.zip files"
echo "  ✅ Verifies ZIP files are password-protected"
echo ""
echo "To test the hook:"
echo "  1. Try to commit a solution file (will be blocked):"
echo "     touch test_solution.ipynb"
echo "     git add test_solution.ipynb"
echo "     git commit -m \"test\" "
echo "     # Should be blocked!"
echo ""
echo "  2. Check solution status:"
echo "     python scripts/list_solutions.py"
echo ""
echo "✅ Setup complete!"
