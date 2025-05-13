from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint, confloat
import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/model.joblib')

class CustomerData(BaseModel):
    age: conint(ge=18, le=100)
    income: conint(ge=0)

model_bundle = joblib.load(MODEL_PATH)
model = model_bundle['model']
scaler = model_bundle['scaler']

app = FastAPI(title="Customer Churn Prediction API")

@app.post("/predict")
def predict(data: CustomerData):
    X = np.array([[data.age, data.income]])
    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[0, 1]
    prediction = int(proba >= 0.5)
    return {
        "churn_probability": round(float(proba), 3),
        "prediction": prediction
    } 