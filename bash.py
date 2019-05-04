# -*- coding: utf-8 -*-

'''
    Ejecuta el contenido de red.sh de forma periódica.
    
    Se lanza por parte del cliente.
    
    red.sh incluye los comportamientos necesarios para que, utilizando SFTP y SSH, un cliente pueda obtener la información
    sobre incidencias que los demás clientes han obtenido.
    
    De esta forma, existen copias redundantes de la información extraída y, en el caso de que se pierda la conexión con el servidor, 
    no se pierde dicha información.
'''

#Imports necesarios
import time
import os
import stat

os.chmod("red.sh", stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

while True:
    os.system("./red.sh")
    time.sleep(3)
    
