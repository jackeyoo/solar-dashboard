import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚡ Nature Biotech")

        st.page_link("streamlit_app.py", label="📊 Overview")
        st.page_link("pages/1_Equipment.py", label="⚙️ Equipment")
        st.page_link("pages/2_Solar.py", label="☀️ Solar")

        st.divider()

        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()