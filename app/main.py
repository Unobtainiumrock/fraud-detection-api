import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import database  # Import the database connection
from app.models import predictions_table  # Import the table model
from app.crud import add_prediction  # Import the CRUD function to insert a prediction
from app.ml_model import random_cut_forest_model, xgboost_model  # Import your preloaded models
from app.config import THRESHOLD

app = FastAPI()

# Define the data structure for the transaction
class Transaction(BaseModel):
    amount: float
    time: float
    type: str
    account_id: int
    location: str

def extract_features(transaction: Transaction) -> np.ndarray:
    """Convert Transaction object to a feature array."""
    return np.array([[
        transaction.amount,
        transaction.time,
        transaction.type,
        transaction.account_id,
        transaction.location
    ]])

def get_model(model_name: str):
    """Select model based on the provided model name."""
    if model_name == 'random_cut_forest':
        return random_cut_forest_model
    elif model_name == 'xgboost':
        return xgboost_model
    else:
        raise HTTPException(status_code=400, detail="Invalid model name")

def make_prediction(model, features: np.ndarray) -> np.ndarray:
    """Make prediction using the provided model and features."""
    return model.predict(features)

async def save_prediction_to_db(account_id: int, prediction: float):
    """Persist the prediction result in the database."""
    await add_prediction(account_id, prediction)

def check_threshold(prediction_value: int, threshold: float) -> bool:
    """Check if the prediction value exceeds the threshold."""
    return prediction_value > threshold

################### Routes ###################

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@app.post('/predict/{model_name}')
async def predict(transaction: Transaction, model_name: str):
    try:
        features = extract_features(transaction)

        # Step 2: Dynamically select model
        model = get_model(model_name)

        # Step 3: Make prediction
        prediction = make_prediction(model, features)
        prediction_value = int(prediction[0])

        # Step 4: Persist prediction to the database
        await save_prediction_to_db(transaction.account_id, float(prediction_value))

        # Step 5: Check if the prediction exceeds the threshold
        if check_threshold(prediction_value, THRESHOLD):
            # You can add an alert trigger function here
            pass

        return {'prediction': prediction_value}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

##############################################


# This system needs to be real-time, meaning that we want to have things like:

# prediction_value = int(prediction[0])
# if prediction_value > THRESHOLD:
#     # Trigger an alert (could be an email, a webhook call, etc.)
#     trigger_alert(prediction_value)
# return {'prediction': prediction_value}

# We may also want data persistence with stuff like:

# prediction = model.predict(features)
# query = "INSERT INTO predictions (prediction) VALUES (:prediction)"
# await database.execute(query, {"prediction": int(prediction[0])})


# Keep the system as decoupled as possible and make routes and functions have single
# responsibilities!

# Add a preprocessing pipeline and feature engineering pipe line (if needed) borrow the
# reusable pipeline framework from my previous ML work.
