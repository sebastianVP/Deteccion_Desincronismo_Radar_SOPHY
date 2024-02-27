# PROGRAMA AURORA ENCARGADO DE :
'''
- Busqueda de un directorio especifico
- Lectura de archivos procesados.
- Configurado para ejecutarse cada 15 minutos.
- Revision de archivos de reflectividad.
- Implementacion de metodo de deteccion de desincronismo.
- Reinicio de experimento usando el SIR Web.
'''

import requests,os,h5py,numpy
link   = 'http://sophy/status/'
PATH   = "/DATA_RM/DATA" #PATH = "/media/soporte/DATA/PIURA/SOPHY/" 
folder = 'Z_PPI_EL_5.0'


class Readsophy():
    def __init__(self):
        self.last_file = None

    def setup(self,path_file):
        self.path_file = path_file
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

    def run(self):
        filename = self.path_file+"/"+self.last_file
        print("dir_filename:",filename)
        self.readAtrributes(filename)





response_status  = requests.get(link)
print(response_status)
if response_status.status_code == 200:
    experiment =  response_status.json()['name']
    print("Name of Experiment:",experiment)
    print("***********************************************")
    path_param= os.path.join(PATH,experiment,'param')
    path = os.path.join(path_param, folder)
    print("path        :",path)
    path = "/media/soporte/DATA/PIURA/SOPHY/PIU@2024-02-05T10-00-31/param-magic10/Z_PPI_EL_5.0"
    obj =Readsophy()
    obj.setup(path_file=path)
    obj.run()






