import numpy as np
import pandas as pd


def add_match_id(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["tourney_date", "match_num"], ignore_index=True)
    df["match_id"] = np.arange(len(df), dtype=np.int32) + 1
    return df