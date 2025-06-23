import re
from sys import argv, exit
from os import path


def main():
    first_checks()

    with open('template.txt') as file:
        questions = get_questions(''.join(file.readlines()))
        print(questions)






#Retorna as perguntas formatadas corretamente
def get_questions(lines):
    data = re.findall(r'-*>([^;]*);', lines)

    formated_questions = []
    pattern = r'(?P<phrase>[^{}]*)(?:\{(?P<points>\d)?,?(?P<C>[ysn])?\})?'

    for question in data: 
        phrase, points, coment = re.search(pattern, question, re.IGNORECASE).group('phrase','points','C')

        if phrase:
            points = int(points) if points else 1
            if not coment: coment = 'n'
            phrase = re.sub(r'\s+', ' ', phrase)
            formated_questions.append((phrase,points,coment))

    return formated_questions


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