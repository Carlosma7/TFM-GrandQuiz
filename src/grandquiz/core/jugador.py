# Clase de jugador
class Jugador():
	def __init__(self, nombre_usuario: str, nombre: str):
		self.__nombre_usuario = nombre_usuario
		self.__nombre = nombre
		self.__edad = ""
		self.__email = ""
		self.__avatar = ""


	# Métodos get/set
	def get_nombre_usuario(self):
		return self.__nombre_usuario

	def get_nombre(self):
		return self.__nombre

	def get_edad(self):
		return self.__edad

	def set_edad(self, edad: int):
		self.__edad = edad

	def get_email(self):
		return self.__email

	def set_email(self, email: str):
		self.__email = email

	def get_avatar(self):
		return self.__avatar

	def set_avatar(self, avatar: str):
		self.__avatar = avatar

	# Override método equal
	def __eq__(self, otra):
		return (self.__nombre_usuario == otra.get_nombre_usuario()) and (self.__nombre == otra.get_nombre()) and (self.__edad == otra.get_edad()) and (self.__email == otra.get_email()) and (self.__avatar == otra.get_avatar())

	# Método para transformar objeto en un dict
	def to_dict(self):
		return {'nombre_usuario': self.get_nombre_usuario(), 'nombre': self.get_nombre(), 'edad': self.get_edad(), 'email': self.get_email(), 'avatar': self.get_avatar()}