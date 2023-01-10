# Entrega Intermedia Proyecto Final
## _Web Django con patron MVT_

Este proyecto fue diseñado y se encuentra en desarrollo en el marco del curso de Python de CODERHOUSE. Se buscar aplicar los conocimientos adquiridos durante la cursada, utilizando el framework Django para el desarrollo de una página web. 

## Funcionalidades
Para esta entrega, la web cuenta con las siguientes funcionalidades:
- Creación de usuario
- Login/Logout
- Edición de datos personales por parte del usuario
- Delete de imágenes por parte de super usuario
- Mensajería entre usuarios
- Creación de personajes ficticios a partir de formularios
- Visualización de personajes creados dentro de un inventario
- Edición de características de personajes
- Delete de personajes solo por super usuario
- Creación de hoja de vida de un personaje a través de IA
- Creación de avatar de personaje a través de IA



## Estructura
>### App PersonajesApp
>- Posee toda la lógica para la creación y la búsqueda de personajes de la web. CRUD relacionado a personajes. Además de la navegación, los templates y los archivos statics del proyecto.  
>- Posee una hoja python llamada funciones_logicas.py en donde se desarrollan (entre otras cosas) la conección a las APIs de IA.
>---
>### App AppRegisto
>- Posee la lógica y los modelos para realizar CRUD de usuarios. Gestionar logins y logouts. 
>---
>### App AppMensajería
>- Posee la lógica para el envío, guardado y lectura de mensajes entre usuarios de la plataforma. 
>---
>### App AppPerfiles
> - Posee lógica para visualizar y editar los perfiles de los usuarios.
> ---


## Tecnologías

Esta web utiliza las siguientes tecnologías
- [Django] - HTML enhanced for web apps! - [Documentation](https://docs.djangoproject.com/en/4.1/)
- [Bootstrap] - awesome web-based text editor - [Documentacion](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
- [chat-gpt3] - IA generación chat - [Documentacion](https://pypi.org/project/pyChatGPT/) 
- [pychatgpt] - wrapper de API chat-gpt - [Documentacion](https://pypi.org/project/pyChatGPT/) 
- [Stable_Diffusion] - IA generación de imágenes - [Documentacion](https://huggingface.co/docs/diffusers/installation) 
- [Replicate] - API wrapper IA generadora de imágenes Stable Diffussion - [Documentacion](https://replicate.com/docs/get-started/python) 
## Instalación

Clonar repositorio en su disco local

```sh
cd dillinger
npm i
node app
```
Instalar dependencias
```sh
# Instalar wrapper de chatGPT3
pip install pychatgpt

# Instalar wrapper StableDiffusion
pip install replicate
```
Con fines de poder replicar la aplicación por el docente:
Es necesario crear una variable de entorno del sistema con el nombre: "REPLICATE_API_TOKEN"
y debe copiar la siguiente api-token como valor del entorno: "952006b617ba2b59a77c40f1a31750d9a8c82ff5"

---
## Ignorar
La siguiente línea puede ser una opción para usar StableDiffusion II sin límites de precios. Pero es una solución más compleja para aplicar. Queda en desarrollo.
```sh
# La siguiente línea no es necesaria. 
pip install diffusers transformers accelerate scipy safetensors
```
---

Correr proyecto en servidor local
Crear BD

```sh
# Crear BBDD
python manage.py migrate

# Crear usuario admin
python manage.py superuser

# Correr servidor local
python manage.py runserver

```

## Autor
- Joaquín Rodríguez Kalmbach - Desarrollador
