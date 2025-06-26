from sys import argv, exit
from os import path
from re import match, IGNORECASE
from yorn_library import yorn


def main():
    # first_checks()

    try:
        with open('template.txt', encoding='utf-8') as file:
            lines = ''.join(file.readlines())
            mode = match(r'mode: *(?P<mode>yorn|regular|toanswer|tofeedback)', lines, IGNORECASE)
            if mode: mode = mode.group('mode')
            else: mode = 'yorn'
    except FileNotFoundError:
        print('Erro: arquivo não encontrado.')
        exit(1)
    except Exception as e:
        print(f'Erro inesperado {e}')
        exit(1)

    match mode:
        case 'tofeedback':
            questions, feedback = yorn.get_tofeedback(lines)
        case _: 
            questions, feedback = yorn.get_yorn(lines)
    
    for q in questions: print(q)
    print(feedback)


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