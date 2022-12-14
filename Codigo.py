# Criar "node" de processamento
# Bibliotecas sys e pyodm
# Para criar "node" de processamento é preciso instalar o Docker, conforme especificado no página do projeto: https://opendronemap.org 

# Importar as bibliotecas

import sys
sys.path.append('..')
from pyodm import Node, exceptions

# Criar "node"
node = Node.from_url("http://localhost:3000?token=abc")

try:
    print(node.info())
except exceptions.NodeConnectionError as e:
    print("Cannot connect: " + str(e))


# Iniciar o processamento
# Bibliotecas glob e pyodm

# Importar as bibliotecas necessárias

import glob
from pyodm import Node, exceptions

# Setar "node" de processamento criado

node = Node("localhost", 3000)

try:
    # Carregar todas os arquivos JPGs a serem processados, tem que estar em um mesmo diretório (pasta)
    images = glob.glob("*.JPG") + glob.glob("*.jpg") + glob.glob("*.JPEG") + glob.glob("*.jpeg")

    print("Uploading images...")
    
    # Ajustes dos parâmetros de processamento
    task = node.create_task(images, {'dsm': True, 'dtm' : True, 'orthophoto-resolution': 3, 'ignore-gsd': True,
                                    ' mesh-size': 300000, 'min-num-features': 12000, 
                                     'mesh-octree-depth': 12 })
    print(task.info())

    try:
        def print_status(task_info):
            msecs = task_info.processing_time
            seconds = int((msecs / 1000) % 60)
            minutes = int((msecs / (1000 * 60)) % 60)
            hours = int((msecs / (1000 * 60 * 60)) % 24)
            print("Task is running: %02d:%02d:%02d" % (hours, minutes, seconds), end="\r")
        task.wait_for_completion(status_callback=print_status)

        print("Task completed, downloading results...")

        # Apresentar resultados e indicar o diretorio a serem salvos (cria uma subpasta na pasta geral)
        def print_download(progress):
            print("Download: %s%%" % progress, end="\r")
        task.download_assets(".//results", progress_callback=print_download)

        print("Assets saved in .//results")
    except exceptions.TaskFailedError as e:
        print("\n".join(task.output()))

except exceptions.NodeConnectionError as e:
    print("Cannot connect: %s" % e)
except exceptions.OdmError as e:
    print("Error: %s" % e)


# Visualizar a nuvem de pontos em formato laz: carregar a nuvem de pontos, biblioteca laspy

# Importar a biblioteca necessária

import laspy as lp

# Leitura do arquivo laz

data=lp.read("./results/odm_georeferencing/odm_georeferenced_model.laz")
print(data)


# Extração dos dados da nuvem de pontos: biblioteca numpy

# Importar a biblioteca necessária

import numpy as np

xyz = np.c_[data['x'], data['y'], data['z']]
rgb = np.c_[data['red'], data['green'], data['blue']]
n = np.c_[data['x'], data['y'], data['z']]


# visualização da nuvem de pontos: biblioteca pptk

# Importar a biblioteca necessária

import pptk

v = pptk.viewer(xyz)
v.attributes(rgb / 255., 0.5* (1 + n))
v.color_map('cool')
v.set(point_size=0.008,bg_color=[0,0,0,0],show_axis=0,show_grid=0)





