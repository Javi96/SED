import time
import json
import requests
import socket
import subprocess
import re
import struct, fcntl
import sys
import os
# from termcolor import colored
RSA_PATH_JAVI = '/home/javi/.ssh/id_rsa.pub'
RSA_PATH_RASP = '/etc/ssh/ssh_host_ed25519_key.pub'


SIOCSIFADDR = 0x8916
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def setIpAddr(iface, ip):
    bin_ip = socket.inet_aton(ip)
    ifreq = struct.pack('16sH2s4s8s', iface, socket.AF_INET, '\x00' * 2, bin_ip, '\x00' * 8)
    fcntl.ioctl(sock, SIOCSIFADDR, ifreq)


def parse_bytes_to_JSON(input):
    decoded = input.decode('utf8') #Decodificamos usando utf-8. El resultado es un string con forma de json.
    return json.loads(decoded)  #Creamos el json a partir del string    

def get_Host_name_IP():
    host_ip = ''
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP") 
    return host_ip

def run_cmd(cmd):
    
    ip = subprocess.check_output(cmd, shell=True).decode('utf-8').replace('\n', '').split(' ')
    return ip[0]


def run_rsa(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8').split(' ')[1]


def get_rsa():

    system_model = tuple(os.uname())[1]
    print(system_model) 
    rsa_value = ''
    if 'rasp' in system_model.lower():
        print(RSA_PATH_RASP)
        with open(RSA_PATH_RASP, 'r') as rsa_file:
            rsa_value = rsa_file.read().split(' ')[1]
    elif 'javi' in system_model.lower():
        print(RSA_PATH_JAVI)
        with open(RSA_PATH_JAVI, 'r') as rsa_file:
            rsa_value = rsa_file.read().split(' ')[1]

    return rsa_value

def connect_server():
    # conectar con server

    setIpAddr('wlp2s0', sys.argv[1])
    port = sys.argv[2]


    url = "http://0.0.0.0:5557/add_client"

    client_rsa_key = run_rsa()
    GET_IP_CMD ="hostname -I"
    client_ip = run_cmd(GET_IP_CMD)
    # print(client_ip)

    params = {
        "client_ip": str(client_ip) + ':' + str(port),
        "client_route_type": "route1",
        "client_rsa_key": client_rsa_key
    }
    # print(params)

 
    
    data = json.loads(requests.post(url, json=params).text.replace("'", '"'))
    print('*******************************************')
    print(data)
    print('*******************************************')

    # ip = socket.gethostbyname(socket.gethostname())
    # print(get_Host_name_IP())
    


if __name__ == '__main__':
    # connect_server()
    print(run_rsa('ssh-keygen -lf ' + RSA_PATH_RASP))
    # 
    # print(run_cmd('hostname -I'))

    # # guardar en fichero
    # fo = open("file.txt", "a")
    # fo.seek(0, 2)
    # fo.write('holaa')
    # fo.close()
    # ?ip=147.96.1.1&via=C&rsa=esto_es_el_rsa

    




 


    # GET_IP_CMD ="hostname -I"

    # setIpAddr('wlp2s0', '192.168.0.48')
    # # setIpAddr('wlan0', '192.168.0.48')

    # ip = run_cmd(GET_IP_CMD)
    # print(ip)





