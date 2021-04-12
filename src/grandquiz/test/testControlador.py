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
	# Comprobar que no existe estadística del usuario en BD
	assert_that(c.mongo.estadisticas.find({'nombre_usuario':j1.get_nombre_usuario()}).count()).is_equal_to(0)
	# Crear administrador
	c.registrar_jugador(j1)
	# Comprobar que existe el usuario en BD
	assert_that(c.mongo.jugadores.find({'nombre_usuario':j1.get_nombre_usuario()}).count()).is_equal_to(1)
	# Comprobar que existe el usuario en BD
	assert_that(c.mongo.estadisticas.find({'nombre_usuario':j1.get_nombre_usuario()}).count()).is_equal_to(1)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})

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
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})

# Test de cambiar edad de jugador
def test_cambiar_edad_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Test3", "Test")
	# Crear administrador
	c.registrar_jugador(j1)
	# Comprobar que el jugador no tiene edad
	assert_that(j1.get_edad()).is_equal_to("")
	# Cambiar edad usuario
	c.cambiar_edad(j1.get_nombre_usuario(), "edad")
	# Obtener el jugador de la BD
	j2 = c.mongo.jugadores.find_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Comprobar que la edad ha cambiado
	assert_that(j2.get('edad')).is_not_equal_to("")
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})

# Test de cambiar correo electrónico de jugador
def test_cambiar_email_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Test4", "Test")
	# Crear administrador
	c.registrar_jugador(j1)
	# Comprobar que el jugador no tiene email
	assert_that(j1.get_edad()).is_equal_to("")
	# Cambiar email usuario
	c.cambiar_email(j1.get_nombre_usuario(), "email@gmail.com")
	# Obtener el jugador de la BD
	j2 = c.mongo.jugadores.find_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Comprobar que el email ha cambiado
	assert_that(j2.get('email')).is_not_equal_to("")
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})

# Test de obtener jugador
def test_obtener_estadisticas_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Test5", "Test")
	# Crear administrador
	c.registrar_jugador(j1)
	# Obtener las estadisticas
	j2 = c.obtener_jugador("Test5")
	# Comprobar que e1 es un objeto de Estadistica
	assert_that(j2).is_type_of(Jugador)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})

# Test de obtener estadisticas de jugador
def test_obtener_estadisticas_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Test6", "Test")
	# Crear administrador
	c.registrar_jugador(j1)
	# Obtener las estadisticas
	e1 = c.obtener_estadisticas("Test6")
	# Comprobar que e1 es un objeto de Estadistica
	assert_that(e1).is_type_of(Estadistica)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})