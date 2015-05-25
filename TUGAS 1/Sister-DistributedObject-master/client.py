# This is the code that visits the warehouse.
import Pyro4
import os
import threading
import time
from base64 import b64decode

def kirim_gambar(daftarFile, r_object, jumlah, nama):
    daftarGambar = []
    n = 0
    while (n + jumlah < len(daftarFile)):
        for i in range(n, n+jumlah):
            f = open(daftarFile[i], 'rb')
            daftarGambar.append(bytearray(f.read()))
            f.close()
        i = n
        daftarGrayscale = r_object.rgb_to_grayscale(daftarGambar)
        for grayscale in daftarGrayscale:
            f = open(daftarFile[i][:-4] + '_grayscale.png', 'wb')
            f.write(b64decode(grayscale['data']))
            f.close()
            i += 1
        daftarGambar[:] = []
        n += jumlah
        print nama + ": " + str(n) + '/' + str(len(daftarFile))

    for i in range(n, len(daftarFile)):
        f = open(daftarFile[i], 'rb')
        daftarGambar.append(bytearray(f.read()))
        f.close()
    i = n
    daftarGrayscale = r_object.rgb_to_grayscale(daftarGambar)
    for grayscale in daftarGrayscale:
        f = open(daftarFile[i][:-4] + '_grayscale.png', 'wb')
        f.write(b64decode(grayscale['data']))
        f.close()
        i += 1
    print nama + ' selesai'


dir = raw_input("Direktori gambar: ")
uri1 = raw_input("URI #1: ").strip()
uri2 = raw_input("URI #2: ").strip()
os.chdir(dir)
r_object1 = Pyro4.Proxy(uri1)
r_object2 = Pyro4.Proxy(uri2)
jumlahBatch = int(raw_input("Jumlah gambar per request: "))
files = os.listdir(os.getcwd())
jumlahFile = len(files)

thread1 = threading.Thread(target=kirim_gambar, args=(files[0:jumlahFile/2], r_object1, jumlahBatch, 'Thread 1'))
thread2 = threading.Thread(target=kirim_gambar, args=(files[jumlahFile/2:jumlahFile], r_object2, jumlahBatch, 'Thread 2'))
start = time.time()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print 'SELESAI yeee, waktu: ' + str(time.time() - start)