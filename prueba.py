# -*- coding: utf-8 -*-


from coapthon.client.helperclient import HelperClient

client = HelperClient(server=('0.0.0.0', 5555))
response = client.get('/')
print(response)
client.stop()


'''
from coapthon.client.helperclient import HelperClient
from coapthon.messages.request import Request
from coapthon import defines

host = "localhost"
port = 5555
path = ""
payload = ''

client = HelperClient(server=(host, port))

request = Request()
request.destination = (host, port)
response = client.send_request(request)

client.stop()
'''
'''
import txthings.coap as coap

def responder(response):
    print(response.payload)

protocol =coap.Coap(None)
request = coap.Message(code=coap.GET)

request.remote = ("0.0.0.0",5555)

d= protocol.request(request, observeCallback=responder)
'''
