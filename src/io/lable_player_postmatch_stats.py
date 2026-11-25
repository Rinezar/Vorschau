import pandas as pd


def label_player_postmatch_stats(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Index-Bereich deiner Post-Match-Spalten
    start_idx, end_idx = 22, 47
    postmatch_cols = df.columns[start_idx : end_idx + 1]

    # Spalten umbenennen mit Präfix "pm_"
    rename_map = {col: f"pm_{col}" for col in postmatch_cols}
    df = df.rename(columns=rename_map)

    return df
