# Clase de estadísticas
class Estadistica():
	def __init__(self):
		self.__num_victorias = 0
		self.__num_partidas = 0

	# Métodos get
	def get_num_victorias(self):
		return self.__num_victorias

	def get_num_partidas(self):
		return self.__num_partidas

	# Ganar partida
	def add_num_victorias(self):
		self.__num_victorias += 1
		self.__num_partidas += 1

	# Perder partida
	def add_num_derrotas(self):
		self.__num_partidas += 1

	# Override método equal
	def __eq__(self, otra):
		return (self.__num_victorias == otra.get_num_victorias()) and (self.__num_partidas == otra.get_num_partidas())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'num_victorias': self.get_num_victorias(), 'num_partidas': self.get_num_partidas()}