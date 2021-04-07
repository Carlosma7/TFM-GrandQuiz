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

# Launch bot
bot.polling()