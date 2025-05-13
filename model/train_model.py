import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def load_and_preprocess_data():
    data = pd.read_csv('data/bank_customer_churn.csv')
    
    le = LabelEncoder()
    data['Geography'] = le.fit_transform(data['Geography'])
    data['Gender'] = le.fit_transform(data['Gender'])
    
    feature_columns = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 
                      'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
    X = data[feature_columns]
    y = data['Exited']
    
    return X, y, data, feature_columns

def train_model():
    X, y, raw_data, feature_columns = load_and_preprocess_data()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nFeature Importance:")
    print(feature_importance)
    
    os.makedirs('model', exist_ok=True)
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_columns': feature_columns,
        'feature_importance': feature_importance.to_dict('records')
    }
    joblib.dump(model_data, 'model/model.joblib')
    print("\nModel and metadata saved to model/model.joblib")

if __name__ == "__main__":
    train_model() 