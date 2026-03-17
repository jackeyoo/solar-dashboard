# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="Nature Biotech Energy Dashboard", layout="wide")
# st.title("⚡ Nature Biotech Energy Dashboard")

# SHEET_ID = "1VrPweycTM3I-bDp7Ipa7zXm40bEjIq_8dvgMtAV5e7w"

# # ใส่ gid จริงจาก URL ของแต่ละแท็บ
# GIDS = {
#     "ac_rooms": 0,            # แก้เป็น gid จริง
#     "equipment": 1016544500,           # แก้เป็น gid จริง
#     "solar_monthly": 2105633948,       # แก้เป็น gid จริง
#     "machines_floor3": 798227041,     # แก้เป็น gid จริง
#     "floor_summary": 2040283256,       # แก้เป็น gid จริง
#     "solar_summary": 374208785,  # ตัวอย่างจากรูปที่เห็น
# }

# @st.cache_data(ttl=60)
# def load_sheet(sheet_id: str, gid: int) -> pd.DataFrame:
#     url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
#     df = pd.read_csv(url)
#     df.columns = df.columns.str.strip()
#     return df

# def safe_load(name: str):
#     gid = GIDS[name]
#     if gid == None:
#         st.warning(f"ยังไม่ได้ใส่ gid ของแท็บ: {name}")
#         return pd.DataFrame()
#     try:
#         return load_sheet(SHEET_ID, gid)
#     except Exception as e:
#         st.error(f"โหลดชีต {name} ไม่สำเร็จ: {e}")
#         return pd.DataFrame()

# equipment = safe_load("equipment")
# machines = safe_load("machines_floor3")
# solar = safe_load("solar_monthly")
# floor = safe_load("floor_summary")
# solar_summary = safe_load("solar_summary")
# ac_rooms = safe_load("ac_rooms")

# page = st.sidebar.selectbox(
#     "เมนู",
#     ["Overview", "Equipment", "AC Rooms", "Machines", "Solar", "Debug"]
# )
# if st.button("🔄 Refresh Data"):
#     st.cache_data.clear()
# if page == "Overview":
#     st.subheader("ภาพรวม")

#     col1, col2, col3 = st.columns(3)

#     if not equipment.empty and "kW Total" in equipment.columns and "$ Per Hour" in equipment.columns:
#         total_kw = pd.to_numeric(equipment["kW Total"], errors="coerce").sum()
#         total_cost = pd.to_numeric(equipment["$ Per Hour"], errors="coerce").sum()

#         col1.metric("Total Power (kW)", f"{total_kw:,.2f}")
#         col2.metric("Cost per Hour", f"{total_cost:,.2f}")
#         col3.metric("Equipment Rows", len(equipment))

#         if "floor" in equipment.columns:
#             floor_kw = (
#                 equipment.assign(**{"kW Total": pd.to_numeric(equipment["kW Total"], errors="coerce")})
#                 .groupby("floor")["kW Total"]
#                 .sum()
#             )
#             st.subheader("Power by Floor")
#             st.bar_chart(floor_kw)
#     else:
#         st.info("Overview ยังแสดงไม่ได้จนกว่าจะใส่ gid ของ Equipment ให้ถูก")

# if page == "Equipment":
#     st.subheader("Equipment")
#     if equipment.empty:
#         st.info("ยังโหลด Equipment ไม่ได้")
#     else:
#         st.dataframe(equipment, use_container_width=True)
#         if "equipment Type" in equipment.columns and "kW Total" in equipment.columns:
#             chart_df = equipment.copy()
#             chart_df["kW Total"] = pd.to_numeric(chart_df["kW Total"], errors="coerce")
#             st.bar_chart(chart_df.set_index("equipment Type")["kW Total"])

# if page == "AC Rooms":
#     st.subheader("AC Rooms")
#     if ac_rooms.empty:
#         st.info("ยังโหลด AC_Rooms ไม่ได้")
#     else:
#         st.dataframe(ac_rooms, use_container_width=True)

