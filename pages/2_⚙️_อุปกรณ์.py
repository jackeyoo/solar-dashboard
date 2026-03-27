import streamlit as st
import plotly.express as px
from utils import safe_load, find_col, to_num
from style import apply_style, plot_theme
import pandas as pd
import datetime
import calendar

# ─────────────────────────────
# 🎨 UI STYLE
# ─────────────────────────────
def apply_custom_ui():
    st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .card {
        background: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }
    div[data-testid="stSegmentedControl"] button,
    div[data-testid="stPills"] button {
        background: transparent !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        margin-right: 8px !important;
    }
    div[data-testid="stSegmentedControl"] button[aria-pressed="true"],
    div[data-testid="stPills"] button[aria-pressed="true"] {
        background: #0ea5e9 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

apply_style()
apply_custom_ui()

st.title("⚡ Energy Dashboard")

# ─────────────────────────────
# 🗓️ MONTH + YEAR SELECTOR
# ─────────────────────────────
THAI_MONTHS = [
    "มกราคม","กุมภาพันธ์","มีนาคม","เมษายน",
    "พฤษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม",
    "กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม",
]

today = datetime.date.today()

# ย้อนหลัง 2 ปี → ล่วงหน้า 2 ปี  (ปรับตัวเลขได้ตามต้องการ)
YEAR_RANGE = list(range(today.year - 2, today.year + 3))
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
    year_options = [today.year + 543 + i for i in range(-2, 10)]  # 16 ปี
    selected_year_be = st.selectbox(
        "ปี (พ.ศ.)",
        options=year_options,
        index=year_options.index(today.year + 543),  # index 5 = ปีปัจจุบัน (เพราะ range เริ่ม -5)
        key="selected_year",
    )
    if selected_year_be is None:
        selected_year_be = today.year + 543

# แปลงกลับเป็น ค.ศ.
selected_year = selected_year_be - 543
selected_month = selected_month_idx + 1
days_in_month  = calendar.monthrange(selected_year, selected_month)[1]
month_start    = pd.Timestamp(selected_year, selected_month, 1)
month_end      = pd.Timestamp(selected_year, selected_month, days_in_month)
working_days   = len(pd.bdate_range(month_start, month_end))
weekend_days   = days_in_month - working_days

st.caption(
    f"📅 **{THAI_MONTHS[selected_month_idx]} {selected_year_be}** — "
    f"วันทำงาน **{working_days} วัน**  |  เสาร์–อาทิตย์ **{weekend_days} วัน**  |  รวม **{days_in_month} วัน**"
)
st.divider()

# ─────────────────────────────
# ⚙️ HELPERS
# ─────────────────────────────
HOUR_OPTIONS = [f"{h} ชม." for h in range(0, 13)]
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

def _floor_label(opt) -> str:
    if opt == MACHINES_LABEL:
        return MACHINES_LABEL
    if isinstance(opt, (int, float)):
        try:
            if float(opt).is_integer():
                return f"ชั้น {int(opt)}"
        except Exception:
            pass
    s = str(opt).strip()
    return f"ชั้น {s}" if s.isdigit() else s

default_selection = [floors[0]] if floors else []
selected_items = st.segmented_control(
    "เลือกชั้น", menu,
    selection_mode="multi",
    default=default_selection,
    format_func=_floor_label,
    key="floor_multi_select",
)
selected_items  = selected_items or []
selected_floors = [x for x in selected_items if x != MACHINES_LABEL]
show_machines   = MACHINES_LABEL in selected_items

# ─────────────────────────────
# 🔧 RENDER FUNCTIONS
# ─────────────────────────────
def _render_machine_page() -> None:
    df_m = safe_load("machines_floor3")
    if df_m.empty:
        st.error("โหลด Machines_Floor3 ไม่ได้")
        return
    name_col_m = find_col(df_m, ["machine"])
    kw_col_m   = find_col(df_m, ["kw"])
    cost_col_m = find_col(df_m, ["cost"])
    qty_col_m  = find_col(df_m, ["qty", "quantity"])
    for col in [kw_col_m, cost_col_m, qty_col_m]:
        if col:
            df_m[col] = to_num(df_m[col])
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        t = df_m[[name_col_m, qty_col_m, kw_col_m, cost_col_m]].copy()
        t.columns = ["เครื่องจักร", "จำนวน", "kW", "฿/ชม."]
        st.dataframe(t, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.bar(df_m, x=kw_col_m, y=name_col_m, orientation="h",
                     text_auto=True, color=kw_col_m, color_continuous_scale="Oranges")
        fig.update_layout(height=420)
        st.plotly_chart(plot_theme(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def _render_ac_floor(floor_val) -> pd.DataFrame:
    df_f = df[df[floor_col] == floor_val]
    if df_f.empty:
        st.warning(f"ไม่พบข้อมูล AC ของ {_floor_label(floor_val)}")
        return df_f
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        cols    = [room_col] + ([btu_col] if btu_col else []) + [kw_col, cost_col]
        table   = df_f[cols].copy()
        headers = ["ห้อง"] + (["BTU"] if btu_col else []) + ["kW", "฿/ชม."]
        table.columns = headers
        total   = table.sum(numeric_only=True)
        tr      = {"ห้อง": "รวม", "kW": total.get("kW", 0), "฿/ชม.": total.get("฿/ชม.", 0)}
        if "BTU" in table.columns:
            tr["BTU"] = total.get("BTU", 0)
        table = pd.concat([table, pd.DataFrame([tr])], ignore_index=True)
        st.dataframe(table, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.bar(df_f, x=kw_col, y=room_col, orientation="h",
                     text_auto=True, color=kw_col, color_continuous_scale="Blues")
        fig.update_layout(height=420)
        st.plotly_chart(plot_theme(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    return df_f


def _render_floor_summary(floor_val, df_f: pd.DataFrame) -> float:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### ⚙️ อุปกรณ์ทั้งหมด {_floor_label(floor_val)}")

    rows: list[dict] = []

    # 1. AC แยกแต่ละห้อง
    if not df_f.empty and kw_col:
        for _, r in df_f.iterrows():
            btu_v = r.get(btu_col, 0) if btu_col else 0
            rows.append({
                "อุปกรณ์": f"❄️ {r.get(room_col, '-')}",
                "จำนวน":   f"{btu_v:,.0f} BTU" if pd.notna(btu_v) and btu_v else "-",
                "kW":       r.get(kw_col, 0),
                "฿/ชม.":   r.get(cost_col, 0),
                "ชม./วัน": f"{DEFAULT_HOURS} ชม.",
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
                "อุปกรณ์": r.get(name_eq, "-"),
                "จำนวน":   _fmt_qty(r, qty_eq, unit_eq),
                "kW":       r.get(kw_eq, 0),
                "฿/ชม.":   r.get(cost_eq, 0),
                "ชม./วัน": f"{DEFAULT_HOURS} ชม.",
            })

    # 3. Machine (ชั้น 3 เท่านั้น)
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
                    "อุปกรณ์": f"🏭 {r.get(nc, '-')}",
                    "จำนวน":   _fmt_qty(r, qc),
                    "kW":       r.get(kc, 0),
                    "฿/ชม.":   r.get(cc, 0),
                    "ชม./วัน": f"{DEFAULT_HOURS} ชม.",
                })

    summary_df = pd.DataFrame(rows)
    if summary_df.empty:
        st.info("ไม่มีข้อมูลสำหรับชั้นนี้")
        st.markdown("</div>", unsafe_allow_html=True)
        return 0.0

    summary_df.insert(0, "เลือก", True)
    summary_df["kW"]     = pd.to_numeric(summary_df["kW"],     errors="coerce").fillna(0)
    summary_df["฿/ชม."] = pd.to_numeric(summary_df["฿/ชม."], errors="coerce").fillna(0)

    edited_df = st.data_editor(
        summary_df,
        use_container_width=True,
        hide_index=True,
        disabled=["อุปกรณ์", "จำนวน", "kW", "฿/ชม."],
        column_config={
            "เลือก": st.column_config.CheckboxColumn(
                "เลือก", default=True,
                help="ติ๊กเพื่อรวมคำนวณ",
            ),
            "kW":     st.column_config.NumberColumn("kW",     format="%.2f"),
            "฿/ชม.": st.column_config.NumberColumn("฿/ชม.", format="%.2f"),
            "ชม./วัน": st.column_config.SelectboxColumn(
                "⏱ ชม./วัน",
                options=HOUR_OPTIONS,
                required=True,
                help="เลือกจำนวนชั่วโมงใช้งานต่อวัน",
                width="small",
            ),
        },
        key=f"eq_summary_{floor_val}",
    )

    sel = edited_df[edited_df["เลือก"]].copy() if "เลือก" in edited_df.columns else edited_df.copy()
    sel["_h"]            = sel["ชม./วัน"].apply(_h)
    sel["_monthly_cost"] = sel["฿/ชม."] * sel["_h"] * working_days
    monthly_cost_floor   = float(sel["_monthly_cost"].sum())

    st.caption(
        f"📅 คำนวณ {THAI_MONTHS[selected_month_idx]} {selected_year_be} — "
        f"วันทำงาน **{working_days} วัน** | "
        f"ค่าไฟชั้นนี้ **฿{monthly_cost_floor:,.0f}**"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    return monthly_cost_floor


# ─────────────────────────────
# 🏢 RENDER แต่ละชั้น
# ─────────────────────────────
floor_monthly_costs: list[float] = []

if selected_floors:
    for floor_val in selected_floors:
        with st.expander(f"🏢 {_floor_label(floor_val)}", expanded=(len(selected_floors) == 1)):
            df_floor_local = _render_ac_floor(floor_val)
            cost = _render_floor_summary(floor_val, df_floor_local)
            floor_monthly_costs.append(cost)

if show_machines:
    with st.expander(MACHINES_LABEL, expanded=False):
        _render_machine_page()

# ─────────────────────────────
# ✅ GRAND TOTAL
# ─────────────────────────────
if selected_floors:
    total = sum(floor_monthly_costs)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### ✅ รวมทุกชั้นที่เลือก ({len(selected_floors)} ชั้น)")

    c1, c2 = st.columns(2)
    with c1:
        st.metric(
            "เดือนที่คำนวณ",
            f"{THAI_MONTHS[selected_month_idx]} {selected_year_be}",
            delta=f"วันทำงาน {working_days} วัน (ตัดเสาร์–อาทิตย์ {weekend_days} วัน)",
            delta_color="off",
        )
    with c2:
        st.metric(
            "ค่าไฟ/เดือน (รวม)",
            f"฿{total:,.0f}",
            delta="คำนวณตาม ชม./วัน ของแต่ละอุปกรณ์",
            delta_color="off",
        )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("เลือกชั้นอย่างน้อย 1 ชั้น เพื่อคำนวณยอดรวม")