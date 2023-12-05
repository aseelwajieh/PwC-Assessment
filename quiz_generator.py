import streamlit as st
from backend import *

if 'generate' not in st.session_state:
    st.session_state.generate = False


def validate_input(user_input, num_of_questions):
    valid = True
    if user_input == "":
        st.error("You entered an invalid input. Try again.")
        valid = False

    if num_of_questions <= 0:
        st.error("You entered an invalid number of questions. Try again.")
        valid = False

    return valid


def create_quiz(generated_questions):
    generated_questions = generated_questions.strip().split("\n")
    # st.write(f"len {generated_questions}")
    i = 0
    answers = []
    while i < len(generated_questions):
        if generated_questions[i + 1] == '':
            answer = st.radio(generated_questions[i],
                              [generated_questions[i + 2], generated_questions[i + 3], generated_questions[i + 4],
                               generated_questions[i + 5]]
                              )
            answers.append(answer)
            i = i + 7
        else:
            answer = st.radio(generated_questions[i],
                              [generated_questions[i + 1], generated_questions[i + 2], generated_questions[i + 3],
                               generated_questions[i + 4]]
                              )
            answers.append(answer)

            i = i + 6

    return answers


def main():
    st.title("Quiz App")

    if "questions" not in st.session_state:
        st.session_state.questions = ""
    if "answers" not in st.session_state:
        st.session_state.answers = []  # Initialize as an empty list
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "num_of_questions" not in st.session_state:
        st.session_state.num_of_questions = 0

    user_input = st.text_input("What is your interest?", value=st.session_state.user_input)
    num_of_questions = st.number_input("How many questions would you like to be asked?",
                                       placeholder="Enter a number...",
                                       value=st.session_state.num_of_questions)
    generate_quiz = st.button("Take Quiz")

    if generate_quiz or st.session_state.generate:
        st.session_state.generate = True
        if user_input != st.session_state.user_input or num_of_questions != st.session_state.num_of_questions:
            st.session_state.user_input = user_input
            st.session_state.num_of_questions = num_of_questions
            st.session_state.questions = generate_questions(user_input, num_of_questions)
            st.session_state.answers = []  # Reset answers to an empty list
        if validate_input(user_input, num_of_questions):
            with st.form("Quiz"):
                answers = create_quiz(st.session_state.questions)
                quiz_submitted = st.form_submit_button("Submit Quiz")
                if quiz_submitted:
                    evaluated_answers = evaluate_answers(st.session_state.questions, answers)
                    st.write("Quiz Results:")
                    for key, result in evaluated_answers.items():
                        st.write(f"**Question {key + 1}:** {result['Question']}")
                        st.write(f"Your Answer: {result['Your Answer']}")
                        st.write(f"Correct Answer: {result['Correct Answer']}")
                        st.write(f"Rating: {result['Rating']}")
                        st.write(f"Your score is : {result['Score']}")
                        st.write("")


if __name__ == "__main__":
    main()


