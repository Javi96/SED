# -*- coding: utf-8 -*-

from flask import Flask, request
import json
import requests
from utils import run_cmd


'''

    1- AÑADIR CLIENTE

    DEL CLIENTE AL SERVIDOR

    client_ip ==> ip del cliente que quiere conectarse al sistema.
    client_route_type ==> tipo de vía del cliente que quiere conectarse al sistema
    client_rsa_key ==> clave RSA asociada al cliente que quiere conectarse al sistema

    
    DEL SERVIDOR AL CLIENTE
    
    ip_list ==> lista de IPs. Cada ip está asociada a otros clientes conectados al sistema.
    max_speed ==> velocidad máxima asociada al tipo de vía.
    rsa_keys_list ==> lista de claves rsa. Cada clave está asciada a otros clientes conectados al sistema.
    
    DEL SERVIDOR A LOS DEMÁS CLIENTES
    
    client_ip ==> ip del nuevo cliente conectado al sistema.
    client_rsa_key ==> clave rsa del nuevo cliente conectado al sistema.
    
    2- INFORMAR DE INFRACCIÓN
    
    DEL CLIENTE AL SERVIDOR
    
    client_infraction_date ==> fecha de la infracción (dia y hora)
    client_route_type ==> tipo de vía en la que ha sucedido la infracción.
    client_real_speed ==> velocidad detectada por el cliente.
    client_max_speed ==> velocidad máxima permitida en el tramo en el que está situado el cliente
    client_ip ==> ip del cliente que informa que ha sucedido una infracción
'''

'''
    Parámetros del servidor
'''
    

'''
    Implementación del servidor
'''

app=Flask(__name__)

class Server:
    
    '''
        ATRIBUTOS
        
        1- client_ips: lista con las ip de todos los clientes conectados.
        2- rsa_keys: diccionario que asocia las ips de los clientes con sus claves RSA.
        3- max_speed: diccionario que asocia las velocidades máximas asociadas a cada tipo de vía.
        
    '''
    
    
    def __init__(self):
        self.client_ips=list()
        self.rsa_keys={}
        self.speeds_file='speed_db'
        #self.max_speed={'route1': 120, 'route2': 100, 'route3': 80, 'route4': 50}
        self.max_speed=self.__load_speeds()
        self.puerto=5555
        self.ip=run_cmd('hostname -I')+':'+str(self.puerto)

        print('my ip: ', self.ip)
        
    def __load_speeds(self):
        with open(self.speeds_file, "r") as myfile:
            lines = myfile.readlines()
            
        #Para cada línea, crea una entrada en la caché.
        self.max_speed = {}
        for x in lines:
            parsed_line=x.split()
            self.max_speed[parsed_line[0]]= json.loads(parsed_line[1].replace("'",'"'))
        
        return self.max_speed
    
    def change_road_speed(self,route_type,new_speed):
        if route_type in self.max_speed:
            self.max_speed[route_type]=new_speed
        '''  
            #Informamos a los clientes sobre la nueva moficación.
            for x in server.client_ips:
                u="http://"+x+"/modify_speed"
                p={'route_type':route_type, 'new_speed':new_speed, 'server_ip': server.ip}
                r = requests.post(url=u, json=p)
                print(r)
        '''
            
        #Si ese tipo de ruta no existe, no hace nada.
        print('Se ha intentado modificar un tipo de vía no existente.')
    
    def run(self):
        app.run(debug=False, host='0.0.0.0', port=self.puerto) 


'''
    Método para ver si la api está activada.
'''
@app.route('/', methods=['GET'])
def state():
    return 'Server API avaliable'


'''
    Método para informar al servidor de que ha sucedido una infracción.
        
    No devuelve nada.
'''

@app.route('/infraction', methods=['GET','POST'])
def process_infraction():
    #El resultado es un string con forma de json. Reemplazamos ' por " para que encaje con el formato de json.
    data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    
    ip=request.remote_addr
    #ip= data['client_ip']
    route_type = data['client_route_type']
    date=data['client_infraction_date']
    real_speed=data['client_real_speed']
    max_speed=data['client_max_speed']
    
    
    print('IP del cliente: ', ip)
    print('Tipo de via del cliente: ', route_type)
    print('Fecha de la infracción: ', date)
    print('IP del cliente conectado: ', ip)
    print('Velocidad real de la infracción: ', real_speed)
    print('Velocidad máxima asociada al tipo de tramo: ', max_speed)

    
    #Realizamos las actualizaciones que corresponda.
    return str({"State":"OK"})


'''
    Añade la ip del cliente que llama al método a la lista de ips que tiene el cliente.
    La ip se transmite a través del cuerpo del mensaje POST. La IP está en el campo 'ip'.

    Devuelve la lista con las ips de todos los clientes (incluyendo la suya).
'''

@app.route('/add_client', methods=['GET','POST'])
def add_client():
    #El resultado es un string con forma de json. Reemplazamos ' por " para que encaje con el formato de json.
    data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    
    #Obtenemos la ip del nuevo cliente.
    #ip= data['client_ip']
    ip=request.remote_addr
    
    
    #Obtenemos el tipo de vía en el cual se ha instalado el cliente.
    route_type = data['client_route_type']
    
    #Obtenemos su clave RSA asociada.
    rsa_key= data['client_rsa_key']

    #Informamos a los demás clientes del nuevo cliente.
    #Le pasamos el RSA asociado y su IP.
    
    
    # for x in server.client_ips:
        
    #     #-------------------------------------------------
    #     #TERMINACIÓN DE LA FUNCIONALIDAD DEL CLIENTE DONDE 
    #     #RECOGE LA RSA KEY Y LA IP DE UN NUEVO CLIENTE.
        
    #     #X CONTIENE TANTO LA IP COMO EL PUERTO (ENTRE :) EN FORMA DE STRING.
        
    #     #-------------------------------------------------
    #     u="http://"+x+"/add_new_neigh"
    #     p={'client_ip':ip, 'client_rsa_key': rsa_key, 'server_ip': server.ip}
    #     r = requests.post(url=u, json=p)
    #     print(r)
    
    
    #Añadimos la ip del nuevo cliente a la lista de ips.
    server.client_ips.append(ip)
    
    #Añadimos la clave RSA asociada al nuevo cliente en el diccionario de claves RSA.
    server.rsa_keys[ip]=rsa_key
    
    #DEBUGGING --------->Mostramos los valores que le devolvemos   
    
    
    print('Un cliente con ip ', ip, ' se ha conectado al sistema.' )
    print('Su clave RSA es ', rsa_key, '.')
    print('Esta en el tipo de vía ', route_type , '.' )

    print('Estado del servidor')

    print('IPs clientes ',server.client_ips)
    print('Claves RSA asociadas al cliente ',server.rsa_keys)
   


    
    #Devolvemos al nuevo cliente: la lista de ips de los demás clientes, la tabla de 
    #velocidades máximas y las claves RSA.
    return str({"State":"OK","client_max_speed": server.max_speed[route_type], \
               "rsa_keys_list": server.rsa_keys,'server_ip':server.ip })

if __name__ == '__main__':
    server=Server()
    server.run()
	  