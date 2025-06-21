import re
import os
print(f"O diretório de trabalho atual é: {os.getcwd()}")

question_found = 0


def main():

    try:
        with open('template.txt') as template:
            question_start, question_end = 0, 0
            current_question = []
            questions = []
            global question_found

            #iterando pelas linhas
            for line in template: 
                line_left = 0
                while line_left < len(line):
                    #Se não achou pergunta, busca o início de uma pergunta
                    if question_found == 0:
                        question_start = find_question(line[line_left:], '>')
                        question_end = 0
                        if question_start: question_found = 1

                    #Se achou a pergunta, busca o fim da pergunta
                    if question_found == 1:
                        question_end = find_question(line[line_left:], ';')
                        if question_end: question_found = 0


                    #se achou o começo de uma pergunta
                    if question_start:
                        #se achou o fim da pergunta
                        if question_end:
                            #se estava em múltiplas linhas
                            if current_question:
                                current_question.append(line[:question_end.start()].strip())
                                questions.append(''.join(current_question).strip())
                                current_question = []
                            #se estava na mesma linha
                            else:
                                questions.append(line[question_start:question_end.start()].strip())
                            #resseta o começa da pergunta e procura no resto da linha
                            line_left = question_end.end()
                            question_start = 0
                            
                        #Se não achou o fim da pergunta -> tá em outra linha
                        else:
                            current_question.append(line[question_start:].strip())
                            break
                    #Se não tem começo da pergunta -> não tem pergunta
                    else:
                        break



    except FileNotFoundError:
        print('File no found.') #a entrada do programa vai ser por argumentos. 2, arv template e o nome do arquivo feedback
        return 1


#função que acha perguntas
def find_question(line, find):
    pattern = r'^-*>' if find == '>' else r'(?P<parameters>\{\d?[sn]?\})?;$'
    data = 0

    if find == '>':
        if data := re.search(pattern, line, re.IGNORECASE):
            data = data.end()
    else:
        data = re.search(pattern, line, re.IGNORECASE)
    return data if data else 0


if __name__ == '__main__':
    main()