from typing import List
# Clase de pregunta
class Pregunta():
	def __init__(self, id: int, enunciado: str, respuestas: List[str], correcta: int):
		self.__id = id
		self.__enunciado = enunciado
		self.__respuestas = respuestas
		self.__correcta = correcta

	# Métodos get/set
	def get_id(self):
		return self.__id

	def get_enunciado(self):
		return self.__enunciado

	def get_respuestas(self):
		return self.__respuestas

	def get_correcta(self):
		return self.__correcta

	# Override método equal
	def __eq__(self, otra):
		return (self.__id == otra.get_id()) and (self.__enunciado == otra.get_enunciado()) and (self.__respuestas == otra.get_respuestas()) and (self.__correcta == otra.get_correcta())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'id': self.get_id(), 'enunciado': self.get_enunciado(), 'respuestas': self.get_respuestas(), 'correcta': self.get_correcta()}