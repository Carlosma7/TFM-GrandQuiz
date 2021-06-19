import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Obtener información de .env
load_dotenv(dotenv_path = '.env')
# Obtener password de gmail
PASS_GMAIL = os.getenv('PASS_GMAIL')

# Clase de mail
class Mail():
	def __init__(self, destinatario: str):
		self.__emisor = 'grandquizbot@gmail.com'
		self.__destinatario = destinatario
		self.__message = ""

	# Métodos
	def set_mail(self, jugador: str, tipo: int):
		# El correo es de registro
		self.__message = MIMEMultipart("alternative")
		self.__message["From"] = self.__emisor
		self.__message["To"] = self.__destinatario

		if tipo == 1:
			self.__message["Subject"] = "Bienvenida a GrandQuiz"
			html = open("src/grandquiz/core/registro.html")
		else:
			self.__message["Subject"] = "Notificación inactividad en GrandQuiz"
			html = open("src/grandquiz/core/inactividad.html")

		html = html.read()
		html = html.replace("Jugador", jugador)

		cuerpo = MIMEText(html, "html")
		self.__message.attach(cuerpo)

		# Create secure connection with server and send email
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login(self.__emisor, PASS_GMAIL)
			server.sendmail(
				self.__emisor, self.__destinatario, self.__message.as_string()
			)