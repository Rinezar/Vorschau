import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import TimeSeriesSplit

from src.training_src.load_data import *
from utils import load_config
from utils.load_config import *


def train_model():
    config = load_config("config/default.yaml")             # Lade Config Datei
    processed_dir = config["path"]["processed_dir"]

    df = load_data(processed_dir)                                 # Lade rohe csv-Dateien
    print(df.info())
    # 1. Features & Target trennen
    BASELINE = ["player_age",
                "opp_age",
                #"player_ht",  
                #"opp_ht",
                #"player_entry",
                #"opp_entry",
                "player_seed", 
                "opp_seed",
                #"player_hand",
                #"opp_hand",
                #"tourney_level",    #->späteres feature
                #"draw_size",       #->späteres feature
                #"surface"          #->späteres feature
                ]
    X = df[BASELINE]
    '''
    X = df.drop(columns=["target", 
                         "player_name", 
                         "player_id",
                         "opp_name", 
                         "opp_id", 
                         "match_id",
                         "player_ioc",
                         "opp_ioc",
                         "lag_pm_score",
                         "lag_pm_round",
                         "opp_lag_pm_score",
                         "opp_lag_pm_round",
                         "opp_lag_player_id",
                         "lag_player_id"
                         ])  # keine Strings oder IDs
                         '''
    y = df["target"]

    # 3. XGBoost Modell anlegen
    model = xgb.XGBClassifier(
        n_estimators=300,        # Anzahl Bäume
        max_depth=6,             # Baumtiefe
        learning_rate=0.05,      # Schrittweite
        subsample=0.8,           # Sampling für Robustheit
        colsample_bytree=0.8,    # Feature-Sampling
        random_state=42,
        eval_metric="logloss",
        use_label_encoder=False
    )

    

    tscv = TimeSeriesSplit(n_splits=5)
    for train_idx, test_idx in tscv.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    # 4. Trainieren
    model.fit(X_train, y_train)

    # 5. Vorhersagen
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]  # Wahrscheinlichkeit für "Sieg"

    # 6. Evaluieren
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("ROC AUC:", roc_auc_score(y_test, y_proba))
    xgb.plot_importance(model, max_num_features=20)
    plt.show()
