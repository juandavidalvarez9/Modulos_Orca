#!/bin/bash 

#SBATCH -J prueba                  # Nombre del trabajo
#SBATCH -o prueba.%j.out                   # Nombre del archivo estandar de salida  (%j expande a jobId)
#SBATCH --ntasks 8                    # Numero de tareas (cores) solicitadas 
#SBATCH --ntasks-per-node 4            # Numero de tareas por nodo 
#SBATCH --partition=test             # Nombre de la particion 
#SBATCH --output=prueba.o%j                # Archivo de salida %x es el nombre del trabajo, %j el jobid 
#SBATCH --error=prueba.o%j                 # Archivo de error 
#SBATCH --mail-type=begin              # Envia un correo cuando el trabajo inicia 
#SBATCH --mail-type=end                # Envia un correo cuando el trabajo finaliza 
#SBATCH --mail-type=fail               # Envia un correo cuando el trabajo falla 
#SBATCH --mail-user=<"juan.alvarez.gamez@correounivalle.edu.co"> 

# Launch MPI-based executable 

echo "Comenzo a simular: `date`" 
cd salida//prueba/MnAl_2020_11_02/MnAl_proof_1/ 
/home/APPS/ORCA/orca_4_2_1_linux_x86-64_openmpi314/orca prueba.inp > prueba_proof_1.out 

mpirun --oversubscribe -n 8 hostname  

sleep 20 

echo "Trabajo finalizado: `date`" 
