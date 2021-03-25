from partida import Partida
from jugador import Jugador
from pregunta import Pregunta
from puntuacion import Puntuacion
from excepciones import *

from typing import List

# Clase controladora
class Controlador():
	# Listas de entidades
	jugadores : List[Jugador] = []
	partidas : List[Partida] = []

	# Crear jugador
	def crear_jugador(self, jugador: Jugador):
		# Comprobar que no existe un jugador con el mismo nick de Telegram
		jug = [j for j in self.jugadores if j.get_nombre_usuario() == jugador.get_nombre_usuario()]
		no_encontrado = (len(jug) == 0)

		# Si no existe
		if no_encontrado:
			# Se comprueba una edad válida
			if jugador.get_edad() in range(6, 99):
				# Se añade el jugador
				self.jugadores.append(jugador)
			else:
				raise AgeNotValidError('La edad indicada no es válida.')
		else:
			raise ExistingGameError('Ya estás registrado.')

	# Crear partida
	def crear_partida(self, partida: Partida):
		# Comprobar que no existe una partida en el mismo grupo
		par = [p for p in self.partidas if p.get_chat() == partida.get_chat()]
		no_encontrada = (len(par) == 0)

		# Si no existe
		if no_encontrada:
			# Se añade la partida
			self.partidas.append(partida)
		else:
			raise ExistingGameError('Ya existe una partida en este grupo.')

