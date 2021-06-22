# Python 3.8-slim (Debian buster-slim based)
FROM python:3.8-slim

# Se indica mantenedor de la imagen
LABEL maintainer="Carlos Morales <carlos7ma@correo.ugr.es>"

# Etiquetas relativas a la imagen creada
LABEL build-date="22/06/2021"
LABEL description="GrandQuiz Project on Python3.8-slim debian based docker."
LABEL github.url="https://github.com/Carlosma7/TFM-GrandQuiz"
LABEL version="4.0.0"

# Se configura el PATH para ejecutar paquetes de Pip
ENV PATH=/home/TFM-GrandQuiz/.local/bin:$PATH

# Creación de usuario con permisos básicos
RUN useradd -ms /bin/bash TFM-GrandQuiz \
	&& mkdir -p app/test \
	&& chown TFM-GrandQuiz /app/test

# Se configura para utilizarse el usuario creado
USER TFM-GrandQuiz

# Se configura el directorio de trabajo
WORKDIR /app/test

# Se copia el fichero de requisitos de paquetes pip
COPY . .

# Instalación de los requisitos y se borra el fichero tras la instalación
RUN pip install -r requirements.txt --no-warn-script-location \
	&& rm requirements.txt

# Ejecución
CMD ["invoke", "execute"]
