import re


def main():
    with open('template.txt') as file:
        data = get_questions(''.join(file.readlines()))

        cleaned_questions = []
        for question in data:
            cleaned_questions.append(clean_questions(question))


def get_questions(lines):
    pattern = r'-*>[^;]*;'
    return re.findall(pattern, lines)


def clean_questions(question):
    s = re.sub(r'-*>|;', '', question).strip()
    return re.sub(r'\s+', ' ', s)


if __name__ == '__main__':
    main()