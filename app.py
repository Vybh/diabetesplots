import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("diabetes_012_health_indicators_BRFSS2015.csv")

st.title("Diabetes Modeller")

plot_choice = st.sidebar.radio("Choice:", ["CorrPlot", "BMI vs Age"])

if plot_choice == "CorrPlot":
    st.header("Correlation Heatmap of Health Factors")
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(12,8))
    sns.heatmap(corr, mask=mask, annot=False, cmap='coolwarm', center=0)
    st.pyplot(fig)

elif plot_choice == "BMI vs Age":
    st.header("BMI vs Age Scatter Plot")

    # Map conditions to colors
    def assign_color(row):
        if row["HighBP"] == 0 and row["HighChol"] == 0:
            return "lightblue"   # Neither
        elif row["HighBP"] == 1 and row["HighChol"] == 0:
            return "pink"        # Only High BP
        elif row["HighBP"] == 0 and row["HighChol"] == 1:
            return "orange"      # Only High Cholesterol
        else:
            return "red"         # Both

    df["color"] = df.apply(assign_color, axis=1)

    fig, ax = plt.subplots()
    ax.scatter(df["BMI"], df["Age"], c=df["color"], alpha=0.6)
    ax.set_xlabel("BMI")
    ax.set_ylabel("Age")
    ax.set_title("BMI vs Age (Colored by BP & Cholesterol Status)")

    # Add a custom legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Neither', markerfacecolor='lightblue', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Only High BP', markerfacecolor='pink', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Only High Cholesterol', markerfacecolor='orange', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Both', markerfacecolor='red', markersize=8)
    ]
    ax.legend(handles=legend_elements, title="Condition")

    st.pyplot(fig)
