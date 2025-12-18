import streamlit as st
import pandas as pd

st.title("AI FinInvest – MHXS 9 ECL Demo")

uploaded_file = st.file_uploader("Excel faylni yuklang", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Yuklangan ma'lumotlar")
    st.dataframe(df)

    def assign_stage(days):
        if days <= 30:
            return "Stage 1"
        elif days <= 90:
            return "Stage 2"
        else:
            return "Stage 3"

    df["Stage"] = df["days_past_due"].apply(assign_stage)

    pd_map = {"A": 0.02, "B": 0.06, "C": 0.15}
    df["PD"] = df["credit_rating"].map(pd_map)

    df["LGD"] = df["collateral"].apply(lambda x: 0.3 if x == "Yes" else 0.6)
    df["EAD"] = df["nominal_amount"]

    df["ECL"] = df["PD"] * df["LGD"] * df["EAD"]

    st.subheader("ECL hisob-kitobi")
    st.dataframe(df[["asset_id", "Stage", "PD", "LGD", "EAD", "ECL"]])

    st.subheader("Umumiy ECL")
    st.metric("Jami ECL (so‘m)", f"{df['ECL'].sum():,.0f}")
