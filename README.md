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

## Releases

Every push to `master` that contains a `feat:` or `fix:` commit since the last tag (or `perf:`, `refactor:`, or a breaking `!`) gets a new `vX.Y.Z` tag and a GitHub release with a generated changelog. `.github/workflows/release.yml` computes the version with commitizen and creates the tag through the release, so no version-bump commit is added. The version lives only in git tags; `version` in `pyproject.toml` stays `0.0.0`.

While the version is below 1.0, `feat:` and breaking changes bump the minor version and everything else bumps the patch version. The `commit-msg` hook rejects messages that are not conventional commits. Pull requests are squash-merged, so the PR title is what lands on `master` and must follow the same format.
