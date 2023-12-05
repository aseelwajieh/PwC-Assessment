import openai
from dotenv import load_dotenv
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
                    "content": f"Create {num_of_questions} MCQs with 4 choices about {user_input},without displaying the right answer,the choices must contain the right answer of thr quiz",
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

        user_answer = user_answers[i // 6].strip().lower()

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


