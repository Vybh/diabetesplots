import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df = pd.read_csv("diabetes_012_health_indicators_BRFSS2015.csv")

st.title("Diabetes Modeller")

plot_choice = st.sidebar.radio("Choice:", ["CorrPlot", "BMI vs Age", "BMI vs Diabetes", "Histogram"])

if plot_choice == "CorrPlot":
    st.header("Correlation Heatmap of Health Factors")
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(12,8))
    sns.heatmap(corr, mask=mask, annot=False, cmap='coolwarm', center=0)
    st.pyplot(fig)

elif plot_choice == "BMI vs Age":
    st.header("BMI vs Age Scatter Plot")

    def assign_color(row):
        if row["HighBP"] == 0 and row["HighChol"] == 0:
            return "lightblue"   
        elif row["HighBP"] == 1 and row["HighChol"] == 0:
            return "orange"        
        elif row["HighBP"] == 0 and row["HighChol"] == 1:
            return "pink"      
        else:
            return "red"

    df["color"] = df.apply(assign_color, axis=1)

    fig, ax = plt.subplots()
    ax.scatter(df["BMI"], df["Age"], c=df["color"], alpha=0.6)
    ax.set_xlabel("BMI")
    ax.set_ylabel("Age")
    ax.set_title("BMI vs Age (Colored by BP & Cholesterol Status)")
    st.pyplot(fig)

elif plot_choice == "BMI vs Diabetes":
    st.header("BMI Distribution by Diabetes Status")

    fig, ax = plt.subplots(figsize=(8,6))
    sns.boxplot(x=df["Diabetes_012"], y=df["BMI"], palette="Set2", ax=ax)
    ax.set_xticklabels(["No Diabetes", "Prediabetes", "Diabetes"])
    ax.set_xlabel("Diabetes Status")
    ax.set_ylabel("BMI")
    ax.set_title("Distribution of BMI by Diabetes Status")
    st.pyplot(fig)

elif plot_choice == "Histogram":
    st.header("5. Cumulative Histogram of Cholesterol Levels")
    plt.figure(figsize=(8,5))
    plt.hist(df["HighChol"], bins=5, cumulative=True, density=True, color="purple", alpha=0.7)
    plt.xlabel("High Cholesterol (0=No, 1=Yes)")
    plt.ylabel("Cumulative Proportion")
    st.pyplot(plt)
