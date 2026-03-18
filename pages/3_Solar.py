import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme

st.set_page_config(page_title="Solar", page_icon="☀️", layout="wide")
apply_style()

st.sidebar.markdown("## ⚡ Nature Biotech")
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.title("☀️ Solar Analysis")

df = safe_load("solar_monthly")

if df.empty:
    st.warning("โหลดข้อมูล Solar Monthly ไม่ได้ — ลองกด Refresh หรือเช็ค GID")
    st.stop()

# ─── debug: แสดงคอลัมน์จริง ───────────────────────────────────────────────────
with st.expander("🔍 ดูคอลัมน์จริง (debug)"):
    st.write(list(df.columns))
    st.dataframe(df.head(3), use_container_width=True)

# ─── หาคอลัมน์ ────────────────────────────────────────────────────────────────
month_col  = find_col(df, ["month_th", "month", ""])
saving_col = find_col(df, ["solar_saving_thb", "saving", "solar", "kw", "kwh", "energy"])
num_col    = find_col(df, ["month_num", "num"])

if saving_col:
    df[saving_col] = to_num(df[saving_col])
    df = df[df[saving_col].notna()]

if num_col:
    df[num_col] = to_num(df[num_col])
    df = df.sort_values(num_col)

# ─── KPI ──────────────────────────────────────────────────────────────────────
if saving_col:
    total = df[saving_col].sum()
    st.markdown(
        f'<div class="card"><div class="label">รวมประหยัดทั้งปี</div>'
        f'<div class="metric">฿{total:,.0f}</div></div>',
        unsafe_allow_html=True,
    )

st.divider()

# ─── กราฟ ─────────────────────────────────────────────────────────────────────
if month_col and saving_col:
    fig = px.line(df, x=month_col, y=saving_col, markers=True,
                  title="Solar Saving ต่อเดือน")
    st.plotly_chart(plot_theme(fig), use_container_width=True)

    fig2 = px.bar(df, x=month_col, y=saving_col, text_auto=True,
                  color=saving_col, color_continuous_scale="YlOrRd",
                  title="Solar Saving (Bar)")
    st.plotly_chart(plot_theme(fig2), use_container_width=True)
else:
    st.info(f"หาคอลัมน์ month/saving ไม่เจอ — คอลัมน์ที่มี: `{'`, `'.join(df.columns)}`")

# ─── ตาราง ────────────────────────────────────────────────────────────────────
st.subheader("📋 ข้อมูลรายเดือน")
st.dataframe(df, use_container_width=True, hide_index=True)