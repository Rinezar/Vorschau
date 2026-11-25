import pandas as pd


def remove_unnecessary_columns(df: pd.DataFrame, cols_to_remove: list[str]) -> pd.DataFrame:
    df = df.drop(columns=cols_to_remove)
    return df