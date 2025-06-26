from .questions import Question, validate_answer
from re import findall, IGNORECASE
    

def get_yorn(lines):
    return get_yorn_answers(Question.get_questions(lines),inicialize_feedback(lines))
    

def get_tofeedback(lines):
    return get_tofeedback_answers(Question.get_questions(lines),inicialize_feedback(lines))

#ANSWERING YORN QUESTIONS ↓
def get_yorn_answers(questions, feedback):
    current_question = 0

    while current_question < len(questions):
        print(f'->{questions[current_question].text} (y/n)')
        while True:
            answer = validate_answer(current_question=current_question)
            if answer != -1: break
        
        if answer == '/back': current_question -= 1
        else:
            questions[current_question].answer_question(answer)
            feedback = update_points(questions[current_question], feedback)
            current_question += 1

    feedback['result'] = update_result(feedback)

    return questions, feedback
#ANSWERING YORN QUESTIONS ↑


#GETTING TOFEEDBACK QUESTIONS ↓
def get_tofeedback_answers(questions, feedback):
    for question in questions:
        feedback = update_points(question, feedback)

    feedback['result'] = update_result(feedback)

    return questions, feedback
#GETTING TOFEEDBACK QUESTIONS ↑


#FEEDBACK FUNCTIONS ↓
def inicialize_feedback(lines):
    pattern = r'feedback: *(\d\d?\d?)'
    data = findall(pattern, lines, IGNORECASE)
    data = int(data) if data and 0 <= int(data[0]) <= 100 else 60
    return {'percentage':data,'total_points':0,'user_points':0,'result':None}


def update_points(question, feedback):
    if question.points > 0:
        feedback['total_points'] = feedback.get('total_points', 0) + question.points
    if question.user_answer and question.user_answer != '/':
        feedback['user_points'] = feedback.get('user_points', 0) + question.points 
    
    return feedback


def update_result(feedback):
    result = ''
    if feedback['user_points'] >= round((feedback['percentage'] * feedback['total_points']) / 100):
         result = 'SUCCESS'
    else:
        result = 'FAILURE' 
    return result
#FEEDBACK FUNCTIONS ↑