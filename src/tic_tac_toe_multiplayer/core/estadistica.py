# Clase de estadísticas
class Estadistica():
	def __init__(self):
		self.__num_victorias = 0
		self.__num_partidas = 0

	# Métodos get
	def get_num_victorias():
		return self.__num_victorias

	def get_num_partidas():
		return self.__num_partidas

	# Ganar partida
	def add_num_victorias():
		self.__num_victorias += 1
		self.__num_partidas += 1

	# Perder partida
	def add_num_derrotas():
		self.__num_partidas += 1

	# Override método equal
	def __eq__(self, otra):
		return (self.__num_victorias == otra.get_num_victorias()) and (self.__num_partidas == otra.get_num_partidas())