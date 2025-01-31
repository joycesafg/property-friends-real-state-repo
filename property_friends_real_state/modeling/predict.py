from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm
import joblib
import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_percentage_error,
    mean_absolute_error)
#from property_friends_real_state.config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()

def print_metrics(predictions, target):
    print("RMSE: ", np.sqrt(mean_squared_error(predictions, target)))
    print("MAPE: ", mean_absolute_percentage_error(predictions, target))
    print("MAE : ", mean_absolute_error(predictions, target))

@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    test_path: Path = Path(__file__).resolve().parents[2] / "data/processed/test.csv",
    model_path: Path = Path(__file__).resolve().parents[1] / "app/model.pkl",
    #predictions_path: Path = PROCESSED_DATA_DIR / "test_predictions.csv",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Performing inference for model...")
    target = "price"
    test = pd.read_csv(test_path)
    
    pipeline = joblib.load(model_path)
    
    feature_names = pipeline[0].feature_names_in_
    
    test_predictions = pipeline.predict(test[feature_names])
    
    test_target = test[target].values
    
    print_metrics(test_predictions, test_target)

    logger.success("Inference complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
