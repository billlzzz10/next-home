#!/usr/bin/env python3
"""
FastAPI Server for BL1NK MCP Tools
Exposes MCP server tools as HTTP endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import json
from src.server import get_server

# Create FastAPI app
app = FastAPI(
    title="BL1NK Skill MCP API",
    description="API for BL1NK Skill Management Center",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get server instance
server = get_server()

# Root endpoint
@app.get("/")
def root():
    """Root endpoint - API status"""
    return {
        "name": "BL1NK Skill MCP API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/docs",
            "/redoc",
            "/health",
            "/skills",
            "/run-skill",
            "/skill-info/{skill_name}"
        ]
    }

# Health check
@app.get("/health")
def health():
    """Health check endpoint"""
    info = server.get_server_info()
    return {
        "status": "healthy",
        "server": info
    }

# List skills
@app.get("/skills")
def list_skills(phase: Optional[str] = None):
    """
    List all available skills
    
    Parameters:
    - phase: Optional filter by phase (critical, integration, platform, advanced)
    """
    try:
        if phase:
            result = server.call_tool("list_skills", phase=phase)
        else:
            result = server.call_tool("list_skills")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run skill
@app.post("/run-skill/{skill_name}")
def run_skill(skill_name: str, params: Optional[Dict[str, Any]] = None):
    """
    Execute a specific skill
    
    Parameters:
    - skill_name: Name of the skill to run (required)
    - params: Optional parameters to pass to the skill
    """
    try:
        result = server.call_tool("run_skill", skill_name=skill_name, params=params or {})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get skill info
@app.get("/skill-info/{skill_name}")
def get_skill_info(skill_name: str):
    """
    Get information about a specific skill
    
    Parameters:
    - skill_name: Name of the skill
    """
    try:
        result = server.call_tool("get_skill_info", skill_name=skill_name)
        
        if not result.get("found"):
            raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# List tools
@app.get("/tools")
def list_tools():
    """Get all available tools"""
    try:
        tools = server.get_tools()
        return {
            "total": len(tools),
            "tools": tools
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get server info
@app.get("/server-info")
def get_server_info():
    """Get server information"""
    try:
        info = server.get_server_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting BL1NK Skill MCP API Server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
