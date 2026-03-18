import streamlit as st
import pandas as pd
import plotly.express as px
from utils import safe_load
from style import apply_style
apply_style()

st.title("☀️ Solar Analysis")

df = safe_load("solar_monthly")

if df.empty:
    st.warning("โหลดข้อมูล Solar ไม่ได้")
else:
    df["solar_saving_thb"] = pd.to_numeric(
        df["solar_saving_thb"], errors="coerce"
    )

    df = df[df["solar_saving_thb"].notna()]

    fig = px.line(
        df,
        x="month_th",
        y="solar_saving_thb",
        markers=True,
        title="Solar Saving ต่อเดือน"
    )

    st.plotly_chart(fig, use_container_width=True)

    total = df["solar_saving_thb"].sum()
    st.metric("รวมประหยัด", f"฿{total:,.0f}")

    st.dataframe(df, use_container_width=True)