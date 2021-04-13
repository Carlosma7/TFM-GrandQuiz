import sys
import os
from dotenv import load_dotenv

# Obtener información de .env
load_dotenv(dotenv_path = '.env')
# Obtener conexión a MongoDB Atlas
MONGO_TOKEN = os.getenv('MONGO')
# Definir path GrandQuiz
sys.path.append(os.path.abspath('./src/grandquiz/core/'))

from pregunta import Pregunta
import pymongo
import re

# Define a client
client = pymongo.MongoClient(MONGO_TOKEN, serverSelectionTimeoutMS = 2000)
# Define the database
database = client.GrandQuiz

if(__name__=="__main__"):
	# Mensaje bienvenida
	print("Bienvenido, este programa tiene como fin definir una pregunta y almacenarla en la BD de GrandQuiz.")
	print("\n\n¿Quiere insertar una pregunta? (S/N)")

	# Entrada del usuario
	opcion = input()
	# Comprobar entrada del usuario
	if opcion.lower() == "s":
		opcion = True
	else:
		opcion = False

	# Mientras se desee introducir una pregunta
	while opcion:
		# Pedir que se introduzca la pregunta
		print("\nPor favor, introduzca la categoría (Arte, Geografía, Ciencia, Historia, Deporte o Entretenimiento):")
		categoria = input()
		# Pedir que se introduzca el enunciado
		print("\nPor favor, introduzca el enunciado:")
		enunciado = input()
		# Pedir que se introduzcan las respuestas una por una
		respuestas = []
		for i in range(1,5):
			print(f"Por favor, introduzca la {i}a respuesta:")
			respuesta = input()
			respuestas.append(respuesta)
		# Pedir que se introduzca el índice de la respuesta correcta
		print("\nPor favor, introduzca el número de la respuesta correcta")
		correcta = input()

		# Creación de la pregunta
		p = Pregunta(categoria, enunciado, respuestas, correcta)
		# Se almacena en BD
		database.preguntas.insert_one(p.to_dict())

		# Informar de éxito
		print("\nEnhorabuena, su pregunta ha sido almacenada con éxito.")

		# Preguntar si quiere insertar otra pregunta
		print("\n\n¿Quiere insertar otra pregunta? (S/N)")
		# Entrada del usuario
		opcion = input()
		# Comprobar entrada del usuario
		if opcion.lower() == "s":
			opcion = True
		else:
			opcion = False