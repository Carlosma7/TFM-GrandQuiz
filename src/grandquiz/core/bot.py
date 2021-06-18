from controlador import *
from markups import *
from variables import *

import telebot
from telebot import types
from dotenv import load_dotenv
import os
import re

# Telegram Bot Token from BotFather
# Obtener información de .env
load_dotenv(dotenv_path = '.env')
# Obtener host y puerto
TOKEN = os.getenv('TOKEN')

# Telebot Bot
bot = telebot.TeleBot(TOKEN)

# Controlador juego
controlador = Controlador()

# Bienvenida al bot
@bot.message_handler(commands=['start'])
def bienvenida(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		bot.send_photo(message.chat.id, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/saludo.jpg?raw=true", caption=f"¡Bienvenido {message.from_user.first_name} a GrandQuiz, el concurso donde todas las generaciones son bienvenidas! \n\nMi nombre es Tercetto y seré tu guía en el concurso.", parse_mode = 'Markdown')
		bot.send_message(message.chat.id, f"Para empezar vamos a registrarnos en el concurso, por favor, escríbeme por privado en @GrandQuizBot y dime que quieres registrarte con \n\n*/registro*", parse_mode = 'Markdown')
	else:
		bot.send_photo(message.chat.id, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/saludo.jpg?raw=true", caption=f"¡Bienvenido {message.from_user.first_name} a GrandQuiz, el concurso donde todas las generaciones son bienvenidas! \n\nMi nombre es Tercetto y seré tu guía en el concurso.", parse_mode = 'Markdown')
		bot.send_message(message.chat.id, f"Para empezar vamos a registrarnos en el concurso, por favor, dime que quieres registrarte con \n\n*/registro*", parse_mode = 'Markdown')

# Registrar jugador
@bot.message_handler(commands=['registro'])
def registrar_jugador(message):

	# Comprobar que la conversación es en un grupo
	if message.chat.type != 'group':
		# Crear un jugador con nombre de usuario, nombre y edad
		j = Jugador(message.from_user.username, message.from_user.first_name)
		try:
			# Crear jugador en controlador
			controlador.registrar_jugador(j)
			# Se guarda mensaje de éxito
			respuesta = f"¡Enhorabuena! Ya eres un jugador oficial de GrandQuiz, es hora de la diversión.\n\n Ahora vamos con el avatar, escoge el que quieras."
			markup = markup_avatar()
			# Informar al usuario
			bot.send_message(message.chat.id, respuesta, reply_markup=markup)
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
			# Informar al usuario
			bot.send_message(message.chat.id, respuesta)
	else:
		respuesta = f"No puedes registrarte en un grupo, por favor escríbeme en privado en @GrandQuizBot."
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta)

# Definir avatar
@bot.callback_query_handler(lambda call: bool(re.match("av[0-9]", call.data)))
def definir_avatar(call):
	try:
		# Cambiar avatar del jugador
		controlador.cambiar_avatar(call.from_user.username, call.data)
		respuesta1 = f"¡Bien! Tu avatar será {avatar.get(call.data)}"
		respuesta2 = f"Ahora vamos con la edad. Por favor, indica a que grupo perteneces:"
		markup = markup_edad()
	except Exception as error:
		# Se produce un error
		respuesta = str(error)

	# Informar al usuario
	bot.edit_message_text(respuesta1, call.message.chat.id, call.message.id)
	# Informar al usuario
	bot.send_message(call.message.chat.id, respuesta2, reply_markup=markup)

# Definir avatar
@bot.callback_query_handler(lambda call: bool(re.match("edad[0-2]", call.data)))
def definir_edad(call):
	try:
		# Cambiar edad del jugador
		controlador.cambiar_edad(call.from_user.username, call.data)
		respuesta1 = f"¡Bien! Estamos ante un {edad.get(call.data)}."
		respuesta2 = f"Ahora vamos con el correo electrónico. Por favor, escríbeme tu email."
	except Exception as error:
		# Se produce un error
		respuesta = str(error)

	# Informar al usuario
	bot.edit_message_text(respuesta1, call.message.chat.id, call.message.id)
	# Informar al usuario
	bot.send_message(call.message.chat.id, respuesta2)

@bot.message_handler(func = lambda message: bool(re.match("([a-zA-Z0-9\.]+@[a-zA-Z\.]+\.)(com|es)", message.text)))
def definir_correo(message):
	# Comprobar que la conversación es en privado
	if message.chat.type == 'private':
		try:
			# Cambiar correo electrónico del jugador
			controlador.cambiar_email(message.from_user.username, message.text)
			respuesta1 = f"¡Bien! Se ha registrado {message.text} como tu correo."
			respuesta2 = f"¡POR FIN! Ya hemos terminado con el registro, es hora de jugar a GrandQuiz.\n\nPara jugar ve a un grupo con amigos e inicia una partida."
		except Exception as error:
			# Se produce un error
			respuesta1 = str(error)

		# Eliminar mensaje informativo previo
		bot.delete_message(message.chat.id, message.id - 1)
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta1)
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta2)

