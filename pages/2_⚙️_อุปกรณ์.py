import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme

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

st.title("❄️ AC Rooms Dashboard")

# ─────────────────────────────
# 📥 LOAD DATA
# ─────────────────────────────
df = safe_load("ac_rooms")

if df.empty:
    st.error("โหลด AC_Rooms ไม่ได้")
    st.stop()

# DEBUG (ลบออกทีหลังได้)
# st.write(df.columns)

# ─────────────────────────────
# 🔎 AUTO MAP COLUMN (กันพัง)
# ─────────────────────────────
floor_col = find_col(df, ["floor"])
room_col  = find_col(df, ["room"])
kw_col    = find_col(df, ["kw"])
btu_col   = find_col(df, ["btu"])
cost_col  = find_col(df, ["cost"])
unit_col  = find_col(df, ["unit"])

required = [floor_col, room_col, kw_col]

if any(c is None for c in required):
    st.error(f"❌ หา column ไม่ครบ: {df.columns.tolist()}")
    st.stop()

# ─────────────────────────────
# 🔧 CLEAN DATA
# ─────────────────────────────
for col in [kw_col, btu_col, cost_col, unit_col]:
    if col:
        df[col] = to_num(df[col])

# ─────────────────────────────
# 🏢 FLOOR SELECT
# ─────────────────────────────
floors = sorted(df[floor_col].dropna().unique())

selected_floor = st.radio(
    "เลือกชั้น",
    floors,
    horizontal=True
)

df_floor = df[df[floor_col] == selected_floor]

# ─────────────────────────────
# 📊 TOP SECTION
# ─────────────────────────────
col1, col2 = st.columns([1.2, 1])

# ---------- LEFT (TABLE)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📋 รายการเครื่องปรับอากาศ")

    show_cols = [room_col]

    if btu_col: show_cols.append(btu_col)
    if kw_col: show_cols.append(kw_col)
    if cost_col: show_cols.append(cost_col)

    st.dataframe(
        df_floor[show_cols],
        use_container_width=True,
        hide_index=True
    )

    # รวม
    st.markdown("#### 🔢 รวม")

    if btu_col:
        st.write(f"BTU: {df_floor[btu_col].sum():,.0f}")

    st.write(f"kW: {df_floor[kw_col].sum():,.2f}")

    if cost_col:
        st.write(f"บาท/ชม.: {df_floor[cost_col].sum():,.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RIGHT (CHART)
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 กำลังไฟ (kW)")

    chart = df_floor.sort_values(kw_col)

    fig = px.bar(
        chart,
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

# ─────────────────────────────
# ⚙️ BOTTOM SECTION
# ─────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown(f"### ⚙️ รายละเอียดทั้งหมด - {selected_floor}")

st.dataframe(df_floor, use_container_width=True, hide_index=True)

# summary
colA, colB = st.columns(2)

with colA:
    st.metric("รวม kW", f"{df_floor[kw_col].sum():,.2f}")

with colB:
    if cost_col:
        st.metric("รวม บาท/ชม.", f"{df_floor[cost_col].sum():,.2f}")

st.markdown('</div>', unsafe_allow_html=True)