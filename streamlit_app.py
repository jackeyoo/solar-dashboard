# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.set_page_config(page_title="Energy Dashboard", layout="wide")

# # ---------------- STYLE ----------------
# st.markdown("""
# <style>
# body {
#     background-color: #0F172A;
# }
# .block-container {
#     padding-top: 2rem;
# }
# .card {
#     background: #1E293B;
#     padding: 20px;
#     border-radius: 15px;
# }
# .metric {
#     font-size: 28px;
#     font-weight: bold;
#     color: white;
# }
# .label {
#     font-size: 14px;
#     color: #94A3B8;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- SIDEBAR ----------------
# if "page" not in st.session_state:
#     st.session_state.page = "Overview"

# st.sidebar.markdown("## ⚡ Nature Biotech")

# if st.sidebar.button("📊 Overview"):
#     st.session_state.page = "Overview"
# if st.sidebar.button("⚙️ Equipment"):
#     st.session_state.page = "Equipment"
# if st.sidebar.button("☀️ Solar"):
#     st.session_state.page = "Solar"

# page = st.session_state.page

# # ---------------- DATA ----------------
# SHEET_ID = "1VrPweycTM3I-bDp7Ipa7zXm40bEjIq_8dvgMtAV5e7w"

# GIDS = {
#     "equipment": 1016544500,
#     "solar_monthly": 2105633948,
#      "floor_summary": 2040283256,  # 👈 เพิ่มอันนี้
#      "ac_rooms":0,
# }

# @st.cache_data(ttl=60)
# def load_sheet(sheet_id, gid):
#     url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
#     df = pd.read_csv(url)
#     df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
#     return df

# def safe_load(name):
#     gid = GIDS.get(name)
#     if gid is None:
#         return pd.DataFrame()
#     try:
#         return load_sheet(SHEET_ID, gid)
#     except:
#         return pd.DataFrame()

# def find_col(df, keys):
#     return next((c for c in df.columns if any(k in c for k in keys)), None)

# def prep_data(df):
#     kw_col = find_col(df, ["kw"])
#     cost_col = find_col(df, ["hour", "cost"])
#     floor_col = find_col(df, ["floor"])
    
#     if kw_col:
#         df[kw_col] = pd.to_numeric(df[kw_col], errors="coerce")
#     if cost_col:
#         df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

#     return kw_col, cost_col, floor_col

# # ================= OVERVIEW =================
# if page == "Overview":
#     st.title("📊 Energy Overview")

#     df = safe_load("floor_summary")
#     ac_rooms = safe_load("ac_rooms")

#     # ================= KPI =================
#     if df.empty:
#         st.warning("โหลดข้อมูลไม่ได้")
#     else:
#         df["value_thb"] = df["value_thb"].astype(str)

#         def get_kpi(name):
#             row = df[df["kpi"].str.contains(name, na=False)]
#             if row.empty:
#                 return 0
            
#             value = row["value_thb"].values[0]
#             value = value.replace(",", "").replace("%", "")
#             return float(value)

#         total_cost = get_kpi("รวม")
#         solar_saving = get_kpi("Solar")
#         net_cost = get_kpi("สุทธิ")
#         percent = get_kpi("%")

#         c1, c2, c3, c4 = st.columns(4)

#         c1.metric("💰 Total Cost", f"{total_cost:,.0f}")
#         c2.metric("☀️ Solar Saving", f"{solar_saving:,.0f}")
#         c3.metric("⚡ Net Cost", f"{net_cost:,.0f}")
#         c4.metric("📉 Saving %", f"{percent:.2f}%")

#     st.divider()

#     # ================= AC ROOMS =================
#     if not ac_rooms.empty:
#         st.subheader("❄️ AC Rooms Analysis")

#         room_col = find_col(ac_rooms, ["room", "ห้อง"])
#         cost_col = find_col(ac_rooms, ["cost", "hour", "บาท"])

#         if cost_col:
#             ac_rooms[cost_col] = pd.to_numeric(ac_rooms[cost_col], errors="coerce")

#         if room_col and cost_col:
#             chart = ac_rooms.groupby(room_col)[cost_col].sum().reset_index()

#             # 🔥 เรียงจากมากไปน้อย
#             chart = chart.sort_values(cost_col, ascending=False)

#             col1, col2 = st.columns(2)

#             # ---------- BAR ----------
#             fig = px.bar(
#                 chart,
#                 x=room_col,
#                 y=cost_col,
#                 text=cost_col,
#                 title="ค่าไฟแต่ละห้อง (เรียงจากมาก → น้อย)"
#             )
#             fig.update_traces(textposition="outside")
#             col1.plotly_chart(fig, use_container_width=True)

