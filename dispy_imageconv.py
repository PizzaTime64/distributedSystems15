#!/usr/bin/env python

# run worker first: ./dispynode.py -d -i ip_address_worker
# run manager: ./kdd-cluster.py

def compute(s, format):    
    import operator
    from scipy.spatial.distance import euclidean
    from PIL import image
    from StringIO import StringIO
    import base64

    #recv and convert image, with PIL
    recv = bytearray(base64.b64decode(s))
    save = StringIO()
    save.write(recv)
    save.seek(0)
    img = Image.open(save).convert('L')

    hasil = StringIO()
    img.save(hasil, format)
    hasilSend = hasil.getvalue()
    hasil.close()

    byte = bytearray(hasilSend)
    send = base64.b64encode(byte)
    return send

if __name__ == '__main__':
    import dispy, random
    import csv
    import pickle
    from PIL import Image
    import base64
    import StringIO
    import thread
    import os

    # initiate cluster
    cluster = dispy.JobCluster(compute, nodes=['10.151.22.*'])
    jobs = []


    #open dataset directories
    gambar = []
    datasetdir = "D:/sister/dataset/"
    resultdir = "D:/sister/converted/"
    filename = os.listdir(datasetdir)
    for img in filename:
        gambar.append(img)

    #read images, and distribute to clusters?
    idx = 1
    for file in gambar:
        img = Image.open(datasetdir+file)
        if ".png" in file:
            format = "png"
        elif ".jpg" in file:
            format = "jpeg"

        imgString = StringIO.StringIO()
        img.save(imgString, format)
        imgSend = imgString.getvalue()
        imgString.close()

        byte = bytearray(imgSend)
        s = byte64.b64encode(byte)

        recv = cluster.submit(s, format)
        recv.id = idx
        idx = idx+1

        byteTerima = bytearray(base64.b64decode(recv))

        #saveimg
        simpan = StringIO.StringIO()
        simpan.write(byteTerima)
        simpan.seek(0)
        simpanImg = Image.open(simpan)
        simpanImg.save(resultdir + "_converted" + file, format)
        print "done"
