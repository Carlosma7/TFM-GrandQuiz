from jugador import Jugador
from equipo import Equipo
from pregunta import Pregunta

from random import randint, choice
from typing import List

# Clase de partida
class Partida():
	def __init__(self, chat: str):
		self.__chat = chat
		self.__equipos = [Equipo(i) for i in range(1,3)]
		self.__turno = 0
		self.__iniciada = False
		self.__ganador = 0
		self.__pregunta_actual = Pregunta("","",[""],0)
		self.__mensaje_pregunta = 0

	# Constructor from_dict
	@classmethod
	def from_dict(cls, data: dict):
		p = cls(data.get('chat'))
		equipos = [Equipo.from_dict(equipo) for equipo in data.get('equipos')]
		p.set_equipos(equipos)
		p.set_turno(data.get('turno'))
		p.set_iniciada(data.get('iniciada'))
		p.set_ganador(data.get('ganador'))
		pregunta_actual = Pregunta.from_dict(data.get('pregunta_actual'))
		p.set_pregunta_actual(pregunta_actual)
		p.set_mensaje_pregunta(data.get('mensaje_pregunta'))
		return p

	# Métodos get/set
	def get_chat(self):
		return self.__chat

	def get_equipos(self):
		return self.__equipos

	def set_equipos(self, equipos: List[Equipo]):
		self.__equipos = equipos

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

	def get_mensaje_pregunta(self):
		return self.__mensaje_pregunta

	def set_mensaje_pregunta(self, mensaje_pregunta: int):
		self.__mensaje_pregunta = mensaje_pregunta

	# Añadir un nuevo jugador
	def add_jugador(self, jugador: str, equipo: int):
		# Añade jugador al equipo
		self.__equipos[equipo - 1].add_jugador(jugador)

	# Iniciar partida
	def iniciar_partida(self):
		# Se activa la partida para evitar reinicios
		self.__iniciada = True
		# Se establece el turno del primer jugador de forma aleatoria
		self.__turno = randint(1,2)

	# Acertar pregunta
	def acertar_pregunta(self, categoria: str):
		# Se añade un punto al jugador que la ha acertado
		self.__equipos[self.__turno - 1].acertar_pregunta(categoria)

	# Fallar pregunta
	def fallar_pregunta(self, categoria: str):
		# Se quita un punto al jugador que la ha fallado
		self.__equipos[self.__turno - 1].fallar_pregunta(categoria)

	# Pasar turno del equipo
	def pasar_turno(self):
		self.__turno = (self.__turno % 2) + 1

	# Obtener el jugador del turno
	def get_jugador_turno(self):
		equipo = self.__equipos[self.__turno - 1]
		return equipo.get_jugador_turno()

	# Obtener el equipo del turno actual
	def get_equipo_turno(self):
		return self.__equipos[self.__turno - 1]

	# Responder una pregunta
	def responder_pregunta(self, respuesta: int):
		return respuesta == int(self.__pregunta_actual.get_correcta())

	# Comprobar victoria
	def comprobar_victoria(self):
		# Comprobar si un jugador ha llegado a 3 puntos
		if self.__equipos[0].comprobar_victoria():
			self.__ganador = 1
		elif self.__equipos[1].comprobar_victoria():
			self.__ganador = 2
		else:
			return False

		return True

	# Override método equal
	def __eq__(self, otra):
		return (self.__chat == otra.get_chat()) and (self.__equipos == otra.get_equipos()) and (self.__turno == otra.get_turno()) and (self.__iniciada == otra.get_iniciada()) and (self.__ganador == otra.get_ganador()) and (self.__pregunta_actual == otra.get_pregunta_actual()) and (self.__mensaje_pregunta == otra.get_mensaje_pregunta())

	# Método para transformar objeto en un dict
	def to_dict(self):
		equipos = [equipo.to_dict() for equipo in self.get_equipos()]
		return {'chat': self.get_chat(), 'equipos': equipos, 'turno': self.get_turno(), 'iniciada': self.get_iniciada(), 'ganador': self.get_ganador(), 'pregunta_actual': self.get_pregunta_actual().to_dict(), 'mensaje_pregunta': self.get_mensaje_pregunta()}