# Not enough players for a game
class NotEnoughPlayersError(Exception):
	"""Raised when there isnt enough players to start a game"""
	pass

# Game list full
class GameFullError(Exception):
	"""Raised when the list of players for a game is full"""
	pass

# Game has no winner and is called to be ended
class GameNotFinishedError(Exception):
	"""Raised when the game has no winner yet"""
	pass

# The age of a player is not valid
class AgeNotValidError(Exception):
	"""Raised when the age of a player is not between 6 and 99"""
	pass

# Theres already a game in the group chat
class ExistingGameError(Exception):
	"""Raised when theres already a game in the group chat"""
	pass