from jugador import Jugador

import os
from dotenv import load_dotenv
import pymongo

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