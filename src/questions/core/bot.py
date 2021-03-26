from controlador import *

import telebot
from telebot import types
import numpy as np
from random import randint
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
	bot.send_photo(message.chat.id, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/saludo.jpg?raw=true", caption=f"¡Bienvenido {message.from_user.first_name} a GrandQuiz, el concurso donde todas las generaciones son bienvenidas! \n\nMi nombre es Tercetto y seré tu guía en el concurso.", parse_mode = 'Markdown')
	bot.send_message(message.chat.id, f"Para empezar vamos a registrarnos en el concurso, por favor dime tu edad de la forma: \n*/registro <edad>* \n\nPor ejemplo: \n*/registro 24*", parse_mode = 'Markdown')

# Registro en el sistema de GrandQuiz
@bot.message_handler(commands=['registro'])
def registro(message):
	# Crear un jugador con nombre de usuario, nombre y edad
	j = Jugador(message.from_user.username, message.from_user.first_name, int(message.text[10:]))
	try:
		# Crear jugador en controlador
		controlador.crear_jugador(j)
		# Se guarda mensaje de éxito
		respuesta = f"¡Enhorabuena! Ya eres un jugador oficial de GrandQuiz, es hora de la diversión."
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
			controlador.crear_partida(p)
			# Se guarda mensaje de éxito
			respuesta = f"¡Allá vamos! {message.from_user.first_name} ha creado una partida. Para unirte indícamelo con */unirme*."
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
	else:
		# No es un grupo
		respuesta = f"Para crear una partida tienes que estar en un grupo."

	# Informar al usuario
	bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Unirse a partida
@bot.message_handler(commands=['unirme'])
def unirse_partida(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			# Unirse a partida
			controlador.add_jugador(message.chat.id, message.from_user.username)
			respuesta = f"¡Bien! {message.from_user.first_name} se ha unido a la partida."
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
	else:
		# No es un grupo
		respuesta = f"Para unirte a una partida tienes que estar en un grupo."

	# Informar al usuario
	bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Listar jugadores de una partida
@bot.message_handler(commands=['lista'])
def listar_jugadores(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			# Obtener lista de jugadores
			lista = controlador.listar_jugadores(message.chat.id)
			if len(lista) == 0:
				respuesta = f"Aún no hay jugadores en la partida. ¡Anímate en ser el primero!"
			else:
				respuesta = f"Jugadores en la partida:\n\n"
				for jug in lista:
					respuesta += f"\U0001f466\U0001f3fb  {jug.get_nombre()}\n"
				if len(lista) == 2:
					respuesta += f"\nYa hay suficientes jugadores. ¡Así que pon /jugar para que comience el juego!"
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
	else:
		# No es un grupo
		respuesta = f"Para ver una partida tienes que estar en un grupo."

	# Informar al usuario
	bot.send_message(message.chat.id, respuesta, parse_mode = 'Markdown')

# Iniciar una partida
@bot.message_handler(commands=['jugar'])
def iniciar_partida(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		try:
			# Iniciar partida
			jug_turno, pregunta = controlador.iniciar_partida(message.chat.id)
			# Informar al usuario
			bot.send_photo(message.chat.id, photo="https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/doc/img/game/nueva_partida.jpg?raw=true", caption=f"¡Por fin es la hora de jugar a GrandQuiz!\n\nY el afortunado en responder primero es \U0001f389 {jug_turno} \U0001f389", parse_mode = 'Markdown')
			# Keyboard
			markup = types.InlineKeyboardMarkup(row_width = 1)
			# Buttons
			bt1 = (types.InlineKeyboardButton(pregunta.get_respuestas()[0], callback_data="1"))
			bt2 = (types.InlineKeyboardButton(pregunta.get_respuestas()[1], callback_data="2"))
			bt3 = (types.InlineKeyboardButton(pregunta.get_respuestas()[2], callback_data="3"))
			bt4 = (types.InlineKeyboardButton(pregunta.get_respuestas()[3], callback_data="4"))
			markup.add(bt1, bt2, bt3, bt4)
			enunciado = f"Turno de: {jug_turno}.\n\n{pregunta.get_enunciado()}"
			bot.send_message(message.chat.id, enunciado, reply_markup=markup)
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

# Responder pregunta
@bot.callback_query_handler(func=lambda call: True)
def responder_pregunta(call):
	if bool(re.match("[1-4]", call.data)):
		try:
			# Responder pregunta
			resultado = controlador.responder_pregunta(call.message.chat.id, call.from_user.username, int(call.data))
			# Pregunta acertada
			if resultado:
				respuesta = f"\u2705 ¡SÍ, HAS ACERTADO! Efectivamente era:\n\n*{controlador.obtener_respuesta(call.message.chat.id)}*"
			# Pregunta fallada
			else:
				respuesta = f"\u274C Noooooo, esa no era la respuesta correcta, la respuesta correcta era:\n\n*{controlador.obtener_respuesta(call.message.chat.id)}*"
			
			# Editar texto con respuesta
			respuesta = f"{call.message.text}\n\n{respuesta}"
			bot.edit_message_text(respuesta, call.message.chat.id, call.message.id, parse_mode = 'Markdown')
		except Exception as error:
			# Se produce un error
			respuesta = f"{call.from_user.first_name}: {str(error)}"
			# Informar al usuario
			bot.send_message(call.message.chat.id, respuesta, parse_mode = 'Markdown')



# Launch bot
bot.polling()