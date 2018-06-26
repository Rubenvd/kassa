import notecount

class EindRekening:
    def __init__(self):
        self.check = []

    def add_rekening(self, rekening):
        self.check.append(rekening)

    def get_rekening(self):
        return self.check