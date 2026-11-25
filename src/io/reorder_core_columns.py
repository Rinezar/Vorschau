import pandas as pd


def reorder_core_columns(df: pd.DataFrame, preferred_order: list[str]) -> pd.DataFrame:
    # nur existierende Spalten aus der Wunschliste nehmen
    head = [c for c in preferred_order if c in df.columns]
    # Rest anhängen
    tail = [c for c in df.columns if c not in head]
    return df.loc[:, head + tail]