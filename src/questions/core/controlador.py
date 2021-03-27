from partida import Partida
from jugador import Jugador
from pregunta import Pregunta
from puntuacion import Puntuacion
from estadistica import Estadistica
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
			raise PlayerRegisteredError('Ya estás registrado.')

	# Crear partida
	def crear_partida(self, partida: Partida, jugador: str):
		# Comprobar que el jugador ya se ha registrado
		jug = [j for j in self.jugadores if j.get_nombre_usuario() == jugador]
		jugador_encontrado = (len(jug) == 1)

		if jugador_encontrado:
			# Comprobar que no existe una partida en el mismo grupo
			par = [p for p in self.partidas if p.get_chat() == partida.get_chat()]
			no_encontrada = (len(par) == 0)

			# Si no existe
			if no_encontrada:
				# Se añade la partida
				self.partidas.append(partida)
			else:
				raise ExistingGameError('Ya existe una partida en este grupo.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Añadir jugador a partida
	def add_jugador(self, partida: str, jugador: str):
		# Comprobar que el jugador ya se ha registrado
		jug = [j for j in self.jugadores if j.get_nombre_usuario() == jugador]
		jugador_encontrado = (len(jug) == 1)

		# Si está registrado
		if jugador_encontrado:
			# Comprobar que existe una partida en el grupo
			par = [p for p in self.partidas if p.get_chat() == partida]
			partida_encontrada = (len(par) == 1)

			# Si existe una partida
			if partida_encontrada:
				jug = jug[0]
				par = par[0]

				# Comprobar que hay huecos disponibles
				if len(par.get_jugadores()) < 2:
					# Comprobar que el jugador no está en la partida
					if jug not in par.get_jugadores():
						# Hay huecos disponibles
						par.add_jugador(jug)
					else:
						raise PlayerInGameError('Ya estás apuntado en la partida.')
				else:
					raise GameFullError('Ya hay dos jugadores inscritos para la partida.')
			else:
				raise GameNotFoundError('No existe ninguna partida creada.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Listar jugadores de la partida
	def listar_jugadores(self, partida: str):
		# Comprobar que existe una partida en el grupo
		par = [p for p in self.partidas if p.get_chat() == partida]
		partida_encontrada = (len(par) == 1)

		# Si existe una partida
		if partida_encontrada:
			par = par[0]
			return par.get_jugadores()
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Iniciar partida
	def iniciar_partida(self, partida: str):
		# Comprobar que existe una partida en el grupo
		par = [p for p in self.partidas if p.get_chat() == partida]
		partida_encontrada = (len(par) == 1)

		# Si existe una partida
		if partida_encontrada:
			par = par[0]
			# Comprobar que la partida tiene dos jugadores
			if len(par.get_jugadores()) == 2:
				# Comprobar que la partida no está iniciada
				if not par.get_iniciada():
					par.iniciar_partida()
					par.add_preguntas()
					return par.get_jugador_turno(), par.realizar_pregunta()
				else:
					raise GameStartedError('Ya hay una partida iniciada en este grupo.')
			else:
				raise NotEnoughPlayersError('Se necesitan 2 jugadores para empezar una partida.')

	# Responder pregunta
	def responder_pregunta(self, partida: str, jugador: str, respuesta: int):
		# Comprobar que el jugador ya se ha registrado
		jug = [j for j in self.jugadores if j.get_nombre_usuario() == jugador]
		jugador_encontrado = (len(jug) == 1)

		# Si está registrado
		if jugador_encontrado:
			# Comprobar que existe una partida en el grupo
			par = [p for p in self.partidas if p.get_chat() == partida]
			partida_encontrada = (len(par) == 1)

			# Si existe una partida
			if partida_encontrada:
				jug = jug[0]
				par = par[0]

				# Comprobar que responde el jugador del turno actual
				if par.get_jugadores()[par.get_turno() - 1].get_nombre_usuario() == jugador:
					# Responder la pregunta
					if par.responder_pregunta(respuesta):
						par.get_puntuaciones()[par.get_turno() - 1].anotar_punto()
						return True
					else:
						return False
				else:
					raise WrongTurnError(f'Es el turno de {par.get_jugadores()[par.get_turno() - 1].get_nombre()}')
			else:
				raise GameNotFoundError('No existe ninguna partida creada.')
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')

	# Obtener respuesta de la pregunta actual de una partida
	def obtener_respuesta(self, partida: str):
		# Comprobar que existe una partida en el grupo
		par = [p for p in self.partidas if p.get_chat() == partida]
		partida_encontrada = (len(par) == 1)

		if partida_encontrada:
			par = par[0]
			return par.get_pregunta_actual().get_respuesta()
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Cambiar turno de una partida
	def cambiar_turno(self, partida: str):
		# Comprobar que existe una partida en el grupo
		par = [p for p in self.partidas if p.get_chat() == partida]
		partida_encontrada = (len(par) == 1)

		if partida_encontrada:
			par = par[0]
			par.pasar_turno()
			# Devolver siguiente pregunta
			return par.get_jugador_turno(), par.realizar_pregunta()
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Comprobar victoria en una partida
	def comprobar_victoria(self, partida: str):
		# Comprobar que existe una partida en el grupo
		par = [p for p in self.partidas if p.get_chat() == partida]
		partida_encontrada = (len(par) == 1)

		if partida_encontrada:
			par = par[0]
			# Comprobar si algún jugador ha ganado
			return par.comprobar_victoria()
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Terminar partida y obtener ganador
	def terminar_partida(self, partida: str):
		# Comprobar que existe una partida en el grupo
		par = [p for p in self.partidas if p.get_chat() == partida]
		partida_encontrada = (len(par) == 1)

		if partida_encontrada:
			par = par[0]
			if par.terminar_partida():
				# Eliminar partida del grupo al estar finalizada
				self.partidas = [p for p in self.partidas if p.get_chat() != partida]
				# Obtener el nombre del ganador
				return par.get_jugadores()[par.get_ganador() - 1].get_nombre()
			else:
				raise GameNotFinishedError('No hay ningún ganador todavía.')
		else:
			raise GameNotFoundError('No existe ninguna partida creada.')

	# Obtener estadísticas de un jugador
	def obtener_estadisticas(self, jugador: str):
		# Comprobar que no existe un jugador con el mismo nick de Telegram
		jug = [j for j in self.jugadores if j.get_nombre_usuario() == jugador]
		encontrado = (len(jug) == 1)

		# Si existe
		if encontrado:
			jug = jug[0]
			# Se obtienen las estadisticas
			return jug.get_estadisticas()
		else:
			raise PlayerNotRegisteredError('No estás registrado en GrandQuiz.')