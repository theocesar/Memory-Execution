#es.py

import sys

class IO:
    def __init__(self, entrada = sys.stdin, saida=sys.stdout):
        self.entrada = entrada
        self.saida = saida
    def output(self, s):
        print(s, end='', file=self.saida)

