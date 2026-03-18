import streamlit as st

def apply_style():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
    /* ===== ซ่อน menu default ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ===== ซ่อน streamlit_app ใน sidebar nav ===== */
    [data-testid="stSidebarNav"] ul li:first-child {
        display: none !important;
    }

    /* ===== Background ===== */
    .stApp {
        background: #DCDCDC;
    }

    /* ===== Layout ===== */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* ===== Sidebar ===== */
    [data-testid="stSidebar"] {
        background: #000000;
        border-right: 1px solid rgba(148,163,184,0.2);
    }

    /* ===== Sidebar text ทั้งหมด ===== */
    [data-testid="stSidebar"] * {
        color: white !important;
        font-size: 15px !important;
        font-family: 'Prompt', sans-serif !important;
    }

    /* ===== Sidebar Title ===== */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: white !important;
    }

    /* ===== Sidebar Button ===== */
    [data-testid="stSidebar"] .stButton button {
        background-color: #111827 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #22c55e !important;
        color: white !important;
    }

    /* ===== Selectbox / Input ===== */
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stTextArea textarea,
    [data-testid="stSidebar"] .stNumberInput input {
        color: white !important;
        background-color: #111827 !important;
    }

    /* ===== Card ===== */
    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        padding: 18px;
        margin-bottom: 8px;
    }

    /* ===== Text ===== */
    .label {
        color: #64748b;
        font-size: 0.85rem;
        margin-bottom: 0.4rem;
    }

    .metric {
        color: #0f172a;
        font-size: 1.7rem;
        font-weight: 700;
        line-height: 1.2;
    }

    /* ===== Dataframe ===== */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(148,163,184,0.2);
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)


def plot_theme(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig