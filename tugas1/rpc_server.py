import rpyc
import cv2
import os
from rpyc.utils.server import ThreadedServer


class Greyscaler(rpyc.Service):
    def on_connect(self):
        print "someone's connected!"

    def on_disconnect(self):
        pass

    def exposed_openFile(self, filename, mode):
        return open(filename, mode)
        print filename

    def exposed_convertImage(self, rgb_image):
        image = cv2.imread(rgb_image)
        convert = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('converted_' + rgb_image, convert)

    def exposed_delete(self, filename):
        os.remove(filename)
        os.remove('converted_' + filename)

if __name__ == "__main__":
   
    hostname = raw_input()
    port = raw_input()
    print hostname, port
    t = ThreadedServer(Greyscaler, hostname=hostname, port=int(port), protocol_config={"allow_public_attrs": True})
    t.start()
