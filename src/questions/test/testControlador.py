import sys
import os
sys.path.append(os.path.abspath('./src/questions/core/'))

from controlador import *
import pytest
from assertpy import assert_that

# Test de creación de jugador
def test_crear_jugador_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Carlosma7", "Carlos", 24)
	# Comprobar que no existe el jugador
	assert_that(c.jugadores).does_not_contain(j1)
	# Crear jugador
	c.crear_jugador(j1)
	# Comprobar que existe el jugador
	assert_that(c.jugadores).contains(j1)

# Test de creación de jugador
def test_crear_partida_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto partida
	p = Partida('Chat')
	# Comprobar que no existe la partida
	assert_that(c.partidas).does_not_contain(p)
	# Crear partida
	c.crear_partida(p)
	# Comprobar que existe la partida
	assert_that(c.partidas).contains(p)

# Test de añadir jugador a partida
def test_add_jugador_partida_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Carlosma8", "Carlos", 24)
	# Crear jugador
	c.crear_jugador(j1)

	# Crear objeto partida
	p = Partida('Chat2')
	# Crear partida
	c.crear_partida(p)

	# Comprobar que la partida no tiene ningún jugador
	assert_that(c.partidas[-1].get_jugadores()).is_length(0)
	# Añadir jugador a la partida
	c.add_jugador('Chat2', 'Carlosma8')
	# Comprobar que la partida tiene un jugador
	assert_that(c.partidas[-1].get_jugadores()).is_length(1)

# Test de listar jugadores de una partida
def test_listar_jugadores_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Carlosma9", "Carlos", 24)
	# Crear jugador
	c.crear_jugador(j1)

	# Crear objeto partida
	p = Partida('Chat3')
	# Crear partida
	c.crear_partida(p)

	# Añadir jugador a la partida
	c.add_jugador('Chat3', 'Carlosma9')

	# Obtener lista de jugadores de la partida
	lista_jugadores = c.listar_jugadores('Chat3')
	# Comprobar que el objeto es una lista
	assert_that(lista_jugadores).is_type_of(list)
	# Comprobar que el contenido son objetos de tipo jugador
	assert_that(lista_jugadores[0]).is_type_of(Jugador)

# Test de iniciar una partida
def test_iniciar_partida_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Carlosma0", "Carlos", 24)
	j2 = Jugador("Pepito0", "Pepe", 23)
	# Crear jugador
	c.crear_jugador(j1)
	c.crear_jugador(j2)

	# Crear objeto partida
	p = Partida('Chat4')
	# Crear partida
	c.crear_partida(p)

	# Añadir jugador a la partida
	c.add_jugador('Chat4', 'Carlosma0')
	c.add_jugador('Chat4', 'Pepito0')

	# Comprobar que la partida no está iniciada
	assert_that(c.partidas[-1].get_turno()).is_equal_to(0)
	assert_that(c.partidas[-1].get_iniciada()).is_false()
	# Se inicia la partida
	c.iniciar_partida('Chat4')
	# Comprobar que la partida está iniciada
	assert_that(c.partidas[-1].get_turno()).is_in(1,2)
	assert_that(c.partidas[-1].get_iniciada()).is_true()

# Test de responder pregunta
def test_responder_pregunta_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Carlosma01", "Carlos", 24)
	j2 = Jugador("Pepito01", "Pepe", 23)
	# Crear jugador
	c.crear_jugador(j1)
	c.crear_jugador(j2)

	# Crear objeto partida
	p = Partida('Chat5')
	# Crear partida
	c.crear_partida(p)

	# Añadir jugador a la partida
	c.add_jugador('Chat5', 'Carlosma01')
	c.add_jugador('Chat5', 'Pepito01')

	# Se inicia la partida
	jug, pregunta = c.iniciar_partida('Chat5')

	# Responder pregunta
	resultado = c.responder_pregunta('Chat5', 'Carlosma01', 1)
	# Comprobar que si la respuesta es correcta el resultado es True
	if c.partidas[-1].get_pregunta_actual().get_correcta() == 1:
		assert_that(resultado).is_true()
	# Comprobar que si la respuesta es incorrecta el resultado es False
	else:
		assert_that(resultado).is_false()