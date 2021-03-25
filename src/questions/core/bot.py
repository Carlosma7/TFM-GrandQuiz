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
  bot.send_message(message.chat.id, f"¡Bienvenido {message.from_user.first_name} a GrandQuiz, el concurso donde todas las generaciones son bienvenidas! \n\nMi nombre es Tercetto y seré tu guía en el concurso.\n\nPara empezar vamos a registrarnos en el concurso, por favor dime tu edad de la forma: \n*/registro <edad>* \n\nPor ejemplo: \n*/registro 24*", parse_mode= 'Markdown')

# Launch bot
bot.polling()