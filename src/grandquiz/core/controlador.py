from jugador import Jugador
from estadistica import Estadistica
from logros import Logro
from equipo import Equipo
from partida import Partida
from duelo import Duelo
from pregunta import Pregunta
from desafio import Desafio
from mail import Mail
from variables import *
from excepciones import *

import os
from dotenv import load_dotenv
import pymongo
import re
from random import choice, randint
from typing import List
import datetime

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
			# Se crean los logros del jugador
			logros = Logro(jugador.get_nombre_usuario())
			# Se añade el logro
			self.mongo.logros.insert_one(logros.to_dict())
		else:
			raise PlayerRegisteredError('Ya estás registrado.')

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
			raise PlayerNotRegisteredError('No estás registrado.')

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
			raise PlayerNotRegisteredError('No estás registrado.')

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
				raise EmailNotValidError('El email proporcionado no es válido')
			# Se actualiza en BD
			self.mongo.jugadores.update({'nombre_usuario': jugador}, {'$set': jug.to_dict()})
			# Enviar mail de notificacion
			mail = Mail(email)
			# Configurar mail
			mail.set_mail(jug.get_nombre(), 1)
		else:
			raise PlayerNotRegisteredError('No estás registrado.')

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
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

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
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

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
				raise ExistingGameError('Ya existe una partida en este grupo.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

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
							raise AgeNotValidError('Existe otro jugador de tu grupo de edad en el equipo indicado.')
					else:
						raise TeamFullError('Ya hay dos jugadores inscritos en el equipo para la partida.')
				else:
					raise PlayerInGameError('Ya estás apuntado en la partida.')
			else:
				raise GameNotFoundError('No existe ninguna partida creada.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

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
				raise GameNotFoundError('No existe ninguna partida en este grupo.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

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
				raise GameNotFoundError('No existe ninguna partida en este grupo.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

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
				raise GameNotFoundError('No existe ninguna partida en este grupo.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

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

						# Se añaden los jugadores de los mismos equipos como amigos
						self.add_amigos(par.get_equipos()[0].get_jugadores())
						self.add_amigos(par.get_equipos()[1].get_jugadores())

						# Se devuelve el jugador con el turno actual, su avatar, su equipo, la pregunta actual y la categoría 
						return jug_turno, ava_jug_turno, equipo_turno, pregunta_actual, categoria_pregunta
					else:
						raise GameStartedError('Ya hay una partida iniciada en este grupo.')
				else:
					raise NotEnoughPlayersError('Uno de los dos equipos aún no está completo.')
			else:
				raise GameNotFoundError('No existe ninguna partida en este grupo.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

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

				# Se obtienen las estadisticas del jugador
				est = self.mongo.estadisticas.find_one({'nombre_usuario': jugador})
				est = Estadistica.from_dict(est)

				# Comprobar que responde el jugador del turno actual
				if par.get_jugador_turno() == jugador:
					# Responder la pregunta
					if par.responder_pregunta(respuesta):
						par.acertar_pregunta(par.get_pregunta_actual().get_categoria())
						# Se actualiza la partida en BD
						self.mongo.partidas.update({'chat': partida}, {'$set': par.to_dict()})

						# Se actualizan las estadisticas de categoria y numero de preguntas acertadas del jugador
						est.add_acierto(par.get_pregunta_actual().get_categoria())
						# Se actualizan las estadisticas en BD
						self.mongo.estadisticas.update({'nombre_usuario': jugador}, {'$set': est.to_dict()})

						# Se obtienen los logros del jugador
						log = self.mongo.logros.find_one({'nombre_usuario': jugador})
						log = Logro.from_dict(log)
						# Se actualizan los logros de aciertos en la categoría de la pregunta
						log.update_logro_categorias(est.get_categorias().get(par.get_pregunta_actual().get_categoria()), par.get_pregunta_actual().get_categoria())
						# Se actualizan los logros en BD
						self.mongo.logros.update({'nombre_usuario': jugador}, {'$set': log.to_dict()})

						# Se añaden los quizzies si el jugador acierta 25 preguntas
						if int(est.get_preguntas_acertadas()) % 25 == 0: 
							jug.add_quizzies("1", 1)
							jug.add_quizzies("2", 1)
							jug.add_quizzies("3", 1)

						# Se añaden los quizzies si el jugador 10 preguntas de categoría
						if int(est.get_categorias().get(par.get_pregunta_actual().get_categoria())) % 10 == 0:
							if par.get_pregunta_actual().get_categoria() == 'Arte' or par.get_pregunta_actual().get_categoria() == 'Historia':
								jug.add_quizzies("3", 1)
							elif par.get_pregunta_actual().get_categoria() == 'Deporte' or par.get_pregunta_actual().get_categoria() == 'Entretenimiento':
								jug.add_quizzies("2", 1)
							elif par.get_pregunta_actual().get_categoria() == 'Geografía' or par.get_pregunta_actual().get_categoria() == 'Ciencias':
								jug.add_quizzies("1", 1)

						# Se actualizan los jugadores en BD
						self.mongo.jugadores.update({'nombre_usuario': jugador}, {'$set': jug.to_dict()})


						return True
					else:
						par.fallar_pregunta(par.get_pregunta_actual().get_categoria())
						# Se actualiza la partida en BD
						self.mongo.partidas.update({'chat': partida}, {'$set': par.to_dict()})

						# Se actualiza la estadistica de numero de preguntas falladas del jugador
						est.add_fallo()
						# Se actualizan las estadisticas en BD
						self.mongo.estadisticas.update({'nombre_usuario': jugador}, {'$set': est.to_dict()})

						return False
				else:
					nombre_jugador_turno = self.mongo.jugadores.find_one({'nombre_usuario': par.get_jugador_turno()})
					nombre_jugador_turno = nombre_jugador_turno.get('nombre')
					raise WrongTurnError(f'Es el turno de {nombre_jugador_turno}.')
			else:
				raise GameNotFoundError('No existe ninguna partida creada.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Obtener la respuesta de la pregunta actual de la partida
	def obtener_respuesta(self, partida: str):
		# Comprobar que existe una partida en el chat indicado
		par = self.mongo.partidas.find_one({'chat': partida})
		encontrada = (par != None)

		if encontrada:
			par = Partida.from_dict(par)
			return par.get_pregunta_actual().get_respuesta()
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

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
			raise GameNotFoundError('No existe ninguna partida creada.')

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
				# Se actualiza la partida en BD
				self.mongo.partidas.update({'chat': partida}, {'$set': par.to_dict()})

				# Se añade una partida y una victoria al equipo ganador
				self.add_estadisticas_partida(par.get_equipos()[par.get_ganador() - 1].get_jugadores()[0], True)
				self.add_estadisticas_partida(par.get_equipos()[par.get_ganador() - 1].get_jugadores()[1], True)
				# Se añade una partida al equipo perdedor
				self.add_estadisticas_partida(par.get_equipos()[par.get_ganador() % 2].get_jugadores()[0], False)
				self.add_estadisticas_partida(par.get_equipos()[par.get_ganador() % 2].get_jugadores()[1], False)
				return True, equipo_ganador
			else:
				return False, None
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

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
			raise PlayerNotRegisteredError(f'El jugador con nick {equipo.get_jugadores()[0]} no existe.')
		else:
			# Se notifica que no existe el jugador 2
			raise PlayerNotRegisteredError(f'El jugador con nick {equipo.get_jugadores()[1]} no existe.')

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
				return True, categoria, equipo.get_color()
			else:
				return False, categoria, equipo.get_color()
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Terminar partida eliminándola de BD
	def terminar_partida(self, partida: str):
		# Comprobar que existe una partida en el chat indicado
		par = self.mongo.partidas.find_one({'chat': partida})
		encontrada = (par != None)

		if encontrada:
			# Eliminar partida de BD
			self.mongo.partidas.remove({'chat': partida})
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Añadir estadisticas de partida a un jugador
	def add_estadisticas_partida(self, jugador: str, ganador: bool):
		# Comprobar que existe el jugador 1
		est = self.mongo.estadisticas.find_one({'nombre_usuario': jugador})
		encontrado = (est != None)

		if encontrado:
			# Se obtienen los logros
			log = self.mongo.logros.find_one({'nombre_usuario': jugador})
			log = Logro.from_dict(log)

			est = Estadistica.from_dict(est)

			# Se comprueba si ha ganado
			if ganador:
				est.add_num_victorias()
				# Se actualizan los logros de victorias
				log.update_logro_victorias(est.get_num_victorias())

				# Se obtienen los jugadores
				jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
				jug = Jugador.from_dict(jug)

				# Se añaden los quizzies si el jugador tiene 10 victorias
				if int(est.get_num_victorias()) % 10 == 0: 
					jug.add_quizzies("1", 3)
					jug.add_quizzies("2", 3)
					jug.add_quizzies("3", 3)

				# Se actualizan los logros en BD
				self.mongo.jugadores.update({'nombre_usuario': jugador}, {'$set': jug.to_dict()})

			else:
				est.add_num_derrotas()

			# Se actualizan los logros de amigos
			log.update_logro_amigos(len(est.get_amigos()))

			# Se actualizan la estadisticas en BD
			self.mongo.estadisticas.update({'nombre_usuario': jugador}, {'$set': est.to_dict()})
			# Se actualizan los logros en BD
			self.mongo.logros.update({'nombre_usuario': jugador}, {'$set': log.to_dict()})
		else:
			raise PlayerNotRegisteredError(f'El jugador con nick {jugador} no existe.')

	# Añadir a un jugador como amigo
	def add_amigos(self, jugadores: List[str]):
		# Comprobar que existe el jugador 1
		est1 = self.mongo.estadisticas.find_one({'nombre_usuario': jugadores[0]})
		encontrado1 = (est1 != None)

		if encontrado1:
			est1 = Estadistica.from_dict(est1)

			# Comprobar que existe el jugador 2
			est2 = self.mongo.estadisticas.find_one({'nombre_usuario': jugadores[1]})
			encontrado2 = (est2 != None)

			if encontrado2:
				est2 = Estadistica.from_dict(est2)

				# Se añaden los jugadores como amigos
				est1.add_amigo(jugadores[1])
				est2.add_amigo(jugadores[0])

				# Se actualizan la estadisticas en BD
				self.mongo.estadisticas.update({'nombre_usuario': jugadores[0]}, {'$set': est1.to_dict()})
				self.mongo.estadisticas.update({'nombre_usuario': jugadores[1]}, {'$set': est2.to_dict()})
			else:
				raise PlayerNotRegisteredError(f'El jugador con nick {jugadores[1]} no existe.')
		else:
			raise PlayerNotRegisteredError(f'El jugador con nick {jugadores[0]} no existe.')

	# Definir top 3 de características estadística
	def obtener_top3(self, jugador: str):
		# Comprobar que existe el jugador 1
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		if encontrado:
			top3_victorias = self.mongo.estadisticas.aggregate([{'$sort':{'num_victorias': -1}}, {'$limit': 3}])
			top3_amigos = self.mongo.estadisticas.aggregate([{'$project': {'nombre_usuario': 1, 'num_amigos': {'$size': {"$objectToArray": "$amigos"}}}}, {'$sort':{'num_amigos': -1}}, {'$limit': 4}])
			top3_aciertos = self.mongo.estadisticas.aggregate([{'$sort':{'preguntas_acertadas': -1}}, {'$limit': 3}])
			top3_duelos = self.mongo.estadisticas.aggregate([{'$sort':{'num_duelos': -1}}, {'$limit': 3}])
			return [list(top3_victorias), list(top3_amigos), list(top3_aciertos), list(top3_duelos)]
		else:
			raise PlayerNotRegisteredError(f'No estás registrado en GrandQuiz.')

	# Obtener logros de un jugador
	def obtener_logros(self, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		log = self.mongo.logros.find_one({'nombre_usuario': jugador})
		encontrado = (log != None)

		# Si existe
		if encontrado:
			# Se construyen los logros desde el objeto JSON
			log = Logro.from_dict(log)
			# Se obtienen los logros
			return log
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Obtener quizzies de un jugador
	def obtener_quizzies(self, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		# Si existe
		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Se obtienen los quizzies del jugador
			return jug.get_quizzies()
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Utilizar un quizzie en la partida
	def usar_quizzie(self, partida: str, jugador: str, quizzie: str):
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

				# Comprobar que usa el quizzie el jugador del turno actual
				if par.get_jugador_turno() == jugador:
					# Comprobar el quizzie a utilizar
					if quizzie == '1':
						# Quizzie del 50%
						pregunta_actual = par.get_pregunta_actual()
						categoria_pregunta = pregunta_actual.get_categoria()
						correcta = pregunta_actual.get_correcta()

						respuestas_disponibles = ['1','2','3','4']
						respuestas_disponibles.remove(correcta)
						segunda_resp = choice(respuestas_disponibles)
						respuestas = [correcta, segunda_resp]


						# Se obtiene el avatar del jugador
						ava_jug_turno = jug.get_avatar()
						# Se obtiene el nombre del jugador
						jug_turno = jug.get_nombre()
						# Se obtiene el equipo del turno
						equipo_turno = par.get_equipo_turno().get_color()

					elif quizzie == '2':
						# Quizzie de pasar pregunta al compañero
						equipo_actual = par.get_equipo_turno()
						# Se cambiar el turno del equipo para cambiar el jugador que responde
						equipo_actual.pasar_turno()
						# Se actualiza en BD la partida
						self.mongo.partidas.update({'chat': par.get_chat()}, {'$set': par.to_dict()})

						# Se obtiene el nuevo jugador
						jug_nuevo = self.mongo.jugadores.find_one({'nombre_usuario': par.get_jugador_turno()})
						jug_nuevo = Jugador.from_dict(jug_nuevo)
						# Se obtiene el avatar del jugador
						ava_jug_turno = jug_nuevo.get_avatar()
						# Se obtiene el nombre del jugador
						jug_turno = jug_nuevo.get_nombre()
						# Se obtiene pregunta actual y categoria
						pregunta_actual = par.get_pregunta_actual()
						categoria_pregunta = pregunta_actual.get_categoria()
						# Se obtiene el equipo del turno
						equipo_turno = par.get_equipo_turno().get_color()
						# Se obtiene las respuestas disponibles
						respuestas = ['1','2','3','4']

					else:
						# Quizzie de pasar de pregunta
						pregunta_actual = par.get_pregunta_actual()
						categoria_pregunta = pregunta_actual.get_categoria()

						# Se obtiene una nueva pregunta de la categoría
						pregunta_actual = self.mongo.preguntas.aggregate([{'$match':{'categoria': categoria_pregunta}}, {'$sample':{'size': 1}}])
						pregunta_actual = list(pregunta_actual)
						pregunta_actual = Pregunta.from_dict(pregunta_actual[0])
						# Se almacena la pregunta como actual
						par.set_pregunta_actual(pregunta_actual)
						# Se actualiza la partida en BD
						self.mongo.partidas.update({'chat': par.get_chat()}, {'$set': par.to_dict()})

						# Se obtiene el avatar del jugador
						ava_jug_turno = jug.get_avatar()
						# Se obtiene el nombre del jugador
						jug_turno = jug.get_nombre()
						# Se obtiene el equipo del turno
						equipo_turno = par.get_equipo_turno().get_color()
						# Se obtiene las respuestas disponibles
						respuestas = ['1','2','3','4']

					# Se resta el quizzie utilizado
					jug.usar_quizzie(quizzie)

					# Se actualiza el jugador en BD
					self.mongo.jugadores.update({'nombre_usuario': jugador}, {'$set': jug.to_dict()})

					# Se devuelve el jugador con el turno actual, su avatar, su equipo, la pregunta actual y la categoría 
					return jug_turno, ava_jug_turno, equipo_turno, pregunta_actual, categoria_pregunta, respuestas

				else:
					nombre_jugador_turno = self.mongo.jugadores.find_one({'nombre_usuario': par.get_jugador_turno()})
					nombre_jugador_turno = nombre_jugador_turno.get('nombre')
					raise WrongTurnError(f'Es el turno de {nombre_jugador_turno}.')
			else:
				raise GameNotFoundError('No existe ninguna partida creada.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Almacenar mensaje de la ultima pregunta realizada
	def almacenar_mensaje(self, partida: str, mensaje: int):
		# Comprobar que existe una partida en el chat indicado
		par = self.mongo.partidas.find_one({'chat': partida})
		encontrada = (par != None)

		if encontrada:
			# Se construye el objeto partida
			par = Partida.from_dict(par)
			# Se almacena el mensaje nuevo de la última pregunta
			par.set_mensaje_pregunta(mensaje)
			# Se actualiza la BD
			self.mongo.partidas.update({'chat': partida}, {'$set': par.to_dict()})
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Obtener el mensaje asociado a la ultima pregunta realizada en la partida
	def obtener_mensaje(self, partida: str):
		# Comprobar que existe una partida en el chat indicado
		par = self.mongo.partidas.find_one({'chat': partida})
		encontrada = (par != None)

		if encontrada:
			# Se construye el objeto partida
			par = Partida.from_dict(par)
			# Se obtiene el mensaje de la última pregunta realizada
			return par.get_mensaje_pregunta()
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Utilizar un desafio en la partida
	def usar_desafio(self, partida: str, jugador: str):
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
				# Se construye la partida desde el objeto JSON
				par = Partida.from_dict(par)
				# Comprobar que lo solicita el jugador del turno actual
				if par.get_jugador_turno() == jugador:
					# Comprobar que el jugador tiene el desafio disponible
					if par.get_equipo_turno().get_desafios()[par.get_equipo_turno().get_turno() - 1] == 1:
						# Tiene el desafío disponible

						# Se gasta el desafío del jugador
						par.get_equipo_turno().usar_desafio()
						# Se obtiene un desafío aleatoriamente
						desafio_actual = self.mongo.desafios.aggregate([{'$sample':{'size': 1}}])
						desafio_actual = list(desafio_actual)
						desafio_actual = Desafio.from_dict(desafio_actual[0])
						# Se almacena el desafio como actual
						par.set_desafio_actual(desafio_actual)
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
						# Se devuelve el jugador con el turno actual, su avatar, su equipo y el desafio actual
						return jug_turno, ava_jug_turno, equipo_turno, desafio_actual
					else:
						# No tiene el desafío disponible
						raise ChallengeAlreadyUsed('Ya has usado el desafío en esta partida.')
				else:
					nombre_jugador_turno = self.mongo.jugadores.find_one({'nombre_usuario': par.get_jugador_turno()})
					nombre_jugador_turno = nombre_jugador_turno.get('nombre')
					raise WrongTurnError(f'Es el turno de {nombre_jugador_turno}.')


	# Responder desafio
	def responder_desafio(self, partida: str, jugador: str, respuesta: int):
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
					# Responder el desafio
					if par.responder_desafio(respuesta):
						# Acierta el desafio, por lo tanto roba una medalla al equipo contrario aleatoria
						medalla = par.get_equipos()[par.get_turno() % 2].obtener_medalla()
						if medalla:
							par.acertar_desafio(medalla)
							# Se actualiza la partida en BD
							self.mongo.partidas.update({'chat': partida}, {'$set': par.to_dict()})
							return True, medalla, par.get_desafio_actual().get_justificacion(), par.get_equipo_turno().get_color()
						else:
							return True, False, par.get_desafio_actual().get_justificacion(), par.get_equipo_turno().get_color()
					else:
						# Pierde el desafio, por lo tanto pierde una medalla aleatoria
						medalla = par.get_equipo_turno().obtener_medalla()
						if medalla:
							par.fallar_desafio(medalla)
							# Se actualiza la partida en BD
							self.mongo.partidas.update({'chat': partida}, {'$set': par.to_dict()})

							return False, medalla, par.get_desafio_actual().get_justificacion(), par.get_equipo_turno().get_color()
						else:
							return False, False, par.get_desafio_actual().get_justificacion(), par.get_equipo_turno().get_color()
				else:
					nombre_jugador_turno = self.mongo.jugadores.find_one({'nombre_usuario': par.get_jugador_turno()})
					nombre_jugador_turno = nombre_jugador_turno.get('nombre')
					raise WrongTurnError(f'Es el turno de {nombre_jugador_turno}.')
			else:
				raise GameNotFoundError('No existe ninguna partida creada.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Comprobar estado de la partida
	def estado_partida(self, partida: str, jugador: str):
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
				if par.get_iniciada():
					# Obtener equipos
					equipos = par.get_equipos()
					return equipos[0].get_medallas(), equipos[1].get_medallas()
				else:
					raise GameNotStartedError('No existe ninguna partida iniciada.')
			else:
				raise GameNotFoundError('No existe ninguna partida creada.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Crear duelo
	def crear_duelo(self, duelo: Duelo, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Comprobar que existe un duelo
			due = self.mongo.duelos.find_one({'iniciada': False})
			duelo_propio = self.mongo.duelos.find_one({'chat': duelo.get_chat()})
			duelo_ajeno = self.mongo.duelos.find_one({'chat2': duelo.get_chat()})
			no_encontrada = (due == None)

			# Si no existe
			if no_encontrada:
				# Se almacena el duelo
				self.mongo.duelos.insert_one(duelo.to_dict())
				# Se obtiene el jugador con el nombre de usuario
				jug_turno = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
				# Se obtiene el avatar del jugador
				ava_jug_turno = jug_turno.get('avatar')
				# Se obtiene el nombre del jugador
				jug_turno = jug_turno.get('nombre')
				return jug_turno, ava_jug_turno, False, False, False, False
			else:
				no_duelo_propio = (duelo_propio == None)
				no_duelo_ajeno = (duelo_ajeno == None)
				if no_duelo_propio and no_duelo_ajeno:
					# Se une al duelo existente
					due = Duelo.from_dict(due)
					# Se guarda el chat del jugador
					due.set_chat2(duelo.get_chat())
					due.add_jugador(duelo.get_jugadores()[0])
					# Se inicia el duelo
					due.iniciar_duelo()

					# Se obtienen una de las categorías disponibles del jugador
					categoria_pregunta = due.obtener_categoria()
					#pregunta_actual = self.mongo.preguntas.aggregate([{ $sample: {size: 1} }, { $match:  {"categoria": categoria_pregunta} }])
					pregunta_actual = self.mongo.preguntas.aggregate([{'$match':{'categoria': categoria_pregunta}}, {'$sample':{'size': 1}}])
					pregunta_actual = list(pregunta_actual)
					pregunta_actual = Pregunta.from_dict(pregunta_actual[0])
					# Se almacena la pregunta como actual
					due.set_pregunta_actual(pregunta_actual)
					# Se actualiza el duelo en BD
					self.mongo.duelos.update({'chat': due.get_chat()}, {'$set': due.to_dict()})
					# Se obtiene el jugador con el nombre de usuario
					jug_turno = self.mongo.jugadores.find_one({'nombre_usuario': due.get_jugador_turno()})
					# Se obtiene el avatar del jugador
					ava_jug_turno = jug_turno.get('avatar')
					# Se obtiene el nombre del jugador
					jug_turno = jug_turno.get('nombre')

					# Se devuelve el jugador con el turno actual, su avatar, la pregunta actual y la categoría 
					return jug_turno, ava_jug_turno, pregunta_actual, categoria_pregunta, due.get_chat(), due.get_chat2()
				else:
					raise ExistingDuelError('Ya estás jugando un duelo.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Responder pregunta en un duelo
	def responder_pregunta_duelo(self, duelo: str, jugador: str, respuesta: int):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Comprobar que existe un duelo en el chat indicado
			due = self.mongo.duelos.find_one({'chat': duelo})
			due2 = self.mongo.duelos.find_one({'chat2': duelo})
			encontrada = (due != None)
			encontrada2 = (due2 != None)

			# Comprobar tambien por si es chat 2
			if encontrada2:
				due = due2
				encontrada = encontrada2

			# Si existe una partida
			if encontrada:
				due = Duelo.from_dict(due)

				# Se obtienen las estadisticas del jugador
				est = self.mongo.estadisticas.find_one({'nombre_usuario': jugador})
				est = Estadistica.from_dict(est)

				# Comprobar que responde el jugador del turno actual
				if due.get_jugador_turno() == jugador:
					# Responder la pregunta
					if due.responder_pregunta(respuesta):
						due.acertar_pregunta(due.get_pregunta_actual().get_categoria())
						# Se actualiza el duelo en BD
						if encontrada2:
							self.mongo.duelos.update({'chat2': duelo}, {'$set': due.to_dict()})
						else:
							self.mongo.duelos.update({'chat': duelo}, {'$set': due.to_dict()})

						# Se actualizan las estadisticas de categoria y numero de preguntas acertadas del jugador
						est.add_acierto(due.get_pregunta_actual().get_categoria())
						# Se actualizan las estadisticas en BD
						self.mongo.estadisticas.update({'nombre_usuario': jugador}, {'$set': est.to_dict()})

						# Se obtienen los logros del jugador
						log = self.mongo.logros.find_one({'nombre_usuario': jugador})
						log = Logro.from_dict(log)
						# Se actualizan los logros de aciertos en la categoría de la pregunta
						log.update_logro_categorias(est.get_categorias().get(due.get_pregunta_actual().get_categoria()), due.get_pregunta_actual().get_categoria())
						# Se actualizan los logros en BD
						self.mongo.logros.update({'nombre_usuario': jugador}, {'$set': log.to_dict()})

						# Se actualizan los jugadores en BD
						self.mongo.jugadores.update({'nombre_usuario': jugador}, {'$set': jug.to_dict()})


						return True, due.get_chat(), due.get_chat2()
					else:
						due.fallar_pregunta(due.get_pregunta_actual().get_categoria())
						# Se actualiza el duelo en BD
						if encontrada2:
							self.mongo.duelos.update({'chat2': duelo}, {'$set': due.to_dict()})
						else:
							self.mongo.duelos.update({'chat': duelo}, {'$set': due.to_dict()})

						# Se actualiza la estadistica de numero de preguntas falladas del jugador
						est.add_fallo()
						# Se actualizan las estadisticas en BD
						self.mongo.estadisticas.update({'nombre_usuario': jugador}, {'$set': est.to_dict()})

						return False, due.get_chat(), due.get_chat2()
				else:
					nombre_jugador_turno = self.mongo.jugadores.find_one({'nombre_usuario': due.get_jugador_turno()})
					nombre_jugador_turno = nombre_jugador_turno.get('nombre')
					raise WrongTurnError(f'Es el turno de {nombre_jugador_turno}.')
			else:
				raise DuelNotFoundError('No existe ningún duelo creado.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Obtener la respuesta de la pregunta actual del duelo
	def obtener_respuesta_duelo(self, duelo: str):
		# Comprobar que existe un duelo en el chat indicado
		due = self.mongo.duelos.find_one({'chat': duelo})
		encontrada = (due != None)

		if encontrada:
			due = Duelo.from_dict(due)
			return due.get_pregunta_actual().get_respuesta()
		else:
			raise DuelNotFoundError('No existe ningún duelo creado.')

	# Pasar el turno de un duelo al siguiente jugador
	def cambiar_turno_duelo(self, duelo: str):
		# Comprobar que existe un duelo en el chat indicado
		due = self.mongo.duelos.find_one({'chat': duelo})
		encontrada = (due != None)

		if encontrada:
			due = Duelo.from_dict(due)
			
			# Cambiar de turno de la partida
			due.pasar_turno()

			# Se obtienen una de las categorías disponibles del jugador
			categoria_pregunta = due.obtener_categoria()
			#pregunta_actual = self.mongo.preguntas.aggregate([{ $sample: {size: 1} }, { $match:  {"categoria": categoria_pregunta} }])
			pregunta_actual = self.mongo.preguntas.aggregate([{'$match':{'categoria': categoria_pregunta}}, {'$sample':{'size': 1}}])
			pregunta_actual = list(pregunta_actual)
			pregunta_actual = Pregunta.from_dict(pregunta_actual[0])
			# Se almacena la pregunta como actual
			due.set_pregunta_actual(pregunta_actual)
			# Se actualiza el duelo en BD
			self.mongo.duelos.update({'chat': due.get_chat()}, {'$set': due.to_dict()})
			# Se obtiene el jugador con el nombre de usuario
			jug_turno = self.mongo.jugadores.find_one({'nombre_usuario': due.get_jugador_turno()})
			# Se obtiene el avatar del jugador
			ava_jug_turno = jug_turno.get('avatar')
			# Se obtiene el nombre del jugador
			jug_turno = jug_turno.get('nombre')

			# Se devuelve el jugador con el turno actual, su avatar, la pregunta actual y la categoría 
			return jug_turno, ava_jug_turno, pregunta_actual, categoria_pregunta, due.get_chat(), due.get_chat2()
		else:
			raise ExistingDuelError('Ya estás jugando un duelo.')

	# Comprobar si un jugador ha ganado el duelo y en caso positivo devolver el jugador ganador
	def comprobar_victoria_duelo(self, duelo: str):
		# Comprobar que existe una partida en el chat indicado
		due = self.mongo.duelos.find_one({'chat': duelo})
		encontrada = (due != None)

		if encontrada:
			due = Duelo.from_dict(due)
			
			if due.comprobar_victoria():
				# Obtener jugador ganador
				jug_ganador = due.get_ganador()
				jug_ganador = due.get_jugadores()[jug_ganador - 1]
				# Se actualiza la partida en BD
				self.mongo.duelos.update({'chat': duelo}, {'$set': due.to_dict()})

				# Se añade un duelo y una victoria al jugador ganador
				self.add_estadisticas_duelo(due.get_jugadores()[due.get_ganador() - 1], True)
				# Se añade un duelo al jugador perdedor
				self.add_estadisticas_duelo(due.get_jugadores()[due.get_ganador() % 2], False)
				return True, jug_ganador
			else:
				return False, None
		else:
			raise DuelNotFoundError('No existe ningún duelo creado.')

	# Añadir estadisticas de duelo a un jugador
	def add_estadisticas_duelo(self, jugador: str, ganador: bool):
		# Comprobar que existe el jugador 1
		est = self.mongo.estadisticas.find_one({'nombre_usuario': jugador})
		encontrado = (est != None)

		if encontrado:
			# Se obtienen los logros
			log = self.mongo.logros.find_one({'nombre_usuario': jugador})
			log = Logro.from_dict(log)

			est = Estadistica.from_dict(est)

			# Se comprueba si ha ganado el duelo
			if ganador:
				est.add_duelo()
				# Se actualizan los logros de victorias
				log.update_logro_duelos(est.get_num_duelos())

			# Se actualizan la estadisticas en BD
			self.mongo.estadisticas.update({'nombre_usuario': jugador}, {'$set': est.to_dict()})
			# Se actualizan los logros en BD
			self.mongo.logros.update({'nombre_usuario': jugador}, {'$set': log.to_dict()})
		else:
			raise PlayerNotRegisteredError(f'El jugador con nick {jugador} no existe.')

	# Comprobar si un jugador posee una medalla en un duelo tras responder a la categoría
	def comprobar_medalla_duelo(self, duelo: str):
		# Comprobar que existe un duelo en el chat indicado
		due = self.mongo.duelos.find_one({'chat': duelo})
		encontrada = (due != None)

		if encontrada:
			due = Duelo.from_dict(due)
			
			# Obtener el jugador actual
			jugador = due.get_jugador_turno()
			# Obtener categoría de la pregunta actual
			categoria = due.get_pregunta_actual().get_categoria()

			# Comprobar si el equipo tiene la medalla de la categoria
			medalla = due.get_medallas()[due.get_turno() - 1].get(categoria)

			# Si la tiene
			if medalla == 1:
				return True, categoria
			else:
				return False, categoria
		else:
			raise DuelNotFoundError('No existe ningún duelo creado.')

	# Terminar duelo eliminándola de BD
	def terminar_duelo(self, duelo: str):
		# Comprobar que existe un duelo en el chat indicado
		due = self.mongo.duelos.find_one({'chat': duelo})
		encontrada = (due != None)

		if encontrada:
			# Eliminar duelo de BD
			self.mongo.duelos.remove({'chat': duelo})
		else:
			raise DuelNotFoundError('No existe ningún duelo creado.')

	# Almacenar mensaje de la ultima pregunta realizada en duelo
	def almacenar_mensaje_duelo(self, duelo: str, mensaje: int, chat: int):
		# Comprobar que existe un duelo en el chat indicado
		due = self.mongo.duelos.find_one({'chat': duelo})
		encontrada = (due != None)

		if encontrada:
			# Se construye el objeto duelo
			due = Duelo.from_dict(due)
			if chat == 1:
				# Se almacena el mensaje nuevo de la última pregunta
				due.set_mensaje_pregunta1(mensaje)
			else:
				due.set_mensaje_pregunta2(mensaje)
			# Se actualiza la BD
			self.mongo.duelos.update({'chat': duelo}, {'$set': due.to_dict()})
		else:
			raise DuelNotFoundError('No existe ningún duelo creado.')

	# Obtener el mensaje asociado a la ultima pregunta realizada en el duelo
	def obtener_mensaje_duelo(self, duelo: str, chat: int):
		# Comprobar que existe un duelo en el chat indicado
		due = self.mongo.duelos.find_one({'chat': duelo})
		encontrada = (due != None)

		if encontrada:
			# Se construye el objeto partida
			due = Duelo.from_dict(due)
			if chat == 1:
				# Se obtiene el mensaje de la última pregunta realizada
				return due.get_mensaje_pregunta1()
			else:
				# Se obtiene el mensaje de la última pregunta realizada
				return due.get_mensaje_pregunta2()
		else:
			raise DuelNotFoundError('No existe ningún duelo creado.')

	# Comprobar estado del duelo
	def estado_duelo(self, duelo: str, jugador: str):
		# Comprobar que existe un jugador con el mismo nick de Telegram
		jug = self.mongo.jugadores.find_one({'nombre_usuario': jugador})
		encontrado = (jug != None)

		if encontrado:
			# Se construye el jugador desde el objeto JSON
			jug = Jugador.from_dict(jug)
			# Comprobar que existe un duelo en el chat indicado
			due = self.mongo.duelos.find_one({'chat': duelo})
			due2 = self.mongo.duelos.find_one({'chat2': duelo})
			encontrada = (due != None)
			encontrada2 = (due2 != None)

			# Comprobar tambien por si es chat 2
			jugador1 = True
			if encontrada2:
				due = due2
				encontrada = encontrada2
				jugador1 = False

			# Si existe una partida
			if encontrada:
				due = Duelo.from_dict(due)
				if due.get_iniciada():
					if jugador1:
						# Obtener medallas de jugadores
						return due.get_medallas()
					else:
						medallas = due.get_medallas()
						medallas.reverse()
						return medallas
				else:
					raise DuelNotStartedError('No existe ningún duelo iniciado.')
			else:
				raise DuelNotFoundError('No existe ningún duelo creado.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Comprobar partidas inactivas
	def comprobar_tiempo_partidas(self):
		# Obtener las partidas inactivas de GrandQuiz
		partidas_inactivas = self.mongo.partidas.find({'date': {'$lt': datetime.datetime.utcnow() - datetime.timedelta(hours=23, minutes=59)}})
		partidas_inactivas = list(partidas_inactivas)

		for partida in partidas_inactivas:
			partida = Partida.from_dict(partida)

			# Comprobar que la partida está iniciada
			if partida.get_iniciada():
				if partida.get_notificado() != partida.get_jugador_turno():
					jug_turno = self.mongo.jugadores.find_one({'nombre_usuario': partida.get_jugador_turno()})
					jug_turno = Jugador.from_dict(jug_turno)
					email = jug_turno.get_email()
					# Enviar mail de notificacion
					mail = Mail(email)
					# Configurar mail
					mail.set_mail(jug_turno.get_nombre(), 2)
					# Se guarda el registro de notificación al jugador
					partida.set_notificado(partida.get_jugador_turno())

		partidas_terminadas = self.mongo.partidas.find({'date': {'$lt': datetime.datetime.utcnow() - datetime.timedelta(hours=47, minutes=59)}})
		partidas_terminadas = list(partidas_terminadas)
		chats = []
		jugadores = []
		equipos = []

		for partida in partidas_terminadas:
			partida = Partida.from_dict(partida)

			# Comprobar que la partida está iniciada
			if partida.get_iniciada():
				jug_turno = self.mongo.jugadores.find_one({'nombre_usuario': partida.get_jugador_turno()})
				jug_turno = Jugador.from_dict(jug_turno)
				jug_turno = jug_turno.get_nombre()
				equipo_ganador = partida.get_equipos()[partida.get_turno() % 2].get_color()

				# Establecer equipo ganador
				partida.set_ganador((partida.get_turno() % 2) + 1)

				# Se actualiza la partida en BD
				self.mongo.partidas.update({'chat': partida.get_chat()}, {'$set': partida.to_dict()})

				# Se añade una partida y una victoria al equipo ganador
				self.add_estadisticas_partida(partida.get_equipos()[partida.get_ganador() - 1].get_jugadores()[0], True)
				self.add_estadisticas_partida(partida.get_equipos()[partida.get_ganador() - 1].get_jugadores()[1], True)
				# Se añade una partida al equipo perdedor
				self.add_estadisticas_partida(partida.get_equipos()[partida.get_ganador() % 2].get_jugadores()[0], False)
				self.add_estadisticas_partida(partida.get_equipos()[partida.get_ganador() % 2].get_jugadores()[1], False)

				# Guardar chat de la partida
				chats.append(partida.get_chat())
				# Guardar jugador que ocasiona derrota de la partida
				jugadores.append(jug_turno)
				# Guardar equipo ganador
				equipos.append(equipo_ganador)

		return chats, jugadores, equipos

	# Dar de baja a un jugador
	def baja_jugador(self, jugador: str):
		# Se elimina de BD
		self.mongo.jugadores.delete_one({'nombre_usuario': jugador})
		self.mongo.logros.delete_one({'nombre_usuario': jugador})
		self.mongo.estadisticas.delete_one({'nombre_usuario': jugador})