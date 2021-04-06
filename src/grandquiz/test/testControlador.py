import sys
import os
sys.path.append(os.path.abspath('./src/grandquiz/core/'))

from controlador import *
import pytest
from assertpy import assert_that

# Test de creación de jugador
def test_registrar_jugador_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Test", "Test")
	# Comprobar que no existe el usuario en BD
	assert_that(c.mongo.jugadores.find({'nombre_usuario':j1.get_nombre_usuario()}).count()).is_equal_to(0)
	# Crear administrador
	c.registrar_jugador(j1)
	# Comprobar que existe el usuario en BD
	assert_that(c.mongo.jugadores.find({'nombre_usuario':j1.get_nombre_usuario()}).count()).is_equal_to(1)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})

# Test de cambiar avatar de jugador
def test_cambiar_avatar_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Test2", "Test")
	# Crear administrador
	c.registrar_jugador(j1)
	# Comprobar que el jugador no tiene avatar
	assert_that(j1.get_avatar()).is_equal_to("")
	# Cambiar avatar usuario
	c.cambiar_avatar(j1.get_nombre_usuario(), "avatar")
	# Obtener el jugador de la BD
	j2 = c.mongo.jugadores.find_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Comprobar que el avatar ha cambiado
	assert_that(j2.get('avatar')).is_not_equal_to("")
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})