from Memoria import Memoria
import math

class CacheLine:
    def __init__(self, tamanho_linha):
        self.tag = None
        self.modificado = 0
        self.data = [0] * tamanho_linha

class CacheSimples(Memoria):
    def __init__(self, capacidade_cache, tamanho_linha, ram):
        super().__init__(capacidade_cache)
        self.capacidade_cache = capacidade_cache
        self.tamanho_linha = tamanho_linha
        self.ram = ram
        self.cache = [CacheLine(tamanho_linha) for _ in range(capacidade_cache // tamanho_linha)]

    # Método responsável por calcular w, r, t e s
    def calcular_wrt(self, endereco):
        w_bits = int(math.log2(self.tamanho_linha))
        r_bits = int(math.log2(self.capacidade_cache // self.tamanho_linha))
        t_bits = max(endereco.bit_length() - (w_bits + r_bits), 0)
        w = endereco & ((1 << w_bits) - 1)
        r = (endereco >> w_bits) & ((1 << r_bits) - 1)
        t = (endereco >> (w_bits + r_bits)) & ((1 << t_bits) - 1)
        s = (t << r) | r
        return w, r, t, s

    # Método responsável pela leitura dos dados na cache
    def read(self, endereco):
        w, r, t, s = self.calcular_wrt(endereco)
        cache_line = self.cache[r]
        if cache_line.tag == t:
            return cache_line.data[w]
        else:
            print(f"MISS: {endereco} -> L{r}")
            if cache_line.modificado != 0:
                self.CacheParaRAM(cache_line, r)
            self.RAMParaCache(s, t, r)
            return cache_line.data[w]

    # Método responsável pela escrita dos dados na cache
    def write(self, endereco, valor):
        w, r, t, s = self.calcular_wrt(endereco)
        cache_line = self.cache[r]
        if cache_line.tag == t:
            cache_line.data[w] = valor
            cache_line.modificado = 1
        else:
            print(f"MISS: {endereco} -> L{r}")
            if cache_line.modificado != 0:
                self.CacheParaRAM(cache_line, r)
            self.RAMParaCache(s, t, r)
            cache_line.data[w] = valor
            cache_line.tag = t
            cache_line.modificado = 1

    # Método responsável por enviar uma linha da cache de volta para a RAM
    def CacheParaRAM(self, cache_line, s):
        if cache_line.modificado:
            index_ram = s * (self.capacidade_cache // self.tamanho_linha)
            for w, valor in enumerate(cache_line.data):
                self.ram.write(index_ram + w, valor)
            cache_line.modificado = 0
    
    # Método responsável por copiar um bloco da RAM e trazer para a cache
    def RAMParaCache(self, s, t, r):
        cache_line = self.cache[r]
        index_ram = s * (self.capacidade_cache // self.tamanho_linha)
        for w in range(self.tamanho_linha):
            valor = self.ram.read(index_ram + w)
            cache_line.data[w] = valor
        cache_line.tag = t
        cache_line.modificado = 0
