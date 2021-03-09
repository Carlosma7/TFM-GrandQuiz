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

# List of tables
tables = []

# Class Table of Tic Tac Toe
class Table:
	# Table init
	def __init__(self, chat):
		self.__table = self.generate_table()
		self.__chat = chat

	# Get chat ID
	def get_chat(self):
		return self.__chat

	# Generate new table
	def generate_table(self):
		self.__table = [[" ", " ", " "], 
					[" ", " ", " "],
					[" ", " ", " "]]
		return self.__table

	# Get game table into string
	def get_table(self):
		table = ''
		# Iterate over table
		for i in range(0,3):
			table = table + '|'
			for j in range(0,3):
				# Get each element
				table = table + str(self.__table[i][j]) + '|'
			table = table + '\n'
		return table

	# Get position of table
	def get_position(self, position):
		# Flatten as vector
		table = np.matrix(self.__table).flatten()
		return table[0, position]

	# Set position if possible
	def set_position(self, position, player):
		x = int(position[0])
		y = int(position[1])
		# If position is empty
		if self.__table[x][y] == ' ':
			self.__table[x][y] = player
			return True
		else:
			return False

	# Random bot position picker
	def set_bot_position(self):
		position = False
		# Until it chooses an empty position
		while not position:
			x = randint(0,2)
			y = randint(0,2)
			position = self.set_position(f"{x}{y}", 'O')

	# Get winner of the game
	def get_winner(self):
		# Possible groups
		positions_groups = (
			[[(x, y) for y in range(3)] for x in range(3)] + # horizontals
			[[(x, y) for x in range(3)] for y in range(3)] + # verticals
			[[(d, d) for d in range(3)]] + # diagonal from top-left to bottom-right
			[[(2-d, d) for d in range(3)]] # diagonal from top-right to bottom-left
		)

		# Check all positions in groups
		for positions in positions_groups:
			values = [self.__table[x][y] for (x, y) in positions]
			if len(set(values)) == 1 and values[0]:
				# Return winner or None
				return values[0]

	# Check if theres a draw
	def check_draw(self):
		# If theres not an empty space
		for x in self.__table:
			if " " in x:
				return False
		return True

# Chat markup for table picker
def get_markup(table):
	# Keyboard
	markup = types.InlineKeyboardMarkup(row_width = 3)
	# Buttons
	bt1 = (types.InlineKeyboardButton(table.get_position(0), callback_data="00"))
	bt2 = (types.InlineKeyboardButton(table.get_position(1), callback_data="01"))
	bt3 = (types.InlineKeyboardButton(table.get_position(2), callback_data="02"))
	bt4 = (types.InlineKeyboardButton(table.get_position(3), callback_data="10"))
	bt5 = (types.InlineKeyboardButton(table.get_position(4), callback_data="11"))
	bt6 = (types.InlineKeyboardButton(table.get_position(5), callback_data="12"))
	bt7 = (types.InlineKeyboardButton(table.get_position(6), callback_data="20"))
	bt8 = (types.InlineKeyboardButton(table.get_position(7), callback_data="21"))
	bt9 = (types.InlineKeyboardButton(table.get_position(8), callback_data="22"))
	markup.add(bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9)

	return markup

# Start and Help commands as bot welcome
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, f"Hola! Soy el Bot de tu TFM!\nPara jugar dímelo usando el comando '/jugar'")

# Jugar command as game start
@bot.message_handler(commands=['jugar'])
def start_game(message):
	bot.reply_to(message, f"Vamos a jugar al 3 en raya! Empiezas tú")
	
	# Check for previous games and remove table
	table = [t for t in tables if t.get_chat() == message.chat.id]
	if table != []:
		pos = tables.index(table[0])
		tables.pop(pos)

	# Create new table and store it
	table = Table(message.chat.id)
	tables.append(table)
	bot.send_message(message.chat.id, table.get_table(), reply_markup=get_markup(table))

# Inline query callback handler for buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
		if call.message:
			# Check for the game
			table = [t for t in tables if t.get_chat() == call.message.chat.id][0]
			# Try to set a position
			if table.set_position(call.data, "X"):
				# Check if player is winner
				winner = table.get_winner()
				# If winner
				if winner == 'X':
					# Congratulate player
					bot.send_message(call.message.chat.id, table.get_table())
					bot.send_message(call.message.chat.id, "ENHORABUENA ME HAS GANADO!")
				else:
					# Check if theres a draw
					if table.check_draw():
						# Recognize player
						bot.send_message(call.message.chat.id, "Acepto el empate, eres un rival a mi altura.")
					else:
						# Bot turn
						bot.send_message(call.message.chat.id, "Ok, me toca!")
						# Set bot position
						table.set_bot_position()
						# Check if bot is winner
						winner = table.get_winner()
						# If winner
						if winner == 'O':
							# Mock player
							bot.send_message(call.message.chat.id, table.get_table())
							bot.send_message(call.message.chat.id, "JA! TE GANÉ! SOY INVENCIIIBLEEEEE!")
						else:
							# Check if theres a draw
							if table.check_draw():
								# Recognize player
								bot.send_message(call.message.chat.id, "Acepto el empate, eres un rival a mi altura.")
							else:
								# Players turn
								bot.send_message(call.message.chat.id, table.get_table(), reply_markup=get_markup(table))
			else:
				# Warn player position chosen is not empty
				bot.send_message(call.message.chat.id, "Esa posición ya está ocupada!")
				bot.send_message(call.message.chat.id, table.get_table(), reply_markup=get_markup(table))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	user = message.from_user.first_name
	bot.send_message(message.chat.id, f"{user} ha dicho: '{message.text}'")

# Launch bot
bot.polling()
