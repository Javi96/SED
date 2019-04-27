# -*- coding: utf-8 -*-

from flask import Flask, request
import json


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
    
puerto=5555

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
        self.max_speed={'route1': 120, 'route2': 100, 'route3': 80, 'route4': 50}
        
    def run(self):
        app.run(debug=False, host='0.0.0.0', port=puerto) 


'''
    Método para ver si la api está activada.
'''
@app.route('/', methods=['GET'])
def state():
    return 'Server API avaliable'


'''
    Método para informar al servidor de que ha sucedido una infracción.
    
    Parámetros:
        -infraction_type: Tipo de infracción que ha sucedido.
        
    No devuelve nada.
'''

@app.route('/infraction/<infraction_type>', methods=['GET'])
def process_infraction(infraction_type):
    print('Ha sucedido una infracción tipo '+ infraction_type)
    
    #Realizamos las actualizaciones que corresponda.
    return str({"State":"OK"})


'''
    Añade la ip del cliente que llama al método a la lista de ips que tiene el cliente.
    La ip se transmite a través del cuerpo del mensaje POST. La IP está en el campo 'ip'.

    Devuelve la lista con las ips de todos los clientes (incluyendo la suya).
'''

@app.route('/add_client', methods=['POST'])
def add_client():
    #El resultado es un string con forma de json. Reemplazamos ' por " para que encaje con el formato de json.
    data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    
    #Obtenemos la ip del nuevo cliente.
    ip= data['client_ip']
    
    #Obtenemos el tipo de vía en el cual se ha instalado el cliente.
    route_type = data['client_route_type']
    
    #Obtenemos su clave RSA asociada.
    rsa_key= data['client_rsa_key']
    
    #Añadimos la ip del nuevo cliente a la lista de ips.
    server.client_ips.append(ip)
    
    #Añadimos la clave RSA asociada al nuevo cliente en el diccionario de claves RSA.
    server.rsa_keys[ip]=rsa_key
    
    #DEBUGGING --------->Mostramos los valores que le devolvemos    
    print(server.client_ips)
    print(server.rsa_keys)
    
    #Informamos a los demás clientes del nuevo cliente.
    
    #for x in 
    
    
    #Devolvemos la lista con las ips de los demás clientes
    return str({"State":"OK", "ip_list":server.client_ips})
    

if __name__ == '__main__':
    server=Server()
    server.run()
	  