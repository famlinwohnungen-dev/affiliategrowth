#!/bin/bash
# Fix the directory structure for affiliate-intelligence

cd ~/Dev/affiliategrowth

echo "Fixing directory structure..."

# Create necessary directories
mkdir -p src/models
mkdir -p src/pipelines
mkdir -p src/sources
mkdir -p src/db
mkdir -p src/config
mkdir -p src/analytics
mkdir -p src/reports
mkdir -p config
mkdir -p tests
mkdir -p data

# Move files to correct locations
echo "Moving files..."

# Move Python models
[ -f "niche.py" ] && mv niche.py src/models/niche.py && echo "✓ Moved niche.py → src/models/"

# Move pipeline
[ -f "niche_discovery.py" ] && mv niche_discovery.py src/pipelines/niche_discovery.py && echo "✓ Moved niche_discovery.py → src/pipelines/"

# Move test
[ -f "test_niche_discovery.py" ] && mv test_niche_discovery.py tests/test_niche_discovery.py && echo "✓ Moved test_niche_discovery.py → tests/"

# Move config
[ -f "niches.yaml" ] && mv niches.yaml config/niches.yaml && echo "✓ Moved niches.yaml → config/"

# Fix dotfiles (hidden files)
[ -f "gitignore" ] && mv gitignore .gitignore && echo "✓ Renamed gitignore → .gitignore"
[ -f "env.example" ] && mv env.example .env.example && echo "✓ Renamed env.example → .env.example"

# Create __init__ files if they don't exist
touch src/__init__.py
touch src/models/__init__.py
touch src/pipelines/__init__.py
touch src/sources/__init__.py
touch src/db/__init__.py
touch src/config/__init__.py
touch src/analytics/__init__.py
touch src/reports/__init__.py
touch tests/__init__.py

echo ""
echo "Checking structure..."
ls -la | grep -E "^d.*src|config|tests"
echo ""
echo "✅ Structure fixed!"
echo ""
echo "Now run: python3 main.py"
