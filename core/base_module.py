class BaseModule:
    def __init__(self, name):
        self.name = name

    def run(self, data):
        raise NotImplementedError("Implement run() en el módulo")