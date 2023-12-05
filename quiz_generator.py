import streamlit as st
from streamlit.runtime.state import session_state
from backend import *

if 'generate' not in st.session_state:
    st.session_state.generate = False

if 'submit_quiz' not in st.session_state:
    st.session_state.submit_quiz = False

if 'generated_answers' not in st.session_state:
    st.session_state.generated_answers = False


def callback():
    st.session_state.generate = True


def stop():
    st.session_state.submit_quiz = True


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


# def main():
#     answers = []
#     user_input = st.text_input("What is your interest?")
#     num_of_questions = st.number_input("How many Questions you'd like to be asked?",
#                                        placeholder="Enter a number...",
#                                        value=None)
#     generate_quiz = st.checkbox("Take Quiz")
#     passed = False
#
#     if generate_quiz:
#         if validate_input(user_input, num_of_questions):
#             questions = generate_questions(user_input, num_of_questions)
#             with st.form("Quiz"):
#                 answers = create_quiz(questions)
#                 quiz_submitted = st.form_submit_button("Submit Quiz")
#                 if quiz_submitted:
#                     evaluated_answers = evaluate_answers(questions, answers)
#                     st.write("Quiz Results:")
#                     for key, result in evaluated_answers.items():
#                         st.write(f"**Question {key + 1}:** {result['Question']}")
#                         st.write(f"Your Answer: {result['Your Answer']}")
#                         st.write(f"Correct Answer: {result['Correct Answer']}")
#                         st.write(f"Rating: {result['Rating']}")
#                         st.write(f"Your score is : {result['Score']}")
#                         st.write("")

import streamlit as st

# def main():
#     if 'question_index' not in st.session_state:
#         st.session_state.question_index = 0
#
#     user_input = st.text_input("What is your interest?")
#     num_of_questions = st.number_input("How many questions would you like to be asked?",
#                                        placeholder="Enter a number...",
#                                        value=None)
#     generate_quiz = st.button("Take Quiz")
#
#     if generate_quiz or st.session_state.generate:
#         st.session_state.generate = True
#         questions = generate_questions(user_input, num_of_questions)
#
#         if st.session_state.question_index < num_of_questions:
#             with st.form("Quiz"):
#                 user_answer = create_quiz(questions, st.session_state.question_index)
#                 quiz_submitted = st.form_submit_button("Proceed to Next Question")
#
#                 if quiz_submitted:
#                     st.session_state.question_index += 1
#
#                     if st.session_state.question_index == num_of_questions:
#                         st.session_state.generate = False  # End the quiz after the last question
#
#         else:
#             st.write("Quiz Completed!")
#             st.session_state.generate = False  # Reset the session state for the next quiz

# def main():
#     st.title("Quiz App")
#
#     if "questions" not in st.session_state:
#         st.session_state.questions = ""
#     if "answers" not in st.session_state:
#         st.session_state.answers = ""
#
#     user_input = st.text_input("What is your interest?")
#     num_of_questions = st.number_input("How many Questions you'd like to be asked?",
#                                        placeholder="Enter a number...",)
#     generate_quiz = st.button("Take Quiz")
#
#     if generate_quiz or st.session_state.generate:
#             st.session_state.questions = generate_questions(user_input, num_of_questions)
#             st.session_state.answers = ""
#             if validate_input(user_input,num_of_questions):
#                 st.session_state.generate = True
#
#
#                 with st.form("Quiz"):
#                     if not st.session_state.answers:
#                         st.session_state.answers = create_quiz(st.session_state.questions)
#
#                     quiz_submitted = st.form_submit_button("Submit Quiz")
#                     if quiz_submitted:
#                         evaluated_answers = evaluate_answers(st.session_state.questions, st.session_state.answers)
#                         st.write("Quiz Results:")
#                         for key, result in evaluated_answers.items():
#                             st.write(f"**Question {key + 1}:** {result['Question']}")
#                             st.write(f"Your Answer: {result['Your Answer']}")
#                             st.write(f"Correct Answer: {result['Correct Answer']}")
#                             st.write(f"Rating: {result['Rating']}")
#                             st.write(f"Your score is : {result['Score']}")
#                             st.write("")

