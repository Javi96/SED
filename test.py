import time
import json
import requests
def parse_bytes_to_JSON(input):
    decoded = input.decode('utf8') #Decodificamos usando utf-8. El resultado es un string con forma de json.
    return json.loads(decoded)  #Creamos el json a partir del string    

if __name__ == '__main__':

    # fo = open("file.txt", "a")
    # fo.seek(0, 2)
    # fo.write('holaa')
    # fo.close()
    # ?ip=147.96.1.1&via=C&rsa=esto_es_el_rsa
    url = "http://0.0.0.0:5555/test"
    params = {
        "ip": "147.96.1.1",
        "via": "C",
        "rsa": "rsa_value"
    }

    # data=json.loads(request.get_data().decode('utf8').replace("'",'"'))
    data = json.loads(requests.post(url, data=params).text.replace("'", '"'))
    print(data['State'])
