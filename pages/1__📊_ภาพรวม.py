import streamlit as st
st.set_page_config(page_title="Dashboard Solarcell", page_icon="📊", layout="wide")

import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme

st.sidebar.markdown("## ⚡ Nature Biotech")

apply_style()

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.title("📊 Energy Overview")

df = safe_load("floor_summary")
ac_rooms = safe_load("ac_rooms")

# ─── KPI ─────────────────────────────────────────────────────
if df.empty:
    st.warning("โหลดข้อมูล floor_summary ไม่ได้")
else:
    # กันคอลัมน์หาย
    if "kpi" not in df.columns or "value_thb" not in df.columns:
        st.error("ไม่พบคอลัมน์ kpi หรือ value_thb ใน floor_summary")
        st.write("Columns:", df.columns.tolist())
        st.stop()

    df["kpi"] = df["kpi"].astype(str)
    df["value_thb"] = df["value_thb"].astype(str)

    def get_kpi(name):
        row = df[df["kpi"].str.contains(name, case=False, na=False)]
        if row.empty:
            return 0

        val = str(row["value_thb"].values[0]).replace(",", "").replace("%", "").strip()
        try:
            return float(val)
        except:
            return 0

    total_cost = get_kpi("รวม")
    solar_saving = get_kpi("Solar")
    net_cost = get_kpi("สุทธิ")
    percent = get_kpi("%")

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(
        f'<div class="card"><div class="label">💰 Total Cost</div><div class="metric">฿{total_cost:,.0f}</div></div>',
        unsafe_allow_html=True
    )
    c2.markdown(
        f'<div class="card"><div class="label">☀️ Solar Saving</div><div class="metric">฿{solar_saving:,.0f}</div></div>',
        unsafe_allow_html=True
    )
    c3.markdown(
        f'<div class="card"><div class="label">⚡ Net Cost</div><div class="metric">฿{net_cost:,.0f}</div></div>',
        unsafe_allow_html=True
    )
    c4.markdown(
        f'<div class="card"><div class="label">📉 Saving %</div><div class="metric">{percent:.1f}%</div></div>',
        unsafe_allow_html=True
    )

st.divider()

# ─── AC ROOMS ─────────────────────────────────────────────────
if ac_rooms.empty:
    st.warning("ไม่มีข้อมูล AC Rooms")
else:
    st.subheader("❄️ AC Rooms Analysis")

    room_col = find_col(ac_rooms, ["room", "ห้อง"])
    cost_col = find_col(ac_rooms, ["cost", "hour", "บาท"])

    if not room_col or not cost_col:
        st.error("หา column ของ AC Rooms ไม่เจอ")
        st.write("Columns:", ac_rooms.columns.tolist())
        st.stop()

    ac_rooms[cost_col] = to_num(ac_rooms[cost_col])

    chart = (
        ac_rooms
        .dropna(subset=[room_col, cost_col])
        .groupby(room_col, as_index=False)[cost_col]
        .sum()
        .sort_values(cost_col, ascending=False)
    )

    col1, col2 = st.columns(2)

    # BAR
    fig = px.bar(
        chart,
        x=room_col,
        y=cost_col,
        text=cost_col,
        title="ค่าไฟแต่ละห้อง (มาก → น้อย)"
    )
    fig.update_traces(textposition="outside")
    col1.plotly_chart(plot_theme(fig), use_container_width=True)

    # PIE
    fig2 = px.pie(
        chart,
        names=room_col,
        values=cost_col,
        hole=0.6,
        title="สัดส่วนค่าไฟแต่ละห้อง"
    )
    col2.plotly_chart(plot_theme(fig2), use_container_width=True)

    if not chart.empty:
        top = chart.iloc[0]
        st.error(f"🔥 ห้องกินไฟสูงสุด: {top[room_col]} ({top[cost_col]:,.0f} บาท)")

        st.subheader("🏆 Top 5 ห้องกินไฟสูงสุด")
        st.dataframe(chart.head(5), use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("📋 รายการห้องแอร์ทั้งหมด")
    st.dataframe(ac_rooms, use_container_width=True, hide_index=True)