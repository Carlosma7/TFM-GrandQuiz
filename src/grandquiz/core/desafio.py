from typing import List
# Clase de desafio
class Desafio():
	def __init__(self, titulo: str, enunciado: str, respuestas: List[str], correcta: int, justificacion: str):
		self.__titulo = titulo
		self.__enunciado = enunciado
		self.__respuestas = respuestas
		self.__correcta = correcta
		self.__justificacion = justificacion

	# Constructor from_dict
	@classmethod
	def from_dict(cls, data: dict):
		d = cls(data.get('titulo'), data.get('enunciado'), data.get('respuestas'), data.get('correcta'), data.get('justificacion'))
		return d

	# Métodos get/set
	def get_titulo(self):
		return self.__titulo

	def get_enunciado(self):
		return self.__enunciado

	def get_respuestas(self):
		return self.__respuestas

	def get_correcta(self):
		return self.__correcta

	def get_respuesta(self):
		return self.__respuestas[int(self.__correcta) - 1]

	def get_justificacion(self):
		return self.__justificacion

	# Override método equal
	def __eq__(self, otra):
		return (self.__titulo == otra.get_titulo()) and (self.__enunciado == otra.get_enunciado()) and (self.__respuestas == otra.get_respuestas()) and (self.__correcta == otra.get_correcta()) and (self.__justificacion == otra.get_justificacion())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'titulo': self.get_titulo(), 'enunciado': self.get_enunciado(), 'respuestas': self.get_respuestas(), 'correcta': self.get_correcta(), 'justificacion': self.get_justificacion()}