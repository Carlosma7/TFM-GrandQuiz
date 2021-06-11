import sys
import os
sys.path.append(os.path.abspath('./src/grandquiz/core/'))

from partida import Partida
from jugador import Jugador
from equipo import Equipo
from pregunta import Pregunta
import pytest
from assertpy import assert_that

# Test comparación partida
def test_compare_partida():
	# Creación de dos partidas idénticas
	p1 = Partida('Test')
	p2 = Partida('Test')
	# Creación de una partida distinta
	j1 = Jugador("Test", "Test")
	p3 = Partida('Test')
	p3.add_jugador(j1.get_nombre_usuario(), 1)
	# Comprobar que una partida es igual a otra si tienen la misma información
	assert_that(p1).is_equal_to(p2) # Pasa test
	# Comprobar que una partida es distinta de otro si tienen alguna información distinta
	assert_that(p1).is_not_equal_to(p3) # Pasa test

# Test de añadir jugador a partida
def test_add_jugador_partida():
	# Creación de una partida
	p = Partida('Test')
	# Comprobar el equipo 1 de la partida no tiene jugadores
	assert_that(p.get_equipos()[0].get_jugadores()).is_length(0)
	# Se añade un jugador
	j1 = Jugador("Test", "Test")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	# Comprobar que la partida tiene un jugador
	assert_that(p.get_equipos()[0].get_jugadores()).is_length(1)

# Test de iniciar partida
def test_iniciar_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Comprobar que la partida no está iniciada
	assert_that(p.get_iniciada()).is_false()
	# Comprobar que el turno es cero (no iniciada)
	assert_that(p.get_turno()).is_equal_to(0)
	# Iniciar partida
	p.iniciar_partida()
	# Comprobar que la partida está iniciada
	assert_that(p.get_iniciada()).is_true()
	# Comprobar que el turno es de un jugador (iniciada)
	assert_that(p.get_turno()).is_in(1,2)

# Test de acertar pregunta
def test_acertar_pregunta_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Iniciar partida
	p.iniciar_partida()
	# Comprobar que ningún equipo tiene un jugador con un punto en la categoría "Deporte"
	assert_that(p.get_equipos()[0].get_puntuaciones()[0].get('Deporte')).is_equal_to(0)
	assert_that(p.get_equipos()[0].get_puntuaciones()[1].get('Deporte')).is_equal_to(0)
	assert_that(p.get_equipos()[1].get_puntuaciones()[0].get('Deporte')).is_equal_to(0)
	assert_that(p.get_equipos()[1].get_puntuaciones()[1].get('Deporte')).is_equal_to(0)
	# Un jugador acierta una pregunta
	p.acertar_pregunta("Deporte")
	# Comprobar que el jugador del turno actual tiene un punto en la categoría "Deporte"
	assert_that(p.get_equipos()[p.get_turno() - 1].get_puntuaciones()[0].get('Deporte')).is_equal_to(1)

# Test de fallar pregunta
def test_fallar_pregunta_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Iniciar partida
	p.iniciar_partida()
	# Un jugador acierta una pregunta de la categoría "Deporte"
	p.acertar_pregunta("Deporte")
	# Comprobar que el jugador del turno actual tiene un punto en la categoría "Deporte"
	assert_that(p.get_equipos()[p.get_turno() - 1].get_puntuaciones()[0].get('Deporte')).is_equal_to(1)
	# El mismo jugador falla una pregunta de la categoría "Deporte"
	p.fallar_pregunta("Deporte")
	# Comprobar que el jugador del turno actual ya no tiene un punto en la categoría "Deporte"
	assert_that(p.get_equipos()[p.get_turno() - 1].get_puntuaciones()[0].get('Deporte')).is_equal_to(0)

# Test de pasar turno
def test_pasar_turno_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Iniciar partida
	p.iniciar_partida()
	# Obtener el turno
	turno = p.get_turno()
	# Comprobar que el turno es de un equipo (iniciada)
	assert_that(p.get_turno()).is_in(1,2)
	# Cambiar el turno
	turno = (turno % 2) + 1
	# Pasar turno
	p.pasar_turno()
	# Comprobar que el turno ha cambiado al otro jugador
	assert_that(p.get_turno()).is_equal_to(turno)

