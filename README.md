# backend-casei

## Instrucciones para desarrollo:

1. Ejecutar comando `git fetch` para revisar cambios pendinetes
2. Ejecutar comando `git pull` para actualizar el proyecto
3. Ejecutar comando `venv\Scripts\activate` para entrar al entorno virtual
4. Ejecutar comando `pip install -r requirements.txt` para instalar librerias
5. Crear migraciones con el comando `python manage.py makemigrations`
6. Ejecutar migraciones con el comando `python manage.py migrate`
7. Ejecutar servidor con el comando:
```
python manage.py runserver
```

8. Ingresar a la siguiente dirección:
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

## Instrucciones para producción

1. Ejecutar comando `git pull` para actualizar el proyecto
2. Ejecutar comando `source venv/bin/activate` para entrar al entorno virtual
3. Ejecutar comando `pip install -r requirements.txt` para instalar librerias
4. Crear migraciones con el comando `python manage.py makemigrations`
5. Ejecutar migraciones con el comando `python manage.py migrate`
6. Ejecutar los siguentes comando para reiniciar el servidor y borrar cache:
```
sudo systemctl restart gunicorn_cacei
sudo systemctl restart gninx
```




