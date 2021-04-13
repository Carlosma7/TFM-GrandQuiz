from typing import List
# Clase de pregunta
class Pregunta():
	def __init__(self, categoria: str, enunciado: str, respuestas: List[str], correcta: int):
		self.__categoria = categoria
		self.__enunciado = enunciado
		self.__respuestas = respuestas
		self.__correcta = correcta

	# Constructor from_dict
	@classmethod
	def from_dict(cls, data: dict):
		p = cls(data.get('categoria'), data.get('enunciado'), data.get('respuestas'), data.get('correcta'))
		return p

	# Métodos get/set
	def get_categoria(self):
		return self.__categoria

	def get_enunciado(self):
		return self.__enunciado

	def get_respuestas(self):
		return self.__respuestas

	def get_correcta(self):
		return self.__correcta

	def get_respuesta(self):
		return self.__respuestas[self.__correcta - 1]

	# Override método equal
	def __eq__(self, otra):
		return (self.__categoria == otra.get_categoria()) and (self.__enunciado == otra.get_enunciado()) and (self.__respuestas == otra.get_respuestas()) and (self.__correcta == otra.get_correcta())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'categoria': self.get_categoria(), 'enunciado': self.get_enunciado(), 'respuestas': self.get_respuestas(), 'correcta': self.get_correcta()}