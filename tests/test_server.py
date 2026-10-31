import pytest
import uvicorn

from app import __main__ as entrypoint
from app.settings import Settings


def test_settings_default_to_loopback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HOST", raising=False)
    monkeypatch.delenv("PORT", raising=False)

    settings = Settings(_env_file=None)

    assert (settings.host, settings.port) == ("127.0.0.1", 8000)


def test_settings_read_host_and_port_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "9000")

    settings = Settings(_env_file=None)

    assert (settings.host, settings.port) == ("0.0.0.0", 9000)


def test_main_runs_uvicorn_with_app_import_string(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
    monkeypatch.setattr(
        uvicorn, "run", lambda *args, **kwargs: calls.append((args, kwargs))
    )
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "9000")

    entrypoint.main()

    assert calls == [(("app.main:app",), {"host": "0.0.0.0", "port": 9000})]
