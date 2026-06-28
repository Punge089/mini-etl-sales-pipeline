"""Load module for saving cleaned data into a local SQL database."""

from pathlib import Path
import sqlite3
import pandas as pd


def save_cleaned_csv(df: pd.DataFrame, output_path: str | Path) -> None:
    """Save cleaned sales data to CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def load_to_sqlite(df: pd.DataFrame, database_path: str | Path) -> None:
    """Load cleaned sales data into a SQLite database."""
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
