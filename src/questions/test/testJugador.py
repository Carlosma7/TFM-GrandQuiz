import sys
import os
sys.path.append(os.path.abspath('./src/questions/core/'))

from jugador import Jugador
import pytest
from assertpy import assert_that

# Test comparación jugador
def test_compare_jugador():
	# Creación de dos jugadores idénticos
	j1 = Jugador("Carlosma7", "Carlos", 24)
	j2 = Jugador("Carlosma7", "Carlos", 24)
	# Creación de un jugador distinto
	j3 = Jugador("Carlosma7", "Fernando", 24)
	# Comprobar que un jugador es igual a otro si tienen la misma información
	assert_that(j1).is_equal_to(j2) # Pasa test
	# Comprobar que un jugador es distinto de otro si tienen alguna información distinta
	assert_that(j1).is_not_equal_to(j3) # Pasa test