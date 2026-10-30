# fastapi-blueprint

GitHub template for a FastAPI backend service.

## Start a service from it

1. **Use this template** on GitHub.
2. Set `name` and `description` in `pyproject.toml`, then run `uv lock`.
3. `cp .env.example .env` and set `PROJECT_NAME`.

The code imports the package as `app`. The service name comes only from settings, so nothing in the code needs renaming.

## Develop

```sh
uv sync
uv run prek install
uv run fastapi dev app/main.py
uv run pytest
uv run prek run -a
```

## Dependencies

Every dependency is pinned with `==`, and `uv.lock` pins transitive ones. Dependabot (`.github/dependabot.yml`) bumps them weekly. The prek hooks are prek's builtins and local `uv run` hooks, so Dependabot's uv updates keep them current too.
