#!/bin/bash

#SBATCH -J MnAl_1x1x1_1
#SBATCH -o MnAl_1x1x1_1.%j.out                   
#SBATCH --ntasks 8                    # Numero de tareas (cores) solicitadas
#SBATCH --ntasks-per-node 8            # Numero de tareas por nodo
#SBATCH --partition=short             # Nombre de la particion
#SBATCH --output=MnAl_1x1x1_1.o%j                # Archivo de salida %x es el nombre del trabajo, %j el jobid 
#SBATCH --error=MnAl_1x1x1_1.o%j                 # Archivo de error 
#SBATCH --mail-user=<"juan.alvarez.gamez@correounivalle.edu.co">,<"carolina.rojas@correounivalle.edu.co"> 

# Launch MPI-based executable
echo "Comenzo a simular: `date`"

for (( c=51; c<=80; c++ ))
do
 cd /home/dsalazar/Simulacion_ORCA/MnAl_single_point_calculation/MnAl_1x1x1_1/MnAl_2020_10_16/MnAl_proof_$c/ 
 sbatch job_slurm.sh
done

mpirun --oversubscribe -n 8 hostname 

sleep 20 

echo "Trabajo finalizado: `date`"

