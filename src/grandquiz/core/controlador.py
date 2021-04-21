from jugador import Jugador
from estadistica import Estadistica
from equipo import Equipo
from partida import Partida

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

	# Crear partida
	def crear_partida(self, partida: Partida, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Comprobar que existe una partida en el chat indicado
			par = self.mongo.partidas.find_one({'chat': partida.get_chat()})
			no_encontrada = (par == None)

			# Si no existe
			if no_encontrada:
				# Se almacena la partida
				self.mongo.partidas.insert_one(partida.to_dict())
			else:
				raise ValueError('Ya existe una partida en este grupo.')
		else:
			raise ValueError('No estás registrado en GrandQuiz.')

	# Añadir jugador a partida
	def add_jugador(self, partida: str, jugador: str, equipo: int):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		# Si está registrado
		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Comprobar que existe una partida en el chat indicado
			par = self.mongo.partidas.find_one({'chat': partida})
			encontrada = (par != None)

			# Si no existe
			if encontrada:
				# Se construye la partida desde el objeto JSON
				par = Partida.from_dict(par)

				# Comprobar que el jugador no está en la partida
				jugadores_partida = par.get_equipos()[equipo - 1].get_jugadores() + par.get_equipos()[equipo % 2].get_jugadores()
				if jug.get_nombre_usuario() not in jugadores_partida:

					# Comprobar que hay huecos disponibles
					if len(par.get_equipos()[equipo - 1].get_jugadores()) < 2:

						# Comprobar que tiene un compañero
						if len(par.get_equipos()[equipo - 1].get_jugadores()) == 1:
							# Tiene compañero, se comprueba que no tengan la misma edad

							# Se obtiene el jugador de BD
							jug2 = self.mongo.jugadores.find_one({'nombre_usuario': par.get_equipos()[equipo - 1].get_jugadores()[0]})
							# Se construye el jugador desde el objeto JSON
							jug2 = Jugador.from_dict(jug2)
							# Se comprueba que no tengan la misma edad
							if jug.get_edad() == jug2.get_edad():
								distinta_edad = False
							else:
								distinta_edad = True
						else:
							# No tiene compañero
							distinta_edad = True

						# Si tienen distinta edad los compañeros se añade, sino se notifica
						if distinta_edad:
							# Se añade el jugador y se actualiza la partida
							par.add_jugador(jugador, equipo)
							# Se actualiza la partida en BD
							self.mongo.partidas.update({'chat': par.get_chat()}, {'$set': par.to_dict()})
						else:
							raise ValueError('Existe otro jugador de tu grupo de edad en el equipo indicado.')
					else:
						raise ValueError('Ya hay dos jugadores inscritos en el equipo para la partida.')
				else:
					raise ValueError('Ya estás apuntado en la partida.')
			else:
				raise ValueError('No existe ninguna partida creada.')
		else:
			raise ValueError('No estás registrado en GrandQuiz.')

	# Obtener equipos con plazas disponibles
	def obtener_equipos_disponibles(self, partida: str, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Comprobar que existe una partida en el chat indicado
			par = self.mongo.partidas.find_one({'chat': partida})
			encontrada = (par != None)

			# Si existe
			if encontrada:
				# Se construye la partida desde el objeto JSON
				par = Partida.from_dict(par)
				# Se obtienen los equipos
				equipos = par.get_equipos()
				# Se comprueban los equipos con plazas disponibles
				equipos_disponibles = [equipo for equipo in equipos if len(equipo.get_jugadores()) < 2]
				
				return equipos_disponibles
			else:
				raise ValueError('Ya existe una partida en este grupo.')
		else:
			raise ValueError('No estás registrado en GrandQuiz.')