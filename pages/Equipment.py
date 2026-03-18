import streamlit as st
import pandas as pd
import plotly.express as px
from utils import safe_load, find_col
from style import apply_style
apply_style()

st.title("⚙️ Equipment")

df = safe_load("equipment")

if df.empty:
    st.warning("โหลดข้อมูลไม่ได้")
else:
    kw_col = find_col(df, ["kw"])
    floor_col = find_col(df, ["floor"])

    st.dataframe(df, use_container_width=True)

    if floor_col and kw_col:
        df[kw_col] = df[kw_col].astype(float)

        chart = df.groupby(floor_col)[kw_col].sum().reset_index()

        fig = px.bar(
            chart,
            x=floor_col,
            y=kw_col,
            title="Energy per Floor"
        )

        st.plotly_chart(fig, use_container_width=True)