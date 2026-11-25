from pathlib import Path

import pandas as pd


def load_data(data_path: str) -> pd.DataFrame:
    data_dir = Path(data_path)
    file = data_dir / "matches_main.csv"  

    return pd.read_csv(file)
