import os

from src.io.add_match_id import *
from src.io.apply_label_encoding import *
from src.io.create_symmetric_player_match_rows import *
from src.io.extract_tourney_dates import *
from src.io.lable_player_postmatch_stats import *
from src.io.load_data import *
from src.io.remove_unnecessary_columns import *
from src.io.reorder_core_columns import *
from src.io.split_prematch_postmatch import *
from utils import load_config
from utils.load_config import *


def build_data():
    config = load_config("config/default.yaml")             # Lade Config Datei
    
    raw_dir = config["path"]["raw_dir"]
    interim_dir = config["path"]["interim_dir"]
    
    columns_to_remove = config["columns_to_remove"]         # Entnehme Spaltennamen zum entfernen
    preferred_order = config["preferred_order"]             # Entnehme bevorzugte Spaltenreihenfolge
    one_hot_maps = config["one_hot_maps"]
           
    df = load_data(raw_dir)                                 # Lade rohe csv-Dateien
    df = extract_tourney_dates(df)                          # Erstelle Spalten mit Turnierdaten
    df = add_match_id(df)                                   # Füge uniqe match-ID hinzu (für training später wichtig)+
    df = create_symmetric_player_match_rows(df)             # Erstelle symmetrisches 2 Spalten Layout + füge target spalte hinzu
    df = reorder_core_columns(df, preferred_order)          # Ordne Spalten nach preferred order
    df = remove_unnecessary_columns(df, columns_to_remove)  # Entferne unwichtige Spalten 
    df = label_player_postmatch_stats(df)                   # Markiere Spalten mit Post-match-Info
    df = apply_label_encoding(df,one_hot_maps)
    main_df, postmatch_df = split_prematch_postmatch(df)    # Split in zwei DataFrames

    # Pfade
    main_file = os.path.join(interim_dir, config["filenames"]["main"])
    postmatch_file = os.path.join(interim_dir, config["filenames"]["postmatch"])
    # Speichern
    main_df.to_csv(main_file, index=False)
    postmatch_df.to_csv(postmatch_file, index=False)

    print(f"✅ main_df gespeichert unter: {main_file}")
    print(f"✅ postmatch_df gespeichert unter: {postmatch_file}")
