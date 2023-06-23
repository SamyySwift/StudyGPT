import streamlit as st
from utils.config import display_animation


col1, col2 = st.columns([2, 4])
with col1:
    display_animation("lotties/buddies.json")

with col2:
    st.markdown("# :blue[Study]:red[Buddy]")
    st.markdown("**:blue[Meet your study partner]**")


st.markdown(
    "### :green[Yaay!!!!]🎉:blue[Flip]:red[Bot] mactched 🧑‍🤝‍🧑you both😁. You can help each other learn this course effectively😉"
)
