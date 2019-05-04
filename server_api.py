# -*- coding: utf-8 -*-

'''
    Módulo que representa el servidor.
    
    Implementa el servicio API Rest que permitirá que el servidor responda a las solicitudes vía HTTP 
    de los clientes y se comunique con ellos.
    
    De esta forma, el servidor configurará los parámetros necesarios para que los clientes funcionen correctamente 
    y procesará la información sobre las detecciones de infracciones que dichos clientes le han proporcionado.
'''

#Imports necesarios.
from flask import Flask, request
import json
import requests
from utils import run_cmd


'''
    Implementación del servidor
'''

#Aplicación que representa el servicio Rest que se va a lanzar.
app=Flask(__name__)

class Server:
    
    '''
        ATRIBUTOS
        
        1- client_ips: lista con las ips de todos los clientes (radares) conectados.
        2- rsa_keys: lista que asocia las ips de los clientes (radares) con sus claves RSA para que, entre ellos, puedan comunicarse vía SFTP.
        3- speeds_file: ubicación del fichero donde se encuentra la información asociada a las máximas velocidades para cada tipo de vía.
        4- infraccions_file: ubicación del fichero donde se encuentran almacenadas las infracciones detectadas hasta el momento.
        5- max_speed: diccionario que almacena las velocidades máximas asociadas a cada tipo de vía.
        6- infractions: diccionario que almacena las infracciones detectadas hasta el momento.
        7- puerto: puerto a través del cual se va a lanzar el proceso.
        8- ip: dirección ip del computador que lanza el servicio del servidor.
    '''    
    
    
    '''
        MÉTODOS DE LA CLASE SERVER
    '''
    
    #Constructor.
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
        print('Connected clients :', self.client_ips)
        print('-----------------------------------------')
        
    '''
        Carga en el atributo self.max_speed las velocidades máximas asociadas a cada tipo de ruta.
        Estas velocidades máximas se almacenan en el fichero que marca self.speeds_file
    '''
    def __load_speeds(self):
        with open(self.speeds_file, "r") as myfile:
            lines = myfile.readlines()
            
        #Para cada línea, crea una entrada en la caché.
        self.max_speed = {}
        for x in lines:
            parsed_line=x.split()
            self.max_speed[parsed_line[0]]= json.loads(parsed_line[1].replace("'",'"'))
        
        return self.max_speed
    
    
    '''
        Carga en el diccionario self.infractions las infracciones almacenadas previamente por el sistema.
        Estas, se almacenan en el fichero self.infractions_file.
    '''
    def __load_infractions(self):
        with open(self.infractions_file, "r") as myfile:
            lines = myfile.readlines()
        
        #Diccionario cuya clave será el tipo de ruta y el valor una lista con infracciones. Cada infracción tendrá la velocidad a la que iba y la fecha.
        self.infractions={}
        for x in lines:
            line=x.split("&&&&")
            if line[0] in self.infractions:
                self.infractions[line[0]].append((line[1],line[2][:-1]))
            else:
                self.infractions[line[0]]=[(line[1],line[2][:-1])]
    
    '''
        Dado un tipo de ruta (string) en el cual se ha detectado una infracción y la fecha en la que se sucedido 
        en formato YYYY_MM_DD_HH_MM_SS_MMMMMM (string), se almacena la nueva infracción detectada en el diccionario self.infractions
        y en el fichero ubicado en self.infractions_file
    
        Se llama a este método cuando se ha detectado una nueva infracción y se desea almacenarla en el sistema.
    '''
    def save_infraction(self,route_type, speed, date):
        with open(self.infractions_file, "a") as myfile:
            line=route_type+ "&&&&" +speed +"&&&&"+date + '\n'
            myfile.write(line)
    
    '''
        Almacena el contenido de self.max_speed en el fichero self.speeds_file.
        
        Dicho de otra forma, sobreescribe el contenido del fichero ubicado en self.speeds_file, donde se almacenaban
        las velocidades máximas permitidas asociadas a cada tipo de vía, introduciendo el contenido de self.max_speeds.
        
        Se utiliza cuando se ha realizado una modificación en las velocidades máximas asociadas a un tipo de vía.
    '''
    def save_speeds(self):
         with open(self.speeds_file, "w+") as myfile:
            for x, y in self.max_speed.items():
                line= str(x)+ ' '+str(y) + '\n'  
                myfile.write(line)
    
    '''
        Lanza el servicio Rest
    '''
    def run(self):
        app.run(debug=False, host='0.0.0.0', port=self.puerto) 


