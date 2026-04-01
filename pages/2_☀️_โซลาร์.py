import pandas as pd
import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme

st.set_page_config(page_title="Solar Analysis", page_icon="☀️", layout="wide")
apply_style()

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.title("☀️ Solar Analysis")

df = safe_load("solar_monthly")

if df.empty:
    st.warning("โหลดข้อมูล Solar Monthly ไม่ได้ — ลองกด Refresh หรือเช็ค GID")
    st.stop()

# ---------------- หา column ----------------
month_col  = find_col(df, ["month_th", "month", "เดือน"])
saving_col = find_col(df, ["solar_saving_thb", "saving", "solar", "kw", "kwh", "energy"])
num_col    = find_col(df, ["month_num", "num", "เดือนที่"])
year_col   = find_col(df, ["year", "ปี", "year_be", "พศ", "พ.ศ."])

if saving_col:
    df[saving_col] = to_num(df[saving_col])

if num_col:
    df[num_col] = to_num(df[num_col])

if year_col:
    df[year_col] = to_num(df[year_col])

# ---------------- filter ปี ----------------
top_left, top_right = st.columns([4, 1])

with top_left:
    st.markdown("#### โซล่าเซลล์รายเดือน")

selected_year = None
if year_col and df[year_col].notna().any():
    years = sorted(df[year_col].dropna().astype(int).unique().tolist(), reverse=True)
    with top_right:
        selected_year = st.selectbox("เลือกปี", years, index=0)
    df = df[df[year_col].astype("Int64") == selected_year]
else:
    with top_right:
        st.markdown("### ")
        st.caption("ไม่พบคอลัมน์ปี")

# ---------------- เรียงเดือน ----------------
if num_col:
    df = df.sort_values(num_col)

# ---------------- ชื่อเดือน ----------------
thai_months = {
    1: "มกราคม", 2: "กุมภาพันธ์", 3: "มีนาคม", 4: "เมษายน",
    5: "พฤษภาคม", 6: "มิถุนายน", 7: "กรกฎาคม", 8: "สิงหาคม",
    9: "กันยายน", 10: "ตุลาคม", 11: "พฤศจิกายน", 12: "ธันวาคม"
}

if not month_col and num_col:
    df["month_label"] = df[num_col].map(thai_months)
    month_col = "month_label"

# ---------------- KPI รวม ----------------
if saving_col and not df.empty:
    total = df[saving_col].fillna(0).sum()
    st.markdown(
        f"""
        <div class="card">
            <div class="label">รวมประหยัดทั้งปี</div>
            <div class="metric">฿{total:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### ประหยัดค่าไฟจากแผงโซล่าเซลล์ (บาท)")

# ---------------- การ์ดรายเดือนด้านบน ----------------
if saving_col and month_col:
    months_order = list(range(1, 13))
    month_name_map = {i: thai_months[i] for i in months_order}

    monthly_dict = {}
    for i in months_order:
        monthly_dict[i] = None

    for _, row in df.iterrows():
        m = None
        if num_col and not pd.isna(row[num_col]):
            try:
                m = int(row[num_col])
            except:
                m = None

        if m in monthly_dict:
            monthly_dict[m] = row[saving_col]

    cols = st.columns(4)
    for idx, m in enumerate(months_order):
        value = monthly_dict[m]
        month_name = month_name_map[m]

        if value is None or pd.isna(value):
            value_text = "—"
        else:
            value_text = f"฿{value:,.0f}"

        cols[idx % 4].markdown(
            f"""
            <div style="
                background:#f8fafc;
                border:1px solid #d1d5db;
                border-radius:12px;
                padding:14px 12px;
                margin-bottom:10px;
                text-align:center;
            ">
                <div style="font-size:13px; color:#64748b;">{month_name}</div>
                <div style="font-size:28px; font-weight:700; color:#16a34a;">{value_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ---------------- กราฟ ----------------
if month_col and saving_col and not df.empty:
    chart_df = df.copy()

    if num_col:
        chart_df = chart_df.sort_values(num_col)

    fig = px.bar(
        chart_df,
        x=month_col,
        y=saving_col,
        text_auto=True,
        title=f"Solar Saving ต่อเดือน{f' ปี {selected_year}' if selected_year else ''}"
    )
    fig.update_traces(marker_color="#86efac", marker_line_color="#22c55e", marker_line_width=1.2)
    st.plotly_chart(plot_theme(fig), use_container_width=True)
else:
    st.info(f"หาคอลัมน์ month/saving ไม่เจอ — คอลัมน์ที่มี: {', '.join(df.columns)}")

# ---------------- ตาราง ----------------
st.subheader("📋 ข้อมูลรายเดือน")
st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------- debug ไปล่างสุด ----------------
# with st.expander("🔍 Debug: ดูคอลัมน์จริง"):
#     st.write(list(df.columns))
#     st.dataframe(df.head(10), use_container_width=True)