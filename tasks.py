from invoke import task, run

# Tarea de limpieza de ficheros
@task 
def clean(c):
	print("Borrando caché de python.")
	run("find . -maxdepth 5 -type d -name  .pytest_cache -exec rm -r {} +")
	run("find . -maxdepth 5 -type d -name __pycache__ -exec rm -r {} +")

# Tarea de ejecución de 3 en raya contra IA aleatoria
@task
def execute_tic_tac_toe(c):
	print("Ejecución de 3 en raya")
	run("python3 src/tic_tac_toe/bot.py")