'''
    MÉTODOS DEL SERVICIO REST
'''

'''
    Método para ver si la api está activada.
'''
@app.route('/', methods=['GET'])
def state():
    return 'Server API avaliable'


'''
    Dado un tipo de ruta (string) y un número que representa una velocidad (int o double), 
    introduce dicha velocidad como la nueva velocidad máxima permitida asociada al tipo de ruta introducido.
'''
@app.route('/new_speed/<route_type>/<new_speed>', methods=['GET'])
def change_road_speed(route_type,new_speed):
    
    print('-----------------------------------------')
    print('--------------MAX SPEED CHANGED------------')
    print('Max speed change on route ', route_type)
    print('New speed set as ', new_speed)
    print('Connected clients :', server.client_ips)
    print('-----------------------------------------')
    
    #Si ese tipo de ruta existe.
    if route_type in server.max_speed:
        server.max_speed[route_type]=new_speed
        
        #Informamos a los clientes sobre la nueva moficación.
        for x in server.client_ips:
            u="http://"+x+":5555/modify_speed"
            p={'route_type':route_type, 'max_speed':new_speed, 'server_ip': server.ip}
            r=requests.post(url=u, json=p)
            #Muestra que se informa del cambio a todos los radares del sistema.
            print('-Sended to ',x,':5555. Response: ', r)
            
        #Sobreescribimos el contenido del fichero dónde se almacena la información sobre las velocidades.
        server.save_speeds()
        return 'OK'

    #Si ese tipo de ruta no existe, no hace nada.
    print('Se ha intentado modificar un tipo de vía no existente.')
    return 'Error'
    
'''
    Método para informar al servidor de que ha sucedido una infracción. 
    En el cuerpo del mensaje se almacena un JSON que contiene el tipo de ruta en el que ha sucedido la infracción,
    la fecha en la que ha sucedido, la velocidad a la que iba en infractor y la velocidad máxima permitida.
    
    
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
    
    print('---------------------------------------------------')
    print('------------- INFRACTION DETECTED ----------------')
    print('IP del cliente: ', ip)
    print('Tipo de via del cliente: ', route_type)
    print('Fecha de la infracción: ', date)
    print('IP del cliente conectado: ', ip)
    print('Velocidad real de la infracción: ', real_speed)
    print('Velocidad máxima asociada al tipo de tramo: ', max_speed)
    print('---------------------------------------------------')
    
    #La almacenamos en el fichero de infracciones.
    server.save_infraction(route_type,real_speed,date)
    
    #Realizamos las actualizaciones que corresponda.
    return str({"State":"OK"})


'''
    Añade la ip del cliente que llama al método a la lista de ips que tiene el servidor.
    El servidor le devuelve los parámetros de configuración necesarios para el correcto 
    funcionamiento del nuevo cliente (radar) e informa a los demás clientes de la existencia
    del nuevo radar.
    
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
    print('--------------------NEW CLIENT------------------------')
    print('Un cliente con ip ', ip, ' se ha conectado al sistema.' )
    print('Su clave RSA es ', rsa_key, '.')
    print('Esta en el tipo de vía ', route_type , '.' )
    print('IPs clientes ',server.client_ips)
    print('Claves RSA asociadas al cliente ',server.rsa_keys)
    print('----------------------------------------------------------------------')

    #Devolvemos al nuevo cliente: la lista de ips de los demás clientes, la tabla de 
    #velocidades máximas y las claves RSA.
    return str({"State":"OK","client_max_speed": server.max_speed[route_type], \
               "rsa_keys_list": server.rsa_keys })

    
#Se lanza el servicio Rest después de configurarlo como corresponde.
if __name__ == '__main__':
    server=Server()
    server.run()
	  