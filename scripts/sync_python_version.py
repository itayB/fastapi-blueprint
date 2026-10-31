import re
import sys
from pathlib import Path

ARG_LINE = re.compile(r"^ARG PYTHON_VERSION=.*$", re.MULTILINE)


def sync_dockerfile(dockerfile: str, python_version: str) -> str:
    if ARG_LINE.search(dockerfile) is None:
        raise ValueError("Dockerfile has no `ARG PYTHON_VERSION=` line")
    return ARG_LINE.sub(f"ARG PYTHON_VERSION={python_version}", dockerfile, count=1)


def main() -> int:
    python_version = Path(".python-version").read_text().strip()
    dockerfile = Path("Dockerfile")
    current = dockerfile.read_text()
    synced = sync_dockerfile(current, python_version)
    if synced == current:
        return 0
    dockerfile.write_text(synced)
    print(f"Dockerfile: set PYTHON_VERSION={python_version} from .python-version")
    return 1


if __name__ == "__main__":
    sys.exit(main())
