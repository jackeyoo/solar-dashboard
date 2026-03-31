import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme
import pandas as pd
import io
import datetime
import calendar

# ─────────────────────────────
# 🎨 LIGHT CLEAN UI
# ─────────────────────────────
def apply_custom_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif !important;
    }
    .stApp { background: #DCDCDC; }
    .block-container { padding: 1.2rem 2rem 3rem !important; max-width: 1080px; }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Page title ── */
    h1 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        # color: #f8fafc !important;
        letter-spacing: -.3px;
        margin-bottom: 0 !important;
    }
    h2, h3 { color: #1a1d2e !important; font-weight: 500 !important; }

    /* ── Divider ── */
    hr { border-color: #e4e6ef !important; opacity: 1 !important; margin: 10px 0 !important; }

    /* ── Caption ── */
    [data-testid="stCaptionContainer"] p {
        color: #8b92b3 !important;
        font-size: 0.74rem !important;
    }

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] label { color: #5a6080 !important; font-size: 0.78rem !important; }
    [data-testid="stSelectbox"] > div > div {
        background: #fff !important;
        border: 1px solid #dde1f0 !important;
        border-radius: 8px !important;
        color: #1a1d2e !important;
        font-size: 0.82rem !important;
    }

    /* ── Segmented control (floor picker) ── */
    div[data-testid="stSegmentedControl"] > div {
        background: #fff !important;
        border: 1px solid #dde1f0 !important;
        border-radius: 10px !important;
        padding: 3px !important;
        gap: 3px !important;
    }
    div[data-testid="stSegmentedControl"] button {
        background: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        color: #8b92b3 !important;
        font-size: 0.78rem !important;
        padding: 5px 14px !important;
        transition: all .15s;
    }
    div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
        background: #1a1d2e !important;
        color: #fff !important;
    }
    div[data-testid="stSegmentedControl"] label {
        color: #5a6080 !important;
        font-size: 0.78rem !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: #fff !important;
        border: 1px solid #e4e6ef !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,.04) !important;
        overflow: hidden;
        margin-bottom: 10px !important;
    }
    [data-testid="stExpander"] summary {
        color: #1a1d2e !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 13px 18px !important;
        background: #fff !important;
    }
    [data-testid="stExpander"] summary:hover { background: #f7f8fa !important; }
    [data-testid="stExpander"] > div > div { padding: 0 18px 16px !important; }

    /* ── KPI metric cards ── */
    [data-testid="metric-container"] {
        background: #fff;
        border: 1px solid #e4e6ef;
        border-radius: 12px;
        padding: 14px 18px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,.04);
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.68rem !important;
        text-transform: uppercase;
        letter-spacing: .7px;
        color: #8b92b3 !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.45rem !important;
        font-weight: 600 !important;
        color: #1a1d2e !important;
    }
    [data-testid="stMetricDelta"] { font-size: 0.7rem !important; }

    /* ── DataFrame ── */
    [data-testid="stDataFrame"] {
        border-radius: 10px !important;
        border: 1px solid #e4e6ef !important;
        overflow: hidden;
    }

    /* ── Info / warning ── */
    [data-testid="stInfo"] { border-radius: 10px !important; }

    /* ── Custom HTML components ── */
    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .9px;
        color: #8b92b3;
        margin-bottom: 6px;
    }
    .month-row {
        display: flex;
        align-items: center;
        gap: 7px;
        flex-wrap: wrap;
        margin: 4px 0 0;
    }
    .mbadge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 11px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 500;
        border: 1px solid;
    }
    .mbadge.work  { background: #eefaf5; border-color: #a3e6cc; color: #1b7a52; }
    .mbadge.rest  { background: #f4f5f9; border-color: #dde1f0; color: #8b92b3; }
    .mbadge.days  { background: #f4f5f9; border-color: #dde1f0; color: #5a6080; }

    .floor-cost-row {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        padding: 6px 0 10px;
        border-bottom: 1px solid #f0f1f7;
        margin-bottom: 10px;
    }
    .floor-cost-label { font-size: .75rem; color: #8b92b3; }
    .floor-cost-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1d2e;
    }

    .total-card {
        background: #1a1d2e;
        border-radius: 14px;
        padding: 18px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 6px;
    }
    .total-label { font-size: .78rem; color: #8b92b3; }
    .total-sub   { font-size: .68rem; color: #5a6080; margin-top: 3px; }
    .total-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.9rem;
        font-weight: 700;
        color: #fff;
        letter-spacing: -1.5px;
    }

    /* ── Clean HTML table ── */
    .clean-table {
        width: 100%;
        border-collapse: collapse;
        font-size: .82rem;
        color: #1a1d2e;
    }
    .clean-table thead tr { border-bottom: 2px solid #e4e6ef; }
    .clean-table thead th {
        padding: 7px 12px;
        text-align: left;
        font-size: .67rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .8px;
        color: #8b92b3;
    }
    .clean-table thead th.right { text-align: right; }
    .clean-table tbody tr { border-bottom: 1px solid #f0f1f7; transition: background .1s; }
    .clean-table tbody tr:hover { background: #f7f8fa; }
    .clean-table tbody tr.total-row {
        border-top: 2px solid #e4e6ef;
        border-bottom: none;
        background: #f7f8fa;
        font-weight: 600;
    }
    .clean-table tbody td { padding: 9px 12px; color: #3a3f5c; }
    .clean-table tbody td.num {
        text-align: right;
        font-family: 'IBM Plex Mono', monospace;
        font-size: .8rem;
        color: #1a1d2e;
    }
    .clean-table tbody td.name { font-weight: 500; color: #1a1d2e; }
    .table-wrap {
        background: #fff;
        border: 1px solid #e4e6ef;
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)


apply_style()
apply_custom_ui()
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ─────────────────────────────
# 📌 PAGE HEADER
# ─────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:8px;margin-bottom:2px  ">
  <span style="font-size:1.4rem; color:#000000">⚡</span>
  <h1 style="margin:0 ; color:#1a1d2e">Energy Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────
# 🗓️ MONTH + YEAR SELECTOR
# ─────────────────────────────
THAI_MONTHS = [
    "มกราคม","กุมภาพันธ์","มีนาคม","เมษายน",
    "พฤษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม",
    "กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม",
]

today = datetime.date.today()

col_month, col_year = st.columns([2, 1])
with col_month:
    selected_month_idx = st.selectbox(
        "เดือนที่คำนวณ",
        options=list(range(12)),
        index=today.month - 1,
        format_func=lambda i: THAI_MONTHS[i],
        key="selected_month",
    )
with col_year:
    year_options = [today.year + 543 + i for i in range(-2, 10)]
    selected_year_be = st.selectbox(
        "ปี (พ.ศ.)",
        options=year_options,
        index=year_options.index(today.year + 543),
        key="selected_year",
    )
    if selected_year_be is None:
        selected_year_be = today.year + 543

selected_year  = selected_year_be - 543
selected_month = selected_month_idx + 1
days_in_month  = calendar.monthrange(selected_year, selected_month)[1]
month_start    = pd.Timestamp(selected_year, selected_month, 1)
month_end      = pd.Timestamp(selected_year, selected_month, days_in_month)
working_days   = len(pd.bdate_range(month_start, month_end))
weekend_days   = days_in_month - working_days

st.markdown(f"""
<div class="month-row">
  <span style="font-size:.85rem;font-weight:600;color:#1a1d2e">
    {THAI_MONTHS[selected_month_idx]} {selected_year_be}
  </span>
  <span class="mbadge work">✦ {working_days} วันทำงาน</span>
  <span class="mbadge rest">เสาร์–อา. {weekend_days} วัน</span>
  <span class="mbadge days">รวม {days_in_month} วัน</span>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────
# 📊 KPI PLACEHOLDER (จะ fill ทีหลังหลังคำนวณเสร็จ)
# ─────────────────────────────
metrics_placeholder = st.empty()

# ─────────────────────────────
# ⚙️ HELPERS
# ─────────────────────────────
HOUR_OPTIONS  = [f"{h} ชม." for h in range(0, 13)]
DEFAULT_HOURS = 7

def _h(label: str) -> int:
    try:
        return int(label.split()[0])
    except Exception:
        return DEFAULT_HOURS

def _fmt_qty(row: pd.Series, qty_col, unit_col=None) -> str:
    if not qty_col:
        return "-"
    qty_val  = row.get(qty_col)
    unit_val = row.get(unit_col) if unit_col else None
    if pd.isna(qty_val) or str(qty_val).strip() == "":
        return "-"
    try:
        n = float(qty_val)
        qty_text = f"{int(n):,}" if n.is_integer() else f"{n:,.2f}"
    except Exception:
        qty_text = str(qty_val).strip()
    if unit_col and pd.notna(unit_val) and str(unit_val).strip():
        return f"{qty_text} {str(unit_val).strip()}"
    return qty_text

def _is_floor_3(v) -> bool:
    if isinstance(v, (int, float)):
        try:
            return int(v) == 3
        except Exception:
            return False
    return str(v).strip().lower() in {"3", "ชั้น 3", "ชั้น3", "floor 3", "floor3"}

def _floor_label(opt) -> str:
    if isinstance(opt, (int, float)):
        try:
            if float(opt).is_integer():
                return f"ชั้น {int(opt)}"
        except Exception:
            pass
    s = str(opt).strip()
    return f"ชั้น {s}" if s.isdigit() else s

# ─────────────────────────────
# 📥 LOAD AC DATA
# ─────────────────────────────
df = safe_load("ac_rooms")
if df.empty:
    st.error("โหลด AC_Rooms ไม่ได้")
    st.stop()

floor_col = find_col(df, ["floor"])
room_col  = find_col(df, ["room"])
kw_col    = find_col(df, ["kw"])
btu_col   = find_col(df, ["btu"])
cost_col  = find_col(df, ["cost"])

for col in [kw_col, btu_col, cost_col]:
    if col:
        df[col] = to_num(df[col])

# ─────────────────────────────
# 🔘 FLOOR SELECTOR
# ─────────────────────────────
floors         = sorted(df[floor_col].dropna().unique().tolist())
MACHINES_LABEL = "🏭 เครื่องจักร ชั้น 3"
menu           = floors + [MACHINES_LABEL]

default_selection = [floors[0]] if floors else []
selected_items = st.segmented_control(
    "เลือกชั้น",
    menu,
    selection_mode="multi",
    default=default_selection,
    format_func=lambda opt: MACHINES_LABEL if opt == MACHINES_LABEL else _floor_label(opt),
    key="floor_multi_select",
)
selected_items  = selected_items or []
selected_floors = [x for x in selected_items if x != MACHINES_LABEL]
show_machines   = MACHINES_LABEL in selected_items

# ─────────────────────────────
# 📋 HTML TABLE HELPERS
# ─────────────────────────────
def _html_ac_table(df_f: pd.DataFrame) -> str:
    has_btu = bool(btu_col)
    headers = ["ห้อง"] + (["BTU"] if has_btu else []) + ["kW", "฿ / ชม."]
    rows_html = ""
    kw_sum, cost_sum, btu_sum = 0.0, 0.0, 0.0

    for _, r in df_f.iterrows():
        kw_v   = float(r.get(kw_col,   0) or 0)
        cost_v = float(r.get(cost_col, 0) or 0)
        btu_v  = float(r.get(btu_col,  0) or 0) if has_btu else 0
        kw_sum   += kw_v
        cost_sum += cost_v
        btu_sum  += btu_v
        btu_td = f'<td class="num">{int(btu_v):,}</td>' if has_btu else ""
        rows_html += f"""
        <tr>
          <td class="name">{r.get(room_col, "-")}</td>
          {btu_td}
          <td class="num">{kw_v:.2f}</td>
          <td class="num">{cost_v:.2f}</td>
        </tr>"""

    btu_total_td = f'<td class="num"><strong>{int(btu_sum):,}</strong></td>' if has_btu else ""
    rows_html += f"""
    <tr class="total-row">
      <td class="name">รวม</td>
      {btu_total_td}
      <td class="num">{kw_sum:.2f}</td>
      <td class="num">{cost_sum:.2f}</td>
    </tr>"""

    ths = "".join(
        f'<th class="right">{h}</th>' if h != "ห้อง" else f'<th>{h}</th>'
        for h in headers
    )
    return f"""
    <div class="table-wrap">
      <table class="clean-table">
        <thead><tr>{ths}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


def _html_machine_table(df_m, name_col, qty_col, kw_c, cost_c) -> str:
    rows_html = ""
    kw_sum, cost_sum = 0.0, 0.0
    for _, r in df_m.iterrows():
        kw_v   = float(r.get(kw_c,   0) or 0)
        cost_v = float(r.get(cost_c, 0) or 0)
        kw_sum += kw_v; cost_sum += cost_v
        rows_html += f"""
        <tr>
          <td class="name">{r.get(name_col, "-")}</td>
          <td>{_fmt_qty(r, qty_col)}</td>
          <td class="num">{kw_v:.2f}</td>
          <td class="num">{cost_v:.2f}</td>
        </tr>"""
    rows_html += f"""
    <tr class="total-row">
      <td class="name">รวม</td><td>—</td>
      <td class="num">{kw_sum:.2f}</td>
      <td class="num">{cost_sum:.2f}</td>
    </tr>"""
    return f"""
    <div class="table-wrap">
      <table class="clean-table">
        <thead><tr>
          <th>เครื่องจักร</th><th>จำนวน</th>
          <th class="right">kW</th><th class="right">฿ / ชม.</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


# ─────────────────────────────
# 🔧 RENDER FUNCTIONS
# ─────────────────────────────
def _plotly_bar(df_src, x_col, y_col, color="#4a7cf7") -> None:
    fig = px.bar(
        df_src, x=x_col, y=y_col,
        orientation="h", text_auto=True,
        color_discrete_sequence=[color],
    )
    fig.update_layout(
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        font=dict(family="Sarabun, sans-serif", color="#5a6080", size=11),
        xaxis=dict(gridcolor="#f0f1f7", color="#8b92b3", showgrid=True),
        yaxis=dict(gridcolor="#f0f1f7", color="#5a6080", showgrid=False),
        margin=dict(l=4, r=4, t=4, b=4),
        height=300,
        coloraxis_showscale=False,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_machine_page() -> None:
    df_m = safe_load("machines_floor3")
    if df_m.empty:
        st.error("โหลด Machines_Floor3 ไม่ได้")
        return

    name_col_m = find_col(df_m, ["machine"])
    kw_col_m   = find_col(df_m, ["kw"])
    cost_col_m = find_col(df_m, ["cost"])
    qty_col_m  = find_col(df_m, ["qty", "quantity"])
    for col in [kw_col_m, cost_col_m]:
        if col:
            df_m[col] = to_num(df_m[col])

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown('<div class="section-label">รายการเครื่องจักร</div>', unsafe_allow_html=True)
        st.markdown(
            _html_machine_table(df_m, name_col_m, qty_col_m, kw_col_m, cost_col_m),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown('<div class="section-label">กำลังไฟ (kW)</div>', unsafe_allow_html=True)
        _plotly_bar(df_m, kw_col_m, name_col_m, color="#f5a623")


def _render_ac_floor(floor_val) -> pd.DataFrame:
    df_f = df[df[floor_col] == floor_val]
    if df_f.empty:
        st.warning(f"ไม่พบข้อมูล AC ของ {_floor_label(floor_val)}")
        return df_f

    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.markdown('<div class="section-label">ตารางแอร์แต่ละห้อง</div>', unsafe_allow_html=True)
        st.markdown(_html_ac_table(df_f), unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="section-label">กำลังไฟ (kW)</div>', unsafe_allow_html=True)
        _plotly_bar(df_f, kw_col, room_col, color="#4a7cf7")
    return df_f


def _render_floor_summary(floor_val, df_f: pd.DataFrame) -> tuple[float, pd.DataFrame]:
    st.markdown(
        '<div class="section-label" style="margin-top:14px">อุปกรณ์ทั้งหมดในชั้นนี้</div>',
        unsafe_allow_html=True,
    )

    rows: list[dict] = []

    # 1. AC
    if not df_f.empty and kw_col:
        for _, r in df_f.iterrows():
            btu_v = r.get(btu_col, 0) if btu_col else 0
            rows.append({
                "อุปกรณ์":  f"❄️ {r.get(room_col, '-')}",
                "จำนวน":    f"{btu_v:,.0f} BTU" if pd.notna(btu_v) and btu_v else "-",
                "kW":        r.get(kw_col, 0),
                "฿/ชม.":    r.get(cost_col, 0),
                "ชม./วัน":  f"{DEFAULT_HOURS} ชม.",
            })

    # 2. Equipment
    df_eq = safe_load("equipment")
    if not df_eq.empty:
        floor_eq = find_col(df_eq, ["floor"])
        name_eq  = find_col(df_eq, ["equipment", "name"])
        qty_eq   = find_col(df_eq, ["quantity", "qty", "count"])
        unit_eq  = find_col(df_eq, ["unit"])
        kw_eq    = find_col(df_eq, ["kw_total"]) or find_col(df_eq, ["kw"])
        cost_eq  = find_col(df_eq, ["cost_per_hour", "cost"])
        for col in [kw_eq, cost_eq]:
            if col:
                df_eq[col] = to_num(df_eq[col])
        df_eq_f = df_eq[df_eq[floor_eq] == floor_val] if floor_eq else pd.DataFrame()
        if df_eq_f.empty and floor_eq:
            df_eq_f = df_eq[df_eq[floor_eq].astype(str).str.strip() == str(floor_val).strip()]
        for _, r in df_eq_f.iterrows():
            rows.append({
                "อุปกรณ์":  r.get(name_eq, "-"),
                "จำนวน":    _fmt_qty(r, qty_eq, unit_eq),
                "kW":        r.get(kw_eq, 0),
                "฿/ชม.":    r.get(cost_eq, 0),
                "ชม./วัน":  f"{DEFAULT_HOURS} ชม.",
            })

    # 3. Machines (floor 3)
    if _is_floor_3(floor_val):
        df_m = safe_load("machines_floor3")
        if not df_m.empty:
            nc = find_col(df_m, ["machine"])
            kc = find_col(df_m, ["kw"])
            cc = find_col(df_m, ["cost"])
            qc = find_col(df_m, ["qty", "quantity"])
            for col in [kc, cc]:
                if col:
                    df_m[col] = to_num(df_m[col])
            for _, r in df_m.iterrows():
                rows.append({
                    "อุปกรณ์":  f"🏭 {r.get(nc, '-')}",
                    "จำนวน":    _fmt_qty(r, qc),
                    "kW":        r.get(kc, 0),
                    "฿/ชม.":    r.get(cc, 0),
                    "ชม./วัน":  f"{DEFAULT_HOURS} ชม.",
                })

    summary_df = pd.DataFrame(rows)
    if summary_df.empty:
        st.info("ไม่มีข้อมูลสำหรับชั้นนี้")
        return 0.0, pd.DataFrame()

    summary_df.insert(0, "เลือก", True)
    summary_df["kW"]     = pd.to_numeric(summary_df["kW"],     errors="coerce").fillna(0)
    summary_df["฿/ชม."] = pd.to_numeric(summary_df["฿/ชม."], errors="coerce").fillna(0)

    edited_df = st.data_editor(
        summary_df,
        use_container_width=True,
        hide_index=True,
        disabled=["อุปกรณ์", "จำนวน", "kW", "฿/ชม."],
        column_config={
            "เลือก": st.column_config.CheckboxColumn("เลือก", default=True),
            "kW":     st.column_config.NumberColumn("kW",     format="%.2f"),
            "฿/ชม.": st.column_config.NumberColumn("฿/ชม.", format="%.2f"),
            "ชม./วัน": st.column_config.SelectboxColumn(
                "⏱ ชม./วัน",
                options=HOUR_OPTIONS,
                required=True,
                width="small",
            ),
        },
        key=f"eq_summary_{floor_val}",
    )

    sel = edited_df[edited_df["เลือก"]].copy() if "เลือก" in edited_df.columns else edited_df.copy()
    sel["_h"] = sel["ชม./วัน"].apply(_h)
    sel["ค่าไฟ/วัน"] = sel["฿/ชม."] * sel["_h"]
    sel["ค่าไฟ/เดือน"] = sel["ค่าไฟ/วัน"] * working_days
    monthly_cost_floor = float(sel["ค่าไฟ/เดือน"].sum())

    export_df = sel[["อุปกรณ์", "จำนวน", "kW", "฿/ชม.", "ชม./วัน", "ค่าไฟ/วัน", "ค่าไฟ/เดือน"]].copy()
    export_df.insert(0, "ชั้น", _floor_label(floor_val))

    c_dl1, c_dl2 = st.columns([1, 1])
    with c_dl1:
        st.markdown(f"""
        <div class="floor-cost-row">
          <span class="floor-cost-label">
            ค่าไฟชั้นนี้ — {THAI_MONTHS[selected_month_idx]} {selected_year_be}
            &nbsp;·&nbsp; วันทำงาน {working_days} วัน
          </span>
          <span class="floor-cost-value">฿{monthly_cost_floor:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    with c_dl2:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            export_df.to_excel(writer, index=False, sheet_name="Summary")

        st.download_button(
            label=f"⬇️ ดาวน์โหลด Excel {_floor_label(floor_val)}",
            data=output.getvalue(),
            file_name=f"energy_summary_{str(floor_val).replace(' ', '_')}_{selected_year}_{selected_month:02d}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_excel_{floor_val}",
            use_container_width=True,
        )

    return monthly_cost_floor, export_df


# ─────────────────────────────
# 🏢 RENDER แต่ละชั้น (Expander)
# ─────────────────────────────
floor_monthly_costs: list[float] = []
all_export_frames: list[pd.DataFrame] = []

if selected_floors:
    for floor_val in selected_floors:
        with st.expander(f"🏢 {_floor_label(floor_val)}", expanded=(len(selected_floors) == 1)):
            df_floor_local = _render_ac_floor(floor_val)
            cost, export_df = _render_floor_summary(floor_val, df_floor_local)
            floor_monthly_costs.append(cost)
            if export_df is not None and not export_df.empty:
                all_export_frames.append(export_df)

if show_machines:
    with st.expander(MACHINES_LABEL, expanded=False):
        _render_machine_page()

# ─────────────────────────────
# ✅ GRAND TOTAL
# ─────────────────────────────
if selected_floors:
    total = sum(floor_monthly_costs)

    # ── fill KPI cards ขึ้นไปด้านบน (เหนือ expander) ──
    with metrics_placeholder.container():
        k1, k2, k3 = st.columns(3)
        k1.metric(
            "เดือนที่คำนวณ",
            f"{THAI_MONTHS[selected_month_idx]} {selected_year_be}",
            delta=f"วันทำงาน {working_days} วัน",
            delta_color="off",
        )
        k2.metric(
            "ชั้นที่เลือก",
            f"{len(selected_floors)} ชั้น",
            delta="รวมอุปกรณ์ทั้งหมด",
            delta_color="off",
        )
        k3.metric(
            "ค่าไฟรวม / เดือน",
            f"฿{total:,.0f}",
            delta="คำนวณตาม ชม./วัน ของแต่ละอุปกรณ์",
            delta_color="off",
        )

    # ── total card ด้านล่างสุด ──
    st.markdown(f"""
    <div class="total-card">
      <div>
        <div class="total-label">รวมค่าไฟทุกชั้นที่เลือก — {THAI_MONTHS[selected_month_idx]} {selected_year_be}</div>
        <div class="total-sub">{working_days} วันทำงาน · คำนวณตาม ชม./วัน ของแต่ละอุปกรณ์</div>
      </div>
      <div class="total-value">฿{total:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    if all_export_frames:
        all_export_df = pd.concat(all_export_frames, ignore_index=True)
        summary_total_df = (
            all_export_df.groupby("ชั้น", as_index=False)["ค่าไฟ/เดือน"]
            .sum()
            .rename(columns={"ค่าไฟ/เดือน": "รวมค่าไฟ/เดือน"})
        )
        summary_total_df.loc[len(summary_total_df)] = ["รวมทั้งหมด", float(summary_total_df["รวมค่าไฟ/เดือน"].sum())]

        output_all = io.BytesIO()
        with pd.ExcelWriter(output_all, engine="openpyxl") as writer:
            all_export_df.to_excel(writer, index=False, sheet_name="รายละเอียดทั้งหมด")
            summary_total_df.to_excel(writer, index=False, sheet_name="สรุปรวม")

        st.download_button(
            label="⬇️ ดาวน์โหลด Excel รวมทุกชั้น",
            data=output_all.getvalue(),
            file_name=f"energy_summary_all_floors_{selected_year}_{selected_month:02d}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel_all_floors",
            use_container_width=True,
        )

        st.dataframe(summary_total_df, use_container_width=True, hide_index=True)

else:
    st.info("เลือกชั้นอย่างน้อย 1 ชั้น เพื่อคำนวณยอดรวม")