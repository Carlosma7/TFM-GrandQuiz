# Clase de logros
class Logro():
	def __init__(self, nombre_usuario: str):
		self.__nombre_usuario = nombre_usuario
		self.__logro_victorias = 0
		self.__logro_amigos = 0
		self.__logro_categorias = {"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}
		self.__logro_duelos = 0

	# Constructor from_dict
	@classmethod
	def from_dict(cls, data: dict):
		l = cls(data.get('nombre_usuario'))
		l.set_logro_victorias(data.get('logro_victorias'))
		l.set_logro_amigos(data.get('logro_amigos'))
		l.set_logro_categorias(data.get('logro_categorias'))
		l.set_logro_duelos(data.get('logro_duelos'))
		return l

	# Métodos get/set
	def get_nombre_usuario(self):
		return self.__nombre_usuario

	def get_logro_victorias(self):
		return self.__logro_victorias

	def set_logro_victorias(self, logro_victorias: int):
		self.__logro_victorias = logro_victorias

	def get_logro_amigos(self):
		return self.__logro_amigos

	def set_logro_amigos(self, logro_amigos: int):
		self.__logro_amigos = logro_amigos

	def get_logro_categorias(self):
		return self.__logro_categorias

	def set_logro_categorias(self, logro_categorias: dict):
		self.__logro_categorias = logro_categorias

	def get_logro_duelos(self):
		return self.__logro_duelos

	def set_logro_duelos(self, logro_duelos: int):
		self.__logro_duelos = logro_duelos

	def update_logro_victorias(self, num_victorias: int):
		if num_victorias == 10:
			self.__logro_victorias = 1
		elif num_victorias == 20:
			self.__logro_victorias = 2
		elif num_victorias == 50:
			self.__logro_victorias = 3
		elif num_victorias == 100:
			self.__logro_victorias = 4

	def update_logro_amigos(self, num_amigos: int):
		if num_amigos == 1:
			self.__logro_amigos = 1
		elif num_amigos == 5:
			self.__logro_amigos = 2
		elif num_amigos == 10:
			self.__logro_amigos = 3
		elif num_amigos == 20:
			self.__logro_amigos = 4

	def update_logro_categorias(self, num_aciertos: int, categoria: str):
		if num_aciertos == 5:
			self.__logro_categorias[categoria] = 1
		elif num_aciertos == 15:
			self.__logro_categorias[categoria] = 2
		elif num_aciertos == 30:
			self.__logro_categorias[categoria] = 3
		elif num_aciertos == 50:
			self.__logro_categorias[categoria] = 4

	def update_logro_duelos(self, num_duelos: int):
		if num_duelos == 10:
			self.__logro_duelos = 1
		elif num_duelos == 20:
			self.__logro_duelos = 2
		elif num_duelos == 50:
			self.__logro_duelos = 3
		elif num_duelos == 100:
			self.__logro_duelos = 4


	# Override método equal
	def __eq__(self, otra):
		return (self.__nombre_usuario == otra.get_nombre_usuario()) and (self.__logro_victorias == otra.get_logro_victorias()) and (self.__logro_amigos == otra.get_logro_amigos()) and (self.__logro_categorias == otra.get_logro_categorias()) and (self.__logro_duelos == otra.get_logro_duelos())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'nombre_usuario': self.get_nombre_usuario(), 'logro_victorias': self.get_logro_victorias(), 'logro_amigos': self.get_logro_amigos(), 'logro_categorias': self.get_logro_categorias(), 'logro_duelos': self.get_logro_duelos()}