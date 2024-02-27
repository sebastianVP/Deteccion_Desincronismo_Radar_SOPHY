# PROGRAMA AURORA ENCARGADO DE :
'''
- Busqueda de un directorio especifico
- Lectura de archivos procesados.
- Configurado para ejecutarse cada 15 minutos.
- Revision de archivos de reflectividad.
- Implementacion de metodo de deteccion de desincronismo.
- Reinicio de experimento usando el SIR Web.
- Intalar selenium: pip install selenium==4.17.2
- Linea 65 genera el restart desde el SIR.
'''

import requests,os,h5py,numpy

from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

#CONFIGURACION DE FOLDERY LINK DE EXPERIMENTO
link   = 'http://sophy/status/'
PATH   = "/DATA_RM/DATA" #PATH = "/media/soporte/DATA/PIURA/SOPHY/" 
folder = 'Z_PPI_EL_5.0'

#CONFIGURACION DE DESINCRONISMO
threshold             = 60
num_alturas_iniciales = 100 # Recuerda H0= -2 Km y Rmix = 5 Km  , dividimos 7km-> 7000 m. entre 60 metros de resolucion esto nos da 116 alturas
cant_alt_consecutivas  = 30


class Sirselenium():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://sophy/accounts/login/?next=/experiment/1/edit/")
        self.driver.maximize_window()
        time.sleep(1)

    def slow_typing(self,element,text):
        for character in text:
            element.send_keys(character)
            time.sleep(0.3)

    def registro(self):
        ci = self.driver.find_element(By.ID, 'id_username')
        self.slow_typing(ci, 'developer')#71846355, syañez@igp.gob.pe # 43485084 yellyna
        ci = self.driver.find_element(By.ID, 'id_password')
        self.slow_typing(ci, 'developer9')#71846355, syañez@igp.gob.pe # 43485084 yellyna
        time.sleep(2)
    
    def aceptar(self):
        submit = self.driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        submit.click()
        time.sleep(3)
    
    def restart(self):
        self.driver.get("http://sophy/experiment/1/stop/")
        time.sleep(15)
        self.driver.get("http://sophy/experiment/1/start/")
        time.sleep(3)

    def run(self):
        print("Working with Selenium")
        self.registro()
        self.aceptar()
        self.restart()
        print("Restart Experiment[OK]")



class Readsophy():
    def __init__(self):
        self.last_file = None

    def setup(self,path_file,threshold,num_alturas_iniciales,cant_alt_consecutivas):
        self.path_file = path_file
        self.threshold             = threshold
        self.num_alturas_iniciales = num_alturas_iniciales
        self.cant_alt_consecutivas = cant_alt_consecutivas
        self.last_file = self.read_files(path_file=self.path_file)
    
    def read_files(self,path_file):
        grado          = 5
        variable       = 'Z'
        validFilelist  = []
        filter         = "_E"+str(grado)+".0_"+variable
        fileList       = os.listdir(path_file)

        for thisFile in fileList:
            if (os.path.splitext(thisFile)[0][-7:] != filter):
                #print("s_:",os.path.splitext(thisFile)[0][-7:])
                continue
            validFilelist.append(thisFile)
            validFilelist.sort()
        print("Lastfile    :",validFilelist[-1])
        return validFilelist[-1]
    
    def readAtrributes(self,filename):
        with h5py.File(filename, "r") as obj:
            var        = 'reflectivity'
            channel    = 'H'
            var_       = 'Data/'+var+'/'+str(channel)
            data_arr   = numpy.array(obj[var_]) 
            print("***********************************************")
            print("ARR shape:",data_arr.shape)
            print("ARR shape:",data_arr)
            return data_arr
        
    def detectar_desincronismo(self,arr , threshold, num_alturas_iniciales,cant_alt_consecutivas):
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
        #import matplotlib.pyplot as plt
        #plt.plot(prom_por_altura)
        #plt.show()
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


    def run(self,obj_sir):
        filename     = self.path_file+"/"+self.last_file
        print("dir_filename:",filename)
        arr          = self.readAtrributes(filename)
        resultado    = self.detectar_desincronismo(arr                  = arr,
                                                   threshold            = self.threshold,
                                                   num_alturas_iniciales= self.num_alturas_iniciales,
                                                   cant_alt_consecutivas= self.cant_alt_consecutivas)
        if len(resultado)> 0:
            print("\n [Desincronismo detectado] \n")
            SIR = obj_sir
            SIR.run()

        else:
            print("\n Todo [OK] \n")


response_status  = requests.get(link)
print(response_status)
if response_status.status_code == 200:
    experiment =  response_status.json()['name']
    print("Name of Experiment:",experiment)
    print("***********************************************")
    path_param= os.path.join(PATH,experiment,'param')
    path = os.path.join(path_param, folder)
    print("path        :",path)
    # ESTA LINEA path es de prueba con la data real: /DATA_RM/DATA/PIU@2024-02-16T16-00-34/param/Z_PPI_EL_5.0/
    path = "/media/soporte/DATA/PIURA/SOPHY/PIU@2024-02-05T10-00-31/param-magic10/Z_PPI_EL_5.0"
    threshold             = 60
    num_alturas_iniciales = 100 # Recuerda H0= -2 Km y Rmix = 5 Km  , dividimos 7km-> 7000 m. entre 60 metros de resolucion esto nos da 116 alturas
    cant_alt_consecutivas  = 30
    obj     = Readsophy()
    obj.setup(path_file=path,threshold=threshold,num_alturas_iniciales=num_alturas_iniciales,cant_alt_consecutivas=cant_alt_consecutivas)
    obj_sir = Sirselenium()
    obj.run(obj_sir=obj_sir)






