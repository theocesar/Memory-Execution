#Main.py
import sys

from es import IO
from RAM import RAM
from CPU import CPU
from Cache import CacheSimples
from Memoria import EnderecoInvalido

try:
	io = IO()
	ram = RAM(22)   # 4M de RAM (2**22)
	cache = CacheSimples(4 * 2**10, 64, ram)  # total cache = 4K, cacheline = 64 
	cpu = CPU(cache, io)

	inicio = 0

	print("Programa 1:\n")
	ram.write(inicio, 118)
	ram.write(inicio+1, 130)
	cpu.run(inicio)

	print("\n\nPrograma 2:\n")
	cache.write(inicio, 4155)
	cache.write(inicio+1, 4165)
	cpu.run(inicio)
except EnderecoInvalido as e:
	print("Endereco inválido:", e.ender, file=sys.stderr)
sys.exit(1)
    