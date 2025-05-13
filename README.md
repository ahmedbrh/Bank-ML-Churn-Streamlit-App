# 🏦 Bank Customer Churn Prediction App

A machine learning application that predicts customer churn probability for banking customers based on demographic (🇫🇷, 🇩🇪, 🇪🇸) and account information (Annual Salary, age, balance, credit score...etc)

![Workflow Diagram](docs/Churn%20Prediction%20Interaction%20Sequence.png)

## Overview

This application uses a RandomForest model trained on bank customer data to predict the likelihood of customer churn. It consists of:

- **ML Model** - Predicts churn probability based on customer attributes
- **FastAPI Backend** - Serves predictions through a REST API
- **Streamlit Frontend** - User-friendly interface for inputs and visualizations

## 🔍 Features

- Customer churn prediction with probability estimation
- Interactive dashboard with feature importance visualization
- Risk analysis with key factor identification
- Support for multiple currencies (EUR)
- Multilingual support (English and French)


### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ahmedbrh/ML-Churn-Streamlit-App.git
cd ML-Churn-Streamlit-App
```

2. activate a Venv:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the dataset to the data directory:
```bash
mkdir -p data
# Download Churn_Modelling.csv from Kaggle to the data directory
```

5. Cmdline to Train the model:
```bash
python model/train_model.py
```

6. Start the FastAPI server :
```bash
uvicorn api.main:app --reload
```

7. start the Streamlit server frontend:
```bash
streamlit run frontend/app.py
```

8. Open your browser and navigate to: http://localhost:8501


## 📊 Dataset

This project uses the [Bank Customer Churn Prediction dataset](https://www.kaggle.com/datasets/adammaus/predicting-churn-for-bank-customers) from Kaggle which include features like 
- Customer demographics (age, gender, geography- (France, Germany, Spain))
- Account information (balance, tenure, products)
- Activity metrics (credit score, active status)
