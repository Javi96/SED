# -*- coding: utf-8 -*-

'''
    Conjunto de funciones y parámetros que múltiples componentes del sistema utilizan para 
    realizar sus funcionalidades.
'''

#Imports necesarios
import subprocess

RSA_PATH_JAVI = '/home/javi/.ssh/id_rsa.pub'
RSA_PATH_RASP = '/etc/ssh/ssh_host_ed25519_key.pub'
SAVE_FILE_PATH = './db/localhost.txt'
DB_PATH = './db'
RED_BASH = './red.sh'

'''
    Carga las infracciones almacenadas en el fichero file y devuelve un diccionario que asocia una lista de infracciones a cada tipo de ruta.
'''
def load_infractions(file):
        with open(file, "r") as myfile:
            lines = myfile.readlines()
            
        #Diccionario cuya clave será el tipo de ruta y el valor una lista con infracciones. Cada infracción tendrá la velocidad a la que iba y la fecha.
        infractions={}
        for x in lines:
            line=x.split("&&&&")
            if line[0] in infractions:
                infractions[line[0]].append((line[1],line[2][:-1]))
            else:
                infractions[line[0]]=[(line[1],line[2][:-1])]
        return infractions

'''
    Dada una cadena de caracteres que representa un comando en bash, lanza dicho comando.
'''
def run_cmd(cmd):
    ip = subprocess.check_output(cmd, shell=True).decode('utf-8').replace('\n', '').split(' ')
    return ip[0]

'''
   Obtiene el algoritmo de cifrado y la clave RSA asociada a la RPI que realiza las funcionalidades de cliente (radar).
'''
def run_rsa(cmd):
    return '_'.join( subprocess.check_output(cmd, shell=True).decode('utf-8').split(' ')[:-1] )

