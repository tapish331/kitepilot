from fastapi.testclient import TestClient

from kitepilot_api.main import app


def test_health_ok() -> None:
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
