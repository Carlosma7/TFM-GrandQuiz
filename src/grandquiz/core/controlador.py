from jugador import Jugador
from estadistica import Estadistica

import os
from dotenv import load_dotenv
import pymongo
import re

# Obtener información de .env
load_dotenv(dotenv_path = '.env')
# Obtener conexión a MongoDB Atlas
MONGO_TOKEN = os.getenv('MONGO')

# Define a client
client = pymongo.MongoClient(MONGO_TOKEN, serverSelectionTimeoutMS = 2000)
# Define the database
database = client.GrandQuiz

# Clase controlador
class Controlador():

	# Definir la conexión a MongoDB Atlas
	mongo = database

	# Registrar jugador
	def registrar_jugador(self, jugador: Jugador):
		# Comprobar que no existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find({'nombre_usuario': jugador.get_nombre_usuario()})
		no_encontrado = (jug.count() == 0)

		# Si no existe
		if no_encontrado:
			# Se añade el jugador
			self.mongo.jugadores.insert_one(jugador.to_dict())
			# Se crean las estadisticas del jugador
			estadistica = Estadistica(jugador.get_nombre_usuario())
			# Se añade la estadistica
			self.mongo.estadisticas.insert_one(estadistica.to_dict())
		else:
			raise ValueError('Ya estás registrado.')

	# Cambiar avatar jugador
	def cambiar_avatar(self, jugador: str, avatar: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		# Si no existe
		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Se cambia el avatar
			jug.set_avatar(avatar)
			# Se actualiza en BD
			self.mongo.jugadores.update({'nombre_usuario': jugador}, {'$set': jug.to_dict()})
		else:
			raise ValueError('No estás registrado.')

	# Cambiar grupo edad jugador
	def cambiar_edad(self, jugador: str, edad: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		# Si no existe
		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Se cambia la edad
			jug.set_edad(edad)
			# Se actualiza en BD
			self.mongo.jugadores.update({'nombre_usuario': jugador}, {'$set': jug.to_dict()})
		else:
			raise ValueError('No estás registrado.')

	# Cambiar correo electrónico jugador
	def cambiar_email(self, jugador: str, email: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		# Si no existe
		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			if bool(re.match("([a-zA-Z0-9\.]+@[a-zA-Z\.]+\.)(com|es)", email)):
				# Se cambia el email
				jug.set_email(email)
			else:
				raise ValueError('El email proporcionado no es válido')
			# Se actualiza en BD
			self.mongo.jugadores.update({'nombre_usuario': jugador}, {'$set': jug.to_dict()})
		else:
			raise ValueError('No estás registrado.')

	# Obtener jugador
	def obtener_jugador(self, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		# Si existe
		if encontrado:
			# Se construyen el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Se obtienen las estadisticas
			return jug
		else:
			raise ValueError('No estás registrado en GrandQuiz.')

	# Obtener estadísticas de un jugador
	def obtener_estadisticas(self, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		est = self.mongo.estadisticas.find_one({'nombre_usuario': jugador})
		encontrado = (est != None)

		# Si existe
		if encontrado:
			# Se construyen las estadísticas desde el objeto JSON
			est = Estadistica.from_dict(est)
			# Se obtienen las estadisticas
			return est
		else:
			raise ValueError('No estás registrado en GrandQuiz.')