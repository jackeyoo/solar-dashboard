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

    df = safe_load("equipment")

    if df.empty:
        st.warning("โหลดข้อมูลไม่ได้")
    else:
        kw_col, cost_col, floor_col = prep_data(df)

        total_kw = df[kw_col].sum()
        total_cost = df[cost_col].sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f'<div class="card"><div class="label">Total Cost</div><div class="metric">{total_cost:,.0f}</div></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="card"><div class="label">Solar Saving</div><div class="metric">{total_cost*0.4:,.0f}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="card"><div class="label">Net Cost</div><div class="metric">{total_cost*0.6:,.0f}</div></div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="card"><div class="label">Total kW</div><div class="metric">{total_kw:,.2f}</div></div>', unsafe_allow_html=True)

        st.divider()

        col_left, col_right = st.columns([2,1])

        if floor_col:
            floor_df = df.groupby(floor_col)[cost_col].sum()
            col_left.subheader("ค่าไฟแต่ละชั้น")

            max_val = floor_df.max()
            for f, v in floor_df.items():
                col_left.progress(v/max_val, text=f"{f} | ฿{v:,.0f}")

            pie = floor_df.reset_index(name=cost_col)
            fig = px.pie(pie, names=floor_col, values=cost_col, hole=0.6)
            col_right.plotly_chart(fig, use_container_width=True)

        st.dataframe(df, use_container_width=True)

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

    if df.empty:
        st.warning("โหลดข้อมูลไม่ได้")
    else:
        kw_col, _, _ = prep_data(df)
        month_col = find_col(df, ["month", "เดือน"])

        st.dataframe(df, use_container_width=True)

        if month_col and kw_col:
            fig = px.line(df, x=month_col, y=kw_col)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("ไม่มี column month หรือ kW")