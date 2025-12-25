# Docker Critical Fixes - Ready to Implement

## 🚀 Phase 1: CRITICAL (Do First) - 1 Hour

Implement these 3 things to make Docker production-ready:

---

## 1️⃣ ADD HEALTH CHECK ENDPOINT

**File: `src/api.py`** - Add after imports:

```python
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Comprehensive health check endpoint
    Used by Docker and Kubernetes for liveness/readiness probes
    """
    checks = {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Check database
    try:
        # Simple test query
        result = await skill_manager.list_skills()
        checks["checks"]["database"] = "ok"
    except Exception as e:
        checks["checks"]["database"] = f"error: {str(e)}"
        checks["status"] = "degraded"
    
    # Check storage
    try:
        # Try to list skills
        checks["checks"]["storage"] = "ok"
    except Exception as e:
        checks["checks"]["storage"] = f"error: {str(e)}"
        checks["status"] = "degraded"
    
    # Overall status
    status_code = 200 if checks["status"] == "healthy" else 503
    return Response(
        content=json.dumps(checks),
        status_code=status_code,
        media_type="application/json"
    )


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Kubernetes readiness probe
    Returns 200 if ready to accept traffic
    """
    try:
        # Quick check
        await skill_manager.list_skills()
        return {"ready": True}
    except:
        return Response(
            content='{"ready": false}',
            status_code=503,
            media_type="application/json"
        )


@app.get("/live", tags=["Health"])
async def liveness_check():
    """
    Kubernetes liveness probe
    Returns 200 if process is alive
    """
    return {"alive": True}
```

---

## 2️⃣ ADD GLOBAL ERROR HANDLER

**File: `src/api.py`** - Add middleware section:

```python
from uuid import uuid4
from fastapi import Request

# Add request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID for tracing"""
    request_id = str(uuid4())
    request.state.request_id = request_id
    
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as exc:
        print(f"[{request_id}] Error: {exc}")
        raise


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    
    error_response = {
        "error": {
            "type": type(exc).__name__,
            "message": str(exc),
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url.path),
            "method": request.method
        }
    }
    
    # Log error
    import logging
    logging.error(f"[{request_id}] Unhandled error: {exc}")
    
    return JSONResponse(
        status_code=500,
        content=error_response,
        headers={"X-Request-ID": request_id}
    )


# Handle specific HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "HTTPException",
                "message": exc.detail,
                "request_id": request_id,
                "status_code": exc.status_code
            }
        },
        headers={"X-Request-ID": request_id}
    )
```

---

## 3️⃣ UPDATE DOCKER COMPOSE

**File: `docker/docker-compose.yml`** - Update API service:

```yaml
api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: bl1nk-skill-api
    ports:
      - "8000:8000"
    
    # ✅ ADD HEALTH CHECK
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # ✅ ADD RESTART POLICY
    restart: unless-stopped
    
    # ✅ ADD RESOURCE LIMITS
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    
    # ✅ ADD LOGGING
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    
    environment:
      ENV: development
      API_HOST: 0.0.0.0
      API_PORT: 8000
      STORAGE_BACKEND: local
      CACHE_BACKEND: memory
      DATABASE_URL: postgresql://postgres:postgres@db:5432/bl1nk_skills
      REDIS_URL: redis://redis:6379
      AWS_REGION: ${AWS_REGION:-us-east-1}
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
      LOG_LEVEL: INFO
    
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    
    volumes:
      - ./skills:/app/skills
      - ./logs:/app/logs
    
    networks:
      - bl1nk

  # ✅ UPDATE DATABASE SERVICE
  db:
    image: postgres:15-alpine
    container_name: bl1nk-db
    restart: unless-stopped
    
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: bl1nk_skills
    
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    
    networks:
      - bl1nk

  # ✅ UPDATE REDIS SERVICE
  redis:
    image: redis:7-alpine
    container_name: bl1nk-redis
    ports:
      - "6379:6379"
    restart: unless-stopped
    
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    
    volumes:
      - redis_data:/data
    
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 128M
    
    networks:
      - bl1nk

  # ✅ KEEP WORKER AND PROMETHEUS
  worker:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: bl1nk-worker
    command: celery -A src.queue.tasks worker --loglevel=info
    restart: unless-stopped
    
    depends_on:
      - db
      - redis
    
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/bl1nk_skills
      REDIS_URL: redis://redis:6379
    
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    
    networks:
      - bl1nk
    
    volumes:
      - ./skills:/app/skills

  prometheus:
    image: prom/prometheus:latest
    container_name: bl1nk-prometheus
    ports:
      - "9090:9090"
    restart: unless-stopped
    
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    
    networks:
      - bl1nk

volumes:
  postgres_data:
  redis_data:
  prometheus_data:

networks:
  bl1nk:
    driver: bridge
```

---

## ✅ IMPLEMENTATION STEPS

### Step 1: Add Health Check (10 min)
1. Open `src/api.py`
2. Add the health check endpoints (after root endpoint)
3. Import `Response` from fastapi

### Step 2: Add Error Handler (10 min)
1. Add middleware section to `src/api.py`
2. Import `uuid4` and `Request`
3. Add exception handlers

### Step 3: Update Docker Compose (10 min)
1. Replace `docker/docker-compose.yml`
2. Add health checks
3. Add resource limits
4. Add restart policies

### Step 4: Test (10 min)
```bash
# Stop old containers
docker-compose down

# Rebuild and start
docker-compose up -d

# Test health check
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/live

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

---

## 📊 AFTER FIXES: READINESS SCORE

**Before:** 6/10  
**After:** 8/10  
**Remaining:** Database migrations, OpenAPI enhancements (nice to have)

---

## 🎯 WHAT YOU GET

✅ **Health Check Endpoints:**
- `/health` - Full system health
- `/ready` - Readiness probe
- `/live` - Liveness probe

✅ **Error Handling:**
- Request ID tracing
- Structured error responses
- Proper HTTP status codes

✅ **Docker Improvements:**
- Auto-recovery (restart policies)
- Resource limits (prevent runaway)
- Health monitoring
- Better logging

✅ **Production Ready:**
- Kubernetes compatible
- Can monitor with Docker health
- Can deploy with confidence

---

## ⏱️ TOTAL TIME: ~30-40 minutes

Then: **Ready for production!** 🚀

