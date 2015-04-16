import zmq
import StringIO
import os

os.chdir('D:/Semester 6/Sister/tugas2/New folder/grey')

context = zmq.Context()
worker_socket = context.socket(zmq.PULL)
worker_socket.bind('tcp://*:5556')
ventilator_socket = context.socket(zmq.PUSH)
ventilator_socket.connect('tcp://localhost:5557')

while True:
    img_dict = worker_socket.recv_pyobj() 
    print("Menerima file %s" % img_dict['nama']) 
    f = open(img_dict['nama'], 'wb')
    f.write(img_dict['data'].getvalue()) 
    f.close()
    print("Selesai menyimpan %s" % img_dict['nama'])
    ventilator_socket.send_string("Selesai memproses %s" % img_dict['nama'])


