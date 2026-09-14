from fastapi.testclient import TestClient

from gateway.main import RATE_LIMIT, app, request_log


def test_gateway_health() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "gateway"}


def test_gateway_rejects_unauthenticated_module_request() -> None:
    request_log.clear()
    response = TestClient(app).post("/api/v1/academic/transcripts", json={})
    assert response.status_code == 401
    assert response.json()["detail"] == "Bearer token required"


def test_gateway_rate_limit_returns_429() -> None:
    request_log.clear()
    client = TestClient(app)
    responses = [client.get("/api/v1/unknown") for _ in range(RATE_LIMIT + 1)]
    assert responses[-1].status_code == 429
    assert responses[-1].json()["detail"] == "Rate limit exceeded"
