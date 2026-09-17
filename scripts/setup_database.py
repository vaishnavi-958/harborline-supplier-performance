"""Create the SQLite database and apply SQL analytics objects."""

from src.database.loaders import apply_analytics_sql
from src.utils.helpers import load_config, project_path


if __name__ == "__main__":
    cfg = load_config()
    apply_analytics_sql()
    print(f"SQLite ready at {project_path(cfg['paths']['sqlite_path'])}")
