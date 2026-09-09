#!/bin/bash
# Complete environment setup for affiliate-intelligence
# Creates venv and installs dependencies

set -e

echo "=========================================="
echo "Affiliate Intelligence Setup"
echo "=========================================="
echo ""

# Check if in correct directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found"
    echo "Run this script from the project root directory"
    exit 1
fi

PROJECT_DIR=$(pwd)
echo "📁 Project directory: $PROJECT_DIR"
echo ""

# Check if venv already exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Remove and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        echo "✓ Removed old venv"
    else
        echo "Using existing venv"
    fi
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."

    # Try uv first (faster)
    if command -v uv &> /dev/null; then
        echo "Using uv..."
        uv venv
    else
        echo "Using standard python venv..."
        python3 -m venv venv
    fi

    echo "✓ Virtual environment created"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Activated (venv)"

echo ""
echo "Installing dependencies..."

# Minimal dependencies for Phase 1
pip install --upgrade pip setuptools wheel
pip install pydantic pyyaml

echo "✓ Core dependencies installed"

echo ""
echo "Verifying installation..."

# Test imports
python -c "import pydantic; print(f'✓ Pydantic {pydantic.__version__}')"
python -c "import yaml; print(f'✓ PyYAML installed')"

echo ""
echo "Testing project import..."

# Add project root to Python path
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# Test the import
python -c "from src.models.niche import Niche; print('✓ src.models.niche imported successfully')"
python -c "from src.pipelines.niche_discovery import main; print('✓ src.pipelines.niche_discovery imported successfully')"

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE"
echo "=========================================="
echo ""
echo "Virtual environment is active!"
echo ""
echo "To use in future terminal sessions:"
echo "  source venv/bin/activate"
echo ""
echo "To generate niches:"
echo "  python main.py"
echo ""
echo "To run tests:"
echo "  pip install pytest"
echo "  pytest tests/"
echo ""
