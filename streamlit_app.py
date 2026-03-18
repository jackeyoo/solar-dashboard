# import streamlit as st
# from style import apply_style

# st.set_page_config(
#     page_title="Nature Biotech Energy Dashboard",
#     page_icon="⚡",
#     layout="wide",
# )

# apply_style()

# st.sidebar.markdown("## ⚡ Nature Biotech")

# if st.sidebar.button("🔄 Refresh Data"):
#     st.cache_data.clear()
#     st.rerun()

# st.markdown("""
# <div style="
#     background: linear-gradient(130deg, rgba(56,189,248,0.16), rgba(34,197,94,0.12));
#     border-radius: 24px; padding: 40px; text-align: center; margin-top: 60px;
# ">
#     <h1 style="color:#E2E8F0;">⚡ Nature Biotech Energy Dashboard</h1>
#     <p style="color:#94A3B8;">เลือกเมนูด้านซ้ายเพื่อดูข้อมูล</p>
# </div>
# """, unsafe_allow_html=True)

# import streamlit as st

# st.switch_page("pages/1_Overview.py")