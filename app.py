import streamlit as st
import pandas as pd
import json
from datetime import datetime
import altair as alt

data = pd.read_csv(".csv")

st.title("Diabetes Modeller")

plot_choice = st.sidebar.radio("Choice:", ["BarPlot", "LinePlot", "AreaPlot", "ScatterPlot"])
