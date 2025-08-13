import streamlit as st
import pandas as pd
import json
from datetime import datetime
import altair as alt
import numpy as np

data = pd.read_csv("diabetes_012_health_indicators_BRFSS2015.csv")

st.title("Diabetes Modeller")

plot_choice = st.sidebar.radio("Choice:", ["CorrPlot"])

if plot_choice == "CorrPlot":
  st.header("Correlation Heatmap of Health Factors")

  corr = df.corr()
  mask = np.triu(np.ones_like(corr, dtype=bool))
  
  fig, ax = plt.subplots(figsize=(12,8))
  sns.heatmap(corr, mask=mask, annot=False, cmap='coolwarm', center=0)
  st.pyplot(fig)

