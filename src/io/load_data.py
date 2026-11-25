from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.io.year_selection import *


def load_data(raw_data_path: str) -> pd.DataFrame:
    start_year, end_year = year_selection()
    start, end = sorted((int(start_year), int(end_year)))                                               # Fehlervermeidung für ungewollten jahreswechsel
    DATA_DIR = Path(raw_data_path)                                                            
    files = [DATA_DIR / f"atp_matches_{y}.csv" for y in range(start, end + 1)]                          # Sucht csv dateien in der range startjahr - endjahr inklusive
    existing = [p for p in files if p.exists()]                                                         # Gefilterte liste der vorhandenen daten
    if not existing:                                                                                    # Error bei fehlernder datei/falsches jahr/name
        raise FileNotFoundError(f"Keine Dateien für {start} - {end} unter {DATA_DIR} gefunden.")        
    
    dfs = [pd.read_csv(p) for p in existing]                                                            # Jede vorhandene datei wird in die liste dfs gesammelt 
    df = pd.concat(dfs, ignore_index=True)                                                              # Listen werden zusammengefügt

    print(f"Zusammengeführt: {len(existing)} Dateien, {len(df)} Zeilen")                                # Ausgabe von dateimengen und allen zusammengeführten zeilen
    return df