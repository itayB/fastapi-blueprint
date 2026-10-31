from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


def test_liveness_reports_ok() -> None:
    client = TestClient(create_app(Settings()))

    response = client.get("/v1/liveness")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_ok_once_lifespan_started() -> None:
    with TestClient(create_app(Settings())) as client:
        response = client.get("/v1/readiness")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_unavailable_before_lifespan_starts() -> None:
    client = TestClient(create_app(Settings()))

    response = client.get("/v1/readiness")

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}


def test_readiness_is_scoped_to_each_app() -> None:
    with TestClient(create_app(Settings())):
        response = TestClient(create_app(Settings())).get("/v1/readiness")

    assert response.status_code == 503


def test_project_name_from_settings_becomes_openapi_title() -> None:
    client = TestClient(create_app(Settings(project_name="my-service")))

    assert client.get("/openapi.json").json()["info"]["title"] == "my-service"


def test_responses_over_1000_bytes_are_gzipped() -> None:
    app = create_app(Settings())
    app.add_api_route("/large", lambda: PlainTextResponse("x" * 1_001))
    client = TestClient(app)

    response = client.get("/large", headers={"Accept-Encoding": "gzip"})

    assert response.headers["content-encoding"] == "gzip"
    assert response.text == "x" * 1_001


def test_small_responses_are_not_gzipped() -> None:
    client = TestClient(create_app(Settings()))

    response = client.get("/v1/liveness", headers={"Accept-Encoding": "gzip"})

    assert "content-encoding" not in response.headers
