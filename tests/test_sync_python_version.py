import pytest

from scripts.sync_python_version import sync_dockerfile


def test_sync_dockerfile_replaces_python_version_arg():
    dockerfile = "ARG PYTHON_VERSION=3.14.1\nFROM python:${PYTHON_VERSION}-slim\n"

    assert sync_dockerfile(dockerfile, "3.15.2") == (
        "ARG PYTHON_VERSION=3.15.2\nFROM python:${PYTHON_VERSION}-slim\n"
    )


def test_sync_dockerfile_rejects_dockerfile_without_python_version_arg():
    with pytest.raises(ValueError, match="ARG PYTHON_VERSION"):
        sync_dockerfile("FROM python:3.15-slim\n", "3.15.2")
