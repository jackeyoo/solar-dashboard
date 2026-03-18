import streamlit as st

def apply_style():
    st.markdown("""
    <style>
    body { background-color: #0F172A; }
    </style>
    """, unsafe_allow_html=True)