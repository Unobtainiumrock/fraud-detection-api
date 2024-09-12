from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import joblib
import numpy as np
import databases

app = FastAPI()

class Transaction(BaseModel):
    amount: float
    time: float
    type: str
    account_id: int
    location: str

random_cut_forest_model = joblib.load('./trained_models/random_cut_forest_model.pkl')
xgboost_model = joblib.load('./trained_models/xgboost_model.pkl')

################### Routes ###################
@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown'):
    await database.disconnect()

@app.post('/predict')
async def predict(transaction: Transaction, model):
    try:
        features = np.array([[
            transaction.amount,
            transaction.time,
            transaction.type,
            transaction.account_id,
            transaction.location
        ]])
        prediction = model.predict(features)


        return {'prediction': int(prediction[0])}
        # return { "hello": "world!" }
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

