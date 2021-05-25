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

# Markup de colores
def get_markup():
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (types.InlineKeyboardButton("rojo", callback_data="rojo"))
	bt2 = (types.InlineKeyboardButton("azul", callback_data="azul"))
	bt3 = (types.InlineKeyboardButton("verde", callback_data="verde"))
	bt4 = (types.InlineKeyboardButton("amarillo", callback_data="amarillo"))
	markup.add(bt1, bt2, bt3, bt4)

	return markup

# Comando start como saludo
@bot.message_handler(commands=['start'])
def saludar(message):
	bot.reply_to(message, f"¡Hola! Soy el Bot de tutorial, bienvenido a Telebot.")

# Comando help como ayuda
@bot.message_handler(commands=['help'])
def ayudar(message):
	bot.reply_to(message, f"Este bot es un ejemplo sencillo de como trabajar:\n/start si quieres que te salude.\n/color si quieres indicarme tu color favorito.\nDime cualquier cosa para que la repita.")

# Comando color para preguntar por el color favorito
@bot.message_handler(commands=['color'])
def preguntar_color(message):
	bot.send_message(message.chat.id, f"Porfa indícame tu color favorito de los siguientes:", reply_markup=get_markup())

# Función para recoger respuesta de color favorito
@bot.callback_query_handler(func=lambda call: True)
def escoger_color(call):
		if call.message:
			bot.edit_message_text(f"¡NO ME DIGAS! Mi color favorito también es el {call.data}.", call.message.chat.id, call.message.id, parse_mode = 'Markdown')
			

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	user = message.from_user.first_name
	bot.send_message(message.chat.id, f"{user} ha dicho: '{message.text}'")

# Launch bot
bot.polling()
