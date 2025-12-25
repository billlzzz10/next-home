#!/bin/bash
echo "🏗️ Bl1nk Architect - Setup"
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
[ ! -f .env ] && cp .env.example .env
mkdir -p logs data /home/user/skills
python check_dependencies.py
