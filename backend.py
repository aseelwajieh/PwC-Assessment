import openai
from dotenv import load_dotenv, dotenv_values
from langchain.llms import OpenAI
import os

load_dotenv()
key = os.getenv('OPENAI_API_KEY')


def generate_questions(user_input, num_of_questions):
    if num_of_questions == 1:
        response = openai.chat.completions.create(

            messages=[
                {
                    "role": "user",
                    "content": f"Create 1 MCQs about {user_input},without displaying the right answer",
                }
            ],
            model="gpt-3.5-turbo",
        )

        return response.choices[0].message.content
    else:
        response = openai.chat.completions.create(

            messages=[
                {
                    "role": "user",
                    "content": f"Create {num_of_questions} MCQs with 4 choices about {user_input},without displaying the right answer",
                }
            ],
            model="gpt-3.5-turbo",
        )

        return response.choices[0].message.content


def get_correct_answer(lm_input):
    return OpenAI(temperature=0)(lm_input).strip()


def evaluate_answers(questions, user_answers):
    question_list = questions.strip().split("\n")
    result_dict = {}
    score = 0

    for i in range(0, len(question_list), 6):
        question = question_list[i]
        answers = question_list[i + 1:i + 5]

        lm_input = (f"Which of these answers {answers} is the correct answer for that question {question}, "
                    f"just give me the answer alone")

        correct_answer = get_correct_answer(lm_input)

        user_answer = user_answers[i // 6].strip().lower()  # Access the correct user answer for the current question

        result_dict[i // 6] = {
            'Question': question,
            'Your Answer': user_answer,
            'Correct Answer': correct_answer,
            'Rating': "You've selected the correct answer. Good job!!" if user_answer.lower() == correct_answer.lower() else "You've selected the wrong answer.",
            'Score': f"{score + 1} / {len(result_dict) + 1}" if user_answer.lower() == correct_answer.lower() else f"{score} / {len(result_dict) + 1}"
        }

        if user_answer.lower() == correct_answer.lower():
            score += 1

    return result_dict


# Example usage
questions = "..."
user_answers = ["...", "...", "...", "..."]  # Make sure this list matches the number of questions
evaluation_result = evaluate_answers(questions, user_answers)
print(evaluation_result)

# def evaluate_answers(questions, user_answers):
#     llm = OpenAI(temperature=0)
#
#     question_list = questions.strip().split("\n")
#
#     result_dict = {}
#     j = 0
#     score = 0
#     correct_answers = []  # Create a new list for each question
#
#     for i in range(0, len(question_list), 6):
#         question = question_list[i]
#
#         answers = question_list[i + 1:i + 5]
#
#         lm_input = (f"Which of these answers {answers} is the correct answer for that question {question},just give me "
#                     f"the answer alone")
#
#         correct_answer = llm(lm_input).strip()
#         print(f"correct answerrss {correct_answer}")
#         correct_answers.append(correct_answer)
#         print(f"lissttts {correct_answers}")
#
#         for user_answer in user_answers:
#             if user_answer.strip().lower() == correct_answer.strip().lower():
#                 score += 1
#
#         result_dict[j] = {
#             'Question': question,
#             'Your Answer': user_answers[j],  # Access the correct user answer for the current question
#             'Correct Answer': correct_answer,
#             'Rating': "You've selected the correct answer. Good job!!" if user_answers[
#                                                                               j].strip() == correct_answer.strip() else "You've selected the wrong answer.",
#             'Score': f"{score} / {len(correct_answers)}"
#         }
#         print(f"dict {result_dict}")
#
#         j += 1
#
#     print(f"dict {result_dict}")
#     return result_dict
