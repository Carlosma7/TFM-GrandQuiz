import sys
import os
sys.path.append(os.path.abspath('./src/grandquiz/core/'))

from jugador import Jugador
from equipo import Equipo
import pytest
from assertpy import assert_that

# Test comparación equipo
def test_compare_equipo():
	# Creación de dos equipos idénticos
	e1 = Equipo(1)
	e2 = Equipo(1)
	# Creación de un equipo distinto
	e3 = Equipo(2)
	# Comprobar que un equipo es igual a otro si tienen la misma información
	assert_that(e1).is_equal_to(e2) # Pasa test
	# Comprobar que un equipo es distinto de otro si tienen alguna información distinta
	assert_that(e1).is_not_equal_to(e3) # Pasa test

# Test añadir jugador
def test_add_jugador_equipo():
	# Creación de un equipo
	e = Equipo(1)
	# Comprobar que no posee jugadores
	assert_that(len(e.get_jugadores())).is_equal_to(0)
	# Crear jugador
	j = Jugador("Test", "Test")
	# Añadir jugador a equipo
	e.add_jugador(j.get_nombre_usuario())
	# Comprobar que posee un jugador
	assert_that(len(e.get_jugadores())).is_equal_to(1)

# Test pasar turno
def test_pasar_turno_equipo():
	# Creación de un equipo
	e = Equipo(1)
	# Comprobar que el turno inicial es 1
	assert_that(e.get_turno()).is_equal_to(1)
	# Pasar turno
	e.pasar_turno()
	# Comprobar que el turno ahora es 2
	assert_that(e.get_turno()).is_equal_to(2)

# Test acertar pregunta
def test_acertar_pregunta_equipo():
	# Creación de un equipo
	e = Equipo(1)
	# Comprobar que el primer jugador no ha acertado la categoría "Deporte"
	assert_that(e.get_puntuaciones()[0]["Deporte"]).is_equal_to(0)
	# Acertar la categoría "Deporte"
	e.acertar_pregunta("Deporte")
	# Comprobar que el primer jugador no ha acertado la categoría "Deporte"
	assert_that(e.get_puntuaciones()[0]["Deporte"]).is_equal_to(1)

# Test fallar pregunta
def test_fallar_pregunta_equipo():
	# Creación de un equipo
	e = Equipo(1)
	# Comprobar que el primer jugador no ha acertado la categoría "Deporte"
	assert_that(e.get_puntuaciones()[0]["Deporte"]).is_equal_to(0)
	# Acertar la categoría "Deporte"
	e.acertar_pregunta("Deporte")
	# Comprobar que el primer jugador no ha acertado la categoría "Deporte"
	assert_that(e.get_puntuaciones()[0]["Deporte"]).is_equal_to(1)
	# Fallar la categoria "Deporte"
	e.fallar_pregunta("Deporte")
	# Comprobar que el primer jugador no ha acertado la categoría "Deporte"
	assert_that(e.get_puntuaciones()[0]["Deporte"]).is_equal_to(0)

# Test obtener categoria
def test_obtener_categoria_equipo():
	# Creación de un equipo
	e = Equipo(1)
	# Definir lista de categorias
	categorias = ["Arte", "Geografía", "Ciencia", "Historia", "Deporte", "Entretenimiento"]
	# Obtener categoria
	cat = e.obtener_categoria()
	# Comprobar que se obtiene una de las categorias definidas en el juego
	assert_that(categorias).contains(cat)

# Test comprobar victoria
def test_comprobar_victoria_equipo():
	# Creación de un equipo
	e = Equipo(1)
	# Comprobar que al crearse un equipo no es ganador
	assert_that(e.comprobar_victoria()).is_false()
	# Establecer que el equipo posee todas las medallas de forma manual
	e.set_medallas({"Arte":1, "Geografía":1, "Ciencia":1, "Historia":1, "Deporte":1, "Entretenimiento":1})
	# Comprobar que al crearse un equipo es ganador
	assert_that(e.comprobar_victoria()).is_true()

# Test obtener jugador turno actual
def test_get_jugador_turno_equipo():
	# Creación de un equipo
	e = Equipo(1)
	# Crear jugador
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	# Añadir jugador a equipo
	e.add_jugador(j1.get_nombre_usuario())
	e.add_jugador(j2.get_nombre_usuario())
	# Comprobar que el jugador del turno es el jugador 1
	assert_that(e.get_jugador_turno()).is_equal_to(j1.get_nombre_usuario())