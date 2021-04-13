from jugador import Jugador
from typing import List
from random import choice

# Clase de equipo
class Equipo():
	def __init__(self, color: int):
		self.__jugadores = []
		self.__color = color
		self.__turno = 1
		self.__medallas = {"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}
		self.__puntuaciones = [{"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}, {"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}]

	# Constructor from_dict
	@classmethod
	def from_dict(cls, data: dict):
		e = cls(data.get('color'))
		jugadores = [Jugador.from_dict(jug) for jug in data.get('jugadores')]
		e.set_jugadores(jugadores)
		e.set_turno(data.get('turno'))
		e.set_medallas(data.get('medallas'))
		e.set_puntuaciones(data.get('puntuaciones'))
		return e

	# Métodos get/set
	def get_jugadores(self):
		return self.__jugadores

	def set_jugadores(self, jugadores: List):
		self.__jugadores = jugadores

	def get_color(self):
		return self.__color

	def get_turno(self):
		return self.__turno

	def set_turno(self, turno: int):
		self.__turno = turno

	def get_medallas(self):
		return self.__medallas

	def set_medallas(self, medallas: dict):
		self.__medallas = medallas

	def get_puntuaciones(self):
		return self.__puntuaciones

	def set_puntuaciones(self, puntuaciones: List[dict]):
		self.__puntuaciones = puntuaciones

	# Añadir jugador al equipo
	def add_jugador(self, jugador: Jugador):
		self.__jugadores.append(jugador)

	# Pasar turno del equipo
	def pasar_turno(self):
		self.__turno = (self.__turno % 2) + 1

	# Acertar pregunta por jugador
	def acertar_pregunta(self, categoria: str):
		# Se anota el punto
		self.__puntuaciones[self.__turno - 1][categoria] = 1
		# Se comprueba si ambos miembros tienen acertada la categoría
		turno_amigo = (self.__turno % 2) + 1
		if self.__puntuaciones[turno_amigo - 1].get(categoria) == 1:
			# Se añade la medalla
			self.__medallas[categoria] = 1

	# Fallar pregunta por jugador
	def fallar_pregunta(self, categoria: str):
		# Se quita el punto
		self.__puntuaciones[self.__turno - 1][categoria] = 0

	# Obtener alguna de las categorias pendientes aleatoriamente
	def obtener_categoria(self):
		# Obtener todas las categorias de las que no se posee medalla
		cat_pendientes = [cat for cat in self.__medallas if self.__medallas[cat] == 0]
		# Escoger aleatoriamente una de las categorias pendientes
		return choice(cat_pendientes)

	# Comprobar victoria del equipo
	def comprobar_victoria(self):
		# Obtener todas las categorias de las que no se posee medalla
		cat_pendientes = [cat for cat in self.__medallas if self.__medallas[cat] == 0]
		# Comprobar si quedan categorias pendientes
		if len(cat_pendientes) == 0:
			return True
		else:
			return False

	# Override método equal
	def __eq__(self, otra):
		return (self.__jugadores == otra.get_jugadores()) and (self.__color == otra.get_color()) and (self.__turno == otra.get_turno()) and (self.__medallas == otra.get_medallas()) and (self.__puntuaciones == otra.get_puntuaciones())

	# Método para transformar objeto en un dict
	def to_dict(self):
		jugadores = [jug_dict.to_dict() for jug_dict in self.get_jugadores()]
		return {'jugadores': jugadores, 'color': self.get_color(), 'turno': self.get_turno(), 'medallas': self.get_medallas(), 'puntuaciones': self.get_puntuaciones()}