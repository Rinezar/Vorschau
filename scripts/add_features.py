import os
from pathlib import Path

import pandas as pd

from src.training_src.load_data import *
from utils import load_config
from utils.load_config import *


def merge_last_pm_stats_for_both(main_df: pd.DataFrame, pm_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fügt die Postmatch-Statistiken des letzten Spiels für player UND opponent ins main_df ein.
    - Nutzt match_id + player_id als Schlüssel
    - Verschiebt Werte pro Spieler um 1 (damit es wirklich das VORHERIGE Spiel ist)
    
    Args:
        main_df (pd.DataFrame): Haupt-Daten (man) mit target, player_id, opp_id, match_id, tourney_date oder tourney_year/week
        pm_df   (pd.DataFrame): Postmatch-Daten mit match_id, player_id und pm_* Spalten
    
    Returns:
        pd.DataFrame: main_df erweitert um lag_pm_* für player und opp_lag_pm_* für opponent
    """
    df = main_df.copy()

    # Sortierspalten definieren
    if "tourney_date" in df.columns:
        sort_cols = ["player_id", "tourney_date", "match_id"]
    else:
        sort_cols = ["player_id", "tourney_year", "tourney_week", "match_id"]

    df = df.sort_values(sort_cols).reset_index(drop=True)
    pm_df = pm_df.sort_values(["player_id", "match_id"]).reset_index(drop=True)

    # ---- Player Lag Stats ----
    player_stats = pm_df.drop(columns=["match_id"]).copy()
    player_stats = player_stats.add_prefix("lag_")  # pm_player_ace -> lag_pm_player_ace
    player_stats["player_id"] = pm_df["player_id"]
    player_stats["match_id"] = pm_df["match_id"]

    df = df.merge(player_stats, on=["player_id", "match_id"], how="left")
    lag_cols_player = [c for c in df.columns if c.startswith("lag_pm_")]
    df[lag_cols_player] = df.groupby("player_id")[lag_cols_player].shift(1)

    # ---- Opponent Lag Stats ----
    opp_stats = pm_df.drop(columns=["match_id"]).copy()
    opp_stats = opp_stats.add_prefix("opp_lag_")  # pm_opp_ace -> opp_lag_pm_opp_ace
    opp_stats["opp_id"] = pm_df["player_id"]   # wichtig: Gegner-ID = pm.player_id
    opp_stats["match_id"] = pm_df["match_id"]

    df = df.merge(opp_stats, on=["opp_id", "match_id"], how="left")
    lag_cols_opp = [c for c in df.columns if c.startswith("opp_lag_pm_")]
    df[lag_cols_opp] = df.groupby("opp_id")[lag_cols_opp].shift(1)
    df = df.sort_values(["match_id", "player_id"]).reset_index(drop=True)
    return df



def add_features():
    config = load_config("config/default.yaml")             # Lade Config Datei
    interim_dir = Path(config["path"]["interim_dir"])
    processed_dir = Path(config["path"]["processed_dir"])

    main_file = interim_dir / "matches_main.csv"  
    pm_file = interim_dir / "matches_postmatch.csv" 
    main_df = pd.read_csv(main_file)
    pm_df = pd.read_csv(pm_file)
    print(main_df.info())
    print(pm_df.info())

    df_with_lag = merge_last_pm_stats_for_both(main_df, pm_df)

    # Beispiel: Nur die neuen Spalten anzeigen
    print(df_with_lag.filter(like="lag_pm_").tail(10))
    print(df_with_lag.filter(like="opp_lag_pm_").tail(10))

    # Pfade
    main_file = os.path.join(processed_dir, config["filenames"]["main"])

    # Speichern
    df_with_lag.to_csv(main_file, index=False)

