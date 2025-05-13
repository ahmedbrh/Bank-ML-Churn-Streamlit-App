import streamlit as st
import requests
import plotly.graph_objects as go

API_URL = "http://localhost:8000/predict"

st.title("Customer Churn Prediction")
st.write("Enter customer details to predict churn probability.")

with st.form("churn_form"):
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    income = st.number_input("Annual Income ($)", min_value=0, value=50000)
    submitted = st.form_submit_button("Predict")

if submitted:
    data = {"age": age, "income": income}
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            churn_prob = result['churn_probability']
            prediction = result['prediction']
            st.success(f"Churn Probability: {churn_prob*100:.1f}%")
            st.info(f"Prediction: {'Churn' if prediction else 'No Churn'}")

            st.subheader("Dashboard")
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Input Summary")
                st.write(f"- Age: {age}")
                st.write(f"- Income: ${income}")
                st.write(f"- Prediction: {'Churn' if prediction else 'No Churn'}")
            with col2:
                st.write("### Churn Probability Gauge")
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = churn_prob*100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Churn %"},
                    gauge = {'axis': {'range': [0, 100]},
                             'bar': {'color': "crimson" if prediction else "green"}}
                ))
                st.plotly_chart(fig, use_container_width=True)

            pie_labels = ['Churn', 'No Churn']
            pie_values = [1, 0] if prediction else [0, 1]
            pie_colors = ['crimson', 'green']
            pie_fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values, marker_colors=pie_colors)])
            st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error connecting to API: {e}") 