from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path
import os
import pandas as pd

# Load the trained model
PROJ_ROOT = Path(__file__).resolve()#.parents[2]
print(PROJ_ROOT)
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
print("############# MODEL PATH################", model_path)
model = joblib.load(model_path)

# Initialize FastAPI app
app = FastAPI()

# Define the input data format using Pydantic models
class PredictionInput(BaseModel):
    type: str
    sector: str
    net_usable_area: float
    net_area: float
    n_rooms: float
    n_bathroom: float
    latitude: float
    longitude: float
    price : float

# Define a prediction endpoint
@app.post("/predict/")
def predict(input_data: PredictionInput):
    # Convert input data to numpy array for prediction
    input_dict = {
        'type': [input_data.type],
        'sector': [input_data.sector],
        'net_usable_area': [input_data.net_usable_area],
        'net_area': [input_data.net_area],
        'n_rooms': [input_data.n_rooms],
        'n_bathroom': [input_data.n_bathroom],
        'latitude': [input_data.latitude],
        'longitude': [input_data.longitude],
        'price': [input_data.price]
    }
    input_df = pd.DataFrame(input_dict)
    
    # Get the prediction from the model
    prediction = model.predict(input_df)
    
    # Return the prediction result
    return {"prediction": int(prediction[0])}