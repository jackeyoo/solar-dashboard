# import streamlit as st

# st.title("Solar Dashboard")

# st.image("assets/NB256-o2zjy16wije0o2airfsyfibi0gvu6yx706i1i9tu80.jpg", use_container_width=True)
# st.markdown("""
# <style>
# .stApp {
#     background-image: url("assets/assets/NB256-o2zjy16wije0o2airfsyfibi0gvu6yx706i1i9tu80.jpg");
#     background-size: cover;
#     background-position: center;
#     background-repeat: no-repeat;
# }
# </style>
# """, unsafe_allow_html=True)

# st.title("⚡ Solar Dashboard")

import streamlit as st
from style import apply_style

st.set_page_config(page_title="Energy Dashboard", layout="wide")
apply_style()
st.empty()