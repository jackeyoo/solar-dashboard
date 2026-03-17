import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Energy Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

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
def load_sheet(sheet_id: str, gid: int) -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    return data


def safe_load(name: str) -> pd.DataFrame:
    gid = GIDS.get(name)
    if gid is None:
        st.warning(f"ยังไม่ได้ตั้งค่า GID สำหรับชีต: {name}")
        return pd.DataFrame()

    try:
        return load_sheet(SHEET_ID, gid)
    except Exception as exc:
        st.error(f"โหลดชีต {name} ไม่สำเร็จ: {exc}")
        return pd.DataFrame()


def find_col(data: pd.DataFrame, keys: list[str]) -> str | None:
    return next((c for c in data.columns if any(k in c for k in keys)), None)


def prep_numeric_cols(data: pd.DataFrame) -> tuple[str | None, str | None, str | None]:
    kw_col = find_col(data, ["kw"])
    cost_col = find_col(data, ["hour", "cost"])
    floor_col = find_col(data, ["floor"])

    if kw_col:
        data[kw_col] = pd.to_numeric(data[kw_col], errors="coerce")
    if cost_col:
        data[cost_col] = pd.to_numeric(data[cost_col], errors="coerce")

    return kw_col, cost_col, floor_col


# ================= OVERVIEW =================
if page == "Overview":
    df = safe_load("equipment")
    st.title("📊 Energy Overview")

    if df.empty:
        st.info("ยังโหลดข้อมูล Equipment ไม่ได้ กรุณาตรวจสอบ GID")
    else:
        kw_col, cost_col, floor_col = prep_numeric_cols(df)
        if not kw_col or not cost_col:
            st.warning("ไม่พบคอลัมน์ kW หรือ Cost ที่ใช้คำนวณ")
        else:
            total_kw = df[kw_col].sum()
            total_cost = df[cost_col].sum()

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(
                f'<div class="card"><div class="label">Total Cost</div><div class="metric">{total_cost:,.0f}</div></div>',
                unsafe_allow_html=True,
            )
            col2.markdown(
                f'<div class="card"><div class="label">Solar Saving</div><div class="metric">{total_cost * 0.4:,.0f}</div></div>',
                unsafe_allow_html=True,
            )
            col3.markdown(
                f'<div class="card"><div class="label">Net Cost</div><div class="metric">{total_cost * 0.6:,.0f}</div></div>',
                unsafe_allow_html=True,
            )
            col4.markdown(
                f'<div class="card"><div class="label">Total kW</div><div class="metric">{total_kw:,.2f}</div></div>',
                unsafe_allow_html=True,
            )

            st.divider()
            col_left, col_right = st.columns([2, 1])

            if floor_col:
                floor_df = df.groupby(floor_col)[cost_col].sum()
                col_left.subheader("ค่าไฟแต่ละชั้น")
                max_value = floor_df.max() if not floor_df.empty else 0
                for floor_name, value in floor_df.items():
                    percent = (value / max_value) if max_value else 0
                    col_left.progress(percent, text=f"{floor_name}  |  ฿{value:,.0f}")

                pie = floor_df.reset_index(name=cost_col)
                fig = px.pie(pie, names=floor_col, values=cost_col, hole=0.6)
                col_right.plotly_chart(fig, use_container_width=True)

            st.divider()
            st.dataframe(df, use_container_width=True)

# ================= EQUIPMENT =================
elif page == "Equipment":
    df = safe_load("equipment")
    st.title("⚙️ Equipment Analysis")

    if df.empty:
        st.info("ยังโหลดข้อมูล Equipment ไม่ได้ กรุณาตรวจสอบ GID")
    else:
        kw_col, _, floor_col = prep_numeric_cols(df)
        st.dataframe(df, use_container_width=True)

        if floor_col and kw_col:
            chart = df.groupby(floor_col)[kw_col].sum().reset_index()
            fig = px.bar(chart, x=floor_col, y=kw_col)
            st.plotly_chart(fig, use_container_width=True)

# ================= SOLAR =================
elif page == "Solar":
    df = safe_load("solar_monthly")
    st.title("☀️ Solar Analysis")

    if df.empty:
        st.info("ยังโหลดข้อมูล Solar ไม่ได้ กรุณาตรวจสอบ GID")
    else:
        kw_col, _, _ = prep_numeric_cols(df)
        month_col = find_col(df, ["month", "เดือน"])

        st.dataframe(df, use_container_width=True)

        if month_col and kw_col:
            fig = px.line(df, x=month_col, y=kw_col)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("ไม่พบคอลัมน์ month หรือ kW สำหรับแสดงกราฟ Solar")
