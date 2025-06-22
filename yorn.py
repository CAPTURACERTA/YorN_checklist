import re


def main():
    with open('template.txt') as file:
        data = get_questions(''.join(file.readlines()))
        print('-=-'*20)
        print(data)

        print('---'*20)
        cleaned_questions = []
        for question in data:
            if current_question := format_questions(question):
                cleaned_questions.append(current_question) 
        print(cleaned_questions)
        print('-=-'*20)


def get_questions(lines):
    pattern = r'-*>([^;]*);'
    return re.findall(pattern, lines)


def format_questions(question):
    pattern = r'(?P<phrase>[^{}]*)(?:\{(?P<points>\d)?,?(?P<C>[ysn])?\})?'
    phrase, points, coment = re.search(pattern, question, re.IGNORECASE).group('phrase','points','C')

    if not phrase: return None
    points = int(points) if points else 1
    if not coment: coment = 'n'

    phrase = re.sub('\s+', ' ', phrase)

    return (phrase,points,coment)


if __name__ == '__main__':
    main()