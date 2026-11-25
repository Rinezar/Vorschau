import numpy as np
import pandas as pd


def create_symmetric_player_match_rows(df: pd.DataFrame) -> pd.DataFrame:
    # --- Winner-View ---
    winner_df = df.copy()
    new_cols = []
    for c in df.columns:
        if c.startswith("winner_"):
            new_cols.append(c.replace("winner_", "player_"))
        elif c.startswith("loser_"):
            new_cols.append(c.replace("loser_", "opp_"))
        elif c.startswith("w_"):
            new_cols.append(c.replace("w_", "player_"))
        elif c.startswith("l_"):
            new_cols.append(c.replace("l_", "opp_"))
        else:
            new_cols.append(c)
    winner_df.columns = new_cols
    winner_df["target"] = 1

    # --- Loser-View ---
    loser_df = df.copy()
    new_cols = []
    for c in df.columns:
        if c.startswith("loser_"):
            new_cols.append(c.replace("loser_", "player_"))
        elif c.startswith("winner_"):
            new_cols.append(c.replace("winner_", "opp_"))
        elif c.startswith("l_"):
            new_cols.append(c.replace("l_", "player_"))
        elif c.startswith("w_"):
            new_cols.append(c.replace("w_", "opp_"))
        else:
            new_cols.append(c)
    loser_df.columns = new_cols
    loser_df["target"] = 0

    # --- Winner + Loser direkt untereinander ---
    pairs = []
    for i in range(len(df)):
        pairs.append(winner_df.iloc[[i]])
        pairs.append(loser_df.iloc[[i]])
    player_df = pd.concat(pairs, ignore_index=True)

    # match_id übernehmen
    if "match_id" in df.columns:
        player_df["match_id"] = player_df["match_id"].astype(np.int32)

    return player_df
