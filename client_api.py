# -*- coding: utf-8 -*-

'''
    Implementación del cliente 
    
    Incluye un servicio Rest que responderá a las solicitudes vía HTTP de los demás 
    clientes y del propio servidor.
    
    Establece la configuración para dicho servicio Rest y también para el correcto
    uso del protocolo SFTP y SSH para el intercambio de información de infracciones detectadas
    con los demás radares del sistema.
'''

#Imports necesarios
from flask import Flask, request
import json
import requests
import sys
import os
from utils import run_cmd, run_rsa,RSA_PATH_RASP, SAVE_FILE_PATH, DB_PATH, RED_BASH

'''
    Instrucciones bash (sin completar) que se introduciran en el fichero red.sh 
    para cada uno de los demás clientes del sistema (sin incluir este).
'''
BASH_FILE = ["""SSHPASS=raspberry sshpass -e sftp -oBatchMode=no -b - pi@""", """ << ! 
cd /home/pi/Desktop/github/SED-PROYECTO/db
lcd /home/pi/Desktop/github/SED-PROYECTO/db
get localhost.txt """, """.txt
bye
!
"""]

KEYS_FILE = "/home/pi/.ssh/known_hosts"

# pasamos la ip del server y puerto por parametro: <<ip>> <<port>> 
server_ip= str(sys.argv[1]) + ':' + str(sys.argv[2])


'''
    Implementación del cliente (RADAR)
'''

app=Flask(__name__)

class Client:
    
    '''
        ATRIBUTOS DEL CLIENTE
        
        1- other_clients:
            Diccionario que relaciona las ips de los demás clientes con su clave RPA.
            Se usa para la transferencia de info a través de SFTP para conversar la información
            en el caso de que se pierda la conexión con el servidor.
            
        2- server_ip:
            Dirección IP del servidor al que se tiene que conectar el radar para 
            informar sobre una infracción, etc.
            
        3- route_type: 
            tipo de vía en la que se instancia el cliente.
    
        4- client_ip:
            ip del cliente (RADAR) que se conecta al sistema
        
        5- rsa_key:
            clave RSA asociada al protocolo SFTP del cliente.
            
        6- max_speed: 
            máxima velocidad asociada al tipo de vía del usuario.
        
    '''
    
    '''
        ATRIBUTOS DEL CLIENTE
        
        1- other_clients: diccionario que almacena las ips de los demás radares que contiene
        el sistema y sus correspondientes claves RSA.
        
        2- server_ip: ip del servidor al cual se tiene que conectar el radar para su configuración
        y para informar sobre las infracciones detectadas.
        
        3- port: puerto en el que se va a desplegar el proceso que sostenga el servicio Rest.
        
        4- client_ip: ip del computador que lanza las funcionalidades del cliente (radar)
        
        5- route_type: tipo de ruta en la que está desplegada el radar.
        
        6- rsa_key: clave rsa asociada al cliente (radar) que lanza el servicio Rest.
        
        7-
    '''
    
    #Constructor. El cliente, en función de los parámetros que le proporcionamos
    #se conecta al servidor de una forma u otra.
    def __init__(self,rt):
        
        #IP DEL CLIENTE: request.remote_addr        
        self.other_clients={} 
        self.server_ip=server_ip
        self.port = '5555'
        self.client_ip = run_cmd('hostname -I') + ':' + self.port
        self.route_type = rt
        self.rsa_key= run_rsa('cat ' + RSA_PATH_RASP)
        
        #El cliente estable conexión con el servidor.
        #La conexión se realiza mediante la conexión post.
        u="http://"+self.server_ip+"/add_client"
        p={'client_rsa_key': self.rsa_key, 'client_route_type':self.route_type}
        r = requests.post(url=u, json=p)        
        data=json.loads(r.text.replace("'",'"'))
                
        self.max_speed=data['client_max_speed']
        self.other_clients=data['rsa_keys_list']
        
        print('Cliente configurado con parametros:')
        print('IP propia :', self.client_ip)
        print('IP de los demás clientes: ', self.other_clients)
        print('Tabla de velocidades máximas :', self.max_speed)
        print('Tabla de otras IPs & claves RSA: ', self.other_clients)
        self.config_dir()
        self.save_bs()
        self.save_key()
        
    '''
        Si no existe el fichero contenido en SAVE_FILE_PATH, lo crea.
    '''
    def config_dir(self):
        if not os.path.exists(DB_PATH):
            os.makedirs(DB_PATH)
        if not os.path.isfile(SAVE_FILE_PATH):
            open(SAVE_FILE_PATH, 'w+').close()


    '''
        Escribe las instrucciones en bash asociadas al intercambio de información
        utilizando SFTP y SSH con los demás radares del sistema.
    '''
    def save_bs(self):
        with open(RED_BASH, 'w+', encoding='utf-8') as bs_file:
            for client in self.other_clients.keys():
                if str(client) != str(self.client_ip.split(':')[0]):
                    info = BASH_FILE[0] + client + BASH_FILE[1] + client.split('.')[-1] + BASH_FILE[2]
                    bs_file.write(info)
    
    '''
        Asocia la IP de cada radar del sistema a su correspondiente clave RSA.        
    '''
    def save_key(self):
        with open(KEYS_FILE, 'w+', encoding='utf-8') as key_file:
            for client in self.other_clients.keys():
                if str(client) != str(self.client_ip.split(':')[0]):
                    info = client + " " + self.other_clients[client].replace("_"," ") + "\n"
                    key_file.write(info)

    '''
        Lanza el servicio Rest
    '''
    def run(self): 
        app.run(debug=False, host='0.0.0.0', port=self.port) 


        


