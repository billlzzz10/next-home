"""
Health Check API Endpoints

Expose health checks via FastAPI endpoints:
- GET /health - Basic health check
- GET /health/full - Complete health check report
- GET /health/status/{check_name} - Specific check
- GET /health/summary - Summary only
"""

from fastapi import APIRouter, HTTPException
from src.health_check import get_health_checker, run_health_check
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health():
    """Basic health check - returns 200 if healthy"""
    try:
        checker = get_health_checker()
        if not checker.results:
            await checker.check_basic_health()
        
        summary = checker.get_summary()
        
        if summary["overall_status"] == "error":
            raise HTTPException(status_code=503, detail="Service unhealthy")
        
        return {
            "status": "healthy",
            "overall_status": summary["overall_status"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/full")
async def health_full():
    """Complete health check report"""
    try:
        summary = await run_health_check()
        return summary
    except Exception as e:
        logger.error(f"Full health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{check_name}")
async def health_status(check_name: str):
    """Get specific health check status"""
    try:
        checker = get_health_checker()
        
        if not checker.results:
            await checker.run_all_checks()
        
        check_result = checker.results.get(check_name)
        
        if not check_result:
            raise HTTPException(status_code=404, detail=f"Check not found: {check_name}")
        
        return {
            "check": check_name,
            "status": check_result.status,
            "message": check_result.message,
            "details": check_result.details,
            "timestamp": check_result.timestamp.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
async def health_summary():
    """Get health check summary only"""
    try:
        summary = await run_health_check()
        return {
            "overall_status": summary["overall_status"],
            "summary": summary["summary"],
            "timestamp": summary["timestamp"]
        }
    except Exception as e:
        logger.error(f"Summary error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lint")
async def health_lint():
    """Get lint check details"""
    try:
        checker = get_health_checker()
        
        if "Lint Check" not in checker.results:
            await checker.check_lint()
        
        result = checker.results.get("Lint Check")
        
        if not result:
            raise HTTPException(status_code=500, detail="Lint check failed")
        
        return {
            "check": "Lint Check",
            "status": result.status,
            "message": result.message,
            "details": result.details
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lint check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/skills")
async def health_skills():
    """Get skills check details"""
    try:
        checker = get_health_checker()
        
        if "Skill Check" not in checker.results:
            await checker.check_skills()
        
        result = checker.results.get("Skill Check")
        
        if not result:
            raise HTTPException(status_code=500, detail="Skills check failed")
        
        return {
            "check": "Skill Check",
            "status": result.status,
            "message": result.message,
            "details": result.details
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Skills check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/webhooks")
async def health_webhooks():
    """Get webhooks check details"""
    try:
        checker = get_health_checker()
        
        if "Webhook Check" not in checker.results:
            await checker.check_webhooks()
        
        result = checker.results.get("Webhook Check")
        
        if not result:
            raise HTTPException(status_code=500, detail="Webhooks check failed")
        
        return {
            "check": "Webhook Check",
            "status": result.status,
            "message": result.message,
            "details": result.details
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhooks check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/github")
async def health_github():
    """Get GitHub check details"""
    try:
        checker = get_health_checker()
        
        if "GitHub Check" not in checker.results:
            await checker.check_github()
        
        result = checker.results.get("GitHub Check")
        
        if not result:
            raise HTTPException(status_code=500, detail="GitHub check failed")
        
        return {
            "check": "GitHub Check",
            "status": result.status,
            "message": result.message,
            "details": result.details
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"GitHub check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/deepresearch")
async def health_deepresearch():
    """Get Deep Research check details"""
    try:
        checker = get_health_checker()
        
        if "Deep Research Check" not in checker.results:
            await checker.check_deep_research()
        
        result = checker.results.get("Deep Research Check")
        
        if not result:
            raise HTTPException(status_code=500, detail="Deep Research check failed")
        
        return {
            "check": "Deep Research Check",
            "status": result.status,
            "message": result.message,
            "details": result.details
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Deep Research check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def include_health_routes(app):
    """Include health check routes in FastAPI app"""
    app.include_router(router)
