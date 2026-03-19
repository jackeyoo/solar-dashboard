import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme
import pandas as pd

apply_style()

# 🎨 UI
def apply_custom_ui():
    st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }

    .card {
        background: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

st.title("⚡ Energy Dashboard")

# 🔘 เลือกหน้า
view = st.radio(
    "เลือกหมวด",
    ["❄️ แอร์", "🏭 เครื่องจักร ชั้น 3"],
    horizontal=True
)

# ─────────────────────────────
# ❄️ PAGE: AC ROOMS
# ─────────────────────────────
if view == "❄️ แอร์":

    df = safe_load("ac_rooms")

    if df.empty:
        st.error("โหลด AC_Rooms ไม่ได้")
        st.stop()

    floor_col = find_col(df, ["floor"])
    room_col  = find_col(df, ["room"])
    kw_col    = find_col(df, ["kw"])
    btu_col   = find_col(df, ["btu"])
    cost_col  = find_col(df, ["cost"])

    for col in [kw_col, btu_col, cost_col]:
        if col:
            df[col] = to_num(df[col])

    floors = sorted(df[floor_col].dropna().unique())

    selected_floor = st.radio("เลือกชั้น", floors, horizontal=True)
    df_floor = df[df[floor_col] == selected_floor]

    col1, col2 = st.columns([1.2, 1])

    # TABLE
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        table = df_floor[[room_col, btu_col, kw_col, cost_col]].copy()
        table.columns = ["ห้อง", "BTU", "kW", "฿/ชม."]

        total = table.sum(numeric_only=True)

        total_row = pd.DataFrame([{
            "ห้อง": "รวม",
            "BTU": total["BTU"],
            "kW": total["kW"],
            "฿/ชม.": total["฿/ชม."]
        }])

        table = pd.concat([table, total_row])

        st.dataframe(table, use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # CHART
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        fig = px.bar(
            df_floor,
            x=kw_col,
            y=room_col,
            orientation="h",
            text_auto=True,
            color=kw_col
        )

        st.plotly_chart(plot_theme(fig), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # SUMMARY
    st.markdown('<div class="card">', unsafe_allow_html=True)

    total_kw = df_floor[kw_col].sum()
    total_cost = df_floor[cost_col].sum()

    colA, colB = st.columns(2)

    with colA:
        st.metric("รวม kW", f"{total_kw:,.2f}")

    with colB:
        st.metric("ค่าไฟ/เดือน", f"฿{total_cost*24*30:,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────
# 🏭 PAGE: MACHINES
# ─────────────────────────────
else:

    df = safe_load("machines_floor3")

    if df.empty:
        st.error("โหลด Machines_Floor3 ไม่ได้")
        st.stop()

    name_col = find_col(df, ["machine"])
    kw_col   = find_col(df, ["kw"])
    cost_col = find_col(df, ["cost"])
    qty_col  = find_col(df, ["qty", "quantity"])

    for col in [kw_col, cost_col, qty_col]:
        if col:
            df[col] = to_num(df[col])

    col1, col2 = st.columns([1.2, 1])

    # TABLE
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        table = df[[name_col, qty_col, kw_col, cost_col]].copy()
        table.columns = ["เครื่องจักร", "จำนวน", "kW", "฿/ชม."]

        st.dataframe(table, use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # CHART
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        fig = px.bar(
            df,
            x=kw_col,
            y=name_col,
            orientation="h",
            text_auto=True,
            color=kw_col,
            color_continuous_scale="Oranges"
        )

        st.plotly_chart(plot_theme(fig), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # SUMMARY
    st.markdown('<div class="card">', unsafe_allow_html=True)

    total_kw = df[kw_col].sum()
    total_cost = df[cost_col].sum()

    colA, colB = st.columns(2)

    with colA:
        st.metric("รวม kW", f"{total_kw:,.2f}")

    with colB:
        st.metric("ค่าไฟ/เดือน", f"฿{total_cost*24*30:,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)