import streamlit as st
import pandas as pd
import plotly.express as px
from utils import safe_load

st.title("☀️ Solar Analysis")
st.write("PAGE LOADED")  # debug

df = safe_load("solar_monthly")

if df.empty:
    st.warning("โหลดข้อมูล Solar ไม่ได้")
else:
    st.write(df.head())  # debug ดู data

    if "solar_saving_thb" not in df.columns:
        st.error("ไม่มี column solar_saving_thb")
        st.write(df.columns)
        st.stop()

    df["solar_saving_thb"] = pd.to_numeric(
        df["solar_saving_thb"], errors="coerce"
    )

    df = df[df["solar_saving_thb"].notna()]

    fig = px.line(
        df,
        x="month_th",
        y="solar_saving_thb",
        markers=True,
    )

    st.plotly_chart(fig, use_container_width=True)