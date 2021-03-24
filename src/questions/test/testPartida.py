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