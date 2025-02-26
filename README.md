# backend-casei

Instrucciones para desarrollo:

1. Ejecutar comando `git fetch` para revisar cambios pendinetes
2. Ejecutar comando `git pull` para actualizar el proyecto
3. Ejecutar comando `venv\Scripts\activate` para entrar al entorno virtual
4. Ejecutar comando `pip install -r requirements.txt` para instalar librerias
5. Ejecutar servidor con el comando:
```
python manage.py runserver
```

6. Ingresar a la siguiente dirección:
```
http://127.0.0.1:8000/
```

Instrucciones para guardado de cambios:

1. Ejecutar comando ``git add .`` para seleccionar los archivos modificados
2. Ejecutar comando ``git commmit -m "Mensaje"``

Nomenclatura recomendada:

- fix: para arreglar errores
- update: para actualizar
- create: para nuevos archivos o funcionalidades
- delete: para borrado de archivos

EJEMPLO: fix - carga de archivos desde csv

Link del repositorio: https://github.com/residencias-isc-2025/backend-casei

NOTA:

Si se instala una nuneva librería esta debe ser agregada en el archivo
```
requirements.txt
```

1. URL para el endpoint de Registrar: http://127.0.0.1:8000/registration/register/
2. URL para el endpoint de generar el token de autorizacion: http://127.0.0.1:8000/api/token/
3. URL para el endpoint de reset-password: http://127.0.0.1:8000/registration/reset-password/