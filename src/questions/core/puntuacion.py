from jugador import Jugador

# Clase de puntuación
class Puntuacion():
	def __init__(self, jugador: Jugador):
		self.__puntos = 0
		self.__jugador = jugador

	# Métodos get/set
	def get_puntos(self):
		return self.__puntos

	def get_jugador(self):
		return self.__jugador

	# Anotar punto
	def anotar_punto(self):
		self.__puntos += 1

	# Overrido método equal
	def __eq__(self, otra):
		return (self.__puntos == otra.get_puntos()) and (self.__jugador == otra.get_jugador())