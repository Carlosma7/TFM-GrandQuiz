import sys
import os
sys.path.append(os.path.abspath('./src/grandquiz/core/'))

from duelo import Duelo
from jugador import Jugador
from pregunta import Pregunta
import pytest
from assertpy import assert_that

# Test comparación duelo
def test_compare_duelo():
	# Creación de dos duelos idénticos
	d1 = Duelo('Test')
	d2 = Duelo('Test')
	# Creación de un duelo distinto
	j1 = Jugador("Test", "Test")
	d3 = Duelo('Test')
	d3.set_chat2('Test2')
	# Comprobar que un duelo es igual a otro si tienen la misma información
	assert_that(d1).is_equal_to(d2) # Pasa test
	# Comprobar que un duelo es distinto de otro si tienen alguna información distinta
	assert_that(d1).is_not_equal_to(d3) # Pasa test

# Test de iniciar duelo
def test_iniciar_duelo():
	# Creación de un duelo
	d = Duelo('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	# Comprobar que el duelo no está iniciado
	assert_that(d.get_iniciada()).is_false()
	# Comprobar que el turno es cero (no iniciado)
	assert_that(d.get_turno()).is_equal_to(0)
	# Iniciar duelo
	d.iniciar_duelo()
	# Comprobar que el duelo está iniciado
	assert_that(d.get_iniciada()).is_true()
	# Comprobar que el turno es de un jugador (iniciada)
	assert_that(d.get_turno()).is_in(1,2)

# Test de acertar pregunta
def test_acertar_pregunta_duelo():
	# Creación de un duelo
	d = Duelo('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	# Iniciar duelo
	d.iniciar_duelo()
	# Comprobar que ningún equipo tiene un jugador con un punto en la categoría "Deporte"
	assert_that(d.get_puntuaciones()[0].get('Deporte')).is_equal_to(0)
	assert_that(d.get_puntuaciones()[1].get('Deporte')).is_equal_to(0)
	# Un jugador acierta una pregunta
	d.acertar_pregunta("Deporte")
	# Comprobar que el jugador del turno actual tiene un punto en la categoría "Deporte"
	assert_that(d.get_puntuaciones()[d.get_turno() - 1].get('Deporte')).is_equal_to(1)

# Test de fallar pregunta
def test_fallar_pregunta_duelo():
	# Creación de un duelo
	d = Duelo('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	# Iniciar duelo
	d.iniciar_duelo()
	# Comprobar que ningún equipo tiene un jugador con un punto en la categoría "Deporte"
	assert_that(d.get_puntuaciones()[0].get('Deporte')).is_equal_to(0)
	assert_that(d.get_puntuaciones()[1].get('Deporte')).is_equal_to(0)
	# Un jugador acierta una pregunta
	d.fallar_pregunta("Deporte")
	# Comprobar que el jugador del turno actual tiene un punto en la categoría "Deporte"
	assert_that(d.get_puntuaciones()[d.get_turno() - 1].get('Deporte')).is_equal_to(0)

# Test de pasar turno
def test_pasar_turno_duelo():
	# Creación de un duelo
	d = Duelo('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	# Iniciar duelo
	d.iniciar_duelo()
	# Obtener el turno
	turno = d.get_turno()
	# Comprobar que el turno es de un equipo (iniciada)
	assert_that(d.get_turno()).is_in(1,2)
	# Cambiar el turno
	turno = (turno % 2) + 1
	# Pasar turno
	d.pasar_turno()
	# Comprobar que el turno ha cambiado al otro jugador
	assert_that(d.get_turno()).is_equal_to(turno)

# Test de comprobar victoria
def test_comprobar_victoria_duelo():
	# Creación de un duelo
	d = Duelo('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	# Iniciar duelo
	d.iniciar_duelo()
	# Comprobar que no hay ningún ganador
	assert_that(d.comprobar_victoria()).is_false()
	# Forzar a que un equipo tenga todas las medallas de forma manual
	d.set_medallas([{"Arte":1, "Geografía":1, "Ciencia":1, "Historia":1, "Deporte":1, "Entretenimiento":1}, {"Arte":0, "Geografía":0, "Ciencia":0, "Historia":0, "Deporte":0, "Entretenimiento":0}])
	# Comprobar que hay un ganador
	assert_that(d.comprobar_victoria()).is_true()

# Test de obtener jugador del turno
def test_get_jugador_turno_duelo():
	# Creación de un duelo
	d = Duelo('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	# Se introducen los jugadores en la partida
	d.add_jugador(j1.get_nombre_usuario())
	d.add_jugador(j2.get_nombre_usuario())
	# Iniciar duelo
	d.iniciar_duelo()
	# Obtener el jugador con el turno
	jug = d.get_jugador_turno()
	# Comprobar que se obtiene el nombre de un jugador
	assert_that(jug).is_type_of(str)