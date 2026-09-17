"""Load star-schema tables into SQLite."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.database.connection import connect
from src.utils.helpers import project_path


def load_dataframe(conn, table: str, df: pd.DataFrame) -> None:
    df.to_sql(table, conn, if_exists="replace", index=False)


def load_star_schema(
    tables: dict[str, pd.DataFrame],
    database: str | Path | None = None,
) -> None:
    conn = connect(database)
    try:
        for name, df in tables.items():
            load_dataframe(conn, name, df)
        conn.commit()
    finally:
        conn.close()


def run_sql_file(path: str | Path, database: str | Path | None = None) -> None:
    sql = Path(path).read_text(encoding="utf-8")
    conn = connect(database)
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()


def apply_analytics_sql(sql_dir: str | Path | None = None, database: str | Path | None = None) -> None:
    folder = Path(sql_dir) if sql_dir else project_path("sql")
    conn = connect(database)
    try:
        for path in sorted(folder.glob("*.sql")):
            conn.executescript(path.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()