'''
    Método para ver si la api está activada.
'''
@app.route('/', methods=['GET'])
def state():
    return 'Cliente API avaliable'

'''
    Dada la fecha en la que se ha detectado la velocidad a la que iba un conductor y la velocidad detectada,
    en función del tipo de vía en el que el radar esté desplegado (almacenado en self.route_type), infiere si 
    ha ocurrido una infracción y, si ha sucedido, informa al servidor.
'''
@app.route('/informa_infraccion/<time>/<speed>')
def informa_infraccion(time, speed):
    #Informa al servidor de que ha sucedido una infracción.
    
    if float(speed) > float(client.max_speed):
        u="http://"+client.server_ip+"/infraction"
        p={'client_route_type': client.route_type, \
           'client_infraction_date': time , 'client_max_speed': client.max_speed,
           'client_real_speed':speed }
        
        #Se envía esta información al servidor.
        requests.post(url=u, json=p)        
        
        with open(SAVE_FILE_PATH, 'a+', encoding='utf-8') as save_file:
            data = '\t'.join([time, speed]) + '\n'
            save_file.write(data)
        
        return 'True'
    return 'False'


'''
    Se llama cuando se añade un nuevo radar.
    
    Cuando se añade un nuevo radar al sistema, el servidor llama a este método para que los demaś
    radares almacenen información sobre el nuevo radar y puedan comunicarse con este.
    
    El radar recibe la ip y la clave RSA del nuevo radar y lo almacena para comunicarse con este en 
    un futuro.
'''
@app.route('/add_new_neigh',methods=['GET','POST'])
def add_new_neighbour():
    print('Se ha agregado un vecino ')
    data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    if client.server_ip.split(':')[0] != request.remote_addr:
        raise Exception('Se ha recibido información no procedente del servidor')
    
    #Añadimos la IP y la clave RSA a la lista almacenada por el cliente.
    client.other_clients[data['client_ip']]=data['client_rsa_key']
    client.save_bs()
    client.save_key()
    return 'ok'

'''
    Dado un tipo de ruta y una nueva velocidad, si el radar está establecido en este tipo de vía, modifica su 
    velocidad máxima permitida asociada.
'''
@app.route('/modify_speed',methods=['GET','POST'])
def modify_speed():
    data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    
    if client.server_ip.split(':')[0] != request.remote_addr:
        raise Exception('Se ha recibido información no procedente del servidor')
    
    #Solo si tiene el tipo de vía modificado.
    if client.route_type==data['route_type']:
        client.max_speed=data['max_speed']
        print('se ha cambiado la velocidad a ', client.max_speed)
    return 'ok'

'''
    Se inicializa el cliente con el tipo de ruta en el que se establece y se lanza el servicio Rest.
'''
if __name__ == '__main__':
    client=Client('route6')    
    client.run()
      
