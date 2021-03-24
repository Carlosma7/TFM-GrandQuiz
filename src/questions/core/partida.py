from jugador import Jugador
from pregunta import Pregunta
from puntuacion import Puntuacion
from random import randint, choice

# Clase de partida
class Partida():
	def __init__(self):
		self.__jugadores = []
		self.__puntuaciones = []
		self.__preguntas = []
		self.__turno = 0
		self.__iniciada = False
		self.__ganador = 0

	# Métodos get/set
	def get_jugadores(self):
		return self.__jugadores

	def get_puntuaciones(self):
		return self.__puntuaciones

	def get_preguntas(self):
		return self.__preguntas

	def get_turno(self):
		return self.__turno

	def get_iniciada(self):
		return self.__iniciada

	def get_ganador(self):
		return self.__ganador

	# Añadir un nuevo jugador
	def add_jugador(self, jugador: Jugador):
		if len(self.__jugadores) < 2:
			# Añade jugador
			self.__jugadores.append(jugador)
			# Inicializa y añade puntuación
			puntuacion = Puntuacion(jugador)
			self.__puntuaciones.append(puntuacion)

	# Iniciar partida
	def iniciar_partida(self):
		if len(self.__jugadores) == 2:
			if not self.__iniciada:
				# Se activa la partida para evitar reinicios
				self.__iniciada = True
				# Se establece el turno del primer jugador de forma aleatoria
				self.__turno = randint(1,2)

	# Override método equal
	def __eq__(self, otra):
		return (self.__jugadores == otra.get_jugadores()) and (self.__puntuaciones == otra.get_puntuaciones()) and (self.__preguntas == otra.get_preguntas()) and (self.__turno == otra.get_turno()) and (self.__iniciada == otra.get_iniciada()) and (self.__ganador == otra.get_ganador())