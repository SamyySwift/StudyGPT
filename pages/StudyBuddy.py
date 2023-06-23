import streamlit as st
from utils.config import display_animation
from streamlit_extras.add_vertical_space import add_vertical_space
from dataclasses import dataclass
from typing import Literal


col1, col2 = st.columns([2, 4])
with col1:
    display_animation("lotties/buddies.json")

with col2:
    st.markdown("# :blue[Study]:red[Buddy]")
    st.markdown("**:blue[Meet your study partner]**")


st.markdown(
    ":green[Yaay!!!!]🎉:blue[Flip]:red[Bot] mactched 🧑‍🤝‍🧑you both😁. You can help each other learn this course effectively😉"
)

add_vertical_space(2)

st.subheader("Share Files")
uploaded_file = st.file_uploader(
    ":blue[share files with your buddy]", accept_multiple_files=True
)
share_button = st.button("Share")
if share_button and uploaded_file:
    st.success("File Sent!")


@dataclass
class chatMessage:
    """Class for keeping track of a chat message."""

    origin: Literal["human", "ai"]
    message: str


if "chat_hist" not in st.session_state:
    st.session_state.chat_hist = []


def chat_func():
    if st.session_state.chat_query:
        human_prompt = st.session_state.chat_query
        # chatgpt_response = query(
        #     human_prompt,
        #     st.session_state.vectordb,
        #     st.session_state.return_source,
        # )
        st.session_state.chat_hist.append(chatMessage("human", human_prompt))
        # st.session_state.history.append(Message("ai", chatgpt_response))

    # st.session_state.chat_query = ""


chat_placeholder = st.container()

with chat_placeholder:
    for chat in st.session_state.chat_hist:
        div = f"""
        <div class="chat-row 
                    {'' if chat.origin == 'ai' else 'row-reverse'}">
                    <img class="chat-icon" src="app/static/{
                        'ai_icon.png' if chat.origin == 'ai' 
                                    else 'user.png'}"
                        width=32 height=32>
                <div class="chat-bubble
                    {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
                        &#8203;{chat.message}
                </div>
        </div>
                    """
        st.markdown(div, unsafe_allow_html=True)


add_vertical_space(2)
st.subheader("Chat With Buddy")
st.text_input(
    ":blue[Chat with your buddy]",
    placeholder="Type a message...",
    on_change=chat_func,
    key="chat_query",
)
