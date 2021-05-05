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
	# Crear jugador
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
	# Crear jugador
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
	# Crear jugador
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
	# Crear jugador
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
	# Crear jugador
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
	# Crear jugador
	c.registrar_jugador(j1)
	# Obtener las estadisticas
	e1 = c.obtener_estadisticas("Test6")
	# Comprobar que e1 es un objeto de Estadistica
	assert_that(e1).is_type_of(Estadistica)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})

# Test de crear partida en GrandQuiz
def test_crear_partida_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Test7", "Test")
	# Crear jugador
	c.registrar_jugador(j1)
	# Crear objeto partida
	p = Partida("Test")
	# Comprobar que no existe la partida en BD
	assert_that(c.mongo.partidas.find({'chat':p.get_chat()}).count()).is_equal_to(0)
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Comprobar que existe la partida en BD
	assert_that(c.mongo.partidas.find({'chat':p.get_chat()}).count()).is_equal_to(1)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de añadir jugador a partida en GrandQuiz
def test_add_jugador_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objeto jugador
	j1 = Jugador("Test8", "Test")
	# Crear jugador
	c.registrar_jugador(j1)
	# Crear objeto partida
	p = Partida("Test2")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Obtener partida creada
	partida = c.mongo.partidas.find_one({'chat': p.get_chat()})
	# Construir objeto Partida a partir de JSON
	partida = Partida.from_dict(partida)
	# Comprobar que no existe ningún jugador en el equipo 1 de la partida
	assert_that(partida.get_equipos()[0].get_jugadores()).is_length(0)
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Obtener nuevamente partida creada
	partida = c.mongo.partidas.find_one({'chat': p.get_chat()})
	# Construir objeto Partida a partir de JSON
	partida = Partida.from_dict(partida)
	# Comprobar que existe un jugador en el equipo 1 de la partida
	assert_that(partida.get_equipos()[0].get_jugadores()).is_length(1)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de obtener equipos de una partida en GrandQuiz
def test_obtener_equipos_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test9", "Test")
	# Crear jugadores
	c.registrar_jugador(j1)
	# Crear objeto partida
	p = Partida("Test3")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Obtener equipos
	equipos = c.obtener_equipos(p.get_chat(), j1.get_nombre_usuario())
	# Comprobar que se obtiene un objeto del tipo equipo
	assert_that(equipos[0]).is_type_of(Equipo)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de obtener equipos disponibles en GrandQuiz
def test_obtener_equipos_disponibles_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test10", "Test")
	j1.set_edad("edad0")
	j2 = Jugador("Test11", "Test")
	j2.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	# Crear objeto partida
	p = Partida("Test4")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Obtener equipos disponibles
	equipos_disponibles = c.obtener_equipos_disponibles(p.get_chat(), j1.get_nombre_usuario())
	# Comprobar que existen dos equipos disponibles
	assert_that(equipos_disponibles).is_length(2)
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Obtener equipos disponibles
	equipos_disponibles = c.obtener_equipos_disponibles(p.get_chat(), j1.get_nombre_usuario())
	# Comprobar que no existen dos equipos disponibles
	assert_that(equipos_disponibles).is_length(1)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de listar equipos en una partida de GrandQuiz
def test_listar_equipos_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test12", "Test")
	# Crear jugadores
	c.registrar_jugador(j1)
	# Crear objeto partida
	p = Partida("Test5")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Obtener lista de equipos y sus jugadores, junto a si esta completa o no
	lista, completa = c.listar_equipos(p.get_chat(), j1.get_nombre_usuario())
	# Comprobar que la lista es un String
	assert_that(lista).is_type_of(str)
	# Comprobar que no está completa la partida
	assert_that(completa).is_false()
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de iniciar una partida de GrandQuiz
def test_iniciar_partida_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test13", "Test")
	j1.set_edad("edad0")
	j2 = Jugador("Test14", "Test")
	j2.set_edad("edad1")
	j3 = Jugador("Test15", "Test")
	j3.set_edad("edad0")
	j4 = Jugador("Test16", "Test")
	j4.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	c.registrar_jugador(j3)
	c.registrar_jugador(j4)
	# Crear objeto partida
	p = Partida("Test6")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Añadir jugador 3 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j3.get_nombre_usuario(), 2)
	# Añadir jugador 4 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j4.get_nombre_usuario(), 2)
	# Comprobar que la partida no está iniciada
	assert_that(p.get_iniciada()).is_false()
	# Iniciar partida
	turno, ava_turno, equipo, pregunta, categoria = c.iniciar_partida(p.get_chat(), j1.get_nombre_usuario())
	# Obtener partida de la BD
	partida = c.mongo.partidas.find_one({'chat': p.get_chat()})
	# Convertir en objeto partida
	partida = Partida.from_dict(partida)
	# Comprobar que la partida está iniciada
	assert_that(partida.get_iniciada()).is_true()
	# Comprobar que se devuelve una pregunta
	assert_that(pregunta).is_type_of(Pregunta)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de responder pregunta
