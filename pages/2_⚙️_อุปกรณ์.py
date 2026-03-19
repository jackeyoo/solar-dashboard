import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme

# ─────────────────────────────
# 🎨 Style (ทำให้เป็น Card + Dashboard)
# ─────────────────────────────
def apply_custom_ui():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* Card */
    .card {
        background: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }

    h3 {
        margin-bottom: 12px;
    }

    /* radio button inline */
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


# ใช้ style เดิม + custom
apply_style()
apply_custom_ui()

# ─────────────────────────────
# 🔄 Refresh
# ─────────────────────────────
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.title("⚙️ Equipment Analysis")

# ─────────────────────────────
# 📥 Load Data
# ─────────────────────────────
df = safe_load("equipment")

if df.empty:
    st.warning("โหลดข้อมูล Equipment ไม่ได้ — ลองกด Refresh หรือเช็ค GID")
    st.stop()

# ─────────────────────────────
# 🔎 หา column
# ─────────────────────────────
kw_col   = find_col(df, ["kw", "watt", "power"])
cost_col = find_col(df, ["per_hour", "cost", "hour", "price"])
floor_col= find_col(df, ["floor", "ชั้น"])
name_col = find_col(df, ["equipment", "type", "machine", "name"])

# แปลงตัวเลข
if kw_col:
    df[kw_col] = to_num(df[kw_col])
if cost_col:
    df[cost_col] = to_num(df[cost_col])

# ─────────────────────────────
# 🏢 เลือกชั้น (เหมือนปุ่มด้านบน)
# ─────────────────────────────
if not floor_col:
    st.error("ไม่พบ column ชั้น")
    st.stop()

floors = sorted(df[floor_col].dropna().unique())

selected_floor = st.radio(
    "เลือกชั้น",
    floors,
    horizontal=True
)

df_floor = df[df[floor_col] == selected_floor]

# ─────────────────────────────
# 📊 SECTION บน (ซ้าย=ตาราง | ขวา=กราฟ)
# ─────────────────────────────
col1, col2 = st.columns([1.2, 1])

# ---------- LEFT (TABLE)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📋 รายการเครื่องปรับอากาศ")

    st.dataframe(
        df_floor,
        use_container_width=True,
        hide_index=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RIGHT (CHART)
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 กำลังไฟ (kW) แยกห้อง")

    if kw_col and name_col:
        chart = (
            df_floor.groupby(name_col)[kw_col]
            .sum()
            .reset_index()
            .sort_values(kw_col)
        )

        fig = px.bar(
            chart,
            x=kw_col,
            y=name_col,
            orientation="h",   # 👈 ทำให้เหมือนในรูป
            text_auto=True,
            color=kw_col,
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        st.plotly_chart(plot_theme(fig), use_container_width=True)
    else:
        st.info("ไม่พบ column kw/name")

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────
# ⚙️ SECTION ล่าง (ตารางรวม)
# ─────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown(f"### ⚙️ อุปกรณ์ทั้งหมด - ชั้น {selected_floor}")

summary = df_floor.copy()

# รวมค่า
if kw_col:
    total_kw = summary[kw_col].sum()
else:
    total_kw = 0

if cost_col:
    total_cost = summary[cost_col].sum()
else:
    total_cost = 0

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# แสดง summary แบบใน dashboard
colA, colB = st.columns(2)

with colA:
    st.metric("รวม kW", f"{total_kw:,.2f}")

with colB:
    st.metric("รวม Cost/Hour", f"{total_cost:,.2f}")

st.markdown('</div>', unsafe_allow_html=True)