import sys
import os
sys.path.append(os.path.abspath('./src/grandquiz/core/'))

from pregunta import Pregunta
import pytest
from assertpy import assert_that

# Test comparación pregunta
def test_compare_pregunta():
	# Creación de dos preguntas idénticas
	p1 = Pregunta("Arte", "Enunciado", ["Respuesta1", "Respuesta2", "Respuesta3", "Respuesta4"], 3)
	p2 = Pregunta("Arte", "Enunciado", ["Respuesta1", "Respuesta2", "Respuesta3", "Respuesta4"], 3)
	# Creación de una pregunta distinta
	p3 = Pregunta("Deporte", "Enunciado", ["Respuesta1", "Respuesta2", "Respuesta3", "Respuesta4"], 1)
	# Comprobar que una pregunta es igual a otro si tienen la misma información
	assert_that(p1).is_equal_to(p2) # Pasa test
	# Comprobar que una pregunta es distinta de otra si tienen alguna información distinta
	assert_that(p1).is_not_equal_to(p3) # Pasa test