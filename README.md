# REPOSITORIO - DETECCION DE DESINCRONISMO
---
El objetivo de este desarrollo es la deteccion de desincronimo realizando la lectura de datos del Radar Meteorologico SOPHY, para esto utilizaremos la libreria numpy para manejar los arreglos y operaciones, luego la libreria selenium para manipular la pagina web del radar y finalmente telegram para tomar una foto de las operaciones y configuracion restablecida.
El programa se desarrolla en python. Las librerias a utilizar son:
- numpy
- selenium
- python-telegram-bot
- telepot

Las pruebas las realizaremos haciendo primero la conexion vpn al radar. Se probara el control de esta tarea con crontab y puede que sea necesario el uso adicional de la libreria h5py.

# 1 PRUEBA
Vamos a realizar un programa ahora que integre los archivos desincronismo.py y test_selenium_4172.py
# 2 PRUEBA
Se ha probado la libreria telepot en lugar de python-telegram-bot y vamos a enviar ahora mensajes de aviso a el grupo sophy, desde el bot llamado ghost.
