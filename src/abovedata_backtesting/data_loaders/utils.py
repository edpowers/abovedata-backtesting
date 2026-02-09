from functools import lru_cache
from pathlib import Path


@lru_cache
def find_project_root() -> Path:
    current_dir = Path.cwd()
    while not (current_dir / ".git").exists():
        current_dir = current_dir.parent
    return current_dir


def safe_float(val: object) -> float | None:
    if val is None:
        return None
    try:
        f = float(val)  # type: ignore[arg-type]
        return f if f == f else None  # NaN check
    except (ValueError, TypeError):
        return None


def safe_int(val: object) -> int | None:
    if val is None:
        return None
    try:
        return int(val)  # type: ignore[arg-type]
    except (ValueError, TypeError):
        return None


data_root = find_project_root().joinpath("data")
