import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

API_URL = "http://localhost:8000/predict"

st.set_page_config(layout="wide")
st.title("🏦 Prédiction de Départ Client Bancaire")
st.write("Entrez les informations du client pour prédire la probabilité de départ.")

with st.form("churn_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Âge", min_value=18, max_value=100, value=35, 
                       help="Âge du client")
        gender = st.radio("Genre", ["Homme", "Femme"])
        geography = st.selectbox("Pays", 
                               ["France", "Allemagne", "Espagne"],
                               help="Pays de résidence du client")
        balance = st.number_input("Solde du compte (€)", 
                                min_value=0.0, value=10000.0, step=1000.0,
                                help="Solde actuel du compte en euros")
    
    with col2:
        credit_score = st.select_slider("Score de crédit", 
                                      options=["Très faible", "Faible", "Moyen", "Bon", "Excellent"],
                                      value="Moyen",
                                      help="Évaluation du score de crédit du client")
        
        is_active = st.radio("Client actif ?", 
                            ["Oui", "Non"],
                            help="Le client utilise-t-il régulièrement ses comptes ?")
        
        num_products = st.radio("Nombre de produits bancaires", 
                              [1, 2, 3, "4 ou plus"],
                              help="Nombre de produits bancaires détenus par le client")
        
        salary = st.slider("Salaire annuel (€)", 
                          min_value=20000, max_value=200000, value=45000, step=5000,
                          help="Salaire annuel estimé en euros")
    
    submitted = st.form_submit_button("Prédire")

if submitted:
    # Conversion des données pour l'API
    credit_score_map = {
        "Très faible": 300,
        "Faible": 450,
        "Moyen": 600,
        "Bon": 750,
        "Excellent": 850
    }
    
    gender_map = {"Homme": "Male", "Femme": "Female"}
    is_active_map = {"Oui": 1, "Non": 0}
    num_products_map = {"4 ou plus": 4}
    
    data = {
        "CreditScore": credit_score_map[credit_score],
        "Geography": geography,
        "Gender": gender_map[gender],
        "Age": age,
        "Tenure": 5,  
        "Balance": balance,
        "NumOfProducts": int(num_products) if num_products != "4 ou plus" else 4,
        "HasCrCard": 1,  
        "IsActiveMember": is_active_map[is_active],
        "EstimatedSalary": salary
    }
    
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            churn_prob = result['churn_probability']
            prediction = result['prediction']
            feature_importance = pd.DataFrame(result['feature_importance'])
            
            risk_level = "Élevé" if churn_prob > 0.7 else "Modéré" if churn_prob > 0.3 else "Faible"
            risk_color = "red" if churn_prob > 0.7 else "orange" if churn_prob > 0.3 else "green"
            
            st.markdown(f"### Risque de départ : <span style='color:{risk_color}'>{risk_level}</span>", unsafe_allow_html=True)
            st.progress(churn_prob)
            st.markdown(f"**Probabilité de départ : {churn_prob*100:.1f}%**")
            
            st.subheader("Tableau de bord d'analyse")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Indicateur de risque")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=churn_prob*100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Risque de départ %"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': risk_color},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "salmon"}
                        ]
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("### Importance des facteurs")
                fig = px.bar(
                    feature_importance,
                    x='importance',
                    y='feature',
                    orientation='h',
                    title='Impact des différents facteurs'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.write("### Résumé du profil client")
            profile_col1, profile_col2, profile_col3 = st.columns(3)
            
            with profile_col1:
                st.metric("Score de crédit", credit_score, 
                         delta="Bon" if credit_score in ["Bon", "Excellent"] else "À améliorer")
            with profile_col2:
                st.metric("Âge", f"{age} ans",
                         delta="Senior" if age > 60 else "Adulte")
            with profile_col3:
                st.metric("Solde", f"{balance:,.0f} €",
                         delta="Élevé" if balance > 50000 else "Normal")
            
            st.write("### Facteurs de risque")
            risk_factors = []
            if credit_score in ["Très faible", "Faible"]: 
                risk_factors.append("Score de crédit faible")
            if balance < 1000: 
                risk_factors.append("Solde faible")
            if is_active == "Non": 
                risk_factors.append("Client inactif")
            if age > 70: 
                risk_factors.append("Client senior")
            
            if risk_factors:
                st.warning("Facteurs de risque identifiés : " + ", ".join(risk_factors))
            else:
                st.success("Aucun facteur de risque majeur identifié")
            
        else:
            st.error(f"Erreur API : {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}") 