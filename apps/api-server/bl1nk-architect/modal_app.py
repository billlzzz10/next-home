"""
Modal Serverless Configuration for Bl1nk Architect Bot

This file deploys the Poe bot to Modal infrastructure.
Run: modal deploy modal_app.py
"""

import os
from modal import App, Image, asgi_app, Secret, Mount

# Build container image with dependencies
image = Image.debian_slim().pip_install_from_pyproject(".")

# Create Modal app
app = App("bl1nk-architect")

# Mount source code
src_mount = Mount.from_local_dir("src", remote_path="/root/src")
utils_mount = Mount.from_local_dir("utils", remote_path="/root/utils")


@app.function(
    image=image,
    mounts=[src_mount, utils_mount],
    secrets=[Secret.from_name("bl1nk-secrets")],
    cpu=2.0,
    memory=4096,
    timeout=900,  # 15 minutes
    allow_concurrent_inputs=10,
)
@asgi_app()
def fastapi_app():
    """ASGI entry point for Poe bot"""
    from src.bot import create_app
    return create_app()


# For local development
if __name__ == "__main__":
    import uvicorn
    from src.bot import create_app
    
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
