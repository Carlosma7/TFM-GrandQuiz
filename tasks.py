from invoke import task, run

# Tarea de limpieza de ficheros
@task 
def clean(c):
	print("Borrando caché de python.")
	run("find . -maxdepth 5 -type d -name  .pytest_cache -exec rm -r {} +")
	run("find . -maxdepth 5 -type d -name __pycache__ -exec rm -r {} +")

# Tarea de ejecución de 3 en raya contra IA aleatoria
@task
def executeTicTacToe(c):
	print("Ejecución de 3 en raya")
	run("python3 src/tic_tac_toe/bot.py")

# Tarea de ejecución de tests
@task
def testQuestions(c):
	print("Ejecución de tests de juego Questions")
	run("pytest -v --disable-pytest-warnings src/questions/test/*")

# Tarea de ejecución de juego de preguntas
@task
def executeQuestions(c):
	print("Ejecución de juego Questions")
	run("python3 src/questions/core/bot.py")

# Tarea de ejecución de tests
@task
def test(c):
	print("Ejecución de tests de GrandQuiz")
	run("pytest -v --disable-pytest-warnings src/grandquiz/test/*")

# Tarea de ejecución de GrandQuiz
@task
def execute(c):
	print("Ejecución de GrandQuiz")
	run("python3 src/grandquiz/core/bot.py")