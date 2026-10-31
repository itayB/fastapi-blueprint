# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.15.2

FROM ghcr.io/astral-sh/uv:0.13.6 AS uv

FROM python:${PYTHON_VERSION}-slim-trixie AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

COPY --from=uv /uv /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-dev

FROM python:${PYTHON_VERSION}-slim-trixie

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    HOST=0.0.0.0

RUN useradd --system --uid 10001 --no-create-home app

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY pyproject.toml ./
COPY app ./app
COPY migrations ./migrations

USER app

EXPOSE 8000
CMD ["python", "-m", "app"]
