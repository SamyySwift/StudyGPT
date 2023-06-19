import streamlit as st
from streamlit_lottie import st_lottie
from utils.config import load_lottiefile
from streamlit_extras.add_vertical_space import add_vertical_space

col1, col2 = st.columns([2, 4])
with col1:
    lottie_bot = load_lottiefile("lotties/data-analysis.json")
    st_lottie(lottie_bot)

with col2:
    st.markdown("# :blue[Research]:red[Assistant]")
    st.markdown("**:blue[Extract relevant info from your documents]**")
    # st.markdown("#### Welcome! Samuel Okon👋")

add_vertical_space(2)

st.subheader("Upload files for indexing")
uploaded_file = st.file_uploader(
    ":blue[Upload your documents]", accept_multiple_files=True
)
st.button("Index Docs", key="index-btn")
add_vertical_space(3)
# Display a text input widget
st.text_input(
    ":blue[Search Documents]",
    key="main_query",
)
