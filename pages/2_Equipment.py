import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme



# from components.sidebar import render_sidebar
# from style import apply_style
# apply_style()
# render_sidebar()























st.title("⚙️ Equipment Analysis")

df = safe_load("equipment")

if df.empty:
    st.warning("โหลดข้อมูล Equipment ไม่ได้ — ลองกด Refresh หรือเช็ค GID")
    st.stop()

# ─── แปลงตัวเลข ───────────────────────────────────────────────────────────────
kw_col   = find_col(df, ["kw", "watt", "power"])
cost_col = find_col(df, ["per_hour", "cost", "hour", "price"])
floor_col= find_col(df, ["floor", ""])
name_col = find_col(df, ["equipment", "type", "machine", "name"])

if kw_col:
    df[kw_col]   = to_num(df[kw_col])
if cost_col:
    df[cost_col] = to_num(df[cost_col])

# ─── ตาราง ────────────────────────────────────────────────────────────────────
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ─── กราฟ kW แต่ละชั้น ────────────────────────────────────────────────────────
if floor_col and kw_col:
    chart = df.groupby(floor_col, dropna=False)[kw_col].sum().reset_index()
    fig = px.bar(chart, x=floor_col, y=kw_col, text_auto=True,
                 color=kw_col, color_continuous_scale="Teal",
                 title="Power (kW) by Floor")
    st.plotly_chart(plot_theme(fig), use_container_width=True)
else:
    st.info(f"หาคอลัมน์ floor/kw ไม่เจอ — คอลัมน์ที่มี: `{'`, `'.join(df.columns)}`")

# ─── กราฟ cost รายอุปกรณ์ ─────────────────────────────────────────────────────
if name_col and cost_col:
    top = (
        df[[name_col, cost_col]].dropna()
        .sort_values(cost_col, ascending=False)
        .head(10)
    )
    fig2 = px.bar(top, x=name_col, y=cost_col, text_auto=True,
                  color=cost_col, color_continuous_scale="Sunset",
                  title="Top 10 Equipment by Cost/Hour")
    st.plotly_chart(plot_theme(fig2), use_container_width=True)