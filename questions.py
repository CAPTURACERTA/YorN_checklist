import re


class Question:
    def __init__(self, text, coment, points=1):
        self.text = text
        self.points = int(points)
        self.coment = coment
        self.user_answer = None
        self.user_coment = None
    

    def __str__(self):
        return f'texto: "{self.text}", pontos: "{self.points}", comentario: "{self.coment}"'
    

    @classmethod
    def get_questions_list(cls, lines):
        data = []

        for match in re.finditer(r'-*>(?P<question>[^;]*);|(?P<comand>c\/o(?:n|ff))', lines):
            if question := match.group('question'): data.append(question)
            elif comand := match.group('comand'): data.append(comand)
        
        return data


    def get_question(self, question, global_coment):
        pattern = r'(?P<phrase>[^{}]*)(?:\{(?P<points>\d)?,?(?P<C>[ysn])?\})?'
        text, points, coment = re.search(pattern, question, re.IGNORECASE).group('phrase','points','C')

        if not text: raise ValueError('Not a question')
        text = re.sub(r'\s+', ' ', text).strip()
        self.text = text

        if points: self.points = points

        if coment: self.coment = True if coment.lower() in 'ys' else False
        else: self.coment = global_coment
        