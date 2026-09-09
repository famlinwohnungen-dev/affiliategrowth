#!/bin/bash
# GitHub Setup Script for affiliate-intelligence
# Run this from your local affiliate-intelligence folder

set -e

echo "=========================================="
echo "Affiliate Intelligence — GitHub Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found"
    echo "Make sure you're in the affiliate-intelligence directory"
    exit 1
fi

echo "✓ Found project files"
echo ""

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git repository already exists"
fi

echo ""
echo "Adding all files..."
git add .
echo "✓ Files staged"

echo ""
echo "Creating initial commit..."
git commit -m "feat: Phase 1 niche generation MVP

- 162 DACH niche seeds from affiliate categories
- Pydantic models for validation and serialization
- CSV/JSON export pipeline for data review
- Pytest test suite with full coverage
- SETUP.md with detailed installation instructions
- Configuration for uv and pip
- Ready for Phase 2: Affiliate Programs

This is the foundation for German affiliate market discovery.
The system validates niche selection before investing in content production.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"

echo "✓ Initial commit created"

echo ""
echo "Adding remote origin..."
git remote add origin git@github.com:famlinwohnungen-dev/affiliategrowth.git
echo "✓ Remote added"

echo ""
echo "Setting default branch to main..."
git branch -M main
echo "✓ Branch renamed to main"

echo ""
echo "Pushing to GitHub..."
git push -u origin main
echo "✓ Pushed to GitHub"

echo ""
echo "=========================================="
echo "✅ SUCCESS"
echo "=========================================="
echo ""
echo "Repository is now live at:"
echo "https://github.com/famlinwohnungen-dev/affiliategrowth"
echo ""
echo "Next steps:"
echo "1. Verify on GitHub (should see all files)"
echo "2. Run: python main.py (to generate niches locally)"
echo "3. Review data/NICHE_GENERATION_REPORT.md"
echo "4. When ready for Phase 2, let me know"
echo ""
