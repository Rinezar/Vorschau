import pandas as pd


def extract_tourney_dates(df: pd.DataFrame) -> pd.DataFrame:
    if "tourney_date" not in df.columns:
        return df  # nichts zu tun

    # In datetime umwandeln
    df["tourney_date"] = pd.to_datetime(df["tourney_date"].astype(str), format="%Y%m%d", errors="coerce")

    # Neue Spalten anlegen
    df["tourney_year"] = df["tourney_date"].dt.year
    df["tourney_month"] = df["tourney_date"].dt.month
    df["tourney_week"] = df["tourney_date"].dt.isocalendar().week.astype(int)

    return df