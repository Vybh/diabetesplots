import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df = pd.read_csv("diabetes_012_health_indicators_BRFSS2015.csv")

st.title("Diabetes Modeller")

plot_choice = st.sidebar.radio("Choice:", ["Diabetes Heatmap", "BMI vs Age", "BMI vs Diabetes", "Histogram"])

if plot_choice == "Diabetes Heatmap":
    st.header("Correlation of Health Factors with Diabetes")

    numeric_df = df.select_dtypes(include=["float64", "int64"])
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(corr, cmap="coolwarm", center=0, annot=True, fmt=".2f", linewidths=0.5)
    ax.set_title("Correlation Heatmap: Diabetes vs Health Factors")
    st.pyplot(fig)

    st.subheader("Feature Correlations with Diabetes_012")
    diabetes_corr = corr["Diabetes_012"].sort_values(ascending=False)
    st.write(diabetes_corr)

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
    st.header("4. 2D Histogram (Heatmap) of BMI vs Age")
    plt.figure(figsize=(8,6))
    plt.hist2d(df["Age"], df["BMI"], bins=[30,30], cmap="Blues")
    plt.colorbar(label="Frequency")
    plt.xlabel("Age")
    plt.ylabel("BMI")
    st.pyplot(plt)
