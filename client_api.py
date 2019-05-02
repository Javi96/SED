# -*- coding: utf-8 -*-

from flask import Flask, request
import json
import requests
import sys

from utils import run_cmd, run_rsa


RSA_PATH_JAVI = '/home/javi/.ssh/id_rsa.pub'
RSA_PATH_RASP = '/etc/ssh/ssh_host_ed25519_key.pub'


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
    
    
    
    #Constructor. El cliente, en función de los parámetros que le proporcionamos
    #se conecta al servidor de una forma u otra.
    def __init__(self,rt):
        
        #IP DEL CLIENTE: request.remote_addr
        
        self.other_clients={} 
        #self.server_ip = server_ip
        self.server_ip=request.remote_addr
        self.port = '5555'
        self.client_ip = run_cmd('hostname -I') + ':' + self.port
        self.route_type = rt
        self.rsa_key= run_rsa('ssh-keygen -lf ' + RSA_PATH_JAVI)
        
        #El cliente estable conexión con el servidor.
        #La conexión se realiza mediante la conexión post.
         
        u="http://"+self.server_ip+"/add_client"
        
        p={'client_rsa_key': self.rsa_key, 'client_route_type':self.route_type}
        
        r = requests.post(url=u, json=p)
        
        data=json.loads(r.text.replace("'",'"'))
        
        
        '''
        if data['server_ip'] != server_ip:
            raise Exception('Se ha recibido información no procedente del servidor')
            
        '''

        '''
        return str({"State":"OK","client_max_speed": server.max_speed[route_type], \
               "ip_list": server.client_ips, "rsa_keys_list": server.rsa_keys })
        '''
        
        self.max_speed=data['client_max_speed']
        #self.ip_list=data['ip_list']
        self.other_clients=data['rsa_keys_list']
        
        print('Cliente configurado con parametros:')
        print('IP propia :', self.client_ip)
        print('IP de los demás clientes: ', self.other_clients)
        print('Tabla de velocidades máximas :', self.max_speed)
        print('Tabla de otras IPs & claves RSA: ', self.other_clients)
        
    def run(self): 
        app.run(debug=False, host='0.0.0.0', port=self.port) 

    def informa_infracción(self, time, speed):
        #Informa al servidor de que ha sucedido una infracción.
        u="http://"+self.server_ip+"/infraction"
        p={'client_route_type': self.route_type, \
           'client_infraction_date': 'FECHA' , 'client_max_speed': self.max_speed,
           'client_real_speed':speed }
        
        #Se envía esta información al servidor.
        #r=requests.post(url=u, json=p)
        requests.post(url=u, json=p)
        
        #POR AHORA, NO ESPERAMOS RESPUESTA
        


'''
    Método para ver si la api está activada.
'''
@app.route('/', methods=['GET'])
def state():
    return 'Cliente API avaliable'


@app.route('/add_new_neigh',methods=['GET','POST'])
def add_new_neighbour(self):
    print('Se ha agregado un vecino ')
    data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    
    '''    
    if data['server_ip'] != server_ip:
            raise Exception('Se ha recibido información no procedente del servidor')
    '''
    if data['server_ip'] != request.remote_addr:
        raise Exception('Se ha recibido información no procedente del servidor')
    
    #Añadimos la IP y la clave RSA a la lista almacenada por el cliente.
    self.other_clients[data['client_ip']]=data['client_rsa_key']


@app.route('/modify_speed',methods=['GET','POST'])
def modify_speed(self):
    data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    
    '''    
    if data['server_ip'] != server_ip:
            raise Exception('Se ha recibido información no procedente del servidor')
    '''
    if data['server_ip'] != request.remote_addr:
        raise Exception('Se ha recibido información no procedente del servidor')
    
    #Solo si tiene el tipo de vía modificado.
    if self.route_type==data['route_type']:
        self.max_speed=data['max_speed']


if __name__ == '__main__':
    
    client=Client('route1')    
    client.run()
	  