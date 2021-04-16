# Clase de estadísticas
class Estadistica():
	def __init__(self, nombre_usuario: str):
		self.__nombre_usuario = nombre_usuario
		self.__num_victorias = 0
		self.__num_partidas = 0
		self.__amigos = {}
		self.__categorias = {"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}
		self.__preguntas_acertadas = 0
		self.__preguntas_falladas = 0

	# Constructor from_dict
	@classmethod
	def from_dict(cls, data: dict):
		e = cls(data.get('nombre_usuario'))
		e.set_num_victorias(data.get('num_victorias'))
		e.set_num_partidas(data.get('num_partidas'))
		e.set_amigos(data.get('amigos'))
		e.set_categorias(data.get('categorias'))
		e.set_preguntas_acertadas(data.get('preguntas_acertadas'))
		e.set_preguntas_falladas(data.get('preguntas_falladas'))
		return e

	# Métodos get/set
	def get_nombre_usuario(self):
		return self.__nombre_usuario

	def get_num_victorias(self):
		return self.__num_victorias

	def set_num_victorias(self, num_victorias: int):
		self.__num_victorias = num_victorias

	def get_num_partidas(self):
		return self.__num_partidas

	def set_num_partidas(self, num_partidas: int):
		self.__num_partidas = num_partidas

	def get_amigos(self):
		return self.__amigos

	def set_amigos(self, amigos: dict):
		self.__amigos = amigos

	def get_categorias(self):
		return self.__categorias

	def set_categorias(self, categorias: dict):
		self.__categorias = categorias

	def get_preguntas_acertadas(self):
		return self.__preguntas_acertadas

	def set_preguntas_acertadas(self, preguntas_acertadas: int):
		self.__preguntas_acertadas = preguntas_acertadas

	def get_preguntas_falladas(self):
		return self.__preguntas_falladas

	def set_preguntas_falladas(self, preguntas_falladas: int):
		self.__preguntas_falladas = preguntas_falladas

	# Obtener mejor amigo
	def get_mejor_amigo(self):
		try:
			return max(self.__amigos, key=self.__amigos.get)
		except:
			return "Por descubrir"

	# Obtener categoría favorita
	def get_categoria_fav(self):
		return max(self.__categorias, key=self.__categorias.get)

	# Obtener porcentaje de acierto
	def get_porcentaje_acierto(self):
		try:
			return (self.__preguntas_acertadas/(self.__preguntas_acertadas + self.__preguntas_falladas)) * 100
		except:
			return 0

	# Ganar partida
	def add_num_victorias(self):
		self.__num_partidas += 1
		self.__num_victorias += 1

	# Perder partida
	def add_num_derrotas(self):
		self.__num_partidas += 1

	# Añadir amigo
	def add_amigo(self, amigo: str):
		if amigo in self.__amigos:
			# Se añade una partida jugada con el amigo
			self.__amigos[amigo] += 1
		else:
			# Se guarda la primera partida jugada con el amigo
			self.__amigos[amigo] = 1

	# Añadir pregunta acertada
	def add_acierto(self, categoria: str):
		# Se añade al numero total de aciertos
		self.__preguntas_acertadas += 1
		# Se añade el acierto a la categoria correspondiente
		self.__categorias[categoria] += 1

	# Añadir pregunta fallada
	def add_fallo(self):
		# Se añade al número total de fallos
		self.__preguntas_falladas += 1

	# Override método equal
	def __eq__(self, otra):
		return (self.__nombre_usuario == otra.get_nombre_usuario()) and (self.__num_victorias == otra.get_num_victorias()) and (self.__num_partidas == otra.get_num_partidas()) and (self.__amigos == otra.get_amigos()) and (self.__categorias == otra.get_categorias()) and (self.__preguntas_acertadas == otra.get_preguntas_acertadas()) and (self.__preguntas_falladas == otra.get_preguntas_falladas())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'nombre_usuario': self.get_nombre_usuario(), 'num_victorias': self.get_num_victorias(), 'num_partidas': self.get_num_partidas(), 'amigos': self.get_amigos(), 'categorias': self.get_categorias(), 'preguntas_acertadas': self.get_preguntas_acertadas(), 'preguntas_falladas': self.get_preguntas_falladas()}