# Modulo de almacenamiento de bases
Bases = []

# Modulo para crear directorios de forma recursiva
# Accedo a opciones de consola con la libreria os
import os

for base in range(1,len(Bases)):
     base_1 = (str(base)).zfill(3)
     os.makedirs('C:/Users/Usuario 1/Desktop/MnAl_proof_{}'.format(base_1))
