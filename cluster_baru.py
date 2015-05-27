#!/usr/bin/env python
# run worker first: ./dispynode.py -d -i ip_address_worker
# run manager: ./kdd-cluster.py
# hadrianbsrg

def compute(s, format):    
    from PIL import Image
    import dispy, random
    import StringIO
    import base64

    #recv and convert image, with PIL
    recv = bytearray(base64.b64decode(s))
    simpan = StringIO.StringIO()
    simpan.write(recv)
    simpan.seek(0)
    img = Image.open(simpan).convert('L')

    hasil = StringIO.StringIO()
    img.save(hasil, format)
    hasilSend = hasil.getvalue()
    hasil.close()

    byte = bytearray(hasilSend)
    send = base64.b64encode(byte)
    return send

if __name__ == '__main__':
    import dispy, random
    from PIL import Image
    import base64
    import StringIO
    import thread
    import os

    # initiate cluster
    cluster = dispy.JobCluster(compute, nodes=['10.151.64.*'])
    jobs = []


    #open dataset directories
    gambar = []
    datasetdir = "D:/sister/dataset/"
    resultdir = "D:/sister/converted/"
    filename = os.listdir(datasetdir)
    for img in filename:
        gambar.append(img)
    print gambar

    
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
        ##print imgSend[:512]
        imgString.close()

        byte = bytearray(imgSend)
        s = base64.b64encode(byte)
        print "Sending Data :", s[:55]

        job = cluster.submit(s, format)
        job.id = idx
        idx = idx+1
        jobs.append(job)
        print "Index :",idx
        print "Job Error :",job.result
        
    index = 0
    print "Uh"
    for job in jobs:
        recv = job()
        print "Decoding...."
        byteTerima = bytearray(base64.b64decode(recv))
        
        #saveimg
        simpan = StringIO.StringIO()
        simpan.write(byteTerima)
        simpan.seek(0)
        simpanImg = Image.open(simpan)
        simpanImg.save(resultdir + "converted_" + gambar[index], format)
        index = index + 1
        print "done"
    cluster.stats()
