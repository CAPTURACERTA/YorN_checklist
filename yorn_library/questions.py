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
    

    @classmethod
    def get_questions(cls, lines):
        questions = []
        global_coment = False

        for match in re.finditer(r'-*>(?P<question>[^;]*);|(?P<comand>c\/o(?:n|ff))', lines):
            if question := match.group('question'): 
                try:
                    new_question = cls.create_question(question,global_coment)
                    questions.append(new_question)
                except ValueError: continue
            elif comand := match.group('comand'): 
                global_coment = True if comand.lower() == 'c/on' else False
                 
        return questions


    @classmethod
    def create_question(cls, question, global_coment):
        pattern = r'(?P<phrase>[^{}]*)(?:\{(?P<points>-?\d)?,?(?P<C>[ysn])?\})?'
        text, points, coment = re.search(pattern, question, re.IGNORECASE).group('phrase','points','C')

        if not text: raise ValueError('Not a question')
        text = re.sub(r'\s+', ' ', text).strip()

        if not points: points = 1

        if coment: coment = True if coment.lower() in 'ys' else False
        else: coment = global_coment
        
        return cls(text, points, coment)
    

    def answer_question(self, answer):
        self.user_answer = answer
        if self.coment: self.user_coment = input('Coment: ').strip()
            