# Obtener estadisticas de un jugador
@bot.message_handler(commands=['estadisticas'])
def obtener_estadisticas(message):
	try:
		# Comprobar si es el usuario propio u otro
		if len(message.text.split()) == 2:
			jugador = message.text.split()[1]
		else:
			jugador = message.from_user.username
		# Obtener estadisticas
		est = controlador.obtener_estadisticas(jugador)
		# Obtener jugador
		jug = controlador.obtener_jugador(jugador)
		# Se guarda mensaje de éxito
		respuesta = f"Las estadísticas de {jugador} {avatar.get(jug.get_avatar())} son:\n\n{emojis_estadisticas.get('victorias')} {est.get_num_victorias()} victorias.\n\n{emojis_estadisticas.get('partidas')} {est.get_num_partidas()} partidas. \n\n{emojis_estadisticas.get('amigo')} Mejor amigo: {est.get_mejor_amigo()}. \n\n{emojis_estadisticas.get(est.get_categoria_fav())} Categoría favorita: {est.get_categoria_fav()}. \n\n{emojis_estadisticas.get('porcentaje')} {round(est.get_porcentaje_acierto(), 2)}% preguntas acertadas. \n\n{emojis_estadisticas.get('duelos')} {est.get_num_duelos()} duelos."
	except Exception as error:
		# Se produce un error
		respuesta = str(error)

	# Informar al usuario
	bot.send_message(message.chat.id, respuesta)

