import rpyc
import threading
import time
import os
import shutil

class ClientConn:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = rpyc.connect(host, int(port))

class Main:
    def __init__(self, serverAddress, datasetDir, convertedDir, imgTotal):
        self.serverAddress = serverAddress
        self.datasetDir = datasetDir
        self.convertedDir = convertedDir
        self.imgTotal = int(imgTotal)
        self.clrImg = os.listdir(self.datasetDir)
        self.node_list = []
        self.threads = []
        self.elapsed_time = 0

    def worker(self, node, clrImg):
        for x in clrImg:
            print node.host, x
            loc = open(self.datasetDir + x, 'rb')
            remote = node.conn.root.openImg(x, 'wb')
            shutil.copyfileobj(loc, remote)
            loc.close()
            remote.close()
            node.conn.root.convertImage(x)
            loc = open(self.convertedDir + x, 'wb')
            remote = node.conn.root.open('converted_' + x, 'rb')
            shutil.copyfileobj(remote, loc)
            loc.close()
            remote.close()
            node.conn.delImg(x)

    def run(self):
        for x in self.serverAddress:
            host, port = x.split(':')
            print host, port
            self.node_list.append(ClientConn(host, port))

        serverCounter = 0

        t_start = time.time()
        i = 0
        j = self.imgTotal
        while True:
            if len(self.clrImg) == 0:
                break
            if len(self.clrImg) == i:
                break
            if len(self.node_list) == serverCounter:
                serverCounter = 0 #0 lagi kalo udah ke server terakhir

            t = threading.Thread(target = self.worker, args = (self.node_list[serverCounter], self.clrImg[i:j]))
            self.threads.append(t)
            t.start()

            for x in range(i, j):
                del self.clrImg[0]

            serverCounter += 1

        for thread in self.threads:
            thread.join()

        self.elapsed_time = time.time() - t_start

if __name__ == "__main__":

    serverAddress = ["127.0.0.1:1337"]
    print serverAddress
    datasetDir = "D:\\datasetimg\\"
    convertedDir = "D:\\converted\\"
    print "jumlah img yang mau di convert ?"
    imgTotal = raw_input()

    main = Main(serverAddress, datasetDir, convertedDir, imgTotal)
    main.run()

    print main.elapsed_time
