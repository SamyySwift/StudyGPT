import streamlit as st
from utils.config import display_animation
from streamlit_extras.add_vertical_space import add_vertical_space
import random
import time


if "messages" not in st.session_state:
    st.session_state.messages = []


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
add_vertical_space(2)


if share_button and uploaded_file:
    st.success("File Sent!")
elif share_button and uploaded_file is None:
    st.warning("upload files before sharing")


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])


# st.subheader("Chat With Buddy")
# Accept user input
if prompt := st.chat_input("Send a message..."):
    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "avatar": "👨‍💻"}
    )
    # Display user message in chat message container
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="👦"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, Is there anything I can help you with?",
                "Do you need help?",
                "Where do you have issues?",
                "what topic do you have issues with?",
            ]
        )
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response, "avatar": "👨"}
    )
