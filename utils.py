import pandas as pd
import streamlit as st

SHEET_ID = "1VrPweycTM3I-bDp7Ipa7zXm40bEjIq_8dvgMtAV5e7w"

GIDS = {
    "equipment":     1016544500,
    "solar_monthly": 2105633948,
    "floor_summary": 2040283256,
    "ac_rooms":      0,
        "machines_floor3": 798227041,   # 👈 เพิ่มตรงนี้
       "monthly_bill":1605055572,
}


@st.cache_data(ttl=60)
def load_sheet(sheet_id: str, gid: int) -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def safe_load(name: str) -> pd.DataFrame:
    gid = GIDS.get(name)
    if gid is None:
        return pd.DataFrame()
    try:
        return load_sheet(SHEET_ID, gid)
    except Exception as e:
        st.warning(f"⚠️ โหลด **{name}** ไม่ได้: {e}")
        return pd.DataFrame()


def find_col(df: pd.DataFrame, keys: list) -> str | None:
    return next((c for c in df.columns if any(k in c for k in keys)), None)


def to_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("฿", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip(),
        errors="coerce",
    )