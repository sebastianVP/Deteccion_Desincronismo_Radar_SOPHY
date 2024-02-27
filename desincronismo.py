import numpy
from numpy import random

# Vamos a trabajar con Reflectividad para este caso, tener en cuenta que analizando la data 
# la reflectividad del canal en los pulsos cuando ocurre sincronismo debe ser superior a 60.
# Ademas se ha obserado que la cantidad  de puntos debe ser mayo a 30 para que sea tomado en cuenta.
# Teniendo como referencia que el RMIX es a 5 Km., vamos a considerar que al altura donde empezamos a identificar 
# si es que el sistema esta desincronizado sera a partir de la altura 

threshold             = 60
num_alturas_iniciales = 100 # Recuerda H0= -2 Km y Rmix = 5 Km  , dividimos 7km-> 7000 m. entre 60 metros de resolucion esto nos da 116 alturas
cant_alt_consecutivas  = 30

def detectar_desincronismo(arr , threshold, num_alturas_iniciales,cant_alt_consecutivas):
    '''
    Al inicio todo fue implementado en el metodo run de la clase Block360 jroproc_parameters.py
    Los atributos de entrada son: dataOut.data_param[0,4,:,:] -> Reflectividad de un solo canal.
    arr = dataOut.data_param[0,4,:,:] el shape de este arreglo debe ser los 360 angulos y las alturas
    1. Arreglo de reflectividad
    2. umbral_promedio, valor de reflectividad en los pulsos de tx.
    3. num_alturas_iniciales: mayor al Rmix para detectar desincronismo.
    4. cant_alt_consecutivas: cantidad de alturas consecutivas ancho de pulso
    '''

    print("-----------DESINCRONISMO - DETECCION ----------------------------")
    print("Parametro Utilizado: Reflectividad")
    print("arreglo Z       :",arr)
    print("arr             :",arr.shape)
    print("umbral_promedio :",threshold)
    print("num_alturas_ini :",num_alturas_iniciales)

    arr_data               = arr
    prom_por_altura        = numpy.nanmean(arr_data,axis = 0)
    print("Dimension de arr prom x altura:", prom_por_altura.shape)
    alt_altas              = numpy.where(prom_por_altura> threshold)[0]
    alt_consecutivas_altas = []
    consecutivas_actual    = []

    for altura in alt_altas:
        if altura >= num_alturas_iniciales:
            consecutivas_actual.append(altura)
        else:
            consecutivas_actual=[]
        if len(consecutivas_actual)>cant_alt_consecutivas:
            alt_consecutivas_altas.append(consecutivas_actual.copy())

    return alt_consecutivas_altas



'''
CREAMOS UN ARREGLO DE PRUEA PARA REPRESENTAR LA REFLECTIVIDAD
'''
# Especifica la media y desviación estándar
media = 30
desviacion_estandar = 2
# Crea un arreglo aleatorio de dos dimensiones con la distribución normal
arr1 = numpy.random.normal(loc=media, scale=desviacion_estandar, size=(360, 500))
# Especifica la media y desviación estándar
media = 65
desviacion_estandar = 2
# Crea un arreglo aleatorio de dos dimensiones con la distribución normal
arr2 = numpy.random.normal(loc=media, scale=desviacion_estandar, size=(360, 31))
arr_tmp = numpy.concatenate((arr1,arr2),axis=1)
print("new_array:",arr_tmp.shape)
# Especifica la media y desviación estándar
media = 20
desviacion_estandar = 2
# Crea un arreglo aleatorio de dos dimensiones con la distribución normal
arr3 = numpy.random.normal(loc=media, scale=desviacion_estandar, size=(360, 650))             
'''
Arreglo Reflectividad
'''
arr = numpy.concatenate((arr_tmp,arr3),axis=1)
threshold             = 60
num_alturas_iniciales = 100 # Recuerda H0= -2 Km y Rmix = 5 Km  , dividimos 7km-> 7000 m. entre 60 metros de resolucion esto nos da 116 alturas
cant_alt_consecutivas  = 30

resultado = detectar_desincronismo(arr ,threshold=threshold, num_alturas_iniciales=num_alturas_iniciales,cant_alt_consecutivas=cant_alt_consecutivas)
if len(resultado)> 0:
    print("\n [Desincronismo detectado] \n")
else:
    print("\n Todo [OK] \n")

