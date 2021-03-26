from controlador import *

import telebot
from telebot import types
import numpy as np
from random import randint
from dotenv import load_dotenv
import os

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

# Launch bot
bot.polling()