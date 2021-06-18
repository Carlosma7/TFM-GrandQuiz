from jugador import Jugador
from pregunta import Pregunta

from random import randint, choice
from typing import List

# Clase de duelo
class Duelo():
	def __init__(self, chat: str, jugador: str):
		self.__chat = chat
		self.__chat2 = ""
		self.__jugadores = [jugador]
		self.__turno = 0
		self.__iniciada = False
		self.__ganador = 0
		self.__pregunta_actual = Pregunta("","",[""],0)
		self.__medallas = [{"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}, {"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}]
		self.__puntuaciones = [{"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}, {"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}]
		self.__mensaje_pregunta1 = 0
		self.__mensaje_pregunta2 = 0

	# Constructor from_dict
	@classmethod
	def from_dict(cls, data: dict):
		d = cls(data.get('chat'), data.get('jugadores')[0])
		if len(data.get('jugadores')) == 2:
			d.add_jugador(data.get('jugadores')[1])
		d.set_chat2(data.get('chat2'))
		d.set_turno(data.get('turno'))
		d.set_iniciada(data.get('iniciada'))
		d.set_ganador(data.get('ganador'))
		pregunta_actual = Pregunta.from_dict(data.get('pregunta_actual'))
		d.set_pregunta_actual(pregunta_actual)
		d.set_medallas(data.get('medallas'))
		d.set_puntuaciones(data.get('puntuaciones'))
		d.set_mensaje_pregunta1(data.get('mensaje_pregunta1'))
		d.set_mensaje_pregunta2(data.get('mensaje_pregunta2'))
		return d

	# Métodos get/set
	def get_chat(self):
		return self.__chat

	def get_chat2(self):
		return self.__chat2

	def set_chat2(self, chat2: str):
		self.__chat2 = chat2

	def get_jugadores(self):
		return self.__jugadores

	def set_jugadores(self, jugadores: List[str]):
		self.__jugadores = jugadores

	def get_turno(self):
		return self.__turno

	def set_turno(self, turno: int):
		self.__turno = turno

	def get_iniciada(self):
		return self.__iniciada

	def set_iniciada(self, iniciada: bool):
		self.__iniciada = iniciada

	def get_ganador(self):
		return self.__ganador

	def set_ganador(self, ganador: int):
		self.__ganador = ganador

	def get_pregunta_actual(self):
		return self.__pregunta_actual

	def set_pregunta_actual(self, pregunta_actual: Pregunta):
		self.__pregunta_actual = pregunta_actual

	def get_medallas(self):
		return self.__medallas

	def set_medallas(self, medallas: List[dict]):
		self.__medallas = medallas

	def get_puntuaciones(self):
		return self.__puntuaciones

	def set_puntuaciones(self, puntuaciones: List[dict]):
		self.__puntuaciones = puntuaciones

	def get_mensaje_pregunta1(self):
		return self.__mensaje_pregunta1

	def set_mensaje_pregunta1(self, mensaje_pregunta1: int):
		self.__mensaje_pregunta1 = mensaje_pregunta1

	def get_mensaje_pregunta2(self):
		return self.__mensaje_pregunta2

	def set_mensaje_pregunta2(self, mensaje_pregunta2: int):
		self.__mensaje_pregunta2 = mensaje_pregunta2

	# Iniciar duelo
	def iniciar_duelo(self):
		# Se activa la duelo para evitar reinicios
		self.__iniciada = True
		# Se establece el turno del primer jugador de forma aleatoria
		self.__turno = randint(1,2)

	# Acertar pregunta
	def acertar_pregunta(self, categoria: str):
		# Se anota el punto
		self.__puntuaciones[self.__turno - 1][categoria] += 1
		# Comprobar si se obtiene medalla
		if self.__puntuaciones[self.__turno - 1][categoria] == 2:
			self.__medallas[self.__turno - 1][categoria] = 1

	# Fallar pregunta
	def fallar_pregunta(self, categoria: str):
		# Se quita el punto
		if self.__puntuaciones[self.__turno - 1][categoria] > 1:
			self.__puntuaciones[self.__turno - 1][categoria] -= 1

	# Pasar turno del equipo
	def pasar_turno(self):
		self.__turno = (self.__turno % 2) + 1

	# Obtener el jugador del turno
	def get_jugador_turno(self):
		return self.__jugadores[self.__turno - 1]

	# Añadir jugador al duelo
	def add_jugador(self, jugador: str):
		self.__jugadores.append(jugador)

	# Responder una pregunta
	def responder_pregunta(self, respuesta: int):
		return respuesta == int(self.__pregunta_actual.get_correcta())

	# Comprobar victoria
	def comprobar_victoria(self):
		# Obtener todas las categorias de las que no se posee medalla
		cat_pendientes1 = [cat for cat in self.__medallas[0] if self.__medallas[0][cat] == 0]
		cat_pendientes2 = [cat for cat in self.__medallas[1] if self.__medallas[1][cat] == 0]
		# Comprobar si quedan categorias pendientes
		if len(cat_pendientes1) == 0:
			self.__ganador = 1
			return True
		elif len(cat_pendientes2) == 0:
			self.__ganador = 2
			return True
		else:
			return False

	# Obtener alguna de las categorias pendientes aleatoriamente
	def obtener_categoria(self):
		# Obtener todas las categorias de las que no se posee medalla
		cat_pendientes = [cat for cat in self.__medallas[self.__turno - 1] if self.__medallas[self.__turno - 1][cat] == 0]
		# Escoger aleatoriamente una de las categorias pendientes
		return choice(cat_pendientes)

	# Override método equal
	def __eq__(self, otra):
		return (self.__chat == otra.get_chat()) and (self.__chat2 == otra.get_chat2()) and (self.__jugadores == otra.get_jugadores()) and (self.__turno == otra.get_turno()) and (self.__iniciada == otra.get_iniciada()) and (self.__ganador == otra.get_ganador()) and (self.__pregunta_actual == otra.get_pregunta_actual()) and (self.__medallas == otra.get_medallas()) and (self.__puntuaciones == otra.get_puntuaciones()) and (self.__mensaje_pregunta1 == otra.get_mensaje_pregunta1()) and (self.__mensaje_pregunta2 == otra.get_mensaje_pregunta2())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'chat': self.get_chat(), 'chat2': self.get_chat2(), 'jugadores': self.get_jugadores(), 'turno': self.get_turno(), 'iniciada': self.get_iniciada(), 'ganador': self.get_ganador(), 'pregunta_actual': self.get_pregunta_actual().to_dict(), 'medallas': self.get_medallas(), 'puntuaciones': self.get_puntuaciones(), 'mensaje_pregunta1': self.get_mensaje_pregunta1(), 'mensaje_pregunta2': self.get_mensaje_pregunta2()}