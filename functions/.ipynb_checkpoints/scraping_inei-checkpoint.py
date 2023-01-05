import requests
import time
from zipfile2 import ZipFile
import os
from os.path import join
from os import chdir, listdir, rmdir
from shutil import move




def get_all_in_one(Encuestas, Modulos):
    
    """""  Importa los modulos en una sola carpeta

    Parametros
    ----------
    Encuestas: list
        Lista de numeros de los modulos 
    Modulos: list
        Lista de codigos de los periodos 
    
    """""
    
    try:
        os.makedirs("data")
    except:
        pass
    
    
    for i, n in enumerate(Encuestas):

        for m in Modulos:
            
            # Haciendo el request con la pagina de INEI
            try:
                r = requests.get(f"http://iinei.inei.gob.pe/iinei/srienaho/descarga/STATA/{n}-Modulo{m}", allow_redirects=True)
            except:
                time.sleep(5)
                r = requests.get(f"http://iinei.inei.gob.pe/iinei/srienaho/descarga/STATA/{n}-Modulo{m}", allow_redirects=True)
            

            open(f"data//Modulo{n}{m}.zip", 'wb').write(r.content)

            # Extrayendo todos los archivos del Zip
            with ZipFile(f"data//Modulo{n}{m}.zip", 'r') as file:
                file.extractall(path = "data")

            try:
                ruta = join("data", f"{n}-Modulo{m}")
                
                for filename in listdir(ruta):
                    move(join(ruta, filename), join("data", filename))
                            
                rmdir(ruta)
                
            except:
                pass
            
            
            # Eliminando todos los archivos que no son de interes
            for file in listdir("data"):
                if not (file.startswith("enaho01") or file.startswith("sumaria")):
                    os.remove(f"data//{file}")
                if file.endswith("a.dta"):
                    os.remove(f"data//{file}")
        
    return print("Importación realizada!")





def get_all_in_folders(Periodos, Encuestas, Modulos):

    """""  Importa los modulos en diferentes carpetas

    Parametros
    ----------
    Periodo: list
        Lista de periodos (años)
    Encuestas: list
        Lista de numeros de los modulos 
    Modulos: list
        Lista de codigos de los periodos 
    
    """""

    periodo = Periodos[0]

    for i, n in enumerate(Encuestas):
    
        # Creando la carpeta por cada periodo
        try:
            os.makedirs(f"./data//{str(periodo)}")
        except:
            pass
        

        for m in Modulos:
            
            try:
                r = requests.get(f"http://iinei.inei.gob.pe/iinei/srienaho/descarga/STATA/{n}-Modulo{m}", allow_redirects=True)
            except:
                time.sleep(5)
                r = requests.get(f"http://iinei.inei.gob.pe/iinei/srienaho/descarga/STATA/{n}-Modulo{m}", allow_redirects=True)
            
            
            open(f"data//{str(periodo)}//Modulo{n}{m}.zip", 'wb').write(r.content)

            # Extrayendo todos los archivos del Zip
            with ZipFile(f"data//{str(periodo)}//Modulo{n}{m}.zip", 'r') as file:
                file.extractall(path = f"data//{str(periodo)}")

            try:
                ruta = join(f"data//{str(periodo)}", f"{n}-Modulo{m}")
                
                for filename in listdir(ruta):
                    move(join(ruta, filename), join(f"data//{str(periodo)}", filename))
                            
                rmdir(ruta)
                
            except:
                pass
            
            
            # Eliminando todos los archivos que no son de interes
            for file in listdir(f"data//{str(periodo)}"):
                if not (file.startswith("enaho01") or file.startswith("sumaria")):
                    os.remove(f"data//{str(periodo)}//{file}")
                if file.endswith("a.dta"):
                    os.remove(f"data//{str(periodo)}//{file}")
                                
        periodo += 1
        
    return print("Importación realizada!")
