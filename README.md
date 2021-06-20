
# TFM-GrandQuiz
---

*Este proyecto forma parte del Trabajo Final de Máster del* ***Máster Profesional en Ingeniería Informática de la UGR**, realizado por* ***Carlos Morales Aguilera**. Para más información puede contactar a través de [correo electrónico](carlos7ma@gmail.com).*

<h1 align="center">GrandQuiz</h1>
<p align="center"><img src="https://raw.githubusercontent.com/Carlosma7/TFM-GrandQuiz/main/doc/img/Logo.png"/></p> 

## Tabla de contenidos:
---

:medal_sports: [Badges](#badges)

:video_game: [Descripción y contexto](#descripción-y-contexto)

:notebook_with_decorative_cover: [Guía de usuario](#guía-de-usuario)

:gear: [Guía de instalación](#guía-de-instalación)

:couple: [Cómo contribuir](#cómo-contribuir)

:man: [Autor/es](#autores)

:copyright: [Licencia](#licencia)

## Badges
---
**Proyecto**.

[![Language](https://img.shields.io/badge/Language-Python-red.svg)](https://www.python.org/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Telegram](https://img.shields.io/badge/API-Telegram-cyan.svg)](https://core.telegram.org/) [![Framework](https://img.shields.io/badge/Framework-Telebot-red.svg)](https://github.com/eternnoir/pyTelegramBotAPI)

**Tests**.

[![Testing](https://img.shields.io/badge/Test-Pytest-yellow.svg)](https://docs.pytest.org/en/stable/) [![Coverage](https://img.shields.io/badge/Coverage-100%25-green.svg)](https://github.com/Carlosma7/TFM-GrandQuiz/actions?query=workflow%3AGitHub-Actions-CI)

**Integración Continua**.

[![Build Status](https://github.com/Carlosma7/TFM-GrandQuiz/workflows/GitHub-Actions-CI/badge.svg)](https://github.com/Carlosma7/TFM-GrandQuiz/actions?query=workflow%3AGitHub-Actions-CI)

## Descripción y contexto
---

### Proyecto

**GrandQuiz**, juego mediante Chatbots para el Trabajo Final de Máster del Máster Profesional de Ingeniería Informática en la UGR. Este proyecto aborda la utilización de un sistema mediante chatbots para realizar un juego social e intergeneracional como alternativa al desarrollo de juegos tradicional.

**GrandQuiz** ofrece un enfoque diferente frente a juegos tradicionales, aprovechando las herramientas que ofrece una plataforma de mensajería como **Telegram**, aprovechando la API que ofrece y mediante el uso de frameworks como [Telebot](https://github.com/eternnoir/pyTelegramBotAPI).

Este proyecto a su vez utiliza un despliegue haciendo uso de IaaS en [Digital Ocean](https://www.digitalocean.com/), por lo que se trata de una solución cloud que se ofrece a los jugadores como SaaS abstraído bajo la interfaz de Telegram.

### Descripción

En la [Página Oficial de GrandQuiz](https://grandquizbot.wixsite.com/grandquiz) se puede observar una explicación profunda del juego, destacando los siguientes conceptos:

* **GrandQuiz** se basa en tres pilares fundamentales: **Diversión**, **Colaboración** y **Competición**. A diferencia de otros juegos del sector, nos distinguimos por aportar un enfoque intergeneracional, donde se incluyen diferentes rangos de edad a la hora de formar equipos y donde las preguntas están orientadas al conocimiento general y beneficio de diferentes rangos con el fin de valorar a todos los jugadores independientemente de su edad.
* **GrandQuiz** posee un sistema de partidas dinámicas por equipos, donde estos están conformados por jugadores de diferentes grupos de edad. Estas partidas incluyen preguntas, medallas, desafíos, *quizzies* y algunos elementos que hacen de la partida una experiencia competitiva y colaborativa a la par que mantiene la diversión como principal objetivo.
* **GrandQuiz** posee además un sistema individual de partidas denominado duelos, donde el jugador conecta con otro jugador aleatorio y juegan a una partida sencilla de **GrandQuiz** y gana aquel que acierte más preguntas rápidamente. Este modo está orientado a aquellos jugadores más competitivos e impacientes con ganas de deslumbrar.
* El principal componente de **GrandQuiz**, cuyo objetivo es conectar gente de todos los rangos de edades para jugar, divertirse y compartir, manteniendo sistemas de logros, estadísticas y otros elementos que permitan interactuar con otros jugadores de forma competitiva y colaborativa.

## Guía de usuario
---

**GrandQuiz** es un sistema cuyo despliegue es sencillo, para ello se necesita definir un fichero **.env** donde se recojan los siguientes elementos:
* **Token** del bot definido en Telegram.
* **Mongo** token de conexión al cluster en Mongo Atlas.
* **Pass Gmail** del correo definido para poder trabajar con el sistema de gestión de emails.

A continuación, mediante el uso de **Invoke** la ejecución del proyecto es tan sencilla como ejecutar:

```shell
invoke execute
```
 	
## Guía de instalación
---

### Descarga
---

**Con** Git.

```shell
git clone https://github.com/Carlosma7/TFM-GrandQuiz.git
```

**Con** GitHub CLI.

```shell
gh repo clone Carlosma7/TFM-GrandQuiz
```

**Sin** GitHub.

```shell
wget https://github.com/carlosma7/tfm-grandquiz/archive/main.zip
```

### Dependencias
---

Para instalar las dependecias simplemente se necesita ejecutar:

```shell
pip3 install -r requirements.txt
```

    Puedes usar este estilo de letra diferenciar los comandos de instalación.

## Cómo contribuir
---
Actualmente el proyecto es un **Trabajo Final de Máster** para la **Universidad de Granada** por lo que no se aceptan colaboraciones directas aunque sí admito sugerencias y referencias a posibles mejoras tanto a nivel personal como en *issues* del proyecto. En un futuro se establecerá un nuevo criterio y código de conducta referente al proyecto.

## Autor
---

**Carlos Morales Aguilera**

![Carlos](https://avatars.githubusercontent.com/u/14914668?v=4)

:octocat: [GitHub](https://github.com/Carlosma7)
:email: [Email](carlos7ma@gmail.com)
:busts_in_silhouette: [LinkedIn](https://www.linkedin.com/in/carlos-morales-aguilera/)

## Licencia 
---
[LICENCIA](https://github.com/Carlosma7/TFM-GrandQuiz/blob/main/LICENSE)

**GPLv3**: Los permisos de esta sólida licencia copyleft están condicionados a poner a disposición el código fuente completo de los trabajos con licencia y las modificaciones, que incluyen trabajos más grandes que utilizan un trabajo con licencia, bajo la misma licencia. Deben conservarse los avisos de derechos de autor y licencias. Los contribuyentes proporcionan una concesión expresa de derechos de patente.

**Permisos**:

* Uso comercial.
* Distribución.
* Modificación.
* Uso de patente.
* Uso privado.

**Condiciones**:

* Revelar fuente.
* Aviso de licencia y copyright.
* Misma licencia.
* Cambios de estado.

**Limitaciones**:

* Responsabilidad.
* Garantía.
