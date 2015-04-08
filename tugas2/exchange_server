import time
import zmq
import requests
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:1337")

while True:	
	message = socket.recv()
	print("REQUEST!!!")
	jsoned = json.loads(message)
	apiResponse = requests.get(
		'http://jsonrates.com/convert/?'+
		'from=IDR'+
		'&to=USD'+
		'&amount='+str(jsoned)+
		'&prettify=yes'+
		'&apiKey=jr-4791c3b5d240af239cf81e3ae228f79b'
		)
	
	json_resp = apiResponse.json()
	amount = float(json_resp['amount'])
	print amount
	to_send = json.dumps(amount)
	socket.send(to_send)
