import sys
import os
sys.path.append(os.path.abspath('./src/questions/core/'))

from partida import Partida
from jugador import Jugador
from pregunta import Pregunta
from puntuacion import Puntuacion
import pytest
from assertpy import assert_that

# Test comparación partida
def test_compare_partida():
	# Creación de dos partidas idénticas
	p1 = Partida()
	p2 = Partida()
	# Creación de una partida distinta
	j1 = Jugador("Carlosma7", "Carlos", 24)
	p3 = Partida()
	p3.add_jugador(j1)
	# Comprobar que una partida es igual a otra si tienen la misma información
	assert_that(p1).is_equal_to(p2) # Pasa test
	# Comprobar que una partida es distinta de otro si tienen alguna información distinta
	assert_that(p1).is_not_equal_to(p3) # Pasa test

# Test de añadir jugador a partida
def test_add_jugador():
	# Creación de una partida
	p = Partida()
	# Comprobar que la partida no tiene jugadores
	assert_that(p.get_jugadores()).is_length(0)
	# Se añade un jugador
	j1 = Jugador("Carlosma7", "Carlos", 24)
	p.add_jugador(j1)
	# Comprobar que la partida tiene un jugador
	assert_that(p.get_jugadores()).is_length(1)

# Test de iniciar partida
def test_iniciar_partida():
	# Creación de una partida
	p = Partida()
	# Añadir dos jugadores
	j1 = Jugador("Carlosma7", "Carlos", 24)
	j2 = Jugador("Pepito", "Pepe", 22)
	p.add_jugador(j1)
	p.add_jugador(j2)
	# Comprobar que la partida no está iniciada
	assert_that(p.get_iniciada()).is_false()
	# Comprobar que el turno es cero (no iniciada)
	assert_that(p.get_turno()).is_equal_to(0)
	# Iniciar partida
	p.iniciar_partida()
	# Comprobar que la partida está iniciada
	assert_that(p.get_iniciada()).is_true()
	# Comprobar que el turno es cero (no iniciada)
	assert_that(p.get_turno()).is_in(1,2)

# Test de acertar pregunta
def test_acertar_pregunta():
	# Creación de una partida
	p = Partida()
	# Añadir dos jugadores
	j1 = Jugador("Carlosma7", "Carlos", 24)
	j2 = Jugador("Pepito", "Pepe", 22)
	p.add_jugador(j1)
	p.add_jugador(j2)
	# Iniciar partida
	p.iniciar_partida()
	# Comprobar que ambos jugadores no tienen puntos
	assert_that(p.get_puntuaciones()[0].get_puntos()).is_equal_to(0)
	assert_that(p.get_puntuaciones()[1].get_puntos()).is_equal_to(0)
	# Un jugador acierta una pregunta
	p.acertar_pregunta()
	# Comprobar que uno de los dos tiene un punto
	assert_that(1).is_in(p.get_puntuaciones()[0].get_puntos(), p.get_puntuaciones()[1].get_puntos())