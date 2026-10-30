from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


def test_liveness_reports_ok():
    client = TestClient(create_app(Settings()))

    response = client.get("/v1/liveness")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_ok_once_lifespan_started():
    with TestClient(create_app(Settings())) as client:
        response = client.get("/v1/readiness")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_unavailable_before_lifespan_starts():
    client = TestClient(create_app(Settings()))

    response = client.get("/v1/readiness")

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}


def test_readiness_is_scoped_to_each_app():
    with TestClient(create_app(Settings())):
        response = TestClient(create_app(Settings())).get("/v1/readiness")

    assert response.status_code == 503


def test_project_name_from_settings_becomes_openapi_title():
    client = TestClient(create_app(Settings(project_name="my-service")))

    assert client.get("/openapi.json").json()["info"]["title"] == "my-service"
