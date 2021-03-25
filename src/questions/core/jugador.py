from estadistica import Estadistica

# Clase de jugador
class Jugador():
	def __init__(self, nombre_usuario: str, nombre: str, edad: int):
		self.__nombre_usuario = nombre_usuario
		self.__nombre = nombre
		self.__edad = edad
		self.__estadisticas = Estadistica()

	# Métodos get/set
	def get_nombre_usuario(self):
		return self.__nombre_usuario

	def set_nombre_usuario(self, nombre_usuario: str):
		self.__nombre_usuario = nombre_usuario

	def get_nombre(self):
		return self.__nombre

	def set_nombre(self, nombre: str):
		self.__nombre = nombre

	def get_edad(self):
		return self.__edad

	def set_edad(self, edad: int):
		self.__edad = edad

	def get_estadisticas(self):
		return self.__estadisticas

	# Override método equal
	def __eq__(self, otra):
		return (self.__nombre_usuario == otra.get_nombre_usuario()) and (self.__nombre == otra.get_nombre()) and (self.__edad == otra.get_edad()) and (self.__estadisticas == otra.get_estadisticas())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'nombre_usuario': self.get_nombre_usuario(), 'nombre': self.get_nombre(), 'edad': self.get_edad(), 'estadisticas': self.get_estadisticas().to_dict()}