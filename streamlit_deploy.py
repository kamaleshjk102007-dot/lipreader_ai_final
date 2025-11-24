"""
Streamlit deployment entry point
For Streamlit Cloud deployment
"""
import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the frontend
from frontend import app

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "frontend/app.py"]
    sys.exit(stcli.main())

