# Juan David Alvarez Gamez
# Archivo para trabajar en Orca dentro de un servidor CentOS

#!/bin/python
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
ano = hoy.strftime('%Y')

# Modulo de almacenamiento de bases
Bases = ['6-31++G**', '6-31+G(2d)', '6-31+G(2d,2p)', '6-31+G(2d,p)', '6-31+G(2df)', '6-31+G(2df,2pd)', '6-31+G(d)', '6-31+G(d,p)', '6-31+G*', '6-31+G**', '6-31G', '6-31G(2d)', '6-311+G(2d)', '6-311+G(2d,2p)', '6-311+G(2d,p)','6-311+G(2df)','6-311+G(2df,2p)','6-311+G(2df,2pd)', '6-311+G(d)','6-311+G(d,p)', '6-311G','6-31G(2d,2p)','6-31G(2d,p)','6-31G(d)','6-31G(d,p)', 'aug-pcseg-0','aug-pcseg-1','def2-mSVP','def2-mTZVP','def2-SV(P)','def2-SVP','def2-TZVP','DKH-def2-SV(P)','DKH-def2-SVP','DKH-def2-TZVP','DKH-def2-TZVP(-f)','DKH-def2-TZVPP','DKH-SV(P)','DKH-SVP','DKH-TZV(P)','DKH-TZVP','DKH-TZVPP','ma-def2-mSVP','ma-def2-SV(P)','ma-def2-SVP','ma-def2-TZVP','ma-def2-TZVP(-f)','ma-def2-TZVPP', 'ma-DKH-def2-SV(P)','ma-DKH-def2-TZVP','ma-DKH-def2-TZVP(-f)','ma-DKH-def2-TZVPP','ma-ZORA-def2-SV(P)','ma-ZORA-def2-SVP','ma-ZORA-def2-TZVP(-f)','ma-ZORA-def2-TZVPP','old-DKH-SV(P)','old-DKH-SVP','old-DKH-TZV(P)','old-DKH-TZVP','old-DKH-TZVPP','old-SV','old-SV(P)','old-SVP','old-TZV','old-ZORA-SV(P)','old-ZORA-SVP','old-ZORA-TZV(P)','old-ZORA-TZVP','old-ZORA-TZVPP','pc-1','pcseg-0','pcSseg-0','pcSseg-1','pcSseg-2','SV ','SV(P)','SVP','TZV','TZV(P)','TZVP','TZVPP','ZORA-def2-SV(P)','ZORA-def2-SVP','ZORA-def2-TZVP','ZORA-def2-TZVP(-f)','ZORA-def2-TZVPP','ZORA-SV(P)','ZORA-SVP','ZORA-TZV(P)','ZORA-TZVP','ZORA-TZVPP']

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
Type_conv = input('Indique el tipo de convergencia a utilizar (Loose, Sloppy, Normal, Strong, Tight, VeryTight): ')
dir_principal = '/home/dsalazar/Simulacion_ORCA/MnAl_single_point_calculation'
dir_orca = '/home/APPS/ORCA/orca_4_2_1_linux_x86-64_openmpi314/orca'

# Modulo para escribir el script de Orca 4.2.1 y el job_slurm:
def main():
    for base in range(1,len(Bases)):
        mkdir_p(os.path.dirname('{}/{}/MnAl_{}_{}_{}/MnAl_proof_{}/'.format(dir_principal, Nombre_trabajo, ano, mes, dia, base)))

        os.umask(0)
        job_slurm = open(os.open('{}/{}/MnAl_{}_{}_{}/MnAl_proof_{}/job_slurm.sh'.format(dir_principal, Nombre_trabajo, ano, mes, dia, base), os.O_CREAT | os.O_WRONLY, 0o777), 'w')
        job_slurm.write('#!/bin/bash \n\n')
        job_slurm.write('#SBATCH -J {}                  # Nombre del trabajo\n'.format(Nombre_trabajo))
        job_slurm.write('#SBATCH -o {}.%j.out                   # Nombre del archivo estandar de salida  (%j expande a jobId)\n'.format(Nombre_trabajo))
        job_slurm.write('#SBATCH --ntasks {}                    # Numero de tareas (cores) solicitadas \n'.format(Numero_nucleos))
        job_slurm.write('#SBATCH --ntasks-per-node {}            # Numero de tareas por nodo \n'.format(Nucleos_nodo))
        job_slurm.write('#SBATCH --partition={}             # Nombre de la particion \n'.format(Modulo))
        job_slurm.write('#SBATCH --output={}.o%j                # Archivo de salida %x es el nombre del trabajo, %j el jobid \n'.format(Nombre_trabajo))
        job_slurm.write('#SBATCH --error={}.o%j                 # Archivo de error \n'.format(Nombre_trabajo))
        job_slurm.write('#SBATCH --mail-type=begin              # Envia un correo cuando el trabajo inicia \n')
        job_slurm.write('#SBATCH --mail-type=end                # Envia un correo cuando el trabajo finaliza \n')
        job_slurm.write('#SBATCH --mail-type=fail               # Envia un correo cuando el trabajo falla \n')
        job_slurm.write('#SBATCH --time=2-00:01:00              # Tiempo de ejecucon \n')
        job_slurm.write('#SBATCH --mail-user=<"juan.alvarez.gamez@correounivalle.edu.co">,<"carolina.rojas@correounivalle.edu.co"> \n\n')
        job_slurm.write('# Launch MPI-based executable \n\n')
        job_slurm.write('echo "Comenzo a simular: `date`" \n')
        job_slurm.write('cd {}/{}/MnAl_{}_{}_{}/MnAl_proof_{}/ \n'.format(dir_principal, Nombre_trabajo, ano, mes, dia, base))
        job_slurm.write('{} {}.inp > {}_proof_{}.out \n\n'.format(dir_orca, Nombre_trabajo, Nombre_trabajo, base))
        job_slurm.write('mpirun --oversubscribe -n {} hostname  \n\n'.format(Numero_nucleos))
        job_slurm.write('sleep 20 \n\n')
        job_slurm.write('echo "Trabajo finalizado: `date`" \n')
        job_slurm.close()

        os.umask(0)
        orca_file = open(os.open('{}/{}/MnAl_{}_{}_{}/MnAl_proof_{}/{}.inp'.format(dir_principal,Nombre_trabajo, ano, mes, dia, base, Nombre_trabajo), os.O_CREAT | os.O_WRONLY, 0o777), 'w')
        orca_file.write('! {} {} {} \n'.format(Metodo, Convergencia, Bases[base]))
        orca_file.write('! KDIIS SOSCF Grid4 FinalGrid5 \n\n')
        orca_file.write('%maxcore 10000 \n')
        orca_file.write('%pal \n')
        orca_file.write('nprocs {} \n'.format(Numero_nucleos))
        orca_file.write('end \n')
        orca_file.write('%scf \n\n')
        orca_file.write('SOSCFStart 0.000033		# Retraso en el inicio del gradiente orbital \n')
        orca_file.write('soscfmaxit 150000			# Control de iteraciones para SOSCF \n')
        orca_file.write('sthresh 1e-7			# Aumenta el umbral para reducir las dependencias lineales \n')
        orca_file.write('convergence {} \n'.format(Type_conv))
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
        orca_file.close()

main()