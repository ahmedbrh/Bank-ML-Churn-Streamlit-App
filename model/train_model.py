import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

def generate_data(n_samples=1000):
    np.random.seed(42)
    age = np.random.randint(18, 70, n_samples)
    income = np.random.randint(20000, 120000, n_samples)
    churn_prob = 1 / (1 + np.exp(-(0.03 * (age - 40) - 0.00005 * (income - 50000))))
    churn = (np.random.rand(n_samples) < churn_prob).astype(int)
    data = pd.DataFrame({'age': age, 'income': income, 'churn': churn})
    return data

def main():
    data = generate_data()
    X = data[['age', 'income']]
    y = data['churn']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.2f}")

    os.makedirs('model', exist_ok=True)
    joblib.dump({'model': model, 'scaler': scaler}, 'model/model.joblib')
    print("Model and scaler saved to model/model.joblib")

if __name__ == "__main__":
    main() 