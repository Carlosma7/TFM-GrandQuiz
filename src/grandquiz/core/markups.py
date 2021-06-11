import telebot
from variables import *
from typing import List
from telebot import types
from pregunta import Pregunta
from desafio import Desafio

# Markups Bot API para elegir avatar
def markup_avatar():
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 5)
	# Buttons
	bt1 = (types.InlineKeyboardButton("\U0001f466\U0001f3fb", callback_data="av0"))
	bt2 = (types.InlineKeyboardButton("\U0001f467\U0001f3fb", callback_data="av1"))
	bt3 = (types.InlineKeyboardButton("\U0001f9d1\U0001f3fb\u200D\U0001f9b3", callback_data="av2"))
	bt4 = (types.InlineKeyboardButton("\U0001f468\U0001f3fb\u200D\U0001f9b3", callback_data="av3"))
	bt5 = (types.InlineKeyboardButton("\U0001f916", callback_data="av4"))
	bt6 = (types.InlineKeyboardButton("\U0001f47d", callback_data="av5"))
	bt7 = (types.InlineKeyboardButton("\U0001f435", callback_data="av6"))
	bt8 = (types.InlineKeyboardButton("\U0001f438", callback_data="av7"))
	bt9 = (types.InlineKeyboardButton("\U0001f920", callback_data="av8"))
	bt10 = (types.InlineKeyboardButton("\U0001f60e", callback_data="av9"))
	markup.add(bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9, bt10)

	return markup

# Markups Bot API para elegir rango de edad
def markup_edad():
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (types.InlineKeyboardButton("Menor de 30 años", callback_data="edad0"))
	bt2 = (types.InlineKeyboardButton("Entre 30 y 60 años", callback_data="edad1"))
	bt3 = (types.InlineKeyboardButton("Mayor de 60 años", callback_data="edad2"))
	markup.add(bt1, bt2, bt3)

	return markup

# Markups Bot API para elegir equipo al que unirse
def markup_equipos(equipos_disponibles):
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (types.InlineKeyboardButton(f"Equipo {colores_equipos.get('rojo')}", callback_data="eq0"))
	bt2 = (types.InlineKeyboardButton(f"Equipo {colores_equipos.get('azul')}", callback_data="eq1"))
	# Comprobar equipos disponibles
	if len(equipos_disponibles) == 2:
		# Se añaden botones para los dos equipos
		markup.add(bt1, bt2)
	elif len(equipos_disponibles) == 1:
		# Se añade el único equipo disponible
		if equipos_disponibles[0] == 1:
			# Es el equipo rojo
			markup.add(bt1)
		else:
			# Es el equipo azul
			markup.add(bt2)
	else:
		# No hay equipos disponibles, no se añaden botones
		markup = None

	return markup

# Markups Bot API para responder a una pregunta
def markup_respuestas(pregunta: Pregunta):
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (types.InlineKeyboardButton(pregunta.get_respuestas()[0], callback_data="pr1"))
	bt2 = (types.InlineKeyboardButton(pregunta.get_respuestas()[1], callback_data="pr2"))
	bt3 = (types.InlineKeyboardButton(pregunta.get_respuestas()[2], callback_data="pr3"))
	bt4 = (types.InlineKeyboardButton(pregunta.get_respuestas()[3], callback_data="pr4"))
	markup.add(bt1, bt2, bt3, bt4)

	return markup

# Markups Bot API para responder a una pregunta
def markup_respuestas_quizzies(pregunta: Pregunta, respuestas: List[str]):
	if len(respuestas) == 4:
		# Se usa el markup genérico
		return markup_respuestas(pregunta)
	else:
		# Keyboard
		markup = types.InlineKeyboardMarkup(row_width = 1)
		# Buttons
		bt1 = (types.InlineKeyboardButton(pregunta.get_respuestas()[int(respuestas[0]) - 1], callback_data=f"pr{respuestas[0]}"))
		bt2 = (types.InlineKeyboardButton(pregunta.get_respuestas()[int(respuestas[1]) - 1], callback_data=f"pr{respuestas[1]}"))
		markup.add(bt1, bt2)

		return markup

# Markups Bot API para mostrar quizzies
def markup_quizzies(quizzies_jugador: dict):
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (types.InlineKeyboardButton(f"{quizzies.get('1')} - {quizzies_jugador.get('1')}", callback_data="qui1"))
	bt2 = (types.InlineKeyboardButton(f"{quizzies.get('2')} - {quizzies_jugador.get('2')}", callback_data="qui2"))
	bt3 = (types.InlineKeyboardButton(f"{quizzies.get('3')} - {quizzies_jugador.get('3')}", callback_data="qui3"))
	# Comprobar los quizzies disponibles
	if quizzies_jugador.get('1') != 0:
		if quizzies_jugador.get('2') != 0:
			if quizzies_jugador.get('3') != 0:
				markup.add(bt1, bt2, bt3)
			else:
				markup.add(bt1, bt2)
		else:
			if quizzies_jugador.get('3') != 0:
				markup.add(bt1, bt3)
			else:
				markup.add(bt1)
	else:
		if quizzies_jugador.get('2') != 0:
			if quizzies_jugador.get('3') != 0:
				markup.add(bt2, bt3)
			else:
				markup.add(bt2)
		else:
			if quizzies_jugador.get('3') != 0:
				markup.add(bt3)

	return markup

# Markups Bot API para responder a un desafío
def markup_desafio(desafio: Desafio):
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (types.InlineKeyboardButton(desafio.get_respuestas()[0], callback_data="des1"))
	bt2 = (types.InlineKeyboardButton(desafio.get_respuestas()[1], callback_data="des2"))
	bt3 = (types.InlineKeyboardButton(desafio.get_respuestas()[2], callback_data="des3"))
	bt4 = (types.InlineKeyboardButton(desafio.get_respuestas()[3], callback_data="des4"))
	markup.add(bt1, bt2, bt3, bt4)

	return markup
