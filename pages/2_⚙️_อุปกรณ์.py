import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme
import pandas as pd

# ─────────────────────────────
# 🎨 UI STYLE
# ─────────────────────────────
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

    div[role="radiogroup"] > label {
        background: #f1f5f9;
        padding: 8px 16px;
        border-radius: 8px;
        margin-right: 8px;
    }

    div[role="radiogroup"] > label[data-selected="true"] {
        background: #0ea5e9;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

apply_style()
apply_custom_ui()

st.title("⚡ Energy Dashboard")

# ─────────────────────────────
# 📥 LOAD AC DATA
# ─────────────────────────────
df = safe_load("ac_rooms")
if df.empty:
    st.error("โหลด AC_Rooms ไม่ได้")
    st.stop()

# ─────────────────────────────
# 🔎 MAP COLUMN
# ─────────────────────────────
floor_col = find_col(df, ["floor"])
room_col  = find_col(df, ["room"])
kw_col    = find_col(df, ["kw"])
btu_col   = find_col(df, ["btu"])
cost_col  = find_col(df, ["cost"])

for col in [kw_col, btu_col, cost_col]:
    if col:
        df[col] = to_num(df[col])

# ─────────────────────────────
# 🔘 MENU (รวมเครื่องจักร)
# ─────────────────────────────
floors = sorted(df[floor_col].dropna().unique())
menu = floors + ["🏭 เครื่องจักร ชั้น 3"]

selected = st.radio("เลือกชั้น", menu, horizontal=True)

# ─────────────────────────────
# 🏭 MACHINE PAGE
# ─────────────────────────────
if selected == "🏭 เครื่องจักร ชั้น 3":

    df_m = safe_load("machines_floor3")

    if df_m.empty:
        st.error("โหลด Machines_Floor3 ไม่ได้")
        st.stop()

    name_col = find_col(df_m, ["machine"])
    kw_col_m = find_col(df_m, ["kw"])
    cost_col_m = find_col(df_m, ["cost"])
    qty_col = find_col(df_m, ["qty", "quantity"])

    for col in [kw_col_m, cost_col_m, qty_col]:
        if col:
            df_m[col] = to_num(df_m[col])

    col1, col2 = st.columns([1.2, 1])

    # TABLE
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        table = df_m[[name_col, qty_col, kw_col_m, cost_col_m]].copy()
        table.columns = ["เครื่องจักร", "จำนวน", "kW", "฿/ชม."]

        st.dataframe(table, use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # CHART
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        fig = px.bar(
            df_m,
            x=kw_col_m,
            y=name_col,
            orientation="h",
            text_auto=True,
            color=kw_col_m,
            color_continuous_scale="Oranges"
        )

        fig.update_layout(height=420)

        st.plotly_chart(plot_theme(fig), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # SUMMARY
    st.markdown('<div class="card">', unsafe_allow_html=True)

    total_kw = df_m[kw_col_m].sum()
    total_cost = df_m[cost_col_m].sum()

    colA, colB = st.columns(2)

    with colA:
        st.metric("รวม kW", f"{total_kw:,.2f}")

    with colB:
        st.metric("ค่าไฟ/เดือน", f"฿{total_cost*24*30:,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────
# ❄️ AC PAGE
# ─────────────────────────────
else:

    selected_floor = selected
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
            color=kw_col,
            color_continuous_scale="Blues"
        )

        fig.update_layout(height=420)

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