# Customer Churn Prediction App

A machine learning-powered web application that predicts customer churn based on user attributes.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── model/
│   ├── train_model.py
│   └── model.joblib
├── api/
│   └── main.py
└── frontend/
    └── app.py
```

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model:
```bash
python model/train_model.py
```

4. Start the FastAPI backend:
```bash
uvicorn api.main:app --reload
```

5. Start the Streamlit frontend:
```bash
streamlit run frontend/app.py
```

## Features

- Machine learning model for churn prediction
- FastAPI backend for model serving
- Streamlit frontend for user interaction
- Input validation and error handling
- Real-time predictions

## API Endpoints

- POST `/predict`: Get churn prediction for customer data
  - Input: Customer attributes (age, income, etc.)
  - Output: Churn probability and prediction

## Technologies Used

- Scikit-learn: Machine learning model
- FastAPI: Backend API
- Streamlit: Frontend interface
- Joblib: Model persistence
- Pandas: Data manipulation 