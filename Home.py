import json
import os

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_custom_notification_box import custom_notification_box
from streamlit_lottie import st_lottie
from streamlit_pills import pills
from streamlit_extras.switch_page_button import switch_page
from utils.extract import process_scanned_documents, extract_text
from utils.config import notification_styles
from utils.langchain_qa import questionAnswer


# -------------------------------- PAGE SETUP --------------------------------------------
st.set_page_config(layout="centered", page_icon="👨", page_title="StudentGPT")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}<\style>", unsafe_allow_html=True)


@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


# -------------------------------- SIDEBAR ------------------------------------------------
with st.sidebar:
    st.header("⚙️**Setup**")
    st.text_input(
        "🔑OpenAI API Key",
        type="password",
        placeholder="Paste your OpenAI API key here (sk-...)",
        help="You can get your API key from https://platform.openai.com/account/api-keys.",
        value=st.session_state.get("OPENAI_API_KEY", ""),
        key="api_inp",
    )

    if st.session_state.api_inp and st.session_state.api_inp[:3] != "sk-":
        st.error("Invalid API key!")
    elif st.session_state.api_inp[:3] == "sk-" and len(st.session_state.api_inp) == 51:
        st.session_state["OPENAI_API_KEY"] = st.session_state.api_inp

    st.header("Source Documents")
    st.session_state.return_source = st.checkbox(
        label="Do you want the source documents?", key="Return_source"
    )

    st.header("💡Hints")
    with st.expander("Some helpful hints on how to use StudyGPT😉"):
        st.write(
            "You can ask the bot any questions based on the materials you provided. You could even ask it to Summarize or Explain specific topics or chapters for you.\
            Here are some helpful propmts you could use to make the bot answer your questions appropriately.  \n\n"
            "1️⃣ Given the context information, can you explain what transformers are?  \n"
            "2️⃣ Summarize this topic; '{put your topic here}'. Or, Summarize chapter {chapter number}  \n"
            "3️⃣ Explain this; '{what you want it to explain goes here}' "
        )


# ---------------------------------- MAIN APP --------------------------------------------

if st.session_state.get("OPENAI_API_KEY"):
    # Instantiate the langchain class
    QA = questionAnswer(key=st.session_state.get("OPENAI_API_KEY"))

    if "QuestionAnswer" not in st.session_state:
        st.session_state.QuestionAnswer = QA

    col1, col2 = st.columns([2, 4])
    with col1:
        lottie_bot = load_lottiefile("lotties\\robot.json")
        st_lottie(lottie_bot)

    with col2:
        st.markdown("# :blue[Study]:red[GPT]")
        st.markdown("**:blue[Your Personal AI school assistant]**")

    st.subheader("Upload files for indexing")
    uploaded_file = st.file_uploader(
        ":blue[Upload your documents]", accept_multiple_files=True
    )
    doc_type = pills(
        "Is document scanned?", ["NO", "YES"], icons=["❌", "✅"], index=None
    )

    if uploaded_file:
        for file in uploaded_file:
            file_name = file.name
            if "file_name" not in st.session_state:
                st.session_state.file_name = file_name
            if doc_type == "YES":
                with open(f"scanned_docs/{file_name}", "wb") as f:
                    f.write(file.read())
                process_scanned_documents()
                extract_text()
            else:
                with open(f"docs/{file_name}", "wb") as f:
                    f.write(file.read())

    if st.button("Index Docs"):
        dir = os.listdir("docs")
        persist_dir = "+".join([os.path.basename(file)[:5] for file in dir])
        persist_dir = f"{persist_dir}_db"
        if os.path.exists(persist_dir):
            custom_notification_box(
                icon="info",
                textDisplay="Document is already Indexed!",
                externalLink="",
                url="#",
                styles=notification_styles,
            )

            with st.spinner("Loading Index..."):
                vectordb = QA.load_vectordb(persist_dir=persist_dir)
                if "vectordb" not in st.session_state:
                    st.session_state.vectordb = vectordb

        else:
            with st.spinner("Indexing your documents..."):
                vectordb = QA.create_vectordb(persist_dir=persist_dir)
                if "vectordb" not in st.session_state:
                    st.session_state.vectordb = vectordb
            custom_notification_box(
                icon="info",
                textDisplay="Done Indexing!",
                externalLink="",
                url="#",
                styles=notification_styles,
            )

    add_vertical_space(3)
    st.subheader("Interact with StudyGPT")
    # Create tabs
    tab1, tab2 = st.tabs(["Ask StudyGPT Questions", "Practice Quiz"])

    with tab1:
        if "result" not in st.session_state:
            st.session_state.result = ""

        def clear_main_query():
            if st.session_state.main_query:
                try:
                    st.session_state.result = QA.query(
                        st.session_state.main_query,
                        st.session_state.vectordb,
                        st.session_state.return_source,
                    )
                except AttributeError:
                    with alert:
                        custom_notification_box(
                            icon="warning",
                            textDisplay="Please ensure that you have indexed your documents",
                            externalLink="",
                            url="#",
                            styles=notification_styles,
                        )

            st.session_state.main_query = ""

        st.text_area(
            "Response",
            value=st.session_state.result,
            height=300,
            key="response",
            label_visibility="hidden",
        )
        add_vertical_space(1)

        alert = st.empty()
        add_vertical_space(1)
        # Display a text input widget
        st.text_input(
            ":blue[Ask StudyGPT any question]",
            placeholder="Ask questions based on your uploaded materials...",
            on_change=clear_main_query,
            key="main_query",
        )
    with tab2:
        add_vertical_space(1)
        st.write("Click the button below to go to practice session")
        want_to_practice = st.button("Take me to quiz")
        if want_to_practice:
            switch_page("Quiz")

else:
    st.markdown(
        "### Please provide your OpenAI Key to start using the application by opening the sidebar from the top left 😉"
    )
