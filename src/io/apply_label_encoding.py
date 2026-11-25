import pandas as pd
import yaml


def apply_label_encoding(df: pd.DataFrame, config: dict) -> pd.DataFrame:
 
    df_encoded = df.copy()
    
    for col, mapping in config.items():
        if col not in df_encoded.columns:
            continue
        
        if col not in df_encoded.columns:
            continue

        # Werte mappen
        df_encoded[col] = df_encoded[col].map(mapping)

        # Nicht gemappte Werte finden
        unmapped = df.loc[df_encoded[col].isna(), col].dropna().unique()
        if len(unmapped) > 0:
            print(
                f"⚠️ Spalte '{col}' enthält nicht gemappte Werte: {list(unmapped)}"
            )

        # Sicherstellen, dass Zahlen-Typ verwendet wird
        df_encoded[col] = df_encoded[col].astype("Int64")
    
    return df_encoded

