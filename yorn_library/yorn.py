from .questions import Question
from re import findall, IGNORECASE
    

def get_yorn(lines):
    return get_answers(Question.get_questions(lines),get_feedback_percentage(lines))
    

def get_feedback_percentage(lines):
    pattern = r'feedback: *(\d\d?\d?)'
    data = findall(pattern, lines, IGNORECASE)
    return {'percentage':int(data[0])} if data and 0 <= int(data[0]) <= 100 else {'percentage':60}
    

#ANSWERING QUESTIONS ↓
def get_answers(questions, feedback):
    current_question = 0

    feedback['total_points'] = feedback.get('total_points', 0)
    feedback['user_points'] = feedback.get('user_points', 0)

    while current_question < len(questions):
        print(f'->{questions[current_question].text} (y/n)')
        while True:
            answer = validate_answer(current_question)
            if answer != -1: break
        
        if answer == '/back': current_question -= 1
        else:
            questions[current_question].answer_question(answer)
            feedback = update_points(questions[current_question], feedback)
            current_question += 1

    if feedback['user_points'] >= round((feedback['percentage'] * feedback['total_points']) / 100):
        feedback['result'] = 'SUCCESS'
    else:
        feedback['result'] = 'FAILURE' 

    return questions, feedback


def validate_answer(current_question):
    answer = input().strip().lower()
    match answer:
        case 'y'|'s': return True
        case 'n': return False
        case '/': return '/'
        case '/back': 
            if current_question > 0: return '/back'
            else: 
                print('--No questions to go back.')
                return -1
        case _: return -1


def update_points(question, feedback):
    if question.points > 0:
        feedback['total_points'] = feedback.get('total_points', 0) + question.points
    if question.user_answer and question.user_answer != '/':
        feedback['user_points'] = feedback.get('user_points', 0) + question.points 
    
    return feedback
#ANSWERING QUESTIONS ↑

