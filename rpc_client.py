import cv2
import rpyc
import sys
import os
from rpyc.utils.server import ThreadedServer

class Greyscaler(rpyc.Service):

    def on_connect(self):
        #code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self):
        #code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass

    #exposed : bisa di akses dari luar
    def exposed_convertImage(self, clrImg):
        img = cv2.imread(clrImg)
        convert = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('converted_' + clrImg, convert)

    def exposed_openImg(self, namaFile, mode):
        return open(namaFile, mode)

    def exposed_delImg(self, namaFile):
        os.remove(namaFile)
        os.remove('converted_' + namaFile)

if __name__ == "__main__":
    hostname = "127.0.0.1"
    port = 1337
    print hostname, port

    t = ThreadedServer(Greyscaler, hostname=hostname, port = int(port), protocol_config={"allwo_public_attrs": True})
    t.start()