#             # ---------- PIE ----------
#             fig2 = px.pie(
#                 chart,
#                 names=room_col,
#                 values=cost_col,
#                 hole=0.6
#             )
#             col2.plotly_chart(fig2, use_container_width=True)

#             # 🔥 ห้องกินไฟสูงสุด
#             top = chart.iloc[0]
#             st.error(f"🔥 ห้องกินไฟสูงสุด: {top[room_col]} ({top[cost_col]:,.0f} บาท)")

#             # 🏆 Top 5
#             st.subheader("🏆 Top 5 ห้องกินไฟสูงสุด")
#             st.dataframe(chart.head(5), use_container_width=True)

#         st.divider()

#         # 📋 ตารางทั้งหมด
#         st.subheader("📋 รายการห้องแอร์ทั้งหมด")
#         st.dataframe(ac_rooms, use_container_width=True)

#     else:
#         st.warning("ไม่มีข้อมูล AC Rooms")
  
# # ================= EQUIPMENT =================


# elif page == "Equipment":
#     st.title("⚙️ Equipment")

#     df = safe_load("equipment")

#     if df.empty:
#         st.warning("โหลดข้อมูลไม่ได้")
#     else:
#         kw_col, _, floor_col = prep_data(df)

#         st.dataframe(df, use_container_width=True)

#         if floor_col and kw_col:
#             chart = df.groupby(floor_col)[kw_col].sum().reset_index()
#             fig = px.bar(chart, x=floor_col, y=kw_col)
#             st.plotly_chart(fig, use_container_width=True)
# # ================= SOLAR =================
# elif page == "Solar":
#     st.title("☀️ Solar Analysis")

#     df_solar = safe_load("solar_monthly")

#     if df_solar.empty:
#         st.warning("โหลดข้อมูล Solar ไม่ได้")
#     else:
#         # แปลงข้อมูลตัวเลข
#         if "solar_saving_thb" in df_solar.columns:
#             df_solar["solar_saving_thb"] = pd.to_numeric(
#                 df_solar["solar_saving_thb"], errors="coerce"
#             )

#         if "month_num" in df_solar.columns:
#             df_solar["month_num"] = pd.to_numeric(
#                 df_solar["month_num"], errors="coerce"
#             )

#         # ลบแถวที่ไม่มีค่า
#         df_solar = df_solar[df_solar["solar_saving_thb"].notna()]

#         # เรียงเดือน
#         if "month_num" in df_solar.columns:
#             df_solar = df_solar.sort_values("month_num")

#         # กราฟ
#         fig = px.line(
#             df_solar,
#             x="month_th",
#             y="solar_saving_thb",
#             markers=True,
#             title="Solar Saving ต่อเดือน"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#         # KPI รวม
#         total = df_solar["solar_saving_thb"].sum()
#         st.metric("รวมประหยัด", f"฿{total:,.0f}")

#         # ตารางข้อมูล
#         st.dataframe(df_solar, use_container_width=True)


import re
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Energy Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0F172A;
    color: white;
}
[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stSidebar"] {
    background-color: #111827;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
if "page" not in st.session_state:
    st.session_state.page = "Overview"

st.sidebar.markdown("## ⚡ Nature Biotech")

if st.sidebar.button("📊 Overview", use_container_width=True):
    st.session_state.page = "Overview"
if st.sidebar.button("⚙️ Equipment", use_container_width=True):
    st.session_state.page = "Equipment"
if st.sidebar.button("☀️ Solar", use_container_width=True):
    st.session_state.page = "Solar"

page = st.session_state.page

# ---------------- DATA CONFIG ----------------
SHEET_ID = "1VrPweycTM3I-bDp7Ipa7zXm40bEjIq_8dvgMtAV5e7w"

GIDS = {
    "ac_rooms": 0,
    "equipment": 1016544500,
    "solar_monthly": 2105633948,
    "floor_summary": 2040283256,
}

# ---------------- HELPERS ----------------
def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.replace("\n", " ", regex=False)
        .str.strip()
        .str.lower()
    )
    df.columns = [re.sub(r"[^a-z0-9]+", "_", c).strip("_") for c in df.columns]
    return df

@st.cache_data(ttl=60)
def load_sheet(sheet_id: str, gid: int) -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df = clean_columns(df)
    return df

def safe_load(name: str) -> pd.DataFrame:
    gid = GIDS.get(name)
    if gid is None:
        return pd.DataFrame()
    try:
        return load_sheet(SHEET_ID, gid)
    except Exception:
        return pd.DataFrame()

