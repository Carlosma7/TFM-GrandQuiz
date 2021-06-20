# Not enough players for a game
class NotEnoughPlayersError(Exception):
	"""Raised when there isnt enough players to start a game"""
	pass

# Team list full
class TeamFullError(Exception):
	"""Raised when the list of players for a team in game is full"""
	pass

# Game is not started
class GameNotStartedError(Exception):
	"""Raised when the game has not started yet"""
	pass

# The email of a player is not valid
class EmailNotValidError(Exception):
	"""Raised when the email of a player doesnt follow standarized format"""
	pass

# Theres already a game in the group chat
class ExistingGameError(Exception):
	"""Raised when theres already a game in the group chat"""
	pass

# Player has already joined the game
class PlayerInGameError(Exception):
	"""Raised when the player tries to join a game that has previously joined"""
	pass

# Tries to join a game that doesnt exist
class GameNotFoundError(Exception):
	"""Raised when the player tries to join a game that doesnt exist"""
	pass

# Player is not registered
class PlayerNotRegisteredError(Exception):
	"""Raised when a player tries to do something without being registered"""
	pass

# Player is already registered
class PlayerRegisteredError(Exception):
	"""Raised when a player tries to register again"""
	pass

# The game is already started
class GameStartedError(Exception):
	"""Raised when a player tries to start a game that is already started"""
	pass

# A player tries to answer but it isnt his turn
class WrongTurnError(Exception):
	"""Raised when a player tries to answer a question but it isnt hist turn"""
	pass

# A player tries to use a challenge that has used previously
class ChallengeAlreadyUsed(Exception):
	"""Raised when a player tries to use a challenge but he has used it before"""
	pass