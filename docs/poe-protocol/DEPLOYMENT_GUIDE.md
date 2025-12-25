# Poe Bot Deployment Guide

Step-by-step guide for deploying your Poe bot to production.

## Pre-Deployment Checklist

### Code Quality
- [ ] All request types handled (`query`, `settings`, `report_reaction`, `report_error`)
- [ ] Authorization header verified with correct key
- [ ] Return 501 for unknown request types
- [ ] Proper error handling with `error` events
- [ ] No hardcoded credentials (use environment variables)
- [ ] Logging configured for debugging
- [ ] Code reviewed for security issues

### Protocol Compliance
- [ ] Query responses stream SSE format correctly
- [ ] `meta` event is first in response
- [ ] `done` event always present and last
- [ ] All response times within limits:
  - [ ] Initial response ≤ 5 seconds
  - [ ] Total response ≤ 3600 seconds
  - [ ] Response size ≤ 512,000 characters
  - [ ] Total events ≤ 10,000
- [ ] JSON in event data is valid
- [ ] Content-Type header set to `text/event-stream`
- [ ] Proper HTTP status codes (200, 401, 501)

### Testing
- [ ] Unit tests pass
- [ ] Manual curl tests pass (see QUICK_REFERENCE.md)
- [ ] Settings endpoint returns valid JSON
- [ ] Query endpoint streams correct SSE format
- [ ] Error handling tested
- [ ] Attachment handling tested (if enabled)
- [ ] Timeouts configured on external calls

### Documentation
- [ ] Bot purpose documented
- [ ] Configuration documented
- [ ] API dependencies documented
- [ ] Error cases documented

---

## Platform-Specific Deployment

### Option 1: Heroku

**Setup:**
```bash
# Create app
heroku create your-bot-name
heroku config:set POE_ACCESS_KEY=your_32_char_key_here

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

**Procfile:**
```
web: gunicorn app:app --timeout 60
```

**requirements.txt:**
```
flask==2.3.0
gunicorn==20.1.0
requests==2.31.0
```

**Cost**: Free tier or $5+/month  
**Pros**: Easy deployment, built-in logging  
**Cons**: Sleeps after 30 minutes on free tier  

---

### Option 2: AWS Lambda + API Gateway

**Setup:**
```bash
# Create function
aws lambda create-function \
  --function-name poe-bot \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --environment Variables={POE_ACCESS_KEY=key123}

# Create API
aws apigateway create-rest-api --name poe-bot-api
```

**lambda_function.py:**
```python
import json
import os

ACCESS_KEY = os.environ["POE_ACCESS_KEY"]

def lambda_handler(event, context):
    # Parse request
    auth = event.get("headers", {}).get("Authorization", "")
    if auth != f"Bearer {ACCESS_KEY}":
        return {"statusCode": 401, "body": "Unauthorized"}
    
    body = json.loads(event.get("body", "{}"))
    request_type = body.get("type")
    
    if request_type == "settings":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"response_version": 1})
        }
    
    elif request_type == "query":
        # Note: Lambda has response size limits (6MB)
        # For streaming, use Lambda + API Gateway WebSocket or DynamoDB
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/event-stream"},
            "body": stream_query(body)
        }
    
    else:
        return {"statusCode": 501, "body": "Not implemented"}

def stream_query(payload):
    # Streaming not directly supported in Lambda
    # See: AWS docs on streaming responses
    return 'event: done\ndata: {}\n\n'
```

**Cost**: Free tier (1M requests), then $0.20/M  
**Pros**: Scalable, serverless  
**Cons**: Cold starts, streaming complexity  

---

### Option 3: Railway

**Setup:**
```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Create project
railway init

# Deploy
railway up

# Set environment
railway variables set POE_ACCESS_KEY=key123
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
EXPOSE 8000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```

**Cost**: Free tier with $5 credit, $0.05/hour after  
**Pros**: Simple, good free tier  
**Cons**: Limited always-free tier  

---

### Option 4: DigitalOcean App Platform

**Setup:**
```bash
# Create app.yaml
cat > app.yaml << 'EOL'
name: poe-bot
services:
- name: api
  github:
    repo: your-username/your-repo
    branch: main
  build_command: pip install -r requirements.txt
  run_command: gunicorn app:app --bind 0.0.0.0:8080
  http_port: 8080
  envs:
  - key: POE_ACCESS_KEY
    value: your_32_char_key
  http:
    routes:
    - path: /
EOL

# Deploy
doctl apps create --spec app.yaml
```

**Cost**: $5/month minimum  
**Pros**: Reliable, simple UI  
**Cons**: No free tier  

---

### Option 5: Self-Hosted (Docker)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
EXPOSE 5000

CMD ["python", "app.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  bot:
    build: .
    ports:
      - "5000:5000"
    environment:
      POE_ACCESS_KEY: ${POE_ACCESS_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Deploy:**
```bash
# Build
docker build -t poe-bot .

# Run
docker run -e POE_ACCESS_KEY=key123 -p 5000:5000 poe-bot

