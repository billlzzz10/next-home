#!/bin/bash
echo "🏗️ Bl1nk Architect - Starting..."
source venv/bin/activate
python health_check.py --quick
echo "✅ Ready! Choose: python modal_app.py OR streamlit run dashboard.py OR docker-compose up"