# if page == "Machines":
#     st.subheader("Machines Floor 3")
#     if machines.empty:
#         st.info("ยังโหลด Machines_Floor3 ไม่ได้")
#     else:
#         st.dataframe(machines, use_container_width=True)

#         # พยายามหาคอลัมน์ที่พอใช้ทำกราฟได้
#         possible_name_cols = ["Machine", "เครื่องจักร", "machine"]
#         possible_value_cols = ["$ Per Hour", "Cost Per Hour", "฿/ชม.", "kW"]

#         name_col = next((c for c in possible_name_cols if c in machines.columns), None)
#         value_col = next((c for c in possible_value_cols if c in machines.columns), None)

#         if name_col and value_col:
#             chart_df = machines.copy()
#             chart_df[value_col] = pd.to_numeric(chart_df[value_col], errors="coerce")
#             st.bar_chart(chart_df.set_index(name_col)[value_col])

# if page == "Solar":
#     st.subheader("Solar Monthly")
#     if solar.empty:
#         st.info("ยังโหลด Solar_Monthly ไม่ได้")
#     else:
#         st.dataframe(solar, use_container_width=True)

# if page == "Debug":
#     st.subheader("Debug Columns")
#     for name, df in {
#         "equipment": equipment,
#         "ac_rooms": ac_rooms,
#         "machines_floor3": machines,
#         "solar_monthly": solar,
#         "floor_summary": floor,
#         "solar_summary": solar_summary,
#     }.items():
#         st.markdown(f"**{name}**")
#         if df.empty:
#             st.write("โหลดไม่ได้ / ยังไม่ได้ใส่ gid")
#         else:
#             st.write(list(df.columns))
#             st.dataframe(df.head(), use_container_width=True)
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.set_page_config(page_title="Energy Dashboard", layout="wide")

# # ---------------- STYLE ----------------
# st.markdown("""
# <style>
# .card {
#     padding:20px;
#     border-radius:15px;
#     background:#111827;
#     color:white;
# }
# .metric {
#     font-size:28px;
#     font-weight:bold;
# }
# .label {
#     font-size:14px;
#     color:#9CA3AF;
# }
# </style>
# """, unsafe_allow_html=True)

# st.title("⚡ Nature Biotech Energy Dashboard")

# SHEET_ID = "1VrPweycTM3I-bDp7Ipa7zXm40bEjIq_8dvgMtAV5e7w"

# GIDS = {
#     "equipment": 1016544500,
# }

# @st.cache_data(ttl=60)
# def load_sheet(sheet_id, gid):
#     url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
#     df = pd.read_csv(url)

#     df.columns = (
#         df.columns
#         .str.strip()
#         .str.replace(" ", "_")
#         .str.lower()
#     )
#     return df

# def find_col(df, keys):
#     return next((c for c in df.columns if any(k in c for k in keys)), None)

# equipment = load_sheet(SHEET_ID, GIDS["equipment"])

# # ---------------- DATA PREP ----------------
# kw_col = find_col(equipment, ["kw"])
# cost_col = find_col(equipment, ["hour", "cost"])
# floor_col = find_col(equipment, ["floor"])

# equipment[kw_col] = pd.to_numeric(equipment[kw_col], errors="coerce")
# equipment[cost_col] = pd.to_numeric(equipment[cost_col], errors="coerce")

# total_kw = equipment[kw_col].sum()
# total_cost = equipment[cost_col].sum()

# # ---------------- KPI ----------------
# col1, col2, col3, col4 = st.columns(4)

# col1.markdown(f"""
# <div class="card">
# <div class="label">ค่าไฟรวมต่อเดือน</div>
# <div class="metric">{total_cost:,.0f}</div>
# </div>
# """, unsafe_allow_html=True)

