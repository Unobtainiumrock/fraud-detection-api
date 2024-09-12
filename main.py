from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import joblib
import numpy as np

app = FastAPI()

class Transaction(BaseModel):
    amount: float
    time: float
    type: str
    account_id: int
    location: str

# model = joblib.load('path_to_model.pkl')

@app.post('/predict')
async def predict(transaction: Transaction):
    features = np.array([[transaction.amount, transaction.time, transaction.type, transaction.account_id, transaction.location]])
    # prediction = model.predict([features])
    # return {'prediction': int(prediction[0])}
    return { "hello": "world!" }

# Some other thigns to note. We'd want to ensure that the outputs (e.g. fraud probability) can 
# be easily accessed and utilized by other systems within Coinbase. This could involve
# - Storing predictions in a database for further analysis
# - Triggering alerts or workflows based on certain prediction thresholds.
