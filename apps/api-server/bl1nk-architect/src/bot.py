"""
Poe Protocol Bot Implementation - Main Interface

Handles Poe protocol events (query, settings, report_reaction, report_error)
Manages authentication flow and workflow orchestration.
"""

import os
import logging
from fastapi import FastAPI
import fastapi_poe as fp

from src.auth import auth_router, is_user_authenticated, get_login_url
from src.orchestrator import run_architect_workflow

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Bl1nkArchitectBot(fp.PoeBot):
    """
    Main Poe bot implementing Bl1nk Architect.
    
    Workflow:
    1. Check user authentication (GitHub App)
    2. If not authenticated, show login link
    3. If authenticated, run 8-step architecture analysis
    4. Stream results as SSE events
    """

    async def get_response(self, request: fp.QueryRequest) -> fp.AsyncGenerator:
        """
        Handle user query (Poe Protocol: query request type)
        
        Yields:
            MetaResponse: Protocol metadata (content_type, suggested_replies)
            PartialResponse: Streaming text chunks
            ErrorResponse: If error occurs
        """
        try:
            # Step 1: Yield meta event (required by Poe Protocol Spec)
            yield fp.MetaResponse(
                content_type="text/markdown",
                linkify=True,
                suggested_replies=False
            )

            user_id = request.user_id
            last_message = request.query[-1].content if request.query else ""

            logger.info(f"Query from user {user_id}: {last_message[:50]}...")

            # Step 2: Check authentication
            if not is_user_authenticated(user_id):
                login_url = get_login_url(user_id)
                yield fp.PartialResponse(
                    text=f"""
🔒 **Authentication Required**

To analyze your private repositories, Bl1nk Architect needs access via the GitHub App.

👉 [**Click here to Authorize GitHub Access**]({login_url})

_After authorizing, please reply with "Start" or "Analyze" again._
                    """
                )
                return

            # Step 3: User is authenticated - start workflow
            yield fp.PartialResponse(
                text="🏗️ **Bl1nk Architect Initialized**\n\n_Connecting to GitHub & Gemini Deep Research..._\n\n"
            )

            # Step 4: Stream workflow results
            async for chunk in run_architect_workflow(last_message, user_id):
                yield fp.PartialResponse(text=chunk)

            # Step 5: Completion message
            yield fp.PartialResponse(
                text="\n\n✅ **Analysis Complete!**\n\n_Ready for next query._"
            )

        except Exception as e:
            logger.exception(f"Error processing query: {e}")
            yield fp.ErrorResponse(
                text=f"❌ Error: {str(e)}",
                allow_retry=True
            )

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        """
        Return bot configuration (Poe Protocol: settings request type)
        
        Declares dependencies, attachments support, introduction message, etc.
        """
        return fp.SettingsResponse(
            server_bot_dependencies={
                "Gemini-1.5-Pro": 1,  # Deep Research
            },
            allow_attachments=True,
            expand_text_attachments=True,
            enable_image_comprehension=False,
            introduction_message=(
                "🏗️ **Welcome to Bl1nk Architect**\n\n"
                "I analyze your GitHub repositories and create architecture plans using AI-powered deep research.\n\n"
                "✨ Features:\n"
                "• Dependency auditing (Python, TypeScript, etc.)\n"
                "• Code duplication detection\n"
                "• 8-step refactoring plan\n"
                "• Integration recommendations\n\n"
                "To get started, please authenticate with GitHub."
            ),
            response_version=1,
        )

    async def on_feedback(self, feedback: fp.FeedbackRequest) -> None:
        """Log feedback (optional)"""
        logger.info(f"Feedback from {feedback.user_id}: {feedback.feedback_type}")

    async def on_error(self, error: fp.ErrorRequest) -> None:
        """Log errors"""
        logger.error(f"Error for message {error.message_id}: {error.error_message}")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Bl1nk Architect",
        description="GitHub repository architecture analysis bot for Poe",
        version="0.1.0",
    )

    # Include auth routes (GitHub callback)
    app.include_router(auth_router, prefix="/auth", tags=["authentication"])

    # Setup Poe bot
    access_key = os.getenv("POE_ACCESS_KEY")
    if not access_key:
        raise ValueError("POE_ACCESS_KEY environment variable not set")

    fp.make_app(
        Bl1nkArchitectBot(),
        access_key=access_key,
        app=app,
        allow_without_key=False,
    )

    # Health check endpoint
    @app.get("/health")
    async def health():
        return {"status": "healthy", "version": "0.1.0"}

    logger.info("Bl1nk Architect bot initialized")
    return app


# Add to imports
# from src.attachment_handler import AttachmentHandler

# Example of sending attachment in response:
async def create_architecture_report_with_attachment(
    self,
    report_content: str,
    user_id: str
) -> bytes:
    """
    Create architecture report and prepare as attachment.
    
    Args:
        report_content: Markdown report content
        user_id: User ID (for context)
        
    Returns:
        Report as bytes for attachment
    """
    from src.attachment_handler import AttachmentHandler
    
    handler = AttachmentHandler()
    file_bytes, filename = await handler.prepare_markdown_file(
        report_content,
        filename=f"architecture_analysis_{user_id[:8]}.md"
    )
    
    return file_bytes


# Add to get_settings method
async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
    """Return bot settings including introduction message"""
    from src.introduction_manager import IntroductionMessages
    
    return fp.SettingsResponse(
        response_version=1,
        server_bot_dependencies={"Gemini-1.5-Pro": 1},
        allow_attachments=True,
        expand_text_attachments=True,
        enable_image_comprehension=False,
        introduction_message=IntroductionMessages.MAIN,
    )
