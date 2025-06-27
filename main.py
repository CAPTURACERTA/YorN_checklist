from sys import argv, exit
from os import path
from re import search, IGNORECASE
from yorn_library import yorn


def main():
    first_checks()

    try:
        with open(argv[1], encoding='utf-8') as file:
            lines = ''.join(file.readlines())
            if mode := search(r'mode: *(?P<mode>yorn|toanswer|tofeedback)', lines, IGNORECASE):
                mode = mode.group('mode').lower()
            else: mode = 'yorn'
    except FileNotFoundError:
        print('--Error: questions file not found.')
        exit(1)
    except Exception as e:
        print(f'--Unexpected error: {e}')
        exit(1)

    questions = []
    feedback = {}

    match mode:
        case 'yorn': 
            questions, feedback = yorn.get_yorn(lines)
        case 'tofeedback':
            questions, feedback = yorn.get_tofeedback(lines)
        case 'toanswer':
            questions = yorn.get_toanswer(lines)       
    
    try:
        with open(argv[2], 'w', encoding='utf-8') as file:
            yorn.draw_result(file, mode, questions, feedback)
    except Exception as e:
        print(f'--Unexpected error: {e}')
        exit(1)
        

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