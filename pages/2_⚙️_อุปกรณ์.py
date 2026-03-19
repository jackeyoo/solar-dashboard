import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme

# ─────────────────────────────
# 🎨 UI Style
# ─────────────────────────────
def apply_custom_ui():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
    }

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

st.title("❄️ AC Rooms Dashboard")

# ─────────────────────────────
# 📥 โหลด AC_Rooms
# ─────────────────────────────
df = safe_load("ac_rooms")

if df.empty:
    st.error("โหลด ac_rooms ไม่ได้")
    st.stop()

# ─────────────────────────────
# 🔧 แปลงข้อมูล
# ─────────────────────────────
df["kW"] = to_num(df["kW"])
df["Cost Per Hour THB"] = to_num(df["Cost Per Hour THB"])
df["BTU"] = to_num(df["BTU"])
df["Unit Count"] = to_num(df["Unit Count"])

# ─────────────────────────────
# 🏢 เลือกชั้น
# ─────────────────────────────
floors = sorted(df["Floor"].dropna().unique())

selected_floor = st.radio(
    "เลือกชั้น",
    floors,
    horizontal=True
)

df_floor = df[df["Floor"] == selected_floor]

# ─────────────────────────────
# 📊 TOP SECTION
# ─────────────────────────────
col1, col2 = st.columns([1.2, 1])

# ---------- TABLE ----------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📋 รายการเครื่องปรับอากาศ")

    display = df_floor[[
        "Room", "BTU", "kW", "Cost Per Hour THB"
    ]]

    st.dataframe(display, use_container_width=True, hide_index=True)

    # รวม
    st.markdown("#### 🔢 รวม")
    st.write(f"BTU: {display['BTU'].sum():,.0f}")
    st.write(f"kW: {display['kW'].sum():,.2f}")
    st.write(f"บาท/ชม.: {display['Cost Per Hour THB'].sum():,.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- CHART ----------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 กำลังไฟ (kW) แยกห้อง")

    chart = df_floor.sort_values("kW")

    fig = px.bar(
        chart,
        x="kW",
        y="Room",
        orientation="h",
        text_auto=True,
        color="kW",
        color_continuous_scale="Blues"
    )

    fig.update_layout(height=420)

    st.plotly_chart(plot_theme(fig), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────
# ⚙️ BOTTOM SECTION
# ─────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown(f"### ⚙️ อุปกรณ์ทั้งหมด - {selected_floor}")

st.dataframe(df_floor, use_container_width=True, hide_index=True)

# summary
total_kw = df_floor["kW"].sum()
total_cost = df_floor["Cost Per Hour THB"].sum()

colA, colB = st.columns(2)

with colA:
    st.metric("รวม kW", f"{total_kw:,.2f}")

with colB:
    st.metric("รวม บาท/ชั่วโมง", f"{total_cost:,.2f}")

st.markdown('</div>', unsafe_allow_html=True)