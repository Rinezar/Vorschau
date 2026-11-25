import pandas as pd


def split_prematch_postmatch(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Post-Match Spalten identifizieren
    pm_cols = [c for c in df.columns if c.startswith("pm_")]

    # Split
    postmatch_df = df[["match_id", "player_id"] + pm_cols].copy()
    main_df = df.drop(columns=pm_cols).copy()

    return main_df, postmatch_df
