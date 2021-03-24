import sys
import os
sys.path.append(os.path.abspath('./src/questions/core/'))

from puntuacion import Puntuacion
from jugador import Jugador
import pytest
from assertpy import assert_that

# Test comparación puntuacion
def test_compare_puntuacion():
	# Creación de un único jugador
	j1 = Jugador("Carlosma7", "Carlos", 24)
	# Creación de dos puntuaciones idénticas
	p1 = Puntuacion(j1)
	p2 = Puntuacion(j1)
	# Creación de una puntuación distinta
	p3 = Puntuacion(j1)
	p3.anotar_punto()
	# Comprobar que una puntuación es igual a otro si tienen la misma información
	assert_that(p1).is_equal_to(p2) # Pasa test
	# Comprobar que una puntuación es distinta de otra si tienen alguna información distinta
	assert_that(p1).is_not_equal_to(p3) # Pasa test