# Test de comprobar victoria
def test_comprobar_victoria_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Iniciar partida
	p.iniciar_partida()
	# Comprobar que no hay ningún ganador
	assert_that(p.comprobar_victoria()).is_false()
	# Forzar a que un equipo tenga todas las medallas de forma manual
	p.get_equipos()[0].set_medallas({"Arte":1, "Geografía":1, "Ciencia":1, "Historia":1, "Deporte":1, "Entretenimiento":1})
	# Comprobar que hay un ganador
	assert_that(p.comprobar_victoria()).is_true()

# Test de obtener jugador del turno
def test_get_jugador_turno_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Iniciar partida
	p.iniciar_partida()
	# Obtener el jugador con el turno
	jug = p.get_jugador_turno()
	# Comprobar que se obtiene el nombre de un jugador
	assert_that(jug).is_type_of(str)
	# Comprobar que el jugador es el jugador 1 del equipo 1 o 2 (j1 o j3)
	assert_that([j1.get_nombre_usuario(), j3.get_nombre_usuario()]).contains(jug)

# Test de obtener equipo del turno
def test_get_equipo_turno_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Iniciar partida
	p.iniciar_partida()
	# Obtener el jugador con el turno
	equi = p.get_equipo_turno()
	# Comprobar que se obtiene el nombre de un jugador
	assert_that(equi).is_type_of(Equipo)
	# Comprobar que el jugador es el jugador 1 del equipo 1 o 2 (j1 o j3)
	assert_that(p.get_equipos()).contains(equi)

# Test de acertar desafio
def test_acertar_desafio_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Iniciar partida
	p.iniciar_partida()
	# Comprobar que ningún equipo tiene un jugador con un punto en la categoría "Deporte"
	assert_that(p.get_equipos()[0].get_puntuaciones()[0].get('Deporte')).is_equal_to(0)
	assert_that(p.get_equipos()[0].get_puntuaciones()[1].get('Deporte')).is_equal_to(0)
	assert_that(p.get_equipos()[1].get_puntuaciones()[0].get('Deporte')).is_equal_to(0)
	assert_that(p.get_equipos()[1].get_puntuaciones()[1].get('Deporte')).is_equal_to(0)
	# Un jugador acierta una pregunta
	p.acertar_desafio("Deporte")
	# Comprobar que el jugador del turno actual tiene un punto en la categoría "Deporte"
	assert_that(p.get_equipos()[p.get_turno() - 1].get_puntuaciones()[0].get('Deporte')).is_equal_to(1)

# Test de fallar desafio
def test_fallar_desafio_partida():
	# Creación de una partida
	p = Partida('Test')
	# Añadir cuatro jugadores
	j1 = Jugador("Test", "Test")
	j2 = Jugador("Test2", "Test2")
	j3 = Jugador("Test3", "Test3")
	j4 = Jugador("Test4", "Test4")
	p.add_jugador(j1.get_nombre_usuario(), 1)
	p.add_jugador(j2.get_nombre_usuario(), 1)
	p.add_jugador(j3.get_nombre_usuario(), 2)
	p.add_jugador(j4.get_nombre_usuario(), 2)
	# Iniciar partida
	p.iniciar_partida()
	# Un jugador acierta una pregunta de la categoría "Deporte"
	p.acertar_desafio("Deporte")
	# Comprobar que el jugador del turno actual tiene un punto en la categoría "Deporte"
	assert_that(p.get_equipos()[p.get_turno() - 1].get_puntuaciones()[0].get('Deporte')).is_equal_to(1)
	# El mismo jugador falla una pregunta de la categoría "Deporte"
	p.fallar_desafio("Deporte")
	# Comprobar que el jugador del turno actual ya no tiene un punto en la categoría "Deporte"
	assert_that(p.get_equipos()[p.get_turno() - 1].get_puntuaciones()[0].get('Deporte')).is_equal_to(0)