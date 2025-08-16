import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df = pd.read_csv("diabetes_012_health_indicators_BRFSS2015.csv")

st.title("Diabetes Modeller")

plot_choice = st.sidebar.radio("Choice:", ["CorrPlot", "BMI vs Age", "Risk Factors"])

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

elif plot_choice == "Risk Factors":
    st.header("Smoker vs HighBP vs HighChol in Diabetics vs Non-Diabetics")
    df["DiabetesStatus"] = df["Diabetes_012"].apply(lambda x: "Diabetic" if x > 0 else "Non-Diabetic")
    risk_factors = ["Smoker", "HighBP", "HighChol"]
    df_melted = df.melt(id_vars="DiabetesStatus", value_vars=risk_factors,
                        var_name="RiskFactor", value_name="Value")
    df_melted = df_melted[df_melted["Value"] == 1]
    proportions = df_melted.groupby(["DiabetesStatus", "RiskFactor"]).size().reset_index(name="Count")
    proportions["Proportion"] = proportions.groupby("DiabetesStatus")["Count"].apply(lambda x: x / x.sum())
    chart = alt.Chart(proportions).mark_bar().encode(
        x=alt.X("RiskFactor:N", title="Risk Factor"),
        y=alt.Y("Proportion:Q", title="Proportion"),
        color="DiabetesStatus:N",
        column=alt.Column("DiabetesStatus:N", title="Diabetes Status")
    ).properties(
        width=200,
        height=300,
        title="Risk Factor Proportions: Diabetic vs Non-Diabetic"
    )
    st.altair_chart(chart, use_container_width=True)
