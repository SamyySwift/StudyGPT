import streamlit as st
import os
import re


def evaluate_response(query, questions, responses):
    correct_answers = {}
    num_correct = 0

    if "correct_answers" not in st.session_state:
        st.session_state.correct_answers = correct_answers
    if "num_correct" not in st.session_state:
        st.session_state.num_correct = num_correct

    for i in range(len(questions)):
        # Specify the prompt for the GPT model
        prompt = f"""Given this Question: {questions[i]} and the Response: {responses[i]}, \
                            Return True if the response is correct compared to the actual answer and return False if the response is \
                            incorrect followed by the correct answer.

                            for example:
                            
                            True
                            False, followed up by the correct answer
                            """
        # Use the GPT model to generate feedback on the student's response
        feedback = query(prompt, st.session_state.vectordb)

        if "True" in feedback:
            st.session_state.num_correct += 1
        elif "False" in feedback or "No" in feedback:
            correct_answers[questions[i]] = feedback

    score = round((st.session_state.num_correct / len(questions)) * 100, 2)

    return score, correct_answers


def delete_question():
    os.remove("questions.txt")


def clear_fields():
    st.session_state.response = st.session_state.txt_inp
    st.session_state.response = st.session_state.txt
    st.session_state.txt_inp = ""
    st.session_state.txt = ""


def reset_quiz(length):
    delete_question()
    st.session_state.response = ""
    st.session_state.user_responses = [0] * length
    st.session_state.count = 0


def extract_questions(file_path):
    questions = []
    current_question = ""

    with open(file_path, "r") as file:
        lines = file.readlines()

        # Skip empty lines at the beginning of the file
        while lines and not lines[0].strip():
            lines.pop(0)

        for line in lines:
            line = line.strip()

            # Check if the line starts with a number followed by a dot
            if re.match(r"^[Q\d]+\.", line):
                # If there is a current question, add it to the list
                if current_question:
                    questions.append(current_question.strip())

                # Start a new question
                current_question = line
            else:
                # Append the line to the current question
                current_question += " " + line

        # Add the last question to the list
        if current_question:
            questions.append(current_question.strip())

    return questions


def present_quiz(query, questions):
    length = len(questions)
    count = 0
    user_responses = [0] * length

    if "count" not in st.session_state:
        st.session_state.count = count
    if "response" not in st.session_state:
        st.session_state.response = ""
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = user_responses

    # Placeholder for question counter
    quest_counter_plc = st.empty()
    with quest_counter_plc:
        st.markdown(f"#### Question {st.session_state.count+1}/{length}")

    placeholder = st.empty()

    with placeholder.container():
        st.write(questions[0])
        st.text_input(
            "Provide your answer",
            key="txt_inp",
            on_change=clear_fields,
            placeholder="Provide your answer",
            label_visibility="hidden",
        )
        try:
            if st.session_state.count != length:
                if st.session_state.response:
                    st.session_state.user_responses[
                        st.session_state.count
                    ] = st.session_state.response

                    st.session_state.response = ""

                _, col4, col5 = st.columns([8, 3, 11])
                with col4:
                    bt_plc1 = st.empty()
                    with bt_plc1:
                        if st.button("Prev") and st.session_state.count != 0:
                            st.session_state.count -= 1

                with col5:
                    bt_plc2 = st.empty()
                    with bt_plc2:
                        if st.button("Next"):
                            st.session_state.count += 1
                    with quest_counter_plc:
                        st.markdown(f"### Question {st.session_state.count+1}/{length}")

                with placeholder.container():
                    st.markdown(questions[st.session_state.count])
                    st.text_input(
                        "Provide your answer",
                        key="txt",
                        on_change=clear_fields,
                        placeholder="Provide your answer",
                        label_visibility="hidden",
                    )
        except:
            with quest_counter_plc:
                st.empty()
            with placeholder.container():
                st.empty()
                with bt_plc1:
                    st.empty()
                with bt_plc2:
                    st.empty()
                with st.spinner(":blue[Flip]:red[Bot] is evaluating your responses..."):
                    score, answers = evaluate_response(
                        query, questions, st.session_state.user_responses
                    )

            st.success("Done evaluating...")

            with placeholder.container():
                st.subheader(":blue[Your Performance]")
                if score >= 50:
                    st.write(f":blue[GRADE:] :green[{score}%]")
                    st.write("✅Congratulations!!! You **:green[passed!🎉]**")

                else:
                    st.write(f":blue[GRADE:] :red[{score}%]")
                    st.write("Unfortunately, you **:red[failed!😔]**")

                st.write("###")
                st.subheader(":blue[Corrections]")
                st.write("Below are the correct answers to the ones you got wrong")
                st.markdown("---")
                # display the questions
                for q, a in answers.items():
                    st.write(q)
                    st.write(f":green[Correct Answer: {a}]")

                st.button("Reset Quiz", on_click=reset_quiz(length))
