from pathlib import Path

import pandas as pd


DATA_PATH = (
    Path("data")
    / "retail_sales.parquet"
)


def load_retail_data() -> pd.DataFrame:

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Retail dataset not found: {DATA_PATH}"
        )

    return pd.read_parquet(DATA_PATH)