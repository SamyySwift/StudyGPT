import streamlit as st
from utils.quiz import present_quiz, extract_questions
import os
from streamlit_extras.add_vertical_space import add_vertical_space
from utils.config import display_alert
from utils.flipbot import query
from utils.quiz import reset_quiz
from utils.config import display_animation


col1, col2 = st.columns([2, 4])
with col1:
    display_animation("lotties/quiz.json")

with col2:
    st.markdown("# :blue[Practice] :red[Quiz]")
    st.markdown("**:blue[Your personal AI examiner]**")
st.markdown(
    "**:blue[Flip]:red[Bot]** can generate both :orange[theoritical] and :red[mulitichoice] questions for you 😉 based on your provided documents. \
    It also evaluates and grades your performance after completing a quiz.  \n :blue[Psst!] You'll need to score at least :green[50%] to pass the quiz."
)

add_vertical_space(2)

try:
    return_source = st.session_state.return_source
except AttributeError:
    display_alert("Please ensure that you have indexed your documents", icon="warning")
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = ""

with st.sidebar:
    try:
        st.button("Reset Quiz", on_click=reset_quiz)
    except FileNotFoundError:
        pass


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
    ":blue[Ask FlipBot to generate practice questions for you]",
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
