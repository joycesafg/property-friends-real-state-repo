from pydantic import BaseModel
import joblib
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pathlib import Path
import os
from datetime import datetime
import pandas as pd

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/logs_db")
client = MongoClient(MONGO_URI)
db = client.logs_db
logs_collection = db.api_logs

# Load the trained model
PROJ_ROOT = Path(__file__).resolve()#.parents[2]
print(PROJ_ROOT)

# API Key head definition
API_KEY_NAME = "x-api-key"
API_KEY_VALUE = "A1bC3dE5FgH7IjK9LmN0OpQrStUvWxY"  # It's in the code only for tests porpuses, it needs to be placed as an ENV variable ou secrets to make it safe.

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Função para validar a API Key
def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY_VALUE:
        raise HTTPException(status_code=403, detail="Acesso negado: API Key inválida")
    return api_key

def log_to_mongo(response_data):
    log_entry = {
        "response_data": response_data,
        "timestamp": datetime.now(),
    }
    logs_collection.insert_one(log_entry)


model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
print("############# MODEL PATH################", model_path)
model = joblib.load(model_path)

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed (can restrict to specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

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
@app.post("/predict/", dependencies=[Depends(validate_api_key)])
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
    
    output_dict = {
        'type': [input_data.type],
        'sector': [input_data.sector],
        'net_usable_area': [input_data.net_usable_area],
        'net_area': [input_data.net_area],
        'n_rooms': [input_data.n_rooms],
        'n_bathroom': [input_data.n_bathroom],
        'latitude': [input_data.latitude],
        'longitude': [input_data.longitude],
        'price': [input_data.price],
        'prediction' : [int(prediction[0])]
    }
    log_to_mongo(output_dict)
    
    # Return the prediction result
    return {"prediction": int(prediction[0])}