import zmq
import json

context = zmq.Context()

print("Connecting to currency exchange server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.101:1337")

while True:
    print("Enter IDR amount\n")
    input = float(raw_input())
    input_jsoned = json.dumps(input)
    socket.send(input_jsoned)

    message = socket.recv()
    json_message = json.loads(message)
    print "USD %.2f" % json_message


