import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib

# Load the saved model
model = xgb.XGBClassifier()
model.load_model('predictor_model/xgb_model.json')

# Load the saved label encoders and fitted scaler
le_region = joblib.load('predictor_model/le_region.pkl')
le_state_response = joblib.load('predictor_model/le_state_response.pkl')
scaler = joblib.load('predictor_model/scaler.pkl')

# Title and Description
st.title("Protest Outcome Prediction Model")

# Image and Caption
st.image("predictor_model/Zimbabwe.webp", 
         caption="Supporters of Zimbabwe's opposition Movement for Democratic Change march in Harare, November 2018, angered by a protracted economic crisis and Prime Minister Emmerson Mnangagwa's election earlier that year.", 
         use_column_width=True)

# Info Section
st.info("""
    **Welcome to the Protest Outcome Prediction Model!**
    
    This application predicts the likely response of a government to a protest based on various factors such as the region of the protest, the demands being made, the duration of the protest, the number of participants, and whether there was protester violence.
    
    **How to use the model:**
    1. Select the region where the protest is taking place.
    2. Choose the primary demand of the protest from the list.
    3. Enter the duration of the protest. (Minimum value is 1 which translates to same-day protest)
    4. Enter the number of participants in the protest.
    5. Indicate whether there was protester violence by selecting Yes or No.
    6. Click on the 'Predict Response' button to see the predicted government response.
""")

# Sidebar with protester demands descriptions and government responses
st.sidebar.header("Protester Demands Descriptions")
st.sidebar.write("""
    **Labor/Wage Dispute**: Demands related to labor rights and wage increases.
    
    **Land/Farm Issue**: Demands concerning land rights and agricultural issues.
    
    **Police Brutality**: Protests against police misconduct and brutality.
    
    **Political Behavior**: Demands related to political actions, behaviors, or policies.
    
    **Price Increases**: Protests against the rise in prices of goods and services.
    
    **Removal of Politician**: Demands for the removal of a specific political figure.
""")

st.sidebar.header("Government Response Descriptions")
st.sidebar.write("""
    **Passive or Concessive**: The government is likely to ignore the protest or accommodate the protesters' demands.

    **Control Measures**: The government is likely to use crowd control measures such as dispersal or arrests.

    **Forceful Repression**: The government is likely to engage in forceful repression, including beatings, shootings, or killings.
""")

# Define numerical and binary features
numerical_features = ['protest_duration', 'participants_numeric']
binary_features = ['protesterviolence']

# Region input
region = st.selectbox("Region", options=[x if x != "Canada" else "N.America (Canada)" for x in le_region.classes_])

# Write for demand checkboxes with smaller font size
st.write("Select Primary Demands (You can choose more than one)")

# Primary demand checkboxes
demands = {
    'demand_labor_wage_dispute': 'Labor/Wage Dispute',
    'demand_land_farm_issue': 'Land/Farm Issue',
    'demand_police_brutality': 'Police Brutality',
    'demand_political_behavior': 'Political Behavior',
    'demand_price_increases': 'Price Increases',
    'demand_removal_of_politician': 'Removal of Politician'
}

# Initialize demand columns with 0
input_data = {key: 0 for key in demands.keys()}

# Checkbox inputs for each demand
for key, label in demands.items():
    input_data[key] = 1 if st.checkbox(label) else 0

# Numerical inputs
protest_duration = st.number_input("Protest Duration (days)", min_value=1)
participants_numeric = st.number_input("Number of Participants", min_value=1)

# Protester violence input
protesterviolence = st.selectbox("Protester Violence", options=["No", "Yes"])

# Add region and numerical features to input_data
input_data.update({
    'region': region,
    'protest_duration': protest_duration - 1,  # Adjusting for backend
    'participants_numeric': participants_numeric,
    'protesterviolence': 1 if protesterviolence == "Yes" else 0
})

# Convert input_data to DataFrame and ensure correct column order
input_df = pd.DataFrame([input_data], columns=[
    'region', 'protest_duration', 'participants_numeric', 'protesterviolence',
    'demand_labor_wage_dispute', 'demand_land_farm_issue', 'demand_police_brutality',
    'demand_political_behavior', 'demand_price_increases', 'demand_removal_of_politician'
])

# Preprocess inputs
input_df['region'] = le_region.transform(input_df['region'].replace("N.America (Canada)", "Canada"))

# Ensure the numerical features are properly handled
input_df[numerical_features] = scaler.transform(input_df[numerical_features])

# Button to predict state response
if st.button('Predict Response'):
    # Make predictions
    prediction = model.predict(input_df)
    prediction_label = le_state_response.inverse_transform(prediction)[0]

    # Mapping prediction to descriptive output
    response_mapping = {
        'Passive or Concessive': 'The government will most likely ignore or accommodate the protesters.',
        'Control Measures': 'The government will most likely use crowd control measures against the protesters.',
        'Forceful Repression': 'The government will most likely take up excessive measures against the protesters.'
    }
    
    # Display the prediction
    st.subheader("Predicted State Response")
    st.write(response_mapping[prediction_label])
