# Contributing

## prek hooks

Checks run through [prek](https://prek.j178.dev), a faster drop-in replacement for `pre-commit` that reads `.pre-commit-config.yaml`.

prek is a dev dependency, so `uv sync` installs it into `.venv`. To have it on your `PATH` outside the project as well:

```sh
uv tool install prek
```

Enable the hooks once per clone:

```sh
uv run prek install
```

The hooks then run at each commit on the files you changed. To run them yourself:

```sh
uv run prek run --all-files    # every hook, every file
uv run prek run <hook-id>      # one hook
```

If this clone already has `pre-commit` hooks installed, `uv run prek install -f` replaces them.

For shell completion, add one of these to `~/.zshrc` or `~/.bashrc`:

```sh
eval "$(COMPLETE=zsh prek)"
eval "$(COMPLETE=bash prek)"
```
