import sys
import os
sys.path.append(os.path.abspath('./src/grandquiz/core/'))

from logros import Logro
import pytest
from assertpy import assert_that

# Test comparación estadisticas
def test_compare_logros():
	# Creación de tres objetos estadistica idénticos
	l1 = Logro("Test")
	l2 = Logro("Test")
	l3 = Logro("Test")
	# El tercer jugador obtiene un logro de victorias
	l3.update_logro_victorias(10)
	# Comprobar que un objeto logro es igual a otro si tienen la misma información
	assert_that(l1).is_equal_to(l2) # Pasa test
	# Comprobar que un objeto logro es distinto de otro si tienen alguna información distinta
	assert_that(l1).is_not_equal_to(l3) # Pasa test