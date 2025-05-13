from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint, confloat
import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/model.joblib')

class CustomerData(BaseModel):
    CreditScore: conint(ge=300, le=900)
    Geography: str
    Gender: str
    Age: conint(ge=18, le=100)
    Tenure: conint(ge=0, le=10)
    Balance: float
    NumOfProducts: conint(ge=1, le=4)
    HasCrCard: conint(ge=0, le=1)
    IsActiveMember: conint(ge=0, le=1)
    EstimatedSalary: float

model_data = joblib.load(MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
feature_columns = model_data['feature_columns']

app = FastAPI(title="Bank Customer Churn Prediction API")

@app.post("/predict")
def predict(data: CustomerData):
    try:
        geography_map = {'France': 0, 'Germany': 1, 'Spain': 2}
        gender_map = {'Female': 0, 'Male': 1}
        
        features = np.array([[
            data.CreditScore,
            geography_map[data.Geography],
            gender_map[data.Gender],
            data.Age,
            data.Tenure,
            data.Balance,
            data.NumOfProducts,
            data.HasCrCard,
            data.IsActiveMember,
            data.EstimatedSalary
        ]])
        
        X_scaled = scaler.transform(features)
        proba = model.predict_proba(X_scaled)[0, 1]
        prediction = int(proba >= 0.5)
        
        return {
            "churn_probability": round(float(proba), 3),
            "prediction": prediction,
            "feature_importance": model_data['feature_importance']
        }
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value for {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 