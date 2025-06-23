import re


def main():
    with open('template.txt') as file:
        questions = get_questions(''.join(file.readlines()))
        print(questions)


def get_questions(lines):
    data = re.findall(r'-*>([^;]*);', lines)

    formated_questions = []
    pattern = r'(?P<phrase>[^{}]*)(?:\{(?P<points>\d)?,?(?P<C>[ysn])?\})?'

    for question in data: 
        phrase, points, coment = re.search(pattern, question, re.IGNORECASE).group('phrase','points','C')

        if phrase:
            points = int(points) if points else 1
            if not coment: coment = 'n'
            phrase = re.sub('\s+', ' ', phrase)
            formated_questions.append((phrase,points,coment))

    return formated_questions


if __name__ == '__main__':
    main()