# Crear partida de GrandQuiz
@bot.message_handler(commands=['nueva_partida'])
def nueva_partida(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		# Crear una partida con el id del chat del grupo
		p = Partida(message.chat.id)
		try:
			# Crear partida en controlador
			controlador.crear_partida(p, message.from_user.username)
			# Se guarda mensaje de éxito
			respuesta = f"¡Allá vamos! {message.from_user.first_name} ha creado una partida."
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
	else:
		# No es un grupo
		respuesta = f"Para crear una partida tienes que estar en un grupo."

	# Informar al usuario
	bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Solicitar equipos disponibles de GrandQuiz
@bot.message_handler(commands=['unirme'])
def obtener_equipos_disponibles(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			# Obtener equipos disponibles de la partida
			equipos_disponibles = controlador.obtener_equipos_disponibles(message.chat.id, message.from_user.username)
			# Se obtienen los índices de los equipos disponibles
			equipos_disponibles_i = [equipo.get_color() for equipo in equipos_disponibles]
			# Se obtiene el markup
			markup = markup_equipos(equipos_disponibles_i)
			# Obtener lista de equipos y jugadores
			lista, completa = controlador.listar_equipos(message.chat.id, message.from_user.username)
			respuesta = lista
			# Comprobar número de equipos disponibles
			if completa:
				respuesta += f"\n\nYa hay suficientes jugadores. ¡Así que pon /jugar para que comience el juego!"
				# Informar al usuario
				bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
			else:
				# Queda algún equipo disponible
				respuesta += f"\n\nPor favor, indica a que equipo quieres unirte."
				# Informar al usuario
				bot.send_message(message.chat.id, respuesta, reply_markup=markup, parse_mode = 'Markdown')
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
			# Informar al usuario
			bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
	else:
		# No es un grupo
		respuesta = f"Para unirte a una partida tienes que estar en un grupo."
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Unirse a un equipo en una partida de GrandQuiz
@bot.callback_query_handler(lambda call: bool(re.match("eq[0-1]", call.data)))
def unirse_partida(call):
	try:
		# Añadir jugador al equipo en la partida
		controlador.add_jugador(call.message.chat.id, call.from_user.username, equipos.get(call.data))
		# Obtener equipo solicitado
		if equipos.get(call.data) == 1:
			equipo_solicitado = 'rojo'
		else:
			equipo_solicitado = 'azul'

		respuesta = f"¡Enhorabuena! Te has unido al equipo {colores_equipos.get(equipo_solicitado)}."
	except Exception as error:
		# Se produce un error
		respuesta = str(error)

	# Informar al usuario
	bot.edit_message_text(respuesta, call.message.chat.id, call.message.id)

# Listar jugadores de una partida de GrandQuiz
@bot.message_handler(commands=['lista'])
def lista_jugadores(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			lista, completa = controlador.listar_equipos(message.chat.id, message.from_user.username)
			respuesta = lista
			if completa:
				respuesta += f"\n\nYa hay suficientes jugadores. ¡Así que pon /jugar para que comience el juego!"
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
	else:
		# No es un grupo
		respuesta = f"Para ver la lista de jugadores de una partida tienes que estar en un grupo."
	
	# Informar al usuario
	bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Iniciar una partida
@bot.message_handler(commands=['jugar'])
def iniciar_partida(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			# Iniciar partida
			jug_turno, avatar_jug, equipo_turno, pregunta, categoria = controlador.iniciar_partida(message.chat.id, message.from_user.username)
			# Informar al usuario
			bot.send_photo(message.chat.id, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/nueva_partida.jpg?raw=true", caption=f"\U0001f389 ¡Por fin es la hora de jugar a GrandQuiz! \U0001f389", parse_mode = 'Markdown')
			# Definir markup
			markup = markup_respuestas(pregunta)
			aviso = f"Turno del equipo {colores_equipos.get(equipo_turno)} responde {jug_turno.upper()} {avatar.get(avatar_jug)}\n\nPregunta sobre {categoria.upper()} {emojis_categorias.get(categoria)}:"
			enunciado = f"\n\n\n\n{pregunta.get_enunciado()}"
			ultima_pregunta = bot.send_message(message.chat.id, aviso + enunciado, reply_markup=markup)
			# Se almacena
			controlador.almacenar_mensaje(message.chat.id, ultima_pregunta.id)
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
			# Informar al usuario
			bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
	else:
		# No es un grupo
		respuesta = f"Para iniciar una partida tienes que estar en un grupo."
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Responder pregunta y continuar partida
@bot.callback_query_handler(lambda call: bool(re.match("pr[1-4]", call.data)))
def responder_pregunta(call):
	# Comprobar que la conversación es en un grupo
	if call.message.chat.type == 'group':
		try:
			# Responder pregunta
			resultado = controlador.responder_pregunta(call.message.chat.id, call.from_user.username, int(call.data[-1]))
			# Comprobar si la pregunta se ha acertado
			if resultado:
				# Se ha acertado
				respuesta = f"\u2705 ¡SÍ, HAS ACERTADO! Efectivamente era:\n\n*{controlador.obtener_respuesta(call.message.chat.id)}*"
			else:
				# Se ha fallado
				respuesta = f"\u274C Noooooo, esa no era la respuesta correcta, la respuesta correcta era:\n\n*{controlador.obtener_respuesta(call.message.chat.id)}*"

			# Editar texto con respuesta
			respuesta = f"{call.message.text}\n\n{respuesta}"
			bot.edit_message_text(respuesta, call.message.chat.id, call.message.id, parse_mode = 'Markdown')

			# Comprobar si el equipo ha conseguido la medalla
			medalla, categoria_medalla, equipo_resp = controlador.comprobar_medalla(call.message.chat.id)
			if medalla:
				# Han conseguido la medalla
				respuesta = f"\n\n¡Enhorabuena! El equipo {colores_equipos.get(equipo_resp)} ha conseguido la medalla de {categoria_medalla} {emojis_categorias.get(categoria_medalla)}"
				# Informar al usuario
				if categoria_medalla == "Geografía":
					categoria_medalla = "Geografia"
				bot.send_photo(call.message.chat.id, photo=f"https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/{categoria_medalla}.jpg?raw=true", caption=respuesta, parse_mode = 'Markdown')

			# Comprobar si ha ganado un equipo
			victoria, equipo_ganador = controlador.comprobar_victoria(call.message.chat.id)
			if not victoria:
				# No ha ganado todavía ningún equipo
				# Cambiar turno al siguiente equipo
				jug_turno, avatar_jug, equipo_turno, pregunta, categoria = controlador.cambiar_turno(call.message.chat.id)
				# Definir markup
				markup = markup_respuestas(pregunta)
				aviso = f"Turno del equipo {colores_equipos.get(equipo_turno)} responde {jug_turno.upper()} {avatar.get(avatar_jug)}\n\nPregunta sobre {categoria.upper()} {emojis_categorias.get(categoria)}:"
				enunciado = f"\n\n\n\n{pregunta.get_enunciado()}"
				ultima_pregunta = bot.send_message(call.message.chat.id, aviso + enunciado, reply_markup=markup)
				# Se almacena
				controlador.almacenar_mensaje(call.message.chat.id, ultima_pregunta.id)
			else:
				# Hay un equipo ganador
				# Obtener jugadores
				jugador_1, jugador_2 = controlador.obtener_jugadores_equipo(equipo_ganador)
				# Informar al usuario
				bot.send_photo(call.message.chat.id, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/ganador.jpg?raw=true", caption=f"\u2B50\U0001f3c6 ¡ENHORABUENA! EL EQUIPO {colores_equipos.get(equipo_ganador.get_color())} ES EL CAMPEÓN DE GRANDQUIZ. \U0001f3c6\u2B50 \n\n¡{jugador_1.upper()} y {jugador_2.upper()} son los ganadores!", parse_mode = 'Markdown')
				# Eliminar partida de BD
				controlador.terminar_partida(call.message.chat.id)
		except Exception as error:
			# Se produce un error
			respuesta = f"{call.from_user.first_name}: {str(error)}"
			# Informar al usuario
			bot.send_message(call.message.chat.id, respuesta, parse_mode = 'Markdown')
	elif call.message.chat.type == 'private':
		try:
			# Responder pregunta
			resultado, chat1, chat2 = controlador.responder_pregunta_duelo(call.message.chat.id, call.from_user.username, int(call.data[-1]))
			# Comprobar si la pregunta se ha acertado
			if resultado:
				# Se ha acertado
				respuesta = f"\u2705 ¡SÍ, HAS ACERTADO! Efectivamente era:\n\n*{controlador.obtener_respuesta_duelo(chat1)}*"
			else:
				# Se ha fallado
				respuesta = f"\u274C Noooooo, esa no era la respuesta correcta, la respuesta correcta era:\n\n*{controlador.obtener_respuesta_duelo(chat1)}*"

			# Editar texto con respuesta
			respuesta = f"{call.message.text}\n\n{respuesta}"
			ultima_pregunta1 = int(controlador.obtener_mensaje_duelo(chat1, 1))
			ultima_pregunta2 = int(controlador.obtener_mensaje_duelo(chat1, 2))
			bot.edit_message_text(respuesta, chat1, ultima_pregunta1, parse_mode = 'Markdown')
			bot.edit_message_text(respuesta, chat2, ultima_pregunta2, parse_mode = 'Markdown')

			# Comprobar si el equipo ha conseguido la medalla
			medalla, categoria_medalla = controlador.comprobar_medalla_duelo(chat1)
			if medalla:
				# Han conseguido la medalla
				respuesta = f"\n\n¡Enhorabuena! {call.from_user.first_name} ha conseguido la medalla de {categoria_medalla} {emojis_categorias.get(categoria_medalla)}"
				# Informar al usuario
				bot.send_message(chat1, respuesta, parse_mode = 'Markdown')
				bot.send_message(chat2, respuesta, parse_mode = 'Markdown')

			# Comprobar si ha ganado un jugador
			victoria, jugador_ganador = controlador.comprobar_victoria_duelo(chat1)
			if not victoria:
				# No ha ganado todavía ningún jugador
				# Cambiar turno al siguiente jugador
				jug_turno, avatar_jug, pregunta, categoria, chat1, chat2 = controlador.cambiar_turno_duelo(chat1)
				# Definir markup
				markup = markup_respuestas(pregunta)
				aviso = f"Turno de {jug_turno.upper()} {avatar.get(avatar_jug)}\n\nPregunta sobre {categoria.upper()} {emojis_categorias.get(categoria)}:"
				enunciado = f"\n\n\n\n{pregunta.get_enunciado()}"
				ultima_pregunta1 = bot.send_message(chat1, aviso + enunciado, reply_markup=markup)
				ultima_pregunta2 = bot.send_message(chat2, aviso + enunciado, reply_markup=markup)
				# Se almacenan
				controlador.almacenar_mensaje_duelo(chat1, ultima_pregunta1.id, 1)
				controlador.almacenar_mensaje_duelo(chat1, ultima_pregunta2.id, 2)
			else:
				# Hay un jugador ganador
				# Informar al usuario
				bot.send_photo(chat1, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/ganador.jpg?raw=true", caption=f"\u2B50\U0001f3c6 ¡ENHORABUENA! {jugador_ganador.upper()} ES EL CAMPEÓN DE GRANDQUIZ. \U0001f3c6\u2B50", parse_mode = 'Markdown')
				bot.send_photo(chat2, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/ganador.jpg?raw=true", caption=f"\u2B50\U0001f3c6 ¡ENHORABUENA! {jugador_ganador.upper()} ES EL CAMPEÓN DE GRANDQUIZ. \U0001f3c6\u2B50", parse_mode = 'Markdown')
				# Eliminar duelo de BD
				controlador.terminar_duelo(chat1)
		except Exception as error:
			# Se produce un error
			respuesta = f"{call.from_user.first_name}: {str(error)}"
			# Informar al usuario
			bot.send_message(call.message.chat.id, respuesta, parse_mode = 'Markdown')

# Obtener top 3 de estadísticas
@bot.message_handler(commands=['top'])
def obtener_top3(message):
	try:
		# Obtener top 3
		top3 = controlador.obtener_top3(message.from_user.username)
		# Se dividen los top3
		top3_victorias = top3[0]
		top3_amigos = top3[1]
		top3_aciertos = top3[2]

		# Se añaden top 3 de victorias
		respuesta = f"\u2B50 GrandQuiz TOP \u2B50"
		respuesta += f"\n\n\U0001f451 TOP 3 Victorias\U0001f451 \n\n \U0001f947 {top3_victorias[0].get('nombre_usuario')} - {top3_victorias[0].get('num_victorias')} \n \U0001f948 {top3_victorias[1].get('nombre_usuario')} - {top3_victorias[1].get('num_victorias')} \n \U0001f949 {top3_victorias[2].get('nombre_usuario')} - {top3_victorias[2].get('num_victorias')}"

		respuesta += f"\n\n\U0001f451 TOP 3 Amigos \U0001f451 \n\n \U0001f947 {top3_amigos[0].get('nombre_usuario')} - {top3_amigos[0].get('num_amigos')} \n \U0001f948 {top3_amigos[1].get('nombre_usuario')} - {top3_amigos[1].get('num_amigos')} \n \U0001f949 {top3_amigos[2].get('nombre_usuario')} - {top3_amigos[2].get('num_amigos')}"

		respuesta += f"\n\n\U0001f451 TOP 3 Aciertos \U0001f451 \n\n \U0001f947 {top3_aciertos[0].get('nombre_usuario')} - {top3_aciertos[0].get('preguntas_acertadas')} \n \U0001f948 {top3_aciertos[1].get('nombre_usuario')} - {top3_aciertos[1].get('preguntas_acertadas')} \n \U0001f949 {top3_aciertos[2].get('nombre_usuario')} - {top3_aciertos[2].get('preguntas_acertadas')}"

	except Exception as error:
		# Se produce un error
		respuesta = str(error)

	# Informar al usuario
	bot.send_message(message.chat.id, respuesta)

# Obtener logros de un jugador
@bot.message_handler(commands=['logros'])
def obtener_logros(message):
	try:
		# Comprobar si es el usuario propio u otro
		if len(message.text.split()) == 2:
			jugador = message.text.split()[1]
		else:
			jugador = message.from_user.username
		# Obtener logros
		log = controlador.obtener_logros(jugador)
		# Obtener jugador
		jug = controlador.obtener_jugador(jugador)
		# Se guarda mensaje de éxito
		respuesta = f"Las logros de {jugador} {avatar.get(jug.get_avatar())} son:\n\n"
		# Comprobar logros de victorias
		if log.get_logro_victorias() != 0:
			respuesta += f"\U0001f3c6 {logros_victorias.get(log.get_logro_victorias())}\n\n"
		# Comprobar logros de amigos
		if log.get_logro_amigos() != 0:
			respuesta += f"\U0001f46b {logros_amigos.get(log.get_logro_amigos())}\n\n"
		# Comprobar logros de categorías
		if log.get_logro_categorias().get('Deporte') != 0:
			respuesta += f"{emojis_categorias.get('Deporte')} {logros_categorias.get('Deporte').get(log.get_logro_categorias().get('Deporte'))}"
		if log.get_logro_categorias().get('Geografía') != 0:
			respuesta += f"{emojis_categorias.get('Geografía')} {logros_categorias.get('Geografía').get(log.get_logro_categorias().get('Geografía'))}"
		if log.get_logro_categorias().get('Arte') != 0:
			respuesta += f"{emojis_categorias.get('Arte')} {logros_categorias.get('Arte').get(log.get_logro_categorias().get('Arte'))}"
		if log.get_logro_categorias().get('Historia') != 0:
			respuesta += f"{emojis_categorias.get('Historia')} {logros_categorias.get('Historia').get(log.get_logro_categorias().get('Historia'))}"
		if log.get_logro_categorias().get('Ciencia') != 0:
			respuesta += f"{emojis_categorias.get('Ciencia')} {logros_categorias.get('Ciencia').get(log.get_logro_categorias().get('Ciencia'))}"
		if log.get_logro_categorias().get('Entretenimiento') != 0:
			respuesta += f"{emojis_categorias.get('Entretenimiento')} {logros_categorias.get('Entretenimiento').get(log.get_logro_categorias().get('Entretenimiento'))}"
	except Exception as error:
		# Se produce un error
		respuesta = str(error)

	# Informar al usuario
	bot.send_message(message.chat.id, respuesta)

# Obtener quizzies de un jugador
@bot.message_handler(commands=['quizzies'])
def obtener_quizzies(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			# Obtener quizzies del jugador
			qui = controlador.obtener_quizzies(message.from_user.username)
			# Obtener jugador
			jug = controlador.obtener_jugador(message.from_user.username)

			respuesta = f"Los comodines de {jug.get_nombre()} {avatar.get(jug.get_avatar())} son:"
			markup = markup_quizzies(qui)

			# Informar al usuario
			bot.send_message(message.chat.id, respuesta, reply_markup=markup)
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
			# Informar al usuario
			bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
	else:
		# No es un grupo
		respuesta = f"Los quizzies solo estan disponibles en partidas en grupo."
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')


# Utilizar un quizzie
@bot.callback_query_handler(lambda call: bool(re.match("qui[1-3]", call.data)))
def usar_quizzie(call):
	try:
		# Obtener jugador que usa el quizzie
		jug = controlador.obtener_jugador(call.from_user.username)
		# Usar quizzie

		jug_turno, avatar_jug, equipo_turno, pregunta, categoria, respuestas = controlador.usar_quizzie(call.message.chat.id, call.from_user.username, call.data[-1])
		# Notificar uso de quizzie
		bot.edit_message_text(f"{call.from_user.first_name.upper()} {avatar.get(jug.get_avatar())} ha usado el quizzie *{quizzies.get(call.data[-1])}*", call.message.chat.id, call.message.id, parse_mode = 'Markdown')
		# Definir markup
		markup = markup_respuestas_quizzies(pregunta, respuestas)
		aviso = f"Turno del equipo {colores_equipos.get(equipo_turno)} responde {jug_turno.upper()} {avatar.get(avatar_jug)}\n\nPregunta sobre {categoria.upper()} {emojis_categorias.get(categoria)}:"
		enunciado = f"\n\n\n\n{pregunta.get_enunciado()}"
		# Eliminar mensaje de ultima pregunta
		bot.delete_message(call.message.chat.id, int(controlador.obtener_mensaje(call.message.chat.id)))
		# Se envía la nueva pregunta
		bot.send_message(call.message.chat.id, aviso + enunciado, reply_markup=markup)
	except Exception as error:
		# Se produce un error
		respuesta = f"{call.from_user.first_name}: {str(error)}"
		# Informar al usuario
		bot.send_message(call.message.chat.id, respuesta, parse_mode = 'Markdown')

# Utilizar un desafio
@bot.message_handler(commands=['desafio'])
def usar_desafio(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			# Utilizar el desafío
			jug_turno, avatar_jug, equipo_turno, desafio = controlador.usar_desafio(message.chat.id, message.from_user.username)
			# Eliminar mensaje de ultima pregunta
			bot.delete_message(message.chat.id, int(controlador.obtener_mensaje(message.chat.id)))
			# Enviar foto del desafío
			bot.send_photo(message.chat.id, photo=f"https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/challenges/{desafio.get_titulo()}.png?raw=true")
			# Definir markup
			markup = markup_desafio(desafio)
			aviso = f"\U0001f4aa DESAFÍO \U0001f4aa \n\nTurno del equipo {colores_equipos.get(equipo_turno)} responde {jug_turno.upper()} {avatar.get(avatar_jug)}."
			enunciado = f"\n\n\n\n{desafio.get_enunciado()}"
			bot.send_message(message.chat.id, aviso + enunciado, reply_markup=markup)
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
			# Informar al usuario
			bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
	else:
		# No es un grupo
		respuesta = f"Solo se puede lanzar un desafío en partidas en grupo."
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Responder desafio y continuar partida
@bot.callback_query_handler(lambda call: bool(re.match("des[1-4]", call.data)))
def responder_desafio(call):
	try:
		# Responder desafio
		resultado, medalla, justificacion, equipo_resp = controlador.responder_desafio(call.message.chat.id, call.from_user.username, int(call.data[-1]))
		# Comprobar si la pregunta se ha acertado
		if resultado:
			# Se ha acertado
			respuesta = f"\u2705 ¡SÍ, HAS ACERTADO! \n\n*{justificacion}*"
		else:
			# Se ha fallado
			respuesta = f"\u274C Noooooo, esa no era la respuesta correcta. \n\n*{justificacion}*"

		# Editar texto con respuesta
		respuesta = f"{call.message.text}\n\n{respuesta}"
		bot.edit_message_text(respuesta, call.message.chat.id, call.message.id, parse_mode = 'Markdown')

		if resultado:
			if medalla:
				# Han conseguido la medalla
				respuesta = f"\n\n¡Enhorabuena! El equipo {colores_equipos.get(equipo_resp)} ha robado la medalla de {medalla} {emojis_categorias.get(medalla)}"
				# Informar al usuario
				if medalla == "Geografía":
					medalla = "Geografia"
				bot.send_photo(call.message.chat.id, photo=f"https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/{medalla}.jpg?raw=true")
			else:
				# Han acertado pero no han conseguido la medalla
				respuesta = f"\n\n¡Oh que pena! El equipo {colores_equipos.get(equipo_resp)} ha acertado el desafío pero al no tener medallas el equipo contrario no ha podido robar nada."
		else:
			if medalla:
				# Han perdido una medalla
				respuesta = f"\n\n¡NOOOOOOO! El equipo {colores_equipos.get(equipo_resp)} ha fallado y ha perdido la medalla de {medalla} {emojis_categorias.get(medalla)}"
			else:
				# No pierden medalla porque no tienen
				respuesta = f"\n\n¡Oh que pena! El equipo {colores_equipos.get(equipo_resp)} ha fallado el desafío pero al no tener medallas no ha perdido nada."

		bot.send_message(call.message.chat.id, respuesta, parse_mode = 'Markdown')

		# Comprobar si ha ganado un equipo
		victoria, equipo_ganador = controlador.comprobar_victoria(call.message.chat.id)
		if not victoria:
			# No ha ganado todavía ningún equipo
			# Cambiar turno al siguiente equipo
			jug_turno, avatar_jug, equipo_turno, pregunta, categoria = controlador.cambiar_turno(call.message.chat.id)
			# Definir markup
			markup = markup_respuestas(pregunta)
			aviso = f"Turno del equipo {colores_equipos.get(equipo_turno)} responde {jug_turno.upper()} {avatar.get(avatar_jug)}\n\nPregunta sobre {categoria.upper()} {emojis_categorias.get(categoria)}:"
			enunciado = f"\n\n\n\n{pregunta.get_enunciado()}"
			ultima_pregunta = bot.send_message(call.message.chat.id, aviso + enunciado, reply_markup=markup)
			# Se almacena
			controlador.almacenar_mensaje(call.message.chat.id, ultima_pregunta.id)
		else:
			# Hay un equipo ganador
			# Obtener jugadores
			jugador_1, jugador_2 = controlador.obtener_jugadores_equipo(equipo_ganador)
			# Informar al usuario
			bot.send_photo(call.message.chat.id, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/ganador.jpg?raw=true", caption=f"\u2B50\U0001f3c6 ¡ENHORABUENA! EL EQUIPO {colores_equipos.get(equipo_ganador.get_color())} ES EL CAMPEÓN DE GRANDQUIZ. \U0001f3c6\u2B50 \n\n¡{jugador_1.upper()} y {jugador_2.upper()} son los ganadores!", parse_mode = 'Markdown')
			# Eliminar partida de BD
			controlador.terminar_partida(call.message.chat.id)
	except Exception as error:
		# Se produce un error
		respuesta = f"{call.from_user.first_name}: {str(error)}"
		# Informar al usuario
		bot.send_message(call.message.chat.id, respuesta, parse_mode = 'Markdown')

# Utilizar un desafio
@bot.message_handler(commands=['estado'])
def estado_partida(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			# Comprobar el estado de la partida
			eq1, eq2 = controlador.estado_partida(message.chat.id, message.from_user.username)
			# Conformar respuesta
			respuesta = f"Equipo {colores_equipos.get('rojo')}:\n"
			# Medallas equipo rojo
			for med in eq1:
				if eq1[med] == 1:
					respuesta += f"{emojis_categorias.get(med)} {med}\n"
			respuesta += f"\nEquipo {colores_equipos.get('azul')}:\n"
			for med in eq2:
				if eq2[med] == 1:
					respuesta += f"{emojis_categorias.get(med)} {med}\n"
			# Utilizar el desafío
			bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
			# Informar al usuario
			bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
	else:
		# No es un grupo
		respuesta = f"Para ver una partida tienes que estar en un grupo."
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Crear duelo de GrandQuiz
@bot.message_handler(commands=['nuevo_duelo'])
def nuevo_duelo(message):
	# Comprobar que la conversación es en privado
	if message.chat.type == 'private':
		# Crear una partida con el id del chat del grupo
		duelo = Duelo(message.chat.id, message.from_user.username)
		try:
			# Crear duelo en controlador
			jug_turno, avatar_jug, pregunta, categoria, chat1, chat2 = controlador.crear_duelo(duelo, message.from_user.username)
			# Se guarda mensaje de éxito
			if not pregunta:
				respuesta = f"¡Bien! Has creado un duelo, solo queda esperar a que se una otro jugador para empezar."
				# Informar al usuario
				bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
			else:
				respuesta = f"¡Bien! Ya hay suficientes jugadores para la partida. Hora de \U0001f64c juuuuuugaaaaaaaaarrrrrrrr \U0001f64c"
				# Informar al usuario
				bot.send_message(chat1, respuesta, parse_mode = 'Markdown')
				bot.send_message(chat2, respuesta, parse_mode = 'Markdown')
				# Definir markup
				markup = markup_respuestas(pregunta)
				aviso = f"Turno de {jug_turno.upper()} {avatar.get(avatar_jug)}\n\nPregunta sobre {categoria.upper()} {emojis_categorias.get(categoria)}:"
				enunciado = f"\n\n\n\n{pregunta.get_enunciado()}"
				ultima_pregunta1 = bot.send_message(chat1, aviso + enunciado, reply_markup=markup)
				ultima_pregunta2 = bot.send_message(chat2, aviso + enunciado, reply_markup=markup)
				# Se almacena
				controlador.almacenar_mensaje_duelo(chat1, ultima_pregunta1.id, 1)
				controlador.almacenar_mensaje_duelo(chat1, ultima_pregunta2.id, 2)
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
			# Informar al usuario
			bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')
	else:
		# No es un grupo
		respuesta = f"Para crear un duelo tienes que estar hablar en privado con GrandQuizBot."
		# Informar al usuario
		bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Launch bot
bot.polling()