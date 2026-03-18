import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚡ Nature Biotech")

        st.page_link("pages/1_Overview.py", label="📊 Overview")
        st.page_link("pages/2_Equipment.py", label="⚙️ Equipment")
        st.page_link("pages/3_Solar.py", label="☀️ Solar")

        st.divider()

        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()