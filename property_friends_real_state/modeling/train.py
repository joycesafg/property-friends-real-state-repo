import pandas as pd
import numpy as np
import joblib


from category_encoders import TargetEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor


from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

#from property_friends_real_state.config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()

def load_data(train_path:str, test_path:str):
    """
    Loads the train and test data into pandas DataFrames
    """
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    return train, test


@app.command()
def main(
    #C:\Users\55819\Documents\DataMaster\challenge\property-friends-real-state-repo\data\processed\train.csv
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    train_path: Path =  Path(__file__).resolve().parents[2] / "data/processed/train.csv",
    test_path: Path = Path(__file__).resolve().parents[2] / "data/processed/test.csv",
    model_path: Path = Path(__file__).resolve().parents[2] / "property_friends_real_state/app",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
   # print(train_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Load the data...")
    train, test = load_data(train_path, test_path)
    
    print("MODEL PATH: ", model_path)
    
    train_cols = [
    col for col in train.columns if col not in ['id', 'target']
    ]

    categorical_cols = ["type", "sector"]
    target           = "price"
    
    categorical_transformer = TargetEncoder()

    preprocessor = ColumnTransformer(
    transformers=[
        ('categorical',
          categorical_transformer,
          categorical_cols)
    ])

    steps = [
    ('preprocessor', preprocessor),
    ('model', GradientBoostingRegressor(**{
        "random_state":42, 
        "learning_rate":0.01,
        "n_estimators":300,
        "max_depth":5,
        "loss":"absolute_error"
    }))
]

    pipeline = Pipeline(steps)
    
    pipeline.fit(train[train_cols], train[target])
    
    #import joblib

# Save the model
    logger.success("Saving the artifact.")
    joblib.dump(pipeline, model_path/"model.pkl")
    
    # Load the model
    #loaded_model = joblib.load("model.pkl")
    logger.success("Modeling training complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
