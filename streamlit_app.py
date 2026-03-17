import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Energy Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #0F172A;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background: #1E293B;
    padding: 20px;
    border-radius: 15px;
}
.metric {
    font-size: 28px;
    font-weight: bold;
    color: white;
}
.label {
    font-size: 14px;
    color: #94A3B8;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
if "page" not in st.session_state:
    st.session_state.page = "Overview"

st.sidebar.markdown("## ⚡ Nature Biotech")

if st.sidebar.button("📊 Overview"):
    st.session_state.page = "Overview"
if st.sidebar.button("⚙️ Equipment"):
    st.session_state.page = "Equipment"
if st.sidebar.button("☀️ Solar"):
    st.session_state.page = "Solar"

page = st.session_state.page

# ---------------- DATA ----------------
SHEET_ID = "1VrPweycTM3I-bDp7Ipa7zXm40bEjIq_8dvgMtAV5e7w"

GIDS = {
    "equipment": 1016544500,
    "solar_monthly": 2105633948,
     "floor_summary": 2040283256,  # 👈 เพิ่มอันนี้
     "ac_rooms":0,
}

@st.cache_data(ttl=60)
def load_sheet(sheet_id, gid):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def safe_load(name):
    gid = GIDS.get(name)
    if gid is None:
        return pd.DataFrame()
    try:
        return load_sheet(SHEET_ID, gid)
    except:
        return pd.DataFrame()

def find_col(df, keys):
    return next((c for c in df.columns if any(k in c for k in keys)), None)

def prep_data(df):
    kw_col = find_col(df, ["kw"])
    cost_col = find_col(df, ["hour", "cost"])
    floor_col = find_col(df, ["floor"])
    
    if kw_col:
        df[kw_col] = pd.to_numeric(df[kw_col], errors="coerce")
    if cost_col:
        df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

    return kw_col, cost_col, floor_col

# ================= OVERVIEW =================
if page == "Overview":
    st.title("📊 Energy Overview")

    df = safe_load("floor_summary")
    ac_rooms = safe_load("ac_rooms")

    # ================= KPI =================
    if df.empty:
        st.warning("โหลดข้อมูลไม่ได้")
    else:
        df["value_thb"] = df["value_thb"].astype(str)

        def get_kpi(name):
            row = df[df["kpi"].str.contains(name, na=False)]
            if row.empty:
                return 0
            
            value = row["value_thb"].values[0]
            value = value.replace(",", "").replace("%", "")
            return float(value)

        total_cost = get_kpi("รวม")
        solar_saving = get_kpi("Solar")
        net_cost = get_kpi("สุทธิ")
        percent = get_kpi("%")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("💰 Total Cost", f"{total_cost:,.0f}")
        c2.metric("☀️ Solar Saving", f"{solar_saving:,.0f}")
        c3.metric("⚡ Net Cost", f"{net_cost:,.0f}")
        c4.metric("📉 Saving %", f"{percent:.2f}%")

    st.divider()

    # ================= AC ROOMS =================
    if not ac_rooms.empty:
        st.subheader("❄️ AC Rooms Analysis")

        room_col = find_col(ac_rooms, ["room", "ห้อง"])
        cost_col = find_col(ac_rooms, ["cost", "hour", "บาท"])

        if cost_col:
            ac_rooms[cost_col] = pd.to_numeric(ac_rooms[cost_col], errors="coerce")

        if room_col and cost_col:
            chart = ac_rooms.groupby(room_col)[cost_col].sum().reset_index()

            # 🔥 เรียงจากมากไปน้อย
            chart = chart.sort_values(cost_col, ascending=False)

            col1, col2 = st.columns(2)

            # ---------- BAR ----------
            fig = px.bar(
                chart,
                x=room_col,
                y=cost_col,
                text=cost_col,
                title="ค่าไฟแต่ละห้อง (เรียงจากมาก → น้อย)"
            )
            fig.update_traces(textposition="outside")
            col1.plotly_chart(fig, use_container_width=True)

            # ---------- PIE ----------
            fig2 = px.pie(
                chart,
                names=room_col,
                values=cost_col,
                hole=0.6
            )
            col2.plotly_chart(fig2, use_container_width=True)

            # 🔥 ห้องกินไฟสูงสุด
            top = chart.iloc[0]
            st.error(f"🔥 ห้องกินไฟสูงสุด: {top[room_col]} ({top[cost_col]:,.0f} บาท)")

            # 🏆 Top 5
            st.subheader("🏆 Top 5 ห้องกินไฟสูงสุด")
            st.dataframe(chart.head(5), use_container_width=True)

        st.divider()

        # 📋 ตารางทั้งหมด
        st.subheader("📋 รายการห้องแอร์ทั้งหมด")
        st.dataframe(ac_rooms, use_container_width=True)

    else:
        st.warning("ไม่มีข้อมูล AC Rooms")
  
# ================= EQUIPMENT =================


elif page == "Equipment":
    st.title("⚙️ Equipment")

    df = safe_load("equipment")

    if df.empty:
        st.warning("โหลดข้อมูลไม่ได้")
    else:
        kw_col, _, floor_col = prep_data(df)

        st.dataframe(df, use_container_width=True)

        if floor_col and kw_col:
            chart = df.groupby(floor_col)[kw_col].sum().reset_index()
            fig = px.bar(chart, x=floor_col, y=kw_col)
            st.plotly_chart(fig, use_container_width=True)

# ================= SOLAR =================
elif page == "Solar":
    st.title("☀️ Solar")

df = safe_load("solar_monthly")

if df is None or df.empty:
    st.warning("ไม่มีข้อมูล")
else:
    # แปลง type กันพลาด
    df["year"] = df["year"].astype(str)
    df["month_num"] = pd.to_numeric(df["month_num"], errors="coerce")

    # ---------------------------
    # 🎯 เลือกปี
    # ---------------------------
    years = sorted(df["year"].dropna().unique(), reverse=True)
    selected_year = st.selectbox("เลือกปี", years)

    df_year = df[df["year"] == selected_year].copy()

    # ---------------------------
    # 🟩 การ์ดรายเดือน
    # ---------------------------
    st.markdown("### ประหยัดค่าไฟจาก Solar (บาท)")

    months_th = [
        "มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน",
        "กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"
    ]

    cols = st.columns(12)

    for i, m in enumerate(months_th, start=1):
        val = df_year.loc[df_year["month_num"] == i, "solar_savings_thb"]
        val = val.values[0] if len(val) > 0 else None

        with cols[i-1]:
            if pd.notna(val):
                st.metric(m, f"฿{int(val):,}")
            else:
                st.metric(m, "-")

    # ---------------------------
    # 📊 กราฟ
    # ---------------------------
    st.markdown("### กราฟ Solar")

    chart_df = df_year.sort_values("month_num")

    if "month_num" in chart_df.columns:
        fig = px.bar(
            chart_df,
            x="month_num",
            y="solar_savings_thb",
            labels={"month_num": "เดือน", "solar_savings_thb": "บาท"},
            text="solar_savings_thb"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("ไม่มี column month_num")

    # ---------------------------
    # 📋 ตาราง (เฉพาะปีที่เลือก)
    # ---------------------------
    st.markdown("### รายการทั้งหมด")

    st.dataframe(
        df_year.sort_values("month_num"),
        use_container_width=True
    )