#!/bin/bash

#SBATCH -J MnAl_1x1x1
#SBATCH -o MnAl_1x1x1.%j.out                   
#SBATCH --ntasks 8                   # Numero de tareas (cores) solicitadas
#SBATCH --ntasks-per-node 8          # Numero de tareas por nodo
#SBATCH --partition=test             # Nombre de la particion
#SBATCH --output=MnAl_1x1x1.o%j      # Archivo de salida %x es el nombre del trabajo, %j el jobid 
#SBATCH --error=MnAl_1x1x1.o%j       # Archivo de error 
#SBATCH --mail-user=<"juan.alvarez.gamez@correounivalle.edu.co"> 

# Launch MPI-based executable
echo "Comenzo a simular: `date`"

for (( c=30; c<=50; c++ ))
do
 cd /home/dsalazar/Simulacion_ORCA/MnAl_NumFreq/MnAl_1x1x1/MnAl_2020_10_27/MnAl_proof_$c/ 
 sbatch job_slurm.sh
done

mpirun --oversubscribe -n 8 hostname 

sleep 20 

echo "Trabajo finalizado: `date`"

