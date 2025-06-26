import re

class Question:
    def __init__(self, text, points, coment):
        self.text = text
        self.points = int(points)
        self.coment = coment
        self.user_answer = None
        self.user_coment = None
    

    def __str__(self):
        return f'texto: "{self.text}", pontos: "{self.points}", comentario?: "{self.coment}", resposta: "{self.user_answer}", comentario: "{self.user_coment}"'
    

    #GET A QUESTION, ANSWER IF tofeedback FORMAT
    @classmethod
    def get_questions(cls, lines):
        questions = []
        global_coment = False

        for match in re.finditer(r'-*>(?P<question>[^;]*);(?P<answer>\([ra]:\s*(?P<a>[sny]),?\s*(?:c:(?P<c>[^;]*))?\);)?|(?P<comand>c\/o(?:n|ff))', lines, re.IGNORECASE):
            if question := match.group('question'): 
                try:
                    new_question = cls.create_question(question,global_coment)

                    #TOFEEDBACK ↓
                    if match.group('answer'):
                        a, c = match.group('a').lower(), match.group('c') if match.group('c') else '/'
                        new_question.answer_question(validate_answer(answer=a), c)
                    #TOFEEDBACK ↑

                    questions.append(new_question)

                except ValueError: continue
                
            elif comand := match.group('comand'): 
                global_coment = True if comand.lower() == 'c/on' else False
                 
        return questions


    #CREATE A NOT ANSWERED QUESTION {TEXT, POINTS, COMENT?}
    @classmethod
    def create_question(cls, question, global_coment):
        pattern = r'(?P<phrase>[^{}]*)(?:\{(?P<points>-?\d)?,?(?P<C>[ysn])?\})?'
        text, points, coment = re.search(pattern, question, re.IGNORECASE).group('phrase','points','C')

        if not text: raise ValueError('Not a question')
        text = re.sub(r'\s+', ' ', text).strip()

        if not points: points = 1

        if coment: coment = validate_answer(answer=coment)
        else: coment = global_coment
        
        return cls(text, points, coment)
    

    def answer_question(self, answer, coment=''):
        self.user_answer = answer
        if self.coment: 
            self.user_coment = coment.strip() if coment else input('Coment: ')
        else: self.user_coment = '/'


def validate_answer(current_question=0, answer=''):
    answer = input().strip().lower() if not answer else answer
    match answer:
        case 'y'|'s': return True
        case 'n': return False
        case '/': return '/'
        case '/back': 
            if current_question > 0: return '/back'
            else: 
                print('--No questions to go back.')
                return -1
        case _: return -1