#!/bin/bash
set -e

echo "🚀 Setting up Bl1nk Architect development environment..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"

# Create .env if doesn't exist
if [ ! -f .env ]; then
  echo "📝 Creating .env file..."
  cp .env.example .env
  echo "⚠️  Please configure .env file with your credentials"
fi

# Create directories
echo "📁 Creating required directories..."
mkdir -p /home/user/skills
mkdir -p logs
mkdir -p data

# Run health check
echo "🏥 Running health check..."
python health_check.py --quick

echo ""
echo "✅ Development environment ready!"
echo ""
echo "Next steps:"
echo "  1. Configure .env file"
echo "  2. Run: python health_check.py"
echo "  3. Run: python modal_app.py (for local development)"
echo "  4. Run: streamlit run dashboard.py (for monitoring)"
