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

app = FastAPI(title="Prédiction de Départ Client Bancaire")

@app.post("/predict")
def predict(data: CustomerData):
    try:
        geography_map = {
            'France': 0, 
            'Allemagne': 1, 'Germany': 1,
            'Espagne': 2, 'Spain': 2
        }
        gender_map = {'Female': 0, 'Femme': 0, 'Male': 1, 'Homme': 1}
        
        # Convert EUR to USD for the model (approximate conversion)
        eur_to_usd = 1.1
        balance_usd = data.Balance * eur_to_usd
        salary_usd = data.EstimatedSalary * eur_to_usd
        
        features = np.array([[
            data.CreditScore,
            geography_map[data.Geography],
            gender_map[data.Gender],
            data.Age,
            data.Tenure,
            balance_usd,
            data.NumOfProducts,
            data.HasCrCard,
            data.IsActiveMember,
            salary_usd
        ]])
        
        X_scaled = scaler.transform(features)
        proba = model.predict_proba(X_scaled)[0, 1]
        prediction = int(proba >= 0.5)
        
        # Translate feature names to French
        feature_importance = model_data['feature_importance']
        feature_name_map = {
            'CreditScore': 'Score de crédit',
            'Geography': 'Pays',
            'Gender': 'Genre',
            'Age': 'Âge',
            'Tenure': 'Ancienneté',
            'Balance': 'Solde',
            'NumOfProducts': 'Nombre de produits',
            'HasCrCard': 'Carte de crédit',
            'IsActiveMember': 'Client actif',
            'EstimatedSalary': 'Salaire estimé'
        }
        
        translated_importance = []
        for item in feature_importance:
            translated_importance.append({
                'feature': feature_name_map.get(item['feature'], item['feature']),
                'importance': item['importance']
            })
        
        return {
            "churn_probability": round(float(proba), 3),
            "prediction": prediction,
            "feature_importance": translated_importance
        }
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Valeur invalide pour {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))