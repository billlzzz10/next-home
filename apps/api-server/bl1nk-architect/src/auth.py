"""
GitHub App OAuth Authentication Flow

Handles user authentication via GitHub App.
"""

import os
import logging
import jwt
import time
import requests
from typing import Dict, Optional
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

logger = logging.getLogger(__name__)

auth_router = APIRouter()

# In-memory session storage
USER_SESSIONS: Dict[str, Dict] = {}


def get_login_url(poe_user_id: str) -> str:
    """Generate GitHub App installation URL with callback state"""
    app_name = os.getenv("GITHUB_APP_NAME")
    if not app_name:
        raise ValueError("GITHUB_APP_NAME environment variable not set")
    
    return f"https://github.com/apps/{app_name}/installations/new?state={poe_user_id}"


def is_user_authenticated(poe_user_id: str) -> bool:
    """Check if user has valid GitHub App authorization"""
    if poe_user_id not in USER_SESSIONS:
        return False
    
    session = USER_SESSIONS[poe_user_id]
    
    if time.time() > session.get("expires_at", 0):
        del USER_SESSIONS[poe_user_id]
        return False
    
    return True


def get_installation_id(poe_user_id: str) -> Optional[str]:
    """Get GitHub App installation ID for user"""
    if not is_user_authenticated(poe_user_id):
        return None
    return USER_SESSIONS[poe_user_id].get("installation_id")


def get_access_token(poe_user_id: str) -> Optional[str]:
    """Get cached GitHub access token for user"""
    if not is_user_authenticated(poe_user_id):
        return None
    return USER_SESSIONS[poe_user_id].get("token")


def create_jwt() -> str:
    """Create JWT for GitHub App authentication"""
    app_id = os.getenv("GITHUB_APP_ID")
    private_key = os.getenv("GITHUB_PRIVATE_KEY")
    
    if not app_id or not private_key:
        raise ValueError("GITHUB_APP_ID or GITHUB_PRIVATE_KEY not set")
    
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + 600,
        "iss": app_id
    }
    
    return jwt.encode(payload, private_key, algorithm="RS256")


def create_access_token(installation_id: str) -> str:
    """Exchange installation_id for access token"""
    jwt_token = create_jwt()
    
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return data["token"]


@auth_router.get("/callback")
async def github_callback(
    installation_id: str = Query(...),
    state: str = Query(...)
):
    """GitHub OAuth callback after user authorizes GitHub App"""
    try:
        poe_user_id = state
        
        access_token = create_access_token(installation_id)
        
        USER_SESSIONS[poe_user_id] = {
            "installation_id": installation_id,
            "token": access_token,
            "expires_at": time.time() + 3600,
        }
        
        logger.info(f"User {poe_user_id} authenticated")
        
        return HTMLResponse("""
        <html>
        <body style="background:#667eea; color:white; text-align:center; padding:50px; font-family:sans-serif;">
            <h1>✅ Connected!</h1>
            <p>GitHub App authorization successful.</p>
            <p>You can now close this window and return to Poe.</p>
        </body>
        </html>
        """)
        
    except Exception as e:
        logger.exception(f"GitHub callback error: {e}")
        return HTMLResponse(f"""
        <html>
        <body style="background:#f5222d; color:white; text-align:center; padding:50px;">
            <h1>Error</h1>
            <p>{str(e)}</p>
        </body>
        </html>
        """, status_code=400)


@auth_router.get("/status/{poe_user_id}")
async def auth_status(poe_user_id: str):
    """Check authentication status"""
    return {
        "authenticated": is_user_authenticated(poe_user_id),
        "installation_id": get_installation_id(poe_user_id)
    }
