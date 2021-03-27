from pregunta import Pregunta

import telebot
from telebot import types

# Markups Bot API
def markup_respuestas(pregunta: Pregunta):
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (types.InlineKeyboardButton(pregunta.get_respuestas()[0], callback_data="1"))
	bt2 = (types.InlineKeyboardButton(pregunta.get_respuestas()[1], callback_data="2"))
	bt3 = (types.InlineKeyboardButton(pregunta.get_respuestas()[2], callback_data="3"))
	bt4 = (types.InlineKeyboardButton(pregunta.get_respuestas()[3], callback_data="4"))
	markup.add(bt1, bt2, bt3, bt4)

	return markup
