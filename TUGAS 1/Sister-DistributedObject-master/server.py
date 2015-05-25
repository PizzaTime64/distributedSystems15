import Pyro4
from base64 import b64decode
import cv2
import numpy as np

class Server(object):
    def __init__(self):
        pass

    def hellO(self):
        print("HELLo")

    def crazy(self, file):
        a = file.read()

    def rgb_to_grayscale(self, arr):
        grayscales = []
        for ele in arr:
            data = ele['data']
            grayscale_m = cv2.imdecode(np.asarray(bytearray(b64decode(data)), dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            grayscales.append(bytearray(cv2.imencode('.png', grayscale_m)[1].tostring()))
        return grayscales






def main():
    alamat = raw_input('Alamat bind: ')
    port = int(raw_input('Port: '))
    server = Server()
    Pyro4.Daemon.serveSimple(
            {
                server: "sister.converter"
            },
            host=alamat,
            port=port,
            ns = False)

if __name__=="__main__":
    main()
