import time
from collections import defaultdict, deque

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

app = FastAPI(title="School ERP API Gateway", version="1.0.0")
RATE_LIMIT = 10
WINDOW_SECONDS = 60
request_log: dict[str, deque[float]] = defaultdict(deque)
ROUTES = {
    "/api/v1/auth": "http://auth-service:8001",
    "/api/v1/academic": "http://academic-service:8002",
    "/api/v1/finance": "http://finance-service:8003",
    "/api/v1/hr": "http://hr-service:8004",
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "gateway"}


@app.api_route("/api/v1/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request) -> Response:
    full_path = f"/api/v1/{path}"
    client_ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    timestamps = request_log[client_ip]
    while timestamps and now - timestamps[0] >= WINDOW_SECONDS:
        timestamps.popleft()
    if len(timestamps) >= RATE_LIMIT:
        return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
    timestamps.append(now)

    upstream = next((url for prefix, url in ROUTES.items() if full_path.startswith(prefix)), None)
    if upstream is None:
        return JSONResponse({"detail": "Route not found"}, status_code=404)
    target = upstream + full_path[len(next(prefix for prefix in ROUTES if full_path.startswith(prefix))):]
    body = await request.body()
    headers = {key: value for key, value in request.headers.items() if key.lower() != "host"}
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.request(request.method, target, params=request.query_params, content=body, headers=headers)
    response_headers = {key: value for key, value in response.headers.items() if key.lower() not in {"content-length", "transfer-encoding", "connection"}}
    return Response(response.content, status_code=response.status_code, headers=response_headers, media_type=response.headers.get("content-type"))
