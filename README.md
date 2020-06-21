# SSWB-UGR
Enlace al repositorio en [github](https://github.com/carlos-el/SSWB-UGR).
## Resumen:
Repositorio para alojar el proyecto de la asignatura SSWB del Master en la UGR.

Se ha realizado un proyecto web que consta principalmente de 2 aplicaciones.
- Una app en python usando Django como framework para la administración de visitas de ocio a la ciudad de Granada. Cuenta con una API REST y con una serie de endpoints enfocados al templating.

- Una app de frontend con React que funciona como SPA y consume la API REST de Django. Esta app se ubica en el directorio `react_spa` dentro del directorio raíz del repositorio. No cuenta con la posibilidad de loguear crear o editar visitas.

Ambas aplicaciones se han deplegado sobre un servidor Nginx. este sirve tanto la app de Django (puerto 80) como la SPA de React (puerto 81)

Todas las tareas del curso (de la 0 a la 11) se han completado junto con algunos de los ejercicios opcionales especificados para cada tarea.

---
## Despliegue:
El despliegue se ha realizado usando `docker-compose`. Los pasos necesarios para replicar el proceso de despliegue completo son los siguientes:
- Clonar el repositorio.
- Abrir una terminal en la carpeta del repositorio clonado.
- Ejecutar los siguientes comandos:
    - `docker-compose up` (puede que sea necesario repetirlo varias veces ya que los contenedores usan alpine y sus servidores suelen dar problemas en la creación de imágenes donde haya que instalar paquetes)
    - En otra terminal:
        - `docker exec -it sswb-ugr_web_1 python3 manage.py migrate`
        - `docker exec -it sswb-ugr_web_1 python3 manage.py collectstatic`
        - `docker exec -it sswb-ugr_web_1 npm install --prefix react_spa`
        - `docker exec -it sswb-ugr_web_1 npm run build --prefix react_spa`
        - `docker exec -it sswb-ugr_web_1 python3 manage.py createsuperuser`
        - `docker exec -it sswb-ugr_web_1 python3 populate.py`

Tras dichos pasos debe ser posible acceder en el navegador a las direcciones [http://localhost/](http://localhost/) para la app de Django y [http://localhost:81/](http://localhost:81/) para la SPA de React.

---
## Algunas peticiones para probar la API REST:
A continuación se ofrecen algunos ejemplos de peticiones para probar la API REST. Se deben tener en cuenta los siguientes aspectos:
- Para los ejemplos se usa la herramienta 'httpie'.
- En algunos ejemplos se usan como credenciales el nombre de usuario 'admin' y la contraseña 'admin'. Estas deben se adecuadas a las credenciales del superusuario que se hayan creado en el despliegue. 
- Los recursos (ids) a los que van dirigidas las peticiones pueden cambiarse. No obstante si no se ha alterado antes la base de datos inicializada, los recursos referenciados en las peticiones deben estar presentes y funcionar.
- El token de JWT obtenido en una petición concreta es necesario para otras. Tiene una duración de una hora. Si expira, basta con obtener un token nuevo y usarlo.

### Ejemplos:
- Obtener todas las visitas:
    - `http --follow --timeout 3600 GET localhost/api/visitas`
- Obtener la visita con id = 1:
    - `http --follow --timeout 3600 GET localhost/api/visitas/1`
- Obtener los comentarios de la visita 1:
    - `http --follow --timeout 3600 GET localhost/api/visitas/comentarios/1`
- Obtener los likes de la visita 1:
    - `http --follow --timeout 3600 GET localhost/api/visitas/likes/1`
- Dar like a la visita 1 (Dar like o dislike depende del valor que se pase. Si se quiere dar like hay que pasar un valor una unidad mayor que el número de likes de la visita):
    - `http --ignore-stdin --form --follow --timeout 3600 PUT localhost/api/visitas/likes/1/ \
 'likes'='3'`
- Pedir token JWT para peticiones que lo requieran (guardar el token devuelto para próximos ejemplos):
    - `http --ignore-stdin --form --follow --timeout 3600 POST localhost/api/token/ \
 'username'='admin' \
 'password'='admin'`
- Crear una nueva visita (usar token de la petición anterior):
    - `http --ignore-stdin --form --follow --timeout 3600 POST localhost/api/visitas/ \
 'nombre'='Un test de POST para la visita.' \
 'descripcion'='Test de POST para la visita.' \
 Authorization:'Bearer <token>'`
- Editar una visita (usar token de la petición anterior):
    - `http --ignore-stdin --form --follow --timeout 3600 PUT localhost/api/visitas/4/ \
 'nombre'='Un test de PUT para la visita' \
 'descripcion'='Test de PUT request para la visita' \
 'Content-Type'='application/json' \
 Authorization:'Bearer <token>'`
 - Eliminar una visita (usar token de la petición anterior):
    - `http --ignore-stdin --form --follow --timeout 3600 DELETE localhost/api/visitas/4/ \
 \
 Authorization:'Bearer <token>'`

 ---
 ## Entorno de desarrollo:
Se puede probar el entorno de desarrollo usado siguiendo los siguientes pasos:
- Modificar el comando del contendor 'web' en [docker-compose.yml](/docker-compose.yml) (en el fichero esta claramente explicado).
- En el fichero [settings.py](/django_web_project/settings.py) comentar de la linea 140 a la 183 y poner DEBUG = True (linea 26).
- Tirar los contenedores con `docker-compose down` si no se habia hecho antes y volver a levantarlos con `docker-compose up`.
- En otra terminal ejecutar `docker exec -it sswb-ugr_web_1 npm start --prefix react_spa`.

Ya sería posible acceder a la app de Django en [http://0.0.0.0:8000/](http://0.0.0.0:8000) y la SPA de React en [http://0.0.0.0:3000/](http://0.0.0.0:3000).
