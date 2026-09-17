"""Re-export dashboard JSON and Excel packs from processed files."""

from scripts.run_pipeline import run_pipeline


if __name__ == "__main__":
    run_pipeline()
    print("Dashboard data exported")
