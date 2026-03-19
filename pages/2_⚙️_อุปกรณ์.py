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
    st.markdown(f"### 📋 รายการแอร์ {selected_floor}")

    table = df_floor[[room_col, btu_col, kw_col, cost_col]].copy()

    # rename ให้สวย
    table.columns = ["ห้อง/พื้นที่", "BTU", "kW", "฿/ชม."]

    # รวม
    total_row = {
        "ห้อง/พื้นที่": "รวม",
        "BTU": table["BTU"].sum(),
        "kW": table["kW"].sum(),
        "฿/ชม.": table["฿/ชม."].sum()
    }

    # format ตัวเลข
    def fmt(x):
        return f"{x:,.2f}" if isinstance(x, (int, float)) else x

    table_fmt = table.copy()
    table_fmt["BTU"] = table_fmt["BTU"].map(lambda x: f"{x:,.0f}")
    table_fmt["kW"] = table_fmt["kW"].map(lambda x: f"{x:,.2f}")
    table_fmt["฿/ชม."] = table_fmt["฿/ชม."].map(lambda x: f"{x:,.2f}")

    total_fmt = {
        "ห้อง/พื้นที่": "รวม",
        "BTU": f"{total_row['BTU']:,.0f}",
        "kW": f"{total_row['kW']:,.2f}",
        "฿/ชม.": f"{total_row['฿/ชม.']:,.2f}",
    }

    import pandas as pd
    table_fmt = pd.concat([table_fmt, pd.DataFrame([total_fmt])], ignore_index=True)

    st.dataframe(table_fmt, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    
    # ---------- RIGHT (CHART)
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 กำลังไฟ (kW) แยกห้อง")

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
    fig.update_traces(textposition="outside")

    st.plotly_chart(plot_theme(fig), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    
    
    
    # ─────────────────────────────
# ⚙️ BOTTOM SECTION (สรุปอุปกรณ์)
# ─────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown(f"### ⚙️ อุปกรณ์อื่น ๆ {selected_floor}")

import pandas as pd

total_kw = df_floor[kw_col].sum()
total_btu = df_floor[btu_col].sum() if btu_col else 0
total_cost = df_floor[cost_col].sum() if cost_col else 0

summary_df = pd.DataFrame([
    {
        "อุปกรณ์": "เครื่องปรับอากาศ (รวม)",
        "จำนวน": f"{total_btu:,.0f} BTU",
        "รวม kW": f"{total_kw:,.2f}",
        "บาท/ชม.": f"{total_cost:,.2f}"
    }
])

st.dataframe(summary_df, use_container_width=True, hide_index=True)

# metric ด้านล่าง
colA, colB = st.columns(2)

with colA:
    st.metric("รวม kW", f"{total_kw:,.2f}")

with colB:
    # สมมติเปิด 24 ชม. 30 วัน
    monthly = total_cost * 24 * 30
    st.metric("ประมาณค่าไฟ/เดือน", f"฿{monthly:,.0f}")

st.markdown('</div>', unsafe_allow_html=True)