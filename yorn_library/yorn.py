from .questions import Question, validate_answer
from re import findall, IGNORECASE
    

def get_yorn(lines):
    return get_yorn_answers(Question.get_questions(lines),inicialize_feedback(lines))
    

def get_tofeedback(lines):
    return get_tofeedback_answers(Question.get_questions(lines),inicialize_feedback(lines))


def get_toanswer(lines):
    return Question.get_questions(lines)


#ANSWERING (YORN) QUESTIONS ↓
def get_yorn_answers(questions, feedback):
    current_question = 0

    print(f'{'yorn'.center(120,'=')}')
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
#ANSWERING (YORN) QUESTIONS ↑


#GETTING (TOFEEDBACK) QUESTIONS ↓
def get_tofeedback_answers(questions, feedback):
    for question in questions:
        feedback = update_points(question, feedback)

    feedback['result'] = update_result(feedback)

    return questions, feedback
#GETTING (TOFEEDBACK) QUESTIONS ↑


#FEEDBACK FUNCTIONS ↓
def inicialize_feedback(lines):
    pattern = r'feedback: *(\d\d?\d?)'
    data = findall(pattern, lines, IGNORECASE)
    data = int(data[0]) if data and 0 <= int(data[0]) <= 100 else 60
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


# OUTPUT ↓
def draw_result(file, mode, questions, feedback):
    match mode:
        case 'toanswer':
            header = f'{'toanswer'.center(120,'-')}\nmode: yorn\nfeedback: 60\n\n{'questions'.center(120,'-')}'
            file.write(header)

            if not questions:
                string = '\n>{1,n};(a: c:);'
                file.write(string)
            else:
                for question in questions:
                    if question.coment:
                        string = '\n>'+question.text+'{'+str(question.points)+','+'y'+'};(a:/ c:/);'
                    else:
                        string = '\n>'+question.text+'{'+str(question.points)+'};(a:/ c:/);'
                    file.write(string)
    
        case _:
            questions = sorted(questions, key=lambda q: q.points, reverse=True)

            header = f'{feedback['result'].center(120,'-')}\npercentage: {feedback['percentage']}\ntotal points: {feedback['total_points']}\nuser points: {feedback['user_points']}\n\n'
            file.write(header)

            #yes
            file.write('"yes" questions'.center(120,'-'))
            yes_questions = [q for q in questions if q.user_answer == True]
            for yes in yes_questions:
                file.write(f'\nquestion: {yes.text}\npoints: {yes.points}\ncoment: {yes.user_coment}\n')

            #no
            file.write('\n')
            file.write('"no" questions'.center(120,'-'))
            no_questions = [q for q in questions if q.user_answer == False]
            for no in no_questions:
                file.write(f'\nquestion: {no.text}\npoints: {no.points}\ncoment: {no.user_coment}\n')

            #unanswered
            file.write('\n')
            file.write('"/" questions'.center(120,'-'))
            unanswered = [q for q in questions if q.user_answer == '/']
            for none in unanswered:
                file.write(f'\nquestion: {none.text}\npoints: {none.points}\ncoment: {none.user_coment}\n')
# OUTPUT ↑