from Memoria import Memoria
import math

class CacheSimples(Memoria):
    def __init__(self, capacidade_cache, tamanho_linha, ram):
        super().__init__(capacidade_cache)
        self.capacidade_cache = capacidade_cache
        self.tamanho_linha = tamanho_linha
        self.ram = ram
        self.cache = [0] * (capacidade_cache // tamanho_linha)
        self.modificada = 0

    # Metódo responsável por calcular w, r, t e s
    def calcular_wrt(self, endereco):
        w_bits = int(math.log2(self.tamanho_linha))
        r_bits = int(math.log2(self.capacidade_cache // self.tamanho_linha))
        t_bits = max(endereco.bit_length() - (w_bits + r_bits), 0)
        w = endereco & (1 << w_bits) - 1
        r = (endereco >> w_bits) & (1 << r_bits) - 1
        t = (endereco >> (w_bits + r_bits)) & (1 << t_bits) - 1
        s = (t << r) | r
        return w, r, t, s

    # Metódo responsável pela leitura dos dados na cache
    def read(self, endereco):
        w, r, t, s = self.calcular_wrt(endereco)
        if self.cache[r] != 0 and self.cache[r][0] == t:
            return self.cache[r][1][w]
        else:
            print(f"MISS: {endereco} -> L{r}")
            if self.modificada != 0:
                self.CacheParaRAM(self.cache[r])  
            self.RAMParaCache(r, t, s)  
            return self.cache[r][1][w]

    # Metódo responsável pela escrita dos dados na cache
    def write(self, endereco, valor):
        w, r, t, s = self.calcular_wrt(endereco)
        if self.cache[r] != 0 and self.cache[r][0] == t:
            self.cache[r][1][w] = valor
            self.modificada = 1 
        else:
            print(f"MISS: {endereco} -> L{r}")
            if self.modificada != 0:
                self.CacheParaRAM(self.cache[r])
            self.RAMParaCache(r, t, s)  
            self.cache[r][1][w] = valor 
            self.modificada = 1

    # Metódo responsável por mandar uma linha da cache de volta para a RAM
    def CacheParaRAM(self, linha_cache):
        if linha_cache != 0:
            tag, dados = linha_cache
            w, r, t, s = self.calcular_wrt(tag)
            index_ram = s * (self.capacidade_cache // len(self.cache))
            for w, valor in enumerate(dados):
                self.ram.write(index_ram + w, valor)

    # Metódo responsável por copiar um bloco da RAM e trazer para a cache
    def RAMParaCache(self, r, t, s):
        dados = []
        index_ram = s * (self.capacidade_cache // len(self.cache))
        for w in range(self.tamanho_linha):
            valor = self.ram.read(index_ram + w)
            dados.append(valor)
        self.cache[r] = (t, dados)