import streamlit as st
from utils.quiz import present_quiz, extract_questions
import os
from streamlit_extras.add_vertical_space import add_vertical_space

st.header(":blue[Practice]:red[Quiz]")
add_vertical_space(3)

try:
    QA = st.session_state.QuestionAnswer
    return_source = st.session_state.return_source
except AttributeError:
    st.error("Please ensure that you have indexed your documents")

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = ""


def clear_quiz_query():
    if st.session_state.quiz_query:
        try:
            st.session_state.quiz_questions = QA.query(
                st.session_state.quiz_query,
                st.session_state.vectordb,
                st.session_state.return_source,
            )
            with open("questions.txt", "w") as f:
                f.write(st.session_state.quiz_questions)
        except AttributeError:
            # reset_quiz(length=len(questions))
            st.warning("Please ensure that you have indexed your documents")

    st.session_state.quiz_query = ""


st.text_input(
    ":blue[Ask StudyGPT to generate practice questions for you]",
    placeholder="",
    key="quiz_query",
    on_change=clear_quiz_query,
)


if os.path.exists("questions.txt"):
    questions = extract_questions("questions.txt")
    present_quiz(QA, questions)
