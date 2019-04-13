# -*- coding: utf-8 -*-

from flask import Flask, request
import json


'''
    Parámetros del servidor
'''
    
puerto=5555

'''
    Implementación del servidor
'''

app=Flask(__name__)

class Server:
    
    def __init__(self):
        self.client_ips=list()
        
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
    
    server.client_ips.append(data['ip'])
    
    print(server.client_ips)
    
    #Devolvemos la lista con las ips de los demás clientes
    return str({"State":"OK", "ip_list":server.client_ips})
    

if __name__ == '__main__':
    server=Server()
    server.run()
	  