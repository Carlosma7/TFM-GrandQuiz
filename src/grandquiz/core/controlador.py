from jugador import Jugador
from estadistica import Estadistica
from equipo import Equipo
from partida import Partida
from pregunta import Pregunta
from variables import *

import os
from dotenv import load_dotenv
import pymongo
import re
from random import choice, randint

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

	# Obtener equipos de una partida
	def obtener_equipos(self, partida: str, jugador: str):
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
				return par.get_equipos()
			else:
				raise ValueError('No existe ninguna partida en este grupo.')
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
				raise ValueError('No existe ninguna partida en este grupo.')
		else:
			raise ValueError('No estás registrado en GrandQuiz.')

	# Obtener una lista de los equipos con los jugadores que los conforman
	def listar_equipos(self, partida:str, jugador: str):
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

				# Obtener equipos de la partida
				equipos_partida = self.obtener_equipos(partida, jugador)
				# Mensajes de cabecera de equipos
				cabecera_rojo = f"*EQUIPO* {colores_equipos.get('rojo')}\n"
				cabecera_azul = f"\n*EQUIPO* {colores_equipos.get('azul')}\n"
				# Lista de jugadores de ambos equipos
				jugadores_rojo = [self.obtener_jugador(jugador) for jugador in equipos_partida[0].get_jugadores()]
				jugadores_azul = [self.obtener_jugador(jugador) for jugador in equipos_partida[1].get_jugadores()]
				# Conformar lista de jugadores
				for jug_rojo in jugadores_rojo:
					cabecera_rojo += f"- {avatar.get(jug_rojo.get_avatar())} {jug_rojo.get_nombre()}\n"
				for jug_azul in jugadores_azul:
					cabecera_azul += f"- {avatar.get(jug_azul.get_avatar())} {jug_azul.get_nombre()}\n"
				# Conformar lista de jugadores
				lista = cabecera_rojo + cabecera_azul
				# Comprobar si la partida está completa
				if len(jugadores_rojo) == len(jugadores_azul) and len(jugadores_rojo) == 2:
					completa = True
				else:
					completa = False

				return lista, completa
			else:
				raise ValueError('No existe ninguna partida en este grupo.')
		else:
			raise ValueError('No estás registrado en GrandQuiz.')

	# Iniciar una partida existente comprobando que los equipos esten completos
	def iniciar_partida(self, partida: str, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Comprobar que existe una partida en el chat indicado
			par = self.mongo.partidas.find_one({'chat': partida})
			encontrada = (par != None)

			# Si existe una partida
			if encontrada:
				par = Partida.from_dict(par)
				# Comprobar que la partida tiene dos equipos completos (con 2 jugadores)
				if len(par.get_equipos()[0].get_jugadores()) == 2 and len(par.get_equipos()[1].get_jugadores()) == 2:
					# Comprobar que la partida no está iniciada
					if not par.get_iniciada():
						# Se inicia la partida
						par.iniciar_partida()
						# Se obtienen una de las categorías disponibles del jugador
						categoria_pregunta = par.get_equipo_turno().obtener_categoria()
						#pregunta_actual = self.mongo.preguntas.aggregate([{ $sample: {size: 1} }, { $match:  {"categoria": categoria_pregunta} }])
						pregunta_actual = self.mongo.preguntas.aggregate([{'$match':{'categoria': categoria_pregunta}}, {'$sample':{'size': 1}}])
						pregunta_actual = list(pregunta_actual)
						pregunta_actual = Pregunta.from_dict(pregunta_actual[0])
						# Se almacena la pregunta como actual
						par.set_pregunta_actual(pregunta_actual)
						# Se actualiza la partida en BD
						self.mongo.partidas.update({'chat': partida}, {'$set': par.to_dict()})
						# Se obtiene el jugador con el nombre de usuario
						jug_turno = self.mongo.jugadores.find_one({'nombre_usuario': par.get_jugador_turno()})
						# Se obtiene el avatar del jugador
						ava_jug_turno = jug_turno.get('avatar')
						# Se obtiene el nombre del jugador
						jug_turno = jug_turno.get('nombre')
						# Se obtiene el equipo del turno
						equipo_turno = par.get_equipo_turno().get_color()
						# Se devuelve el jugador con el turno actual, su avatar, su equipo, la pregunta actual y la categoría 
						return jug_turno, ava_jug_turno, equipo_turno, pregunta_actual, categoria_pregunta
					else:
						raise ValueError('Ya hay una partida iniciada en este grupo.')
				else:
					raise ValueError('Uno de los dos equipos aún no está completo.')
		else:
			raise ValueError('No estás registrado en GrandQuiz.')

	# Responder pregunta
	def responder_pregunta(self, partida: str, jugador: str, respuesta: int):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Comprobar que existe una partida en el chat indicado
			par = self.mongo.partidas.find_one({'chat': partida})
			encontrada = (par != None)

			# Si existe una partida
			if encontrada:
				par = Partida.from_dict(par)
				# Comprobar que responde el jugador del turno actual
				if par.get_jugador_turno() == jugador:
					# Responder la pregunta
					if par.responder_pregunta(respuesta):
						par.acertar_pregunta(par.get_pregunta_actual().get_categoria())
						return True
					else:
						par.fallar_pregunta(par.get_pregunta_actual().get_categoria())
						return False
				else:
					raise ValueError(f'Es el turno de {par.get_jugador_turno()}.')
			else:
				raise ValueError('No existe ninguna partida creada.')
		else:
			raise ValueError('No estás registrado en GrandQuiz.')

	# Obtener la respuesta de la pregunta actual de la partida
	def obtener_respuesta(self, partida: str):
		# Comprobar que existe una partida en el chat indicado
		par = self.mongo.partidas.find_one({'chat': partida})
		encontrada = (par != None)

		if encontrada:
			par = Partida.from_dict(par)
			return par.get_pregunta_actual().get_respuesta()
		else:
			raise ValueError('No existe ninguna partida creada.')

	# Pasar el turno de una partida al siguiente jugador
	def cambiar_turno(self, partida: str):
		# Comprobar que existe una partida en el chat indicado
		par = self.mongo.partidas.find_one({'chat': partida})
		encontrada = (par != None)

		if encontrada:
			par = Partida.from_dict(par)
			
			# Cambiar de turno para el equipo
			par.get_equipo_turno().pasar_turno()
			# Cambiar de turno de la partida
			par.pasar_turno()

			# Se obtienen una de las categorías disponibles del jugador
			categoria_pregunta = par.get_equipo_turno().obtener_categoria()
			#pregunta_actual = self.mongo.preguntas.aggregate([{ $sample: {size: 1} }, { $match:  {"categoria": categoria_pregunta} }])
			pregunta_actual = self.mongo.preguntas.aggregate([{'$match':{'categoria': categoria_pregunta}}, {'$sample':{'size': 1}}])
			pregunta_actual = list(pregunta_actual)
			pregunta_actual = Pregunta.from_dict(pregunta_actual[0])
			# Se almacena la pregunta como actual
			par.set_pregunta_actual(pregunta_actual)
			# Se actualiza la partida en BD
			self.mongo.partidas.update({'chat': partida}, {'$set': par.to_dict()})
			# Se obtiene el jugador con el nombre de usuario
			jug_turno = self.mongo.jugadores.find_one({'nombre_usuario': par.get_jugador_turno()})
			# Se obtiene el avatar del jugador
			ava_jug_turno = jug_turno.get('avatar')
			# Se obtiene el nombre del jugador
			jug_turno = jug_turno.get('nombre')
			# Se obtiene el equipo del turno
			equipo_turno = par.get_equipo_turno().get_color()
			# Se devuelve el jugador con el turno actual, su avatar, su equipo, la pregunta actual y la categoría 
			return jug_turno, ava_jug_turno, equipo_turno, pregunta_actual, categoria_pregunta
		else:
			raise ValueError('No existe ninguna partida creada.')

	# Comprobar si un equipo ha ganado la partida y en caso positivo devolver el equipo ganador
	def comprobar_victoria(self, partida: str):
		# Comprobar que existe una partida en el chat indicado
		par = self.mongo.partidas.find_one({'chat': partida})
		encontrada = (par != None)

		if encontrada:
			par = Partida.from_dict(par)
			
			if par.comprobar_victoria():
				# Obtener equipo ganador
				equipo_ganador = par.get_equipos()[par.get_ganador() - 1]

				return True, equipo_ganador
			else:
				return False, None
		else:
			raise ValueError('No existe ninguna partida creada.')

	# Obtener nombres de jugadores de un equipo indicado
	def obtener_jugadores_equipo(self, equipo: Equipo):
		# Comprobar que existe el jugador 1
		jug1 = self.mongo.jugadores.find_one({'nombre_usuario': equipo.get_jugadores()[0]})
		encontrado1 = (jug1 != None)

		# Comprobar que existe el jugador 2
		jug2 = self.mongo.jugadores.find_one({'nombre_usuario': equipo.get_jugadores()[1]})
		encontrado2 = (jug2 != None)

		if encontrado1 and encontrado2:
			# Ambos existen, se obtienen sus nombres
			return jug1.get('nombre'), jug2.get('nombre')
		elif not encontrado1:
			# Se notifica que no existe el jugador 1
			raise ValueError(f'El jugador con nick {equipo.get_jugadores()[0]} no existe.')
		else:
			# Se notifica que no existe el jugador 2
			raise ValueError(f'El jugador con nick {equipo.get_jugadores()[1]} no existe.')

	# Comprobar si un equipo posee una medalla tras responder a la categoría
	def comprobar_medalla(self, partida: str):
		# Comprobar que existe una partida en el chat indicado
		par = self.mongo.partidas.find_one({'chat': partida})
		encontrada = (par != None)

		if encontrada:
			par = Partida.from_dict(par)
			
			# Obtener el equipo actual
			equipo = par.get_equipo_turno()
			# Obtener categoría de la pregunta actual
			categoria = par.get_pregunta_actual().get_categoria()

			# Comprobar si el equipo tiene la medalla de la categoria
			medalla = equipo.get_medallas().get(categoria)

			# Si la tiene
			if medalla == 1:
				return True
			else:
				return False
		else:
			raise ValueError('No existe ninguna partida creada.')