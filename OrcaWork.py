# Juan David Alvarez Gamez and Carolina Rojas Cabrera
# Archivo para trabajar en Orca dentro de un servidor CentOS

#!/usr/bin/python
# Se cargan las librerias
import os
import sys
import os.path
import errno
import datetime

# Construccion de la fecha del archivo
hoy = datetime.datetime.today()
dia = hoy.strftime('%d')
mes = hoy.strftime('%m')
año = hoy.strftime('%Y')

# Modulo de almacenamiento de bases
Bases = ['3-21G', '6-31+G(d)', '6-31+G(d,p)', '6-31G(d)', '6-31G(d,p)', '6-311G']
   
# Modulo para crear los directorios
def mkdir_p(directorio):
    try:
        os.makedirs(directorio)
    except OSError as exc: # Python > 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(directorio):
            pass
        else: raise

# Indicaciones del trabajo
Nombre_trabajo = input('Indique el nombre que tendra el trabajo de simulacion: ')
Numero_nucleos = input('Indique el numero total de nucleos a usar: ')
Nucleos_nodo = input('El numero de nucleos a usar por nodo: ')
Modulo = input('Indique el modulo a usar (test, short, normal, normal2): ')
Metodo = input('Indique el metodo de simulacion a usar (HF, B3LYP, etc):')
Convergencia = input('Indique la convergencia a usar (SlowConv, VerySlowConv, etc): ')

# Modulo para escribir el script de Orca 4.2.1 y el job_slurm:
def main():
    for base in range(1,len(Bases)):
        base_1 = (str(base)).zfill(3)
        
        mkdir_p(os.path.dirname('C:/Users/Usuario 1/Desktop/MnAl_proof_{}/'.format(base_1)))

        job_slurm = open('C:/Users/Usuario 1/Desktop/MnAl_proof_{}/job_slurm.sh'.format(base_1), 'w')
        job_slurm.write('#!/bin/bash \n\n')
        job_slurm.write('#SBATCH -J {}                  # Nombre del trabajo\n'.format(Nombre_trabajo))
        job_slurm.write('#SBATCH -o %x.%j.out                   # Nombre del archivo estandar de salida  (%j expande a jobId)\n')
        job_slurm.write('#SBATCH --ntasks {}                    # Numero de tareas (cores) solicitadas \n'.format(Numero_nucleos))
        job_slurm.write('#SBATCH --ntasks-per-node {}            # Numero de tareas por nodo \n'.format(Nucleos_nodo))
        job_slurm.write('#SBATCH --partition={}             # Nombre de la particion \n'.format(Modulo))
        job_slurm.write('#SBATCH --output=%x.o%j                # Archivo de salida %x es el nombre del trabajo, %j el jobid \n')
        job_slurm.write('#SBATCH --error=%x.o%j                 # Archivo de error \n')
        job_slurm.write('#SBATCH --mail-type=begin              # Envia un correo cuando el trabajo inicia \n')
        job_slurm.write('#SBATCH --mail-type=end                # Envia un correo cuando el trabajo finaliza \n')
        job_slurm.write('#SBATCH --mail-type=fail               # Envia un correo cuando el trabajo falla \n')
        job_slurm.write('#SBATCH --time=2-00:01:00              # Tiempo de ejecucon \n')
        job_slurm.write('#SBATCH --mail-user=<"juan.alvarez.gamez@correounivalle.edu.co">,<"carolina.rojas@correounivalle.edu.co"> \n\n')
        job_slurm.write('# Launch MPI-based executable \n\n')
        job_slurm.write('echo "Comenzo a simular: `date`" \n')
        job_slurm.write('cd /home/dsalazar/Simulacion_ORCA/MnAl_single_point_calculation/{}/MnAl_{}_{}_{}/MnAl_proof_{}/ \n'.format(Nombre_trabajo, ano, mes, dia, Bases[base]))
        job_slurm.write('/home/APPS/ORCA/orca_4_2_1_linux_x86-64_openmpi314/orca MnAl_1x1x1.inp > MnAl_1x1x1_proof_{}.out \n'.format(Bases[base]))
        job_slurm.write('mpirun --oversubscribe -n {} hostname  \n\n'.format(Numero_nucleos))
        job_slurm.write('sleep 20 \n\n')
        job_slurm.write('echo "Trabajo finalizado: `date`" \n')
        job_slurm.close()

        orca_file = open('/home/dsalazar/Simulacion_ORCA/MnAl_single_point_calculation/{}/MnAl_{}_{}_{}/MnAl_proof_{}/ \n'.format(Nombre_trabajo, ano, mes, dia, Bases[base]), 'w')
        orca_file.write("""Authors: Juan David Alvarez Gamez and Carolina Rojas Cabrera


                                             *****************
                                     * O   R   C   A *
                                     *****************
    
               --- An Ab Initio, DFT and Semiempirical electronic structure package ---
    
                      #######################################################
                      #                        -***-                        #
                      #  Department of molecular theory and spectroscopy    #
                      #              Directorship: Frank Neese              #
                      # Max Planck Institute for Chemical Energy Conversion #
                      #                  D-45470 Muelheim/Ruhr              #
                      #                       Germany                       #
                      #                                                     #
                      #                  All rights reserved                #
                      #                        -***-                        #
                      #######################################################
    
    
                             Program Version 4.2.1 - RELEASE   -
    """+'\n')
        orca_file.write('! {} {} {} \n'.format(Metodo, Convergencia, Bases[base]))
        orca_file.write('! KDIIS SOSCF Grid4 FinalGrid5 \n\n')
        orca_file.write('%maxcore 10000 \n')
        orca_file.write('%pal \n')
        orca_file.write('nprocs {} \n'.format(Numero_nucleos))
        orca_file.write('end \n')
        orca_file.write('%scf \n\n')
        orca_file.write('SOSCFStart 0.00033		# Retraso en el inicio del gradiente orbital \n')
        orca_file.write('soscfmaxit 150000			# Control de iteraciones para SOSCF \n')
        orca_file.write('sthresh 1e-7			# Aumenta el umbral para reducir las dependencias lineales \n')
        orca_file.write('convergence Tight \n')
        orca_file.write('MaxIter 150000 \n')
        orca_file.write('DIISMaxEq 40 \n')
        orca_file.write('directresetfreq 1 \n')
        orca_file.write('end \n')
        orca_file.write('* xyz 0 1 \n')
        orca_file.write('Mn 0 0 0  \n')
        orca_file.write('Mn 3.921 0 0 \n')
        orca_file.write('Mn 0 3.921 0  \n')
        orca_file.write('Mn 3.921 3.921 0 \n')
        orca_file.write('Mn 1.961 1.961 0 \n')
        orca_file.write('Mn 0 0 3.586 \n')
        orca_file.write('Mn 3.921 0 3.586 \n')
        orca_file.write('Mn 0 3.921 3.586 \n')
        orca_file.write('Mn 3.921 3.921 3.586 \n')
        orca_file.write('Mn 1.961 1.961 3.586 \n')
        orca_file.write('Al 1.961 0 1.793 \n')
        orca_file.write('Al 0 1.961 1.793 \n')
        orca_file.write('Al 1.961 3.921 1.793 \n')
        orca_file.write('Al 3.921 1.961 1.793 \n')
        orca_file.write('* \n')
        orca_file.write('\n')
        orca_file.write('-----------------------\n')

        orca_file.close()

main()