def test_responder_pregunta_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test17", "Test")
	j1.set_edad("edad0")
	j2 = Jugador("Test18", "Test")
	j2.set_edad("edad1")
	j3 = Jugador("Test19", "Test")
	j3.set_edad("edad0")
	j4 = Jugador("Test20", "Test")
	j4.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	c.registrar_jugador(j3)
	c.registrar_jugador(j4)
	# Crear objeto partida
	p = Partida("Test7")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Añadir jugador 3 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j3.get_nombre_usuario(), 2)
	# Añadir jugador 4 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j4.get_nombre_usuario(), 2)
	# Iniciar partida
	turno, ava_turno, equipo, pregunta, categoria = c.iniciar_partida(p.get_chat(), j1.get_nombre_usuario())
	# Obtener partida de la BD
	partida = c.mongo.partidas.find_one({'chat': p.get_chat()})
	# Convertir en objeto partida
	partida = Partida.from_dict(partida)
	# Obtener jugador del turno
	jug_turno = partida.get_jugador_turno()
	# Responder pregunta
	resultado = c.responder_pregunta(p.get_chat(), jug_turno, 1)
	# Comprobar que si la respuesta es correcta el resultado es True
	if partida.get_pregunta_actual().get_correcta() == 1:
		assert_that(resultado).is_true()
	# Comprobar que si la respuesta es incorrecta el resultado es False
	else:
		assert_that(resultado).is_false()
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de obtener respuesta
def test_obtener_respuesta_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test21", "Test")
	j1.set_edad("edad0")
	j2 = Jugador("Test22", "Test")
	j2.set_edad("edad1")
	j3 = Jugador("Test23", "Test")
	j3.set_edad("edad0")
	j4 = Jugador("Test24", "Test")
	j4.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	c.registrar_jugador(j3)
	c.registrar_jugador(j4)
	# Crear objeto partida
	p = Partida("Test8")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Añadir jugador 3 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j3.get_nombre_usuario(), 2)
	# Añadir jugador 4 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j4.get_nombre_usuario(), 2)
	# Iniciar partida
	turno, ava_turno, equipo, pregunta, categoria = c.iniciar_partida(p.get_chat(), j1.get_nombre_usuario())
	# Se obtiene la respuesta de la pregunta
	respuesta = c.obtener_respuesta(p.get_chat())
	# Se comprueba que la respuesta y la correcta de la pregunta coinciden
	assert_that(pregunta.get_respuesta()).is_equal_to(respuesta)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de cambiar turno
def test_cambiar_turno_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test25", "Test25")
	j1.set_edad("edad0")
	j2 = Jugador("Test26", "Test26")
	j2.set_edad("edad1")
	j3 = Jugador("Test27", "Test27")
	j3.set_edad("edad0")
	j4 = Jugador("Test28", "Test28")
	j4.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	c.registrar_jugador(j3)
	c.registrar_jugador(j4)
	# Crear objeto partida
	p = Partida("Test9")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Añadir jugador 3 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j3.get_nombre_usuario(), 2)
	# Añadir jugador 4 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j4.get_nombre_usuario(), 2)
	# Iniciar partida
	turno, ava_turno, equipo, pregunta, categoria = c.iniciar_partida(p.get_chat(), j1.get_nombre_usuario())
	# Cambiar el turno
	turno_nuevo, ava_turno, equipo_nuevo, pregunta_nueva, categoria = c.cambiar_turno(p.get_chat())
	# Comprobar que el jugador del turno no coincide
	assert_that(turno).is_not_equal_to(turno_nuevo)
	# Comprobar que el equipo no coincide
	assert_that(equipo).is_not_equal_to(equipo_nuevo)
	# Comprobar que la pregunta no coincide
	assert_that(pregunta).is_not_equal_to(pregunta_nueva)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de comprobar victoria
