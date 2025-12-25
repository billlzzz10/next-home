#!/usr/bin/env python
"""
Bl1nk Architect Monitoring Dashboard

Real-time health monitoring using Streamlit
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, '/home/user/projects/bl1nk-architect')

from src.health_check import run_health_check

# Page config
st.set_page_config(
    page_title="Bl1nk Architect Monitor",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .status-ok {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def get_status_color(status: str):
    """Get color for status"""
    if status == "ok":
        return "green"
    elif status == "warning":
        return "orange"
    else:
        return "red"

def get_status_emoji(status: str):
    """Get emoji for status"""
    if status == "ok":
        return "✅"
    elif status == "warning":
        return "⚠️"
    else:
        return "❌"

async def fetch_health_data():
    """Fetch health check data"""
    result = await run_health_check()
    return result

def main():
    """Main dashboard"""
    st.title("🏗️ Bl1nk Architect Monitor")
    st.markdown("Real-time system health and configuration monitoring")
    
    # Sidebar
    st.sidebar.header("⚙️ Settings")
    auto_refresh = st.sidebar.checkbox("Auto refresh", value=True)
    refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
    
    # Fetch health data
    try:
        health_data = asyncio.run(fetch_health_data())
    except Exception as e:
        st.error(f"Error fetching health data: {str(e)}")
        return
    
    # Overall status
    col1, col2, col3, col4 = st.columns(4)
    
    summary = health_data["summary"]
    
    with col1:
        st.metric("Total Checks", summary["total_checks"])
    
    with col2:
        st.metric("✓ OK", summary["ok"], delta=None)
    
    with col3:
        st.metric("⚠️ Warning", summary["warning"], delta=None)
    
    with col4:
        st.metric("❌ Error", summary["error"], delta=None)
    
    # Overall status card
    overall_status = health_data["overall_status"]
    status_emoji = get_status_emoji(overall_status)
    status_color = get_status_color(overall_status)
    
    st.markdown(f"""
    <div style="background-color: {status_color}20; border: 2px solid {status_color}; padding: 20px; border-radius: 10px;">
        <h2 style="color: {status_color};">{status_emoji} Overall Status: {overall_status.upper()}</h2>
        <p>Last updated: {health_data['timestamp']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed checks
    st.header("📋 Detailed Status")
    
    checks = health_data["checks"]
    
    # Create tabs for each check
    tabs = st.tabs(list(checks.keys()))
    
    for tab, (check_name, check_data) in zip(tabs, checks.items()):
        with tab:
            status = check_data["status"]
            emoji = get_status_emoji(status)
            color = get_status_color(status)
            
            # Status header
            st.markdown(f"### {emoji} {check_name}")
            st.markdown(f"**Status**: <span style='color: {color};'>{status.upper()}</span>", 
                       unsafe_allow_html=True)
            st.markdown(f"**Message**: {check_data['message']}")
            
            # Details
            if check_data.get("details"):
                st.markdown("**Details**:")
                details = check_data["details"]
                
                # Format details nicely
                if isinstance(details, dict):
                    for key, value in details.items():
                        if isinstance(value, list):
                            st.write(f"**{key}** ({len(value)} items):")
                            for item in value[:5]:
                                st.write(f"  • {item}")
                            if len(value) > 5:
                                st.write(f"  ... and {len(value) - 5} more")
                        elif isinstance(value, dict):
                            st.write(f"**{key}**:")
                            for k, v in value.items():
                                st.write(f"  • {k}: {v}")
                        else:
                            st.write(f"**{key}**: {value}")
    
    # JSON view
    st.header("🔍 Raw Data")
    
    if st.checkbox("Show full JSON"):
        st.json(health_data)
    
    # Auto refresh
    if auto_refresh:
        st.info(f"Auto-refreshing every {refresh_interval} seconds...")
        import time
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
