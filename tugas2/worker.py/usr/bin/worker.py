#!/usr/bin/python
import zmq
import os
from PIL import Image
import StringIO

def get_format(filename):
    img_format = filename[filename.rfind('.')+1:].upper()
    if (img_format == 'JPG'):
        img_format = 'JPEG'
    return img_format

context = zmq.Context()
#agar dapat menerima task, buat (zmq)socket yang terhubung ke ventilator
ventilator_socket = context.socket(zmq.PULL)
#baca alamat ventilator dari file
file = open('ventilator', 'r')
ventilator_socket.connect(file.read())
file.close()
sink_socket = context.socket(zmq.PUSH)
file = open('sink', 'r')
sink_socket.connect(file.read())

#infinite loop! worker senantiasa menunggu kerjaan
while True:
    img_dict = ventilator_socket.recv_pyobj();
    print("Menerima file %s, mulai mengkonversi..." % img_dict['nama'])
    try:
        img_format = get_format(img_dict['nama'])
        img = Image.open(img_dict['data'])
        img = img.convert('L')
        data = StringIO.StringIO()
        img.save(data, img_format)
        img_dict['data'] = data
        print("Konversi selesai, mengirim...")
        sink_socket.send_pyobj(img_dict)
        print("Pengiriman file %s selesai" % img_dict['nama'])
    except Exception as e:
        print("Error! %s" % e)
