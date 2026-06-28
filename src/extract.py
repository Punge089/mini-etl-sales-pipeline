"""Extract module for loading raw sales data."""

from pathlib import Path
import pandas as pd


def load_sales_data(file_path: str | Path) -> pd.DataFrame:
    """Load raw sales data from a CSV file.

    Args:
        file_path: Path to the raw CSV file.

    Returns:
        A pandas DataFrame containing raw sales records.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    return pd.read_csv(path)
