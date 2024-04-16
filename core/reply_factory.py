
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(user_id, answer, current_question_id, session):

    if not answer:
        return False, "Answer cannot be empty"
    
    if "user_answers" not in session:
        session['user_answers'] = {}

    if user_id not in session['user_answers']:
        session['user_answers'][user_id] = {}

    session['user_answers'][user_id][current_question_id] = answer

    return True, ""


def get_next_question(current_question_id):
    
    PYTHON_QUESTION_LIST = [
        ("What is Python?", 1),
        ("What is the keyword to define a function?", 2),
        ("What is the result of 2 + 2?", 3),
    ]

    current_question_index = -1
    for i, (question_text, question_id) in enumerate(PYTHON_QUESTION_LIST):
        if question_id == current_question_id:
            current_question_index = i
            break

    if current_question_index != -1 and current_question_index + 1 < len(PYTHON_QUESTION_LIST):
        next_question_text, next_question_id = PYTHON_QUESTION_LIST[current_question_index + 1]
        return next_question_text, next_question_id
    else:
        return "No more questions", -1

    


def generate_final_response(session):
    
    PYTHON_QUESTION_LIST = [
        (1, "What is Python?", "Python is a programming language."),
        (2, "What is the keyword to define a function?", "def"),
        (3, "What is the result of 2 + 2?", "4"),
    ]

    user_answers = session.get('user_answers', {})

    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question_id, correct_answer, _ in PYTHON_QUESTION_LIST:
        if question_id in user_answers and user_answers[question_id] == correct_answer:
            correct_answers += 1

    score = correct_answers / total_questions * 100 if total_questions > 0 else 0
    result_message = f"You scored {correct_answers} out of {total_questions} questions. Your score: {score:.2f}%"

    return result_message
