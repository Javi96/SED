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
        self.infractions_file='infractions_db'
        self.max_speed=self.__load_speeds()
        self.infractions=self.__load_infractions()
        self.puerto=5555
        self.ip=run_cmd('hostname -I')+':'+str(self.puerto)

        print('Server initialization')
        print('-----------------------------------------')
        print( "Here's my ip: ", self.ip)
        print('Route speeds: ', self.max_speed)
        print('Connected clients :', self.client_ips)
        print('-----------------------------------------')
        
    def __load_speeds(self):
        with open(self.speeds_file, "r") as myfile:
            lines = myfile.readlines()
            
        #Para cada línea, crea una entrada en la caché.
        self.max_speed = {}
        for x in lines:
            parsed_line=x.split()
            self.max_speed[parsed_line[0]]= json.loads(parsed_line[1].replace("'",'"'))
        
        return self.max_speed
    
    def __load_infractions(self):
        with open(self.infractions_file, "r") as myfile:
            lines = myfile.readlines()
        
        print(lines)
        #Diccionario cuya clave será el tipo de ruta y el valor una lista con infracciones. Cada infracción tendrá la velocidad a la que iba y la fecha.
        self.infractions={}
        for x in lines:
            line=x.split("&&&&")
            if line[0] in self.infractions:
                self.infractions[line[0]].append((line[1],line[2][:-1]))
            else:
                self.infractions[line[0]]=[(line[1],line[2][:-1])]
        print(self.infractions)
    
    def save_infraction(self,route_type, speed, date):
        with open(self.infractions_file, "a") as myfile:
            line=route_type+ "&&&&" +speed +"&&&&"+date + '\n'
            myfile.write(line)
    
    def save_speeds(self):
         with open(self.speeds_file, "w+") as myfile:
            for x, y in self.max_speed.items():
                line= str(x)+ ' '+str(y) + '\n'  
                myfile.write(line)
    
    def run(self):
        app.run(debug=False, host='0.0.0.0', port=self.puerto) 


'''
    Método para ver si la api está activada.
'''
@app.route('/', methods=['GET'])
def state():
    return 'Server API avaliable'

@app.route('/new_speed/<route_type>/<new_speed>', methods=['GET'])
def change_road_speed(route_type,new_speed):
    
    print('Cambio de velocidad')
    print('-----------------------------------------')
    print( "Route type: ", route_type)
    print('New speed: ', new_speed)
    print('Connected clients :', server.client_ips)
    print('-----------------------------------------')
    
    
    if route_type in server.max_speed:
        server.max_speed[route_type]=new_speed
        
        #Informamos a los clientes sobre la nueva moficación.
        for x in server.client_ips:
            u="http://"+x+":5555/modify_speed"
            p={'route_type':route_type, 'max_speed':new_speed, 'server_ip': server.ip}
            r=requests.post(url=u, json=p)
            print('-Sended to ',x,':5555. Response: ', r)
            
        #Sobreescribimos el contenido del fichero dónde se almacena la información sobre las velocidades.
        server.save_speeds()
        
        
        
        return 'OK'

    #Si ese tipo de ruta no existe, no hace nada.
    print('Se ha intentado modificar un tipo de vía no existente.')

'''
    Método para informar al servidor de que ha sucedido una infracción.
        
    No devuelve nada.
'''

@app.route('/infraction', methods=['GET','POST'])
def process_infraction():
    #El resultado es un string con forma de json. Reemplazamos ' por " para que encaje con el formato de json.
    data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    
    ip=request.remote_addr
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


    #La almacenamos en el fichero de infracciones.
    server.save_infraction(route_type,real_speed,date)
    
    
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
    ip=request.remote_addr
    #Obtenemos el tipo de vía en el cual se ha instalado el cliente.
    route_type = data['client_route_type']
    #Obtenemos su clave RSA asociada.
    rsa_key= data['client_rsa_key']
    #Informamos a los demás clientes del nuevo cliente.
    #Le pasamos el RSA asociado y su IP.
    for x in server.client_ips:
         u="http://"+x+":5555/add_new_neigh"
         p={'client_ip':ip, 'client_rsa_key': rsa_key}
         requests.post(url=u, json=p)
    
    #Añadimos la ip del nuevo cliente a la lista de ips.
    server.client_ips.append(ip)
    
    #Añadimos la clave RSA asociada al nuevo cliente en el diccionario de claves RSA.
    server.rsa_keys[ip]=rsa_key
    
    #DEBUGGING --------->Mostramos los valores que le devolvemos   
    
    print('----------------------------------------------------------------------')
    print('Un cliente con ip ', ip, ' se ha conectado al sistema.' )
    print('Su clave RSA es ', rsa_key, '.')
    print('Esta en el tipo de vía ', route_type , '.' )

    print('Estado del servidor')

    print('IPs clientes ',server.client_ips)
    print('Claves RSA asociadas al cliente ',server.rsa_keys)
    print('----------------------------------------------------------------------')

    #Devolvemos al nuevo cliente: la lista de ips de los demás clientes, la tabla de 
    #velocidades máximas y las claves RSA.
    return str({"State":"OK","client_max_speed": server.max_speed[route_type], \
               "rsa_keys_list": server.rsa_keys })

if __name__ == '__main__':
    server=Server()
    server.run()
	  