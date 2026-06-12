# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found in develop/app.py
1. API key hardcode trong code: `OPENAI_API_KEY = "sk-hardcoded-fake-key-never-do-this"`
2. Database URL hardcode: `DATABASE_URL = "postgresql://admin:password123@localhost:5432/mydb"`
3. Dùng `print()` thay vì proper logging — log ra cả secret key
4. Không có health check endpoint — platform không biết khi nào restart
5. Port cố định `8000` — không đọc từ `PORT` env var
6. Host là `localhost` thay vì `0.0.0.0` — không nhận được kết nối từ bên ngoài container
7. `reload=True` cứng — debug mode bật trong production

### Exercise 1.3: Comparison table

| Feature | Basic (❌) | Advanced (✅) | Tại sao quan trọng? |
|---------|-----------|--------------|---------------------|
| Config | Hardcode trong code | Đọc từ env vars | Bảo mật, linh hoạt theo môi trường |
| Secrets | `api_key = "sk-abc123"` | `os.getenv("OPENAI_API_KEY")` | Tránh lộ key khi push lên GitHub |
| Port | Cố định `8000` | Từ `PORT` env var | Railway/Render inject PORT tự động |
| Health check | Không có | `GET /health` | Platform tự restart khi fail |
| Shutdown | Tắt đột ngột | Graceful — hoàn thành request hiện tại | Không mất data/request đang xử lý |
| Logging | `print()` | Structured JSON | Dễ parse trong log aggregator |
| Host | `localhost` | `0.0.0.0` | Nhận kết nối từ bên ngoài container |

---

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11` (develop) / `python:3.11-slim` (production)
2. Working directory: `/app`
3. COPY requirements.txt trước vì Docker cache layer — nếu code thay đổi nhưng requirements không đổi thì không cần reinstall packages
4. CMD là default command có thể override; ENTRYPOINT là command cố định, CMD là arguments

### Exercise 2.3: Image size comparison
- Develop (single-stage): ~800 MB
- Production (multi-stage): ~160 MB
- Difference: ~80% nhỏ hơn — multi-stage chỉ giữ runtime, bỏ build tools

---

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://day12-agent-production-c760.up.railway.app
- Health check: https://day12-agent-production-c760.up.railway.app/health

---

## Part 4: API Security

### Exercise 4.1-4.3: Test results

**Không có key → 401:**
```json
{"detail": "Invalid or missing API key"}
```

**Có key → 200:**
```json
{
  "question": "What is Docker?",
  "answer": "Container là cách đóng gói app để chạy ở mọi nơi.",
  "model": "gpt-4-mini"
}
```

**Rate limit (request 11+) → 429:**
```json
{"detail": "Rate limit exceeded: 10 req/min"}
```

### Exercise 4.4: Cost guard implementation
Cost guard theo dõi số token sử dụng mỗi ngày/tháng per user.
Mỗi request ước tính cost dựa trên số token input/output.
Khi vượt budget → trả về 402 Payment Required.
Reset theo ngày (daily budget) hoặc tháng (monthly budget).

---

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes

**Health check:**
- `/health` — liveness probe: agent còn sống không → platform restart nếu fail
- `/ready` — readiness probe: agent sẵn sàng nhận traffic chưa → load balancer không route nếu fail

**Graceful shutdown:**
- Bắt SIGTERM signal
- Set `_is_ready = False` → load balancer ngừng gửi traffic mới
- Chờ in-flight requests hoàn thành (tối đa 30s)
- Exit an toàn

**Stateless design:**
- Không lưu conversation history trong memory
- Lưu session vào Redis với TTL 1 giờ
- Bất kỳ instance nào cũng đọc được session → scale tự do

**Test stateless kết quả:**
- 5 requests được xử lý bởi 3 instance khác nhau
- Session history vẫn đầy đủ sau tất cả requests
- ✅ All requests served despite different instances!
- ✅ Session history preserved across all instances via Redis!
