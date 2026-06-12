# Deployment Information

## Public URL
https://day12-agent-production-c760.up.railway.app

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://day12-agent-production-c760.up.railway.app/health
# Expected: {"status": "ok", ...}
```

### API Test (no auth → 401)
```bash
curl -X POST https://day12-agent-production-c760.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected: 401 Unauthorized
```

### API Test (with auth → 200)
```bash
curl -X POST https://day12-agent-production-c760.up.railway.app/ask \
  -H "X-API-Key: demo-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
# Expected: 200 OK with answer
```

## Environment Variables Set
- `PORT` — injected by Railway automatically
- `AGENT_API_KEY` — API key for authentication
- `ENVIRONMENT` — production
- `REDIS_URL` — Redis connection string

## Local Development

```bash
# Clone repo
git clone https://github.com/Vrioustai/day12_ha-tang-cloud_va_deployment-main
cd day12_ha-tang-cloud_va_deployment-main/06-lab-complete

# Setup env
cp .env.example .env

# Run with Docker Compose
docker compose up -d

# Test
curl http://localhost:8000/health
```
