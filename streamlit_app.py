import streamlit as st
from style import apply_style

st.set_page_config(
    page_title="Nature Biotech Energy Dashboard",
    page_icon="⚡",
    layout="wide",
)

apply_style()

st.sidebar.markdown("## ⚡ Nature Biotech")
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# หน้า Home แสดงเมื่อเปิด app ครั้งแรก
st.markdown("""
<div style="
    background: linear-gradient(130deg, rgba(56,189,248,0.16), rgba(34,197,94,0.12));
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 24px;
    padding: 40px 36px;
    margin-top: 60px;
    text-align: center;
">
    <h1 style="color:#E2E8F0; margin:0;">⚡ Nature Biotech Energy Dashboard</h1>
    <p style="color:#94A3B8; margin-top:12px; font-size:1.1rem;">
        เลือกเมนูด้านซ้ายเพื่อดูข้อมูล
    </p>
</div>
""", unsafe_allow_html=True)