def find_col(df: pd.DataFrame, keys) -> str | None:
    keys = [k.lower() for k in keys]
    for c in df.columns:
        c_low = c.lower()
        if any(k in c_low for k in keys):
            return c
    return None

def to_numeric_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False).str.strip(),
        errors="coerce"
    )

def prep_data(df: pd.DataFrame):
    kw_col = find_col(df, ["kw", "kW".lower()])
    cost_col = find_col(df, ["cost", "hour", "บาท", "thb"])
    floor_col = find_col(df, ["floor", "ชั้น"])
    room_col = find_col(df, ["room", "ห้อง"])
    return kw_col, cost_col, floor_col, room_col

# ================= OVERVIEW =================
if page == "Overview":
    st.title("📊 Energy Overview")

    df = safe_load("floor_summary")
    ac_rooms = safe_load("ac_rooms")

    # ---------- KPI ----------
    if df.empty:
        st.warning("โหลดข้อมูล Floor Summary ไม่ได้")
    else:
        kpi_col = find_col(df, ["kpi"])
        value_col = find_col(df, ["value_thb", "value", "total", "amount"])

        if kpi_col and value_col:
            df[value_col] = df[value_col].astype(str)

            def get_kpi(keyword: str) -> float:
                row = df[df[kpi_col].astype(str).str.contains(keyword, case=False, na=False)]
                if row.empty:
                    return 0.0
                val = row[value_col].iloc[0]
                try:
                    return float(str(val).replace(",", "").replace("%", "").strip())
                except Exception:
                    return 0.0

            total_cost = get_kpi("รวม")
            solar_saving = get_kpi("solar")
            net_cost = get_kpi("สุทธิ")
            percent = get_kpi("%")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💰 Total Cost", f"{total_cost:,.0f}")
            c2.metric("☀️ Solar Saving", f"{solar_saving:,.0f}")
            c3.metric("⚡ Net Cost", f"{net_cost:,.0f}")
            c4.metric("📉 Saving %", f"{percent:.2f}%")
        else:
            st.warning("ไม่พบคอลัมน์ KPI หรือ Value ใน Floor Summary")
            st.dataframe(df, use_container_width=True)

    st.divider()

    # ---------- AC ROOMS ----------
    if ac_rooms.empty:
        st.warning("ไม่มีข้อมูล AC Rooms")
    else:
        st.subheader("❄️ AC Rooms Analysis")

        _, cost_col, _, room_col = prep_data(ac_rooms)

        if cost_col:
            ac_rooms[cost_col] = to_numeric_series(ac_rooms[cost_col])

        if room_col and cost_col:
            chart = ac_rooms.groupby(room_col, dropna=False)[cost_col].sum().reset_index()
            chart = chart.sort_values(cost_col, ascending=False)

            col1, col2 = st.columns(2)

            fig = px.bar(
                chart,
                x=room_col,
                y=cost_col,
                text=cost_col,
                title="ค่าไฟแต่ละห้อง (เรียงจากมาก → น้อย)"
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            col1.plotly_chart(fig, use_container_width=True)

            fig2 = px.pie(
                chart,
                names=room_col,
                values=cost_col,
                hole=0.55,
                title="สัดส่วนค่าไฟแต่ละห้อง"
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            col2.plotly_chart(fig2, use_container_width=True)

            if not chart.empty:
                top = chart.iloc[0]
                st.error(f"🔥 ห้องกินไฟสูงสุด: {top[room_col]} ({top[cost_col]:,.0f} บาท)")

            st.subheader("🏆 Top 5 ห้องกินไฟสูงสุด")
            st.dataframe(chart.head(5), use_container_width=True)
        else:
            st.warning("ไม่พบคอลัมน์ห้อง หรือคอลัมน์ค่าใช้จ่ายใน AC Rooms")
            st.write("Columns:", ac_rooms.columns.tolist())

        st.divider()
        st.subheader("📋 รายการห้องแอร์ทั้งหมด")
        st.dataframe(ac_rooms, use_container_width=True)

# ================= EQUIPMENT =================
elif page == "Equipment":
    st.title("⚙️ Equipment")

    df = safe_load("equipment")

    if df.empty:
        st.warning("โหลดข้อมูล Equipment ไม่ได้")
    else:
        kw_col, cost_col, floor_col, room_col = prep_data(df)

        if kw_col:
            df[kw_col] = to_numeric_series(df[kw_col])
        if cost_col:
            df[cost_col] = to_numeric_series(df[cost_col])

        c1, c2 = st.columns(2)

        with c1:
            if kw_col:
                total_kw = df[kw_col].sum(skipna=True)
                st.metric("⚡ Total kW", f"{total_kw:,.2f}")
            else:
                st.info("ไม่พบคอลัมน์ kW")

        with c2:
            if cost_col:
                total_cost = df[cost_col].sum(skipna=True)
                st.metric("💰 Total Cost", f"{total_cost:,.2f}")
            else:
                st.info("ไม่พบคอลัมน์ Cost")

        st.subheader("📋 Equipment Data")
        st.dataframe(df, use_container_width=True)

        if floor_col and kw_col:
            chart_floor = df.groupby(floor_col, dropna=False)[kw_col].sum().reset_index()
            chart_floor = chart_floor.sort_values(kw_col, ascending=False)

            fig = px.bar(
                chart_floor,
                x=floor_col,
                y=kw_col,
                text=kw_col,
                title="การใช้พลังงานแยกตามชั้น"
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            st.plotly_chart(fig, use_container_width=True)

        if room_col and kw_col:
            chart_room = df.groupby(room_col, dropna=False)[kw_col].sum().reset_index()
            chart_room = chart_room.sort_values(kw_col, ascending=False).head(10)

            fig2 = px.bar(
                chart_room,
                x=room_col,
                y=kw_col,
                text=kw_col,
                title="Top 10 ห้อง/พื้นที่ที่ใช้ kW สูงสุด"
            )
            fig2.update_traces(textposition="outside")
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            st.plotly_chart(fig2, use_container_width=True)

# ================= SOLAR =================
elif page == "Solar":
    st.title("☀️ Solar Analysis")

    df_solar = safe_load("solar_monthly")

    if df_solar.empty:
        st.warning("โหลดข้อมูล Solar ไม่ได้")
    else:
        year_col = find_col(df_solar, ["year", "ปี"])
        month_th_col = find_col(df_solar, ["month_th", "month", "เดือน"])
        month_num_col = find_col(df_solar, ["month_num", "month_no", "ลำดับ"])
        saving_col = find_col(df_solar, ["solar_saving_thb", "solar_saving", "saving", "thb"])

        if saving_col is None:
            st.error("ไม่พบคอลัมน์ Solar Saving")
            st.write("Columns:", df_solar.columns.tolist())
            st.dataframe(df_solar, use_container_width=True)
        else:
            df_solar[saving_col] = to_numeric_series(df_solar[saving_col])

            if month_num_col:
                df_solar[month_num_col] = to_numeric_series(df_solar[month_num_col])

            if year_col:
                df_solar[year_col] = to_numeric_series(df_solar[year_col])

            df_solar = df_solar[df_solar[saving_col].notna()]

            if year_col and month_num_col:
                df_solar = df_solar.sort_values([year_col, month_num_col])
            elif month_num_col:
                df_solar = df_solar.sort_values(month_num_col)

            # สร้าง label เดือนสำหรับแสดงบนกราฟ
            if month_th_col and year_col:
                df_solar["period_label"] = (
                    df_solar[month_th_col].astype(str).str.strip()
                    + " "
                    + df_solar[year_col].fillna("").astype(int).astype(str)
                )
                x_axis = "period_label"
            elif month_th_col:
                x_axis = month_th_col
            else:
                x_axis = df_solar.index

            total = df_solar[saving_col].sum()
            avg = df_solar[saving_col].mean() if not df_solar.empty else 0
            max_val = df_solar[saving_col].max() if not df_solar.empty else 0

            c1, c2, c3 = st.columns(3)
            c1.metric("💰 รวมประหยัด", f"฿{total:,.0f}")
            c2.metric("📊 เฉลี่ยต่อเดือน", f"฿{avg:,.0f}")
            c3.metric("🚀 สูงสุด", f"฿{max_val:,.0f}")

            fig = px.line(
                df_solar,
                x=x_axis,
                y=saving_col,
                markers=True,
                title="Solar Saving ต่อเดือน"
            )
            fig.update_layout(
                xaxis_title="เดือน",
                yaxis_title="Solar Saving (THB)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            st.plotly_chart(fig, use_container_width=True)

            if month_th_col:
                bar_fig = px.bar(
                    df_solar,
                    x=x_axis,
                    y=saving_col,
                    text=saving_col,
                    title="Solar Saving แบบรายเดือน"
                )
                bar_fig.update_traces(textposition="outside")
                bar_fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="white"
                )
                st.plotly_chart(bar_fig, use_container_width=True)

            st.subheader("📋 Solar Monthly Data")
            st.dataframe(df_solar, use_container_width=True)