# col2.markdown(f"""
# <div class="card">
# <div class="label">ประหยัดจากโซล่า</div>
# <div class="metric">{total_cost*0.4:,.0f}</div>
# </div>
# """, unsafe_allow_html=True)

# col3.markdown(f"""
# <div class="card">
# <div class="label">ค่าไฟสุทธิ</div>
# <div class="metric">{total_cost*0.6:,.0f}</div>
# </div>
# """, unsafe_allow_html=True)

# col4.markdown(f"""
# <div class="card">
# <div class="label">กำลังไฟรวม (kW)</div>
# <div class="metric">{total_kw:,.2f}</div>
# </div>
# """, unsafe_allow_html=True)

# st.divider()

# # ---------------- MAIN CHART ----------------
# col1, col2 = st.columns([2,1])

# # ---------- FLOOR BAR ----------
# if floor_col:
#     floor_df = equipment.groupby(floor_col)[cost_col].sum()

#     col1.subheader("ค่าไฟแต่ละชั้น")
#     for f, val in floor_df.items():
#         percent = val / floor_df.max()
#         col1.progress(percent, text=f"{f}  |  ฿{val:,.0f}")

# # ---------- DONUT ----------
# if floor_col:
#     pie_df = equipment.groupby(floor_col)[cost_col].sum().reset_index()

#     fig = px.pie(
#         pie_df,
#         names=floor_col,
#         values=cost_col,
#         hole=0.5
#     )

#     col2.subheader("สัดส่วนค่าไฟ")
#     col2.plotly_chart(fig, use_container_width=True)

# st.divider()

# # ---------------- TABLE ----------------
# st.subheader("รายละเอียดอุปกรณ์")
# st.dataframe(equipment, use_container_width=True)

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
GID = 1016544500

@st.cache_data(ttl=60)
def load():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load()

def find_col(keys):
    return next((c for c in df.columns if any(k in c for k in keys)), None)

kw_col = find_col(["kw"])
cost_col = find_col(["hour", "cost"])
floor_col = find_col(["floor"])

df[kw_col] = pd.to_numeric(df[kw_col], errors="coerce")
df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

# ================= OVERVIEW =================
if page == "Overview":
    st.title("📊 Energy Overview")

    total_kw = df[kw_col].sum()
    total_cost = df[cost_col].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f'<div class="card"><div class="label">Total Cost</div><div class="metric">{total_cost:,.0f}</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card"><div class="label">Solar Saving</div><div class="metric">{total_cost*0.4:,.0f}</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card"><div class="label">Net Cost</div><div class="metric">{total_cost*0.6:,.0f}</div></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="card"><div class="label">Total kW</div><div class="metric">{total_kw:,.2f}</div></div>', unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns([2,1])

    # Bar
    if floor_col:
        floor_df = df.groupby(floor_col)[cost_col].sum()
        col1.subheader("ค่าไฟแต่ละชั้น")
        for f, v in floor_df.items():
            col1.progress(v / floor_df.max(), text=f"{f}  |  ฿{v:,.0f}")

    # Donut
    if floor_col:
        pie = df.groupby(floor_col)[cost_col].sum().reset_index()
        fig = px.pie(pie, names=floor_col, values=cost_col, hole=0.6)
        col2.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.dataframe(df, use_container_width=True)

# ================= EQUIPMENT =================
elif page == "Equipment":
    st.title("⚙️ Equipment Analysis")

    st.dataframe(df, use_container_width=True)

    if floor_col:
        chart = df.groupby(floor_col)[kw_col].sum().reset_index()
        fig = px.bar(chart, x=floor_col, y=kw_col)
        st.plotly_chart(fig, use_container_width=True)

# ================= SOLAR =================
elif page == "Solar":
    st.title("☀️ Solar Analysis")

    if "month" in df.columns:
        fig = px.line(df, x="month", y=kw_col)
        st.plotly_chart(fig, use_container_width=True)