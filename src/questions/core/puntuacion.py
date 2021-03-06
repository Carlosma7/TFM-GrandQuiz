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

	# Override método equal
	def __eq__(self, otra):
		return (self.__puntos == otra.get_puntos()) and (self.__jugador == otra.get_jugador())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'puntos': self.get_puntos(), 'jugador': self.get_jugador().to_dict()}