import pickle
import pandas as pd
import streamlit as st
from datetime import datetime
import numpy as np

st.markdown(
    """
    <style>
    /* General Page Styling */
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(120deg, #89f7fe, #66a6ff);
        color: #2c3e50;
        margin: 0;
        padding: 0;
    }
    .main {
        background-color: white;
        padding: 30px;
        margin-top: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .header {
        text-align: center;
        padding: 20px;
        color: white;
        background: linear-gradient(90deg, #2c3e50, #4ca1af);
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    .header h1 {
        font-size: 3em;
        margin: 0;
    }
    .header p {
        margin-top: 10px;
        font-size: 1.2em;
        color: #ecf0f1;
    }
    .st-date-input label {
        font-weight: bold;
        color: #34495e;
    }
    .prediction-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .prediction-card h2 {
        font-size: 2em;
        color: #2c3e50;
    }
    .prediction-card p {
        font-size: 1.2em;
        margin: 5px 0;
    }
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 30px;
        color: #f5f5f5;
        font-size: 0.9em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown(
    """
    <div class="header">
        <h1>🌬️ Wind Prediction</h1>
        <p>Nearly accurate wind speed forecasts for planning and safety</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Main Container
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)

    # Load SARIMAX model
    filename = 'sarimax_model.pkl'
    with open(filename, 'rb') as file:
        model = pickle.load(file)

    # Forecasting 2024-2026
    forecast_start = '2024-01-01'
    forecast_end = '2026-12-31'
    forecast_steps = (pd.to_datetime(forecast_end) - pd.to_datetime(forecast_start)).days * 24  # Hours

    pred_uc = model.get_forecast(steps=forecast_steps)
    pred_ci = pred_uc.conf_int()
    pred_ci.columns = ['Lower', 'Upper'] 

    # Ensure datetime index
    pred_ci.index = pd.to_datetime(pred_ci.index)

    # Filter for 2024-2026
    forecast_2026_2030 = pred_ci[(pred_ci.index >= forecast_start) & (pred_ci.index <= forecast_end)]

    # User input
    date_str = st.date_input('📅 Select a date for prediction', value=datetime(2024, 1, 1))
    date_str = str(date_str)

    # Prediction display
    if date_str in forecast_2026_2030.index.strftime('%Y-%m-%d').tolist():
        lower_speed = forecast_2026_2030.loc[date_str][0]
        upper_speed = forecast_2026_2030.loc[date_str][1]
        st.markdown(
             f"""
    <div class="prediction-card" style="
        background: linear-gradient(to right, #f757da, #168aad); 
        color: white; 
        border-radius: 15px; 
        padding: 20px; 
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);">
        <h2 style="color: white; text-align: center;">🍃 Prediction for {date_str}</h2>
        <p style="font-weight: bold; text-align: center;">Lower Speed:</p>
        <div style="border: 2px solid white; background-color: rgba(255, 255, 255, 0.1); color: white; 
                    font-size: 1.5em; font-weight: bold; text-align: center; 
                    padding: 10px; border-radius: 10px; width: 150px; margin: 0 auto;">
            {lower_speed:.2f} 💨km/h
        </div>
        <p style="font-weight: bold; text-align: center; margin-top: 20px;">Upper Speed:</p>
        <div style="border: 2px solid white; background-color: rgba(255, 255, 255, 0.1); color: white; 
                    font-size: 1.5em; font-weight: bold; text-align: center; 
                    padding: 10px; border-radius: 10px; width: 150px; margin: 0 auto;">
            {upper_speed:.2f} 🌪️km/h
        </div>
    </div>
    """,
            unsafe_allow_html=True
        )
    else:
        st.error("Date out of range. Please select a date between 2024 and 2026.")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        © 2024 Wind Forecast  | Designed by Samyohang Sherma
    </div>
    """,
    unsafe_allow_html=True
)
