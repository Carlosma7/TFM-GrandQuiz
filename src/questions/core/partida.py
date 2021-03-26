from jugador import Jugador
from pregunta import Pregunta
from puntuacion import Puntuacion
from excepciones import *

from random import randint, choice

# Clase de partida
class Partida():
	def __init__(self, chat: str):
		self.__jugadores = []
		self.__puntuaciones = []
		self.__preguntas = []
		self.__turno = 0
		self.__iniciada = False
		self.__ganador = 0
		self.__chat = chat

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

	def get_chat(self):
		return self.__chat

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
		else:
			raise NotEnoughPlayersError('Se necesitan 2 jugadores para empezar una partida.')

	# Acertar pregunta
	def acertar_pregunta(self):
		# Se añade un punto al jugador que la ha acertado
		self.__puntuaciones[self.__turno - 1].anotar_punto()

	# Pasar turno
	def pasar_turno(self):
		# Se cambia el turno al siguiente jugador
		self.__turno = (self.__turno % 2) + 1

	# Comprobar victoria
	def comprobar_victoria(self):
		# Comprobar si un jugador ha llegado a 3 puntos
		if self.__puntuaciones[0].get_puntos() == 3:
			self.__ganador = 1
		elif self.__puntuaciones[1].get_puntos() == 3:
			self.__ganador = 2
		else:
			return False

		return True

	# Terminar partida
	def terminar_partida(self):
		# Anotar el perdedor
		if self.__ganador == 1:
			perdedor = 2
		elif self.__ganador == 2:
			perdedor = 1
		else:
			raise GameNotFinishedError('No hay ningún ganador todavía.')

		# Se añade como victoria y derrota respectivamente
		self.__jugadores[self.__ganador - 1].get_estadisticas().add_num_victorias()
		self.__jugadores[perdedor - 1].get_estadisticas().add_num_derrotas()

	# Añadir preguntas
	def add_preguntas(self):
		p = Pregunta("¿Cuál es el continente más extenso del planeta?", ["América", "Europa", "Asia", "África"], 3)
		self.__preguntas.append(p)
		p = Pregunta("¿De qué estilo arquitectónico es la catedral de Barcelona?", ["Barroco", "Gótico", "Románico", "Renacentista"], 2)
		self.__preguntas.append(p)
		p = Pregunta("En qué ciudad se encuentra la fuente de Cibeles?", ["Sevilla", "Valencia", "Granada", "Madrid"], 4)
		self.__preguntas.append(p)
		p = Pregunta("De las siguientes palabras señala cuál de ellas está escrita correctamente:", ["Excarbar", "Escarvar", "Excarvar", "Escarbar"], 4)
		self.__preguntas.append(p)
		p = Pregunta("¿Cuál de las siguientes palabras no es un verbo?", ["Placer", "Traer", "Romper", "Perder"], 1)
		self.__preguntas.append(p)
		p = Pregunta("¿Qué sustancia se encuentra en el interior de un termómetro?", ["Agua", "Líquido refrigerado", "Agua con gas", "Mercurio"], 4)
		self.__preguntas.append(p)
		p = Pregunta("La capital de Dinamarca es:", ["Zagreb", "Liubliana", "Bratislava", "Copenhague"], 4)
		self.__preguntas.append(p)
		p = Pregunta("¿Cuál fue la primera civilización histórica?", ["Mesopotamia", "Romana", "Griega", "Egipcia"], 1)
		self.__preguntas.append(p)
		p = Pregunta("El pico de Mulhacén se encuentra en:", ["Málaga", "Almería", "Granada", "Jaén"], 3)
		self.__preguntas.append(p)
		p = Pregunta("La ciudad de Sevilla forma parte de la comunidad autónoma de:", ["Murcia", "Andalucía", "Asturias", "Extremadura"], 2)
		self.__preguntas.append(p)
		p = Pregunta("¿Que representa el elemento químico H2O?", ["Sodio", "Agua", "Sal", "Hidrógeno"], 3)
		self.__preguntas.append(p)

	# Realizar pregunta
	def realizar_pregunta(self):
		# Escoger aleatoriamente una pregunta de la lista
		return choice(self.__preguntas)


	# Override método equal
	def __eq__(self, otra):
		return (self.__jugadores == otra.get_jugadores()) and (self.__puntuaciones == otra.get_puntuaciones()) and (self.__preguntas == otra.get_preguntas()) and (self.__turno == otra.get_turno()) and (self.__iniciada == otra.get_iniciada()) and (self.__ganador == otra.get_ganador()) and (self.__chat == otra.get_chat())