import streamlit as st


def apply_style():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer     {visibility: hidden;}
    header     {visibility: hidden;}

    .stApp {
    background: radial-gradient(circle at top right, #FFFAFA 0%, #0f172a 50%, #020617 100%);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
        border-right: 1px solid rgba(148,163,184,0.15);
    }
    .card {
        background: linear-gradient(180deg, rgba(30,41,59,0.94), rgba(15,23,42,0.94));
        border: 1px solid rgba(148,163,184,0.17);
        border-radius: 18px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.2);
        padding: 18px;
        margin-bottom: 8px;
    }
    .label  { color:#94A3B8; font-size:0.82rem; margin-bottom:0.4rem; }
    .metric { color:#E2E8F0; font-size:1.7rem; font-weight:700; line-height:1.2; }
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(148,163,184,0.15);
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)


def plot_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig