from dataclasses import dataclass
from typing import Literal

import streamlit as st
from PIL import Image
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stateful_button import button
from streamlit_extras.switch_page_button import switch_page
from streamlit_pills import pills

from utils.config import display_alert, display_animation
from utils.extract import extract_text
from utils.firebase import folder_exist
from utils.flipbot import create_vectordb, index_cam_input, load_vectordb, query

# -------------------------------- PAGE SETUP --------------------------------------------

im = Image.open("static/logo.png")
st.set_page_config(layout="centered", page_icon=im, page_title="FlipBot")

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}<\style>", unsafe_allow_html=True)

# -------------------------------- SIDEBAR ------------------------------------------------
with st.sidebar:
    # st.header("⚙️**Setup**")
    # st.text_input(
    #     "🔑OpenAI API Key",
    #     type="password",
    #     placeholder="Paste your OpenAI API key here (sk-...)",
    #     help="You can get your API key from https://platform.openai.com/account/api-keys.",
    #     value=st.session_state.get("OPENAI_API_KEY", ""),
    #     key="api_inp",
    # )

    # if st.session_state.api_inp and st.session_state.api_inp[:3] != "sk-":
    #     st.error("Invalid API key!")
    # elif st.session_state.api_inp[:3] == "sk-" and len(st.session_state.api_inp) == 51:
    #     st.session_state["OPENAI_API_KEY"] = st.session_state.api_inp

    st.header("Source Documents")
    st.session_state.return_source = st.checkbox(
        label="Do you want the source documents?", key="Return_source"
    )

    st.header("💡Hints")
    with st.expander("Some helpful hints on how to use FlipBot😉"):
        st.write(
            "You can ask FlipBot any questions based on the materials you provided as well as follow up questions. You could even ask it to Summarize or Explain specific topics or chapters for you.\
            Here are some helpful propmts you could use to make the bot answer your questions appropriately.  \n\n"
            "1️⃣ Given the context information, can you explain what transformers are?  \n"
            "2️⃣ Summarize this topic; '{put your topic here}'. Or, Summarize chapter {chapter number}  \n"
            "3️⃣ Explain this; '{what you want it to explain goes here}' "
        )


# ---------------------------------- MAIN APP --------------------------------------------


@dataclass
class Message:
    """Class for keeping track of a chat message."""

    origin: Literal["human", "ai"]
    message: str


def clear_main_query():
    if st.session_state.main_query:
        try:
            human_prompt = st.session_state.main_query
            chatgpt_response = query(
                human_prompt,
                st.session_state.vectordb,
                st.session_state.return_source,
            )
            st.session_state.history.append(Message("human", human_prompt))
            st.session_state.history.append(Message("ai", chatgpt_response))

        except AttributeError:
            # with alert_placeholder:
            display_alert(
                "Please ensure that you have indexed your documents",
                icon="warning",
            )
    st.session_state.main_query = ""


def process_cam_input(image):
    bytes_data = image.getvalue()
    file_name = image.name
    extract_text(bytes_data, file_name)
    with st.spinner("Indexing Camera Input..."):
        vectordb = index_cam_input(file_name)
        if "vectordb" not in st.session_state:
            st.session_state.vectordb = vectordb
    display_alert("Camera Image Indexed!")


def main():
    col1, col2 = st.columns([2, 4])
    with col1:
        display_animation("lotties/robot.json")

    with col2:
        st.markdown("# :blue[Flip]:red[Bot]")
        st.markdown("**:blue[Your Personal AI school assistant]**")
        # st.markdown("#### Welcome👋 **Samuel Okon**")

    st.subheader("Upload files for indexing")
    uploaded_files = st.file_uploader(
        ":blue[Upload your documents]", accept_multiple_files=True
    )
    col3, col4 = st.columns([2, 7])
    with col3:
        index_btn = st.button("Index Documents")
    with col4:
        if button("Use Camera", key="bt1"):
            image = st.camera_input(label="Snap Document")
            if image:
                process_cam_input(image)

    try:
        if index_btn:
            if uploaded_files is not None:
                persist_dir = "+".join(file.name[:10] for file in uploaded_files)

                if folder_exist(persist_dir):
                    # display_alert("Document is already Indexed!")
                    with st.spinner("Loading Index..."):
                        vectordb = load_vectordb(persist_dir)
                        if "vectordb" not in st.session_state:
                            st.session_state.vectordb = vectordb
                    st.success("🔔There's a match🎉. Would you like to study together?")

                    option = st.checkbox("Yes")
                    if option:
                        st.sidebar.write("yes")
                        switch_page("StudyBuddy")

                else:
                    with st.spinner("Indexing your documents..."):
                        vectordb = create_vectordb(persist_dir, uploaded_files)
                        if "vectordb" not in st.session_state:
                            st.session_state.vectordb = vectordb
                    display_alert("Done Indexing!")
            else:
                display_alert("Upload files before indexing!", icon="warning")
    except IndexError:
        display_alert("Upload files before indexing!", icon="warning")

    add_vertical_space(3)

    st.subheader("Interact with :blue[Flip]:red[Bot]")
    # Create tabs
    tab1, tab2 = st.tabs(["Ask FlipBot", "Practice Quiz"])

    with tab1:
        if "result" not in st.session_state:
            st.session_state.result = ""
        if "history" not in st.session_state:
            st.session_state.history = []

        # Add chat page placeholder
        chat_placeholder = st.container()
        add_vertical_space(2)

        with chat_placeholder:
            for chat in st.session_state.history:
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

        # Display a text input widget
        st.text_input(
            ":blue[Ask FlipBot any question as well as follow up questions]",
            placeholder="Ask questions based on your uploaded materials...",
            on_change=clear_main_query,
            key="main_query",
        )

    with tab2:
        add_vertical_space(1)
        st.write("Click the button below 👇 to go to practice session")
        want_to_practice = st.button("Take me to quiz")
        if want_to_practice:
            switch_page("Quiz")

    # else:
    #     st.markdown(
    #         "##### :green[Psst!] You'd have to provide your [OpenAI API Key](https://platform.openai.com/account/api-keys) 🔑 under the :red[Setup] tab from the sidebar to start using the application. The sidebar can be accessed by clicking on the top left icon 😉"
    #     )


if __name__ == "__main__":
    main()
