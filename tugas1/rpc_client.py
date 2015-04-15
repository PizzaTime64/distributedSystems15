import rpyc
import os
import threading
import time
import shutil


class Client:
    def __init__(self, host, port):
        self.conn = rpyc.connect(host, int(port))
        self.host = host
        self.port = port

class Main:

    def __init__(self, serverAddress, datasetDir, convertedDir, distrib):
        self.serverAddress = serverAddress
        self.datasetDir = datasetDir
        self.convertedDir = convertedDir
        self.distrib = int(distrib)
        self.datasetFile = os.listdir(self.datasetDir)
        self.serverList = []
        self.threads = []
        self.elapsed_time = 0

    def worker(self, node, datasetFile):
        for filename in datasetFile:
            #print node.host + " >> " + filename +"\n"
            local = open(self.datasetDir + filename, 'rb')
            remote = node.conn.root.openFile(filename, 'wb')
            shutil.copyfileobj(local, remote)
            local.close()
            remote.close()
            node.conn.root.convertImage(filename)
            local = open(self.convertedDir + filename, 'wb')
            remote = node.conn.root.openFile('converted_' + filename, 'rb')
            shutil.copyfileobj(remote, local)
            local.close()
            remote.close()
            node.conn.root.delete(filename)

    def run(self):
        for address in self.serverAddress:
            host, port = address.split(':')
            self.serverList.append(Client(host, port))

        i = 0
        j = self.distrib
        server_selector = 0

        start_time = time.time()
        while True:
            if len(self.datasetFile) == 0:
                break

            if i == len(self.datasetFile):
                break

            if server_selector == len(self.serverList):
                server_selector = 0

            t = threading.Thread(target=self.worker, args=(self.serverList[server_selector], self.datasetFile[i:j]))
            self.threads.append(t)
            t.start()
            for files in range(i, j):
                del self.datasetFile[0]

            server_selector += 1

        for thread in self.threads:
            thread.join()

        self.elapsed_time = time.time() - start_time

if __name__ == "__main__":

    serverAddress = ["127.0.0.1:8888"]
    datasetDir = "D:\datasetimg\\"
    convertedDir = "D:\converted\\"
    distrib = 5

    main = Main(serverAddress, datasetDir, convertedDir, distrib)
    main.run()

    print main.elapsed_time