def test_comprobar_victoria_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test29", "Test")
	j1.set_edad("edad0")
	j2 = Jugador("Test30", "Test")
	j2.set_edad("edad1")
	j3 = Jugador("Test31", "Test")
	j3.set_edad("edad0")
	j4 = Jugador("Test32", "Test")
	j4.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	c.registrar_jugador(j3)
	c.registrar_jugador(j4)
	# Crear objeto partida
	p = Partida("Test10")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Añadir jugador 3 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j3.get_nombre_usuario(), 2)
	# Añadir jugador 4 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j4.get_nombre_usuario(), 2)
	# Iniciar partida
	turno, ava_turno, equipo, pregunta, categoria = c.iniciar_partida(p.get_chat(), j1.get_nombre_usuario())
	# Comprobar la victoria
	victoria, equipo_ganador = c.comprobar_victoria(p.get_chat())
	# Comprobar que aún no ha ganado nadie ya que se acaba de iniciar la partida
	assert_that(victoria).is_false()
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de obtener el nombre de los jugadores de un equipo
def test_obtener_jugadores_equipo_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test33", "Test")
	j1.set_edad("edad0")
	j2 = Jugador("Test34", "Test")
	j2.set_edad("edad1")
	j3 = Jugador("Test35", "Test")
	j3.set_edad("edad0")
	j4 = Jugador("Test36", "Test")
	j4.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	c.registrar_jugador(j3)
	c.registrar_jugador(j4)
	# Crear objeto partida
	p = Partida("Test11")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Añadir jugador 3 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j3.get_nombre_usuario(), 2)
	# Añadir jugador 4 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j4.get_nombre_usuario(), 2)
	# Iniciar partida
	turno, ava_turno, equipo, pregunta, categoria = c.iniciar_partida(p.get_chat(), j1.get_nombre_usuario())
	# Obtener equipos de la partida
	equipos = c.obtener_equipos(p.get_chat(), j1.get_nombre_usuario())
	# Obtener el nombre de los jugadores del equipo 1
	jug1, jug2 = c.obtener_jugadores_equipo(equipos[0])
	# Comprobar que ambos son str
	assert_that(jug1).is_type_of(str)
	assert_that(jug2).is_type_of(str)
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de comprobar medalla de un equipo
def test_comprobar_medalla_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test37", "Test")
	j1.set_edad("edad0")
	j2 = Jugador("Test38", "Test")
	j2.set_edad("edad1")
	j3 = Jugador("Test39", "Test")
	j3.set_edad("edad0")
	j4 = Jugador("Test40", "Test")
	j4.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	c.registrar_jugador(j3)
	c.registrar_jugador(j4)
	# Crear objeto partida
	p = Partida("Test12")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Añadir jugador 3 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j3.get_nombre_usuario(), 2)
	# Añadir jugador 4 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j4.get_nombre_usuario(), 2)
	# Iniciar partida
	turno, ava_turno, equipo, pregunta, categoria = c.iniciar_partida(p.get_chat(), j1.get_nombre_usuario())
	# Comprobar que el equipo no tiene la medalla de la categoria actual
	medalla, categoria, equipo = c.comprobar_medalla(p.get_chat())
	# Comprobar que es falso
	assert_that(medalla).is_false()
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})

# Test de terminar partida
def test_terminar_partida_controlador():
	# Crear controlador
	c = Controlador()
	# Crear objetos jugador
	j1 = Jugador("Test41", "Test")
	j1.set_edad("edad0")
	j2 = Jugador("Test42", "Test")
	j2.set_edad("edad1")
	j3 = Jugador("Test43", "Test")
	j3.set_edad("edad0")
	j4 = Jugador("Test44", "Test")
	j4.set_edad("edad1")
	# Crear jugadores
	c.registrar_jugador(j1)
	c.registrar_jugador(j2)
	c.registrar_jugador(j3)
	c.registrar_jugador(j4)
	# Crear objeto partida
	p = Partida("Test13")
	# Crear partida
	c.crear_partida(p, j1.get_nombre_usuario())
	# Añadir jugador 1 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j1.get_nombre_usuario(), 1)
	# Añadir jugador 2 al equipo 1 en la partida
	c.add_jugador(p.get_chat(), j2.get_nombre_usuario(), 1)
	# Añadir jugador 3 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j3.get_nombre_usuario(), 2)
	# Añadir jugador 4 al equipo 2 en la partida
	c.add_jugador(p.get_chat(), j4.get_nombre_usuario(), 2)
	# Iniciar partida
	turno, ava_turno, equipo, pregunta, categoria = c.iniciar_partida(p.get_chat(), j1.get_nombre_usuario())
	# Obtener partida de la BD
	partida = c.mongo.partidas.find_one({'chat': p.get_chat()})
	# Comprobar que la partida existe
	assert_that(partida).is_not_none()
	# Terminar partida
	c.terminar_partida(p.get_chat())
	# Obtener partida de la BD
	partida = c.mongo.partidas.find_one({'chat': p.get_chat()})
	# Comprobar que la partida existe
	assert_that(partida).is_none()
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar jugador de test
	c.mongo.jugadores.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j1.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j2.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j3.get_nombre_usuario()})
	# Borrar estadistica de test
	c.mongo.estadisticas.delete_one({'nombre_usuario':j4.get_nombre_usuario()})
	# Borrar partida de test
	c.mongo.partidas.delete_one({'chat':p.get_chat()})