from controlador import *

import telebot
from telebot import types
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
			respuesta = f"¡Enhorabuena! Ya eres un jugador oficial de GrandQuiz, es hora de la diversión."
		except Exception as error:
			# Se produce un error
			respuesta = str(error)
	else:
		respuesta = f"No puedes registrarte en un grupo, por favor escríbeme en privado en @GrandQuizBot."

	# Informar al usuario
	bot.send_message(message.chat.id, respuesta)

# Launch bot
bot.polling()