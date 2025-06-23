import re
from sys import argv, exit
from os import path
from questions import Question


def main():
    # first_checks()

    with open('template.txt') as file:
        data = Question.get_questions_list(''.join(file.readlines()))
        questions = []

        global_coment = False

        for question in data:
            if question.lower() in ['c/on','c/off']:
                global_coment = True if question.lower() == 'c/on' else False
            else:
                new_question = Question('',False)
                try:
                    new_question.get_question(question, global_coment)
                    questions.append(new_question)
                except ValueError:
                    continue

        for question in questions: print(question)


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