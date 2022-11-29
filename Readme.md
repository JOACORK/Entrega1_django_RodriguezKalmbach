# Entrega Intermedia Proyecto Final
## _Web Django con patron MVT_

Este proyecto está siendo desarrollado en el marco del curso de Python de CODERHOUSE. El mismo busca aplicar los conocimientos adquiridos durante la cursada, utilizando el framework Django para el desarrollo de una página web. 

## Funcionalidades
Para esta entrega intermedia, la web cuenta con dos funcionalidades básicas
- Creación de personajes ficticios a partir de un formulario
- Búsqueda de los personajes creados a partir de sus nombres

> Se pretende crear a futuro la funcionalidad de desarrollar historias de personajes a partir de un determinado input. Para esto se piensa explorar el uso de APIs de inteligencia artifical que puedan vincularse a la web para desarrollar texto/imágenes u otros resultados posibles. 

## Estructura
### App PersonajesApp
Posee toda la lógica para la creación y la búsqueda de personajes de la web. Además de la navegación, los templates y los archivos statics del proyecto. 
#### - Modelos
Alojados en la hoja models.py, conforman la estructura de la base de datos desarrollada. Se pretende mejorar la estructura para crear campos que relacionen a las distintas clases.
#### - Vistas
Alojadas en la hoja views.py, poseen la lógica de trasfondo para navegar, crear personajes y buscar personajes.
#### - Urls
Alojadas en la hoja urls.py
#### - Templates
- inicio.html --> Renderización de inicio
- busquedaPersonaje.html --> Renderización de formulario de búsqueda
- creacion.html --> Renderización de formulario para creación de personaje
- padre.html --> Renderización Padre, el cual se hereda al resto de htmls.
- resultadosBusqueda.html --> Renderización de resultados de búsqueda

## Tecnologías

Esta web utiliza las siguientes tecnologías
- [Django] - HTML enhanced for web apps!
- [Bootstrap] - awesome web-based text editor


## Instalación

Clonar repositorio en su disco local

```sh
cd dillinger
npm i
node app
```

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

