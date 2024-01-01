from abc import abstractmethod

class Memoria:
  def __init__(self, capacidade):
    self._capacidade = capacidade
    
  def verifica_endereco(self, ender):
    if (ender < 0) or (ender >= self._capacidade):
      raise EnderecoInvalido(ender)
    
  def tamanho(self):
      return self._capacidade
    
  @abstractmethod
  def read(self, ender):
      pass
    
  @abstractmethod
  def write(self, ender, val):
      pass


class EnderecoInvalido(Exception):
    
    def __init__(self, ender):
        self.ender = ender

    def __str__(self):
        return str(self.ender)