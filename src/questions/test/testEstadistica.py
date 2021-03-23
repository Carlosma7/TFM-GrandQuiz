import sys
import os
sys.path.append(os.path.abspath('./src/questions/core/'))

from estadistica import Estadistica
import pytest
from assertpy import assert_that

# Test comparación estadisticas
def test_compare_estadistica():
	# Creación de tres objetos estadistica idénticos
	e1 = Estadistica()
	e2 = Estadistica()
	e3 = Estadistica()
	# Las dos primeras ganan partida y la última pierde
	e1.add_num_victorias()
	e2.add_num_victorias()
	e3.add_num_derrotas()
	# Comprobar que un objeto estadistica es igual a otro si tienen la misma información
	assert_that(e1).is_equal_to(e2) # Pasa test
	# Comprobar que un objeto estadistica es distinto de otro si tienen alguna información distinta
	assert_that(e1).is_not_equal_to(e3) # Pasa test