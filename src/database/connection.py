"""SQLite connection helpers. Swap DSN for PostgreSQL / SQL Server in production."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from src.utils.helpers import load_config, project_path


def get_sqlite_path() -> Path:
    config = load_config()
    path = project_path(config["paths"]["sqlite_path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect(database: str | Path | None = None) -> sqlite3.Connection:
    path = Path(database) if database else get_sqlite_path()
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
