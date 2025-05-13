import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

API_URL = "http://localhost:8000/predict"

st.set_page_config(layout="wide")
st.title("Bank Customer Churn Prediction")
st.write("Enter customer details to predict churn probability.")

with st.form("churn_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=650)
        geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        tenure = st.number_input("Tenure (years)", min_value=0, max_value=10, value=5)
    
    with col2:
        balance = st.number_input("Balance", min_value=0.0, value=50000.0)
        num_products = st.number_input("Number of Products", min_value=1, max_value=4, value=1)
        has_card = st.selectbox("Has Credit Card", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        is_active = st.selectbox("Is Active Member", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        salary = st.number_input("Estimated Salary", min_value=0.0, value=50000.0)
    
    submitted = st.form_submit_button("Predict")

if submitted:
    data = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": has_card,
        "IsActiveMember": is_active,
        "EstimatedSalary": salary
    }
    
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            churn_prob = result['churn_probability']
            prediction = result['prediction']
            feature_importance = pd.DataFrame(result['feature_importance'])
            
            st.success(f"Churn Probability: {churn_prob*100:.1f}%")
            st.info(f"Prediction: {'Churn' if prediction else 'No Churn'}")
            
            st.subheader("Customer Risk Analysis Dashboard")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Risk Gauge")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=churn_prob*100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Churn Risk %"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "crimson" if prediction else "green"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "salmon"}
                        ]
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("### Feature Importance")
                fig = px.bar(
                    feature_importance,
                    x='importance',
                    y='feature',
                    orientation='h',
                    title='Impact of Different Factors'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.write("### Customer Profile Summary")
            profile_col1, profile_col2, profile_col3 = st.columns(3)
            
            with profile_col1:
                st.metric("Credit Score", credit_score, 
                         delta="Good" if credit_score > 650 else "Poor")
            with profile_col2:
                st.metric("Customer Age", age,
                         delta="Senior" if age > 60 else "Adult")
            with profile_col3:
                st.metric("Balance", f"${balance:,.2f}",
                         delta="High" if balance > 100000 else "Normal")
            
            st.write("### Risk Factors")
            risk_factors = []
            if credit_score < 600: risk_factors.append("Low credit score")
            if balance < 10000: risk_factors.append("Low balance")
            if not is_active: risk_factors.append("Inactive member")
            if age > 70: risk_factors.append("Senior citizen")
            
            if risk_factors:
                st.warning("Key Risk Factors: " + ", ".join(risk_factors))
            else:
                st.success("No significant risk factors identified")
            
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error connecting to API: {e}") 