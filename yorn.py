from sys import argv, exit
from os import path
from questions import Question
import re


def main():
    # first_checks()

    try:
        with open('template.txt', encoding='utf-8') as file:
            lines = ''.join(file.readlines())
            questions = Question.get_questions(lines)
            feedback = get_feedback_percentage(lines)  
    except FileNotFoundError:
        print('Erro: arquivo não encontrado.')
        exit(1)
    except Exception as e:
        print(f'Erro inesperado {e}')
        exit(1)

    questions, feedback = get_answers(questions, feedback)
    # for question in questions: print(question)
    # print(feedback)



def get_feedback_percentage(lines):
    pattern = r'feedback: *(\d\d?\d?)'
    data = re.findall(pattern, lines, re.IGNORECASE)
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

    return questions, feedback


def validate_answer(current_question):
    answer = input().strip().lower()
    match answer:
        case 'y'|'s': return True
        case 'n'|'/': return False
        case '/back': 
            if current_question > 0: return '/back'
            else: 
                print('--No questions to go back.')
                return -1
        case _: return -1


def update_points(question, feedback):
    if question.points > 0:
        feedback['total_points'] = feedback.get('total_points', 0) + question.points
        if question.user_answer: feedback['user_points'] = feedback.get('user_points', 0) + question.points
    
    return feedback
#ANSWERING QUESTIONS ↑


#Checa os argumentos dado ao programa e se o arquivo "resposta.txt" já existe
def first_checks():
        if len(argv) != 3:
            print('--Exactly 2 arguments expected.\n--Ex: python yorn.py questions.txt answers.txt')
            exit(1)
        if not argv[1].lower().endswith('.txt') or not argv[2].lower().endswith('.txt'):
            print('--Both files must be in ".txt" format.')
            exit(1)
        if path.isfile(argv[2]):
            print(f'--Are you sure you want to replace the existing "{argv[2]}" file? (y/n)')
            while True:
                response = input().lower().strip()
                match response:
                    case 'y'|'s': return 0
                    case 'n': exit(0)


if __name__ == '__main__':
    main()