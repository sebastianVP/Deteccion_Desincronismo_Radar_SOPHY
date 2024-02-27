# REPOSITORIO - DETECCION DE DESINCRONISMO

El objetivo de este desarrollo es la deteccion de desincronimo realizando la lectura de datos del Radar Meteorologico SOPHY, para esto utilizaremos la libreria numpy para manejar los arreglos y operaciones, luego la libreria selenium para manipular la pagina web del radar y finalmente telegram para tomar una foto de las operaciones y configuracion restablecida.
El programa se desarrolla en python. Las librerias a utilizar son:
- numpy
- selenium
- python-telegram-bot

Las pruebas las realizaremos haciendo primero la conexion vpn al radar. Se probara el control de esta tarea con crontab y puede que sea necesario el uso adicional de la libreria h5py.
