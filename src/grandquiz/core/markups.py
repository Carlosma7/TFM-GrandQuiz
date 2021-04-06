import telebot
from telebot import types

# Markups Bot API
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
