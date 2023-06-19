import streamlit as st
from utils.quiz import present_quiz, extract_questions
import os
from streamlit_extras.add_vertical_space import add_vertical_space
from utils.config import display_alert
from utils.flipbot import query


st.header(":blue[Practice] :red[Quiz]")
st.markdown(
    "**:blue[Flip]:red[Bot]** can generate both :orange[theoritical] and :red[mulitichoice] questions for you 😉 based on your provided documents. \
    It also evaluates and grades your performance after completing a quiz.  \n :blue[Psst!] You'll need to score at least :green[50%] to pass the quiz."
)
st.markdown("---")
add_vertical_space(1)

try:
    return_source = st.session_state.return_source
except AttributeError:
    display_alert("Please ensure that you have indexed your documents", icon="warning")
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = ""


def clear_quiz_query():
    if st.session_state.quiz_query:
        try:
            st.session_state.quiz_questions = query(
                st.session_state.quiz_query,
                st.session_state.vectordb,
                st.session_state.return_source,
            )
            with open("questions.txt", "w") as f:
                f.write(st.session_state.quiz_questions)
        except AttributeError:
            # reset_quiz(length=len(questions))
            display_alert(
                "Please ensure that you have indexed your documents", icon="warning"
            )

    st.session_state.quiz_query = ""


st.text_input(
    ":blue[Ask StudyGPT to generate practice questions for you]",
    placeholder="",
    key="quiz_query",
    on_change=clear_quiz_query,
)


if os.path.exists("questions.txt"):
    questions = extract_questions("questions.txt")
    try:
        present_quiz(query, questions)
    except NameError:
        display_alert("Go to home page to start app again")
