#CPU.py

class CPU:
    def __init__(self, cache, io):
        self.cache = cache
        self.io = io
        self.PC = 0
        self.A = self.B = self.C = 0
    def run(self, ender):
        self.PC = ender
        self.A = self.cache.read(self.PC)
        self.PC += 1
        self.B = self.cache.read(self.PC)
        self.PC += 1
        self.C = 1
        while self.A <= self.B:
            self.cache.write(self.A, self.C)
            self.io.output(f'> {self.A} = {self.C}\n')
            self.A += 1
            self.C += 1

            
            
        


        