# Or with compose
docker-compose up -d
```

**Cost**: Depends on hosting (VPS $3-10/month)  
**Pros**: Full control, no vendor lock-in  
**Cons**: Manual scaling and monitoring  

---

## Production Best Practices

### 1. Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("POE_ACCESS_KEY")
if not ACCESS_KEY or len(ACCESS_KEY) != 32:
    raise ValueError("Invalid POE_ACCESS_KEY")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

**Never commit secrets to Git:**
```bash
# .gitignore
.env
.env.local
*.key
secrets.json
```

### 2. Logging

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use it
logger.info("Bot started")
logger.error("Error processing query", exc_info=True)
```

### 3. Monitoring

**Health Check Endpoint:**
```python
@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "healthy",
        "version": "1.0",
        "timestamp": datetime.utcnow().isoformat()
    }, 200
```

**Monitoring Services:**
- Sentry (error tracking)
- Datadog (metrics)
- LogRocket (user sessions)
- New Relic (APM)

### 4. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/", methods=["POST"])
@limiter.limit("10 per minute")
def handle():
    # ...
```

### 5. HTTPS Configuration

**Nginx reverse proxy:**
```nginx
upstream poe_bot {
    server localhost:5000;
}

server {
    listen 80;
    server_name your-bot-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-bot-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-bot-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-bot-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://poe_bot;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Streaming support
        proxy_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

**Get SSL certificate (Let's Encrypt):**
```bash
sudo apt install certbot nginx-certbot
sudo certbot certonly --nginx -d your-bot-domain.com
sudo systemctl restart nginx
```

### 6. Graceful Shutdown

```python
import signal

def graceful_shutdown(signum, frame):
    logger.info("Shutting down gracefully...")
    # Close database connections
    # Finish pending requests
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)
```

### 7. Performance Optimization

```python
# Caching
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(param):
    return result

# Connection pooling
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Async for I/O
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)
future = executor.submit(blocking_call)
```

---

## DNS & Domain Setup

1. **Get a domain**: namecheap.com, godaddy.com, etc.
2. **Point to deployment**:
   - Heroku: Add CNAME to your-app.herokuapp.com
   - AWS: Add ALIAS to API Gateway
   - DigitalOcean: Add A record to app IP
3. **Configure in Poe**: Use your domain as bot server URL

---

## Testing in Production

### Smoke Test
```python
import requests

def smoke_test():
    url = "https://your-bot-domain.com"
    
    # Test settings
    resp = requests.post(
        f"{url}/",
        json={"type": "settings"},
        headers={"Authorization": f"Bearer {KEY}"}
    )
    assert resp.status_code == 200
    
    # Test query
    resp = requests.post(
        f"{url}/",
        json={
            "type": "query",
            "version": "1.0",
            "message_id": "m-test",
            "user_id": "u-test",
            "conversation_id": "c-test",
            "query": [{"role": "user", "content": "test"}]
        },
        headers={"Authorization": f"Bearer {KEY}"},
        stream=True
    )
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers["content-type"]
    
    print("✅ Smoke test passed")

if __name__ == "__main__":
    smoke_test()
```

### Load Testing
```bash
# Install locust
pip install locust

# Create locustfile.py
# Run: locust -f locustfile.py
```

---

## Troubleshooting Deployments

### Bot not responding
1. Check logs: `heroku logs --tail`
2. Test health endpoint: `curl https://your-domain/health`
3. Verify Authorization header is correct
4. Check if bot is listening on correct port

### Timeouts
1. Increase response timeout (but keep ≤3600s total)
2. Optimize external API calls
3. Use caching to reduce latency
4. Stream responses progressively

### High memory usage
1. Reduce batch sizes
2. Use generators instead of lists
3. Clear caches periodically
4. Monitor with `top` or cloud provider tools

### SSL/Certificate issues
1. Check expiration: `openssl s_client -connect your-domain:443`
2. Renew with: `certbot renew`
3. Set up auto-renewal: `systemctl enable certbot-renew`

---

## Scaling

### Horizontal Scaling
```bash
# Docker: Run multiple instances
docker-compose up --scale api=3

# Kubernetes: Auto-scale replicas
kubectl autoscale deployment poe-bot --min=2 --max=10
```

### Load Balancing
```nginx
upstream poe_bot {
    server bot1.internal:5000;
    server bot2.internal:5000;
    server bot3.internal:5000;
    least_conn;  # Load balancing strategy
}
```

### Database
- Use read replicas for queries
- Cache frequently accessed data
- Use message queues for async processing

---

## Rollback Plan

```bash
# Git
git revert HEAD
git push

# Docker
docker pull your-registry/poe-bot:v1.0.0
docker-compose up -d

# Heroku
heroku releases
heroku rollback v123
```

---

## Monitoring Checklist

- [ ] Uptime monitoring (UptimeRobot, Pingdom)
- [ ] Error tracking (Sentry)
- [ ] Performance metrics (New Relic, Datadog)
- [ ] Log aggregation (ELK, Splunk)
- [ ] Alert thresholds set
- [ ] On-call rotation established
- [ ] Incident response documented

---

## Post-Deployment

1. **Announce**: Tell Poe users about your bot
2. **Monitor**: Watch metrics for first 24 hours
3. **Iterate**: Collect feedback and improve
4. **Update**: Add features and fix bugs
5. **Maintain**: Keep dependencies updated