import streamlit as st


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
                # if not st.session_state.answers:
                #     st.session_state.answers += create_quiz(st.session_state.questions)
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

# def main():
#     st.title("Quiz App")
#
#     if "questions" not in st.session_state:
#         st.session_state.questions = ""
#     if "answers" not in st.session_state:
#         st.session_state.answers = ""
#     if "user_input" not in st.session_state:
#         st.session_state.user_input = ""
#     if "num_of_questions" not in st.session_state:
#         st.session_state.num_of_questions = 0
#
#     user_input = st.text_input("What is your interest?", value=st.session_state.user_input)
#     num_of_questions = st.number_input("How many Questions you'd like to be asked?",
#                                        placeholder="Enter a number...",
#                                        value=st.session_state.num_of_questions)
#     generate_quiz = st.button("Take Quiz")
#
#     if generate_quiz or st.session_state.generate:
#         st.session_state.generate = True
#         if user_input != st.session_state.user_input or num_of_questions != st.session_state.num_of_questions:
#             st.session_state.user_input = user_input
#             st.session_state.num_of_questions = num_of_questions
#             st.session_state.questions = generate_questions(user_input, num_of_questions)
#             st.session_state.answers = ""
#         if validate_input(user_input, num_of_questions):
#             with st.form("Quiz"):
#                 if not st.session_state.answers:
#                     st.session_state.answers = create_quiz(st.session_state.questions)
#
#                 quiz_submitted = st.form_submit_button("Submit Quiz")
#                 if quiz_submitted:
#                     evaluated_answers = evaluate_answers(st.session_state.questions, st.session_state.answers)
#                     st.write("Quiz Results:")
#                     for key, result in evaluated_answers.items():
#                         st.write(f"**Question {key + 1}:** {result['Question']}")
#                         st.write(f"Your Answer: {result['Your Answer']}")
#                         st.write(f"Correct Answer: {result['Correct Answer']}")
#                         st.write(f"Rating: {result['Rating']}")
#                         st.write(f"Your score is : {result['Score']}")
#                         st.write("")
#
#
# if __name__ == "__main__":
#     main()

# global questions
# with st.form("Generate Quiz"):
#     user_input = st.text_input("What is your interest?")
#     num_of_questions = st.number_input("How many Questions you'd like to be asked?",
#                                        placeholder="Enter a number...",
#                                        value=None)
#     generate_quiz = st.form_submit_button("Take Quiz")
# if generate_quiz:
#     if validate_input(user_input, num_of_questions):
#         questions = generate_questions(user_input, num_of_questions)
#         print("Generated Questions:", questions)
#     with st.form("Quiz"):
#         answers = create_quiz(questions)
#         quiz_submitted = st.form_submit_button(label="Submit Quiz")
#         print(f"submitted {quiz_submitted}")
#         if quiz_submitted:
#             print("here")
#
#             # Call backend to evaluate answers
#             correct_answers = evaluate_answers(questions, answers)
#             print("Correct Answers:", correct_answers)
#
#             # Display results
#             st.write("Quiz Results:")
#             for i in range(len(questions)):
#                 st.write(f"Question {i + 1}: {questions[i]}")
#                 st.write(f"Your Answer: {answers[i]}")
#                 st.write(f"Correct Answer: {correct_answers[i]}")
#                 st.write(f"Result: {'Correct' if correct_answers[i] == answers[i] else 'Incorrect'}")
#                 st.write("---")

# with st.form("Quiz"):
#     answer = create_quiz(questions)
#     quiz_submitted = st.form_submit_button("Submit Quiz")
#     if quiz_submitted:
#         correct_answers = evaluate_answers(questions, answer)
#         print("Correct Answers:", correct_answers)
# for i in range(len(questions)):
#     st.write(f"Question {i + 1}: {questions[i]}")
#     st.write(f"Your Answer: {answer[i]}")
#     st.write(f"Correct Answer: {correct_answers[i]}")
#     st.write(f"Result: {'Correct' if correct_answers[i] == answer[i] else 'Incorrect'}")
#     st.write("---")
