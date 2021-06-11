import sys
import os
sys.path.append(os.path.abspath('./src/grandquiz/core/'))

from desafio import Desafio
import pytest
from assertpy import assert_that

# Test comparación desafio
def test_compare_desafio():
	# Creación de dos desafios idénticos
	d1 = Desafio("Test", "Enunciado", ["Respuesta1", "Respuesta2", "Respuesta3", "Respuesta4"], 3, "Justificacion")
	d2 = Desafio("Test", "Enunciado", ["Respuesta1", "Respuesta2", "Respuesta3", "Respuesta4"], 3, "Justificacion")
	# Creación de un desafio distinto
	d3 = Desafio("Test", "Enunciado", ["Respuesta1", "Respuesta2", "Respuesta3", "Respuesta4"], 1, "Justificacion")
	# Comprobar que un desafio es igual a otro si tienen la misma información
	assert_that(d1).is_equal_to(d2) # Pasa test
	# Comprobar que un desafio es distinta de otro si tienen alguna información distinta
	assert_that(d1).is_not_equal_to(d3) # Pasa test