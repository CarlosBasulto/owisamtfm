class Engine:
    def __init__(self, modules):
        self.modules = modules

    def execute(self, data):
        for module in self.modules:
            print(f"[+] Ejecutando módulo: {module.name}")
            data = module.run(data)
        return data