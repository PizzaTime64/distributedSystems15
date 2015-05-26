# 'compute' is distributed to each node running 'dispynode'
from PIL import Image
import base64
import StringIO
import Image
import dispy, random

def conv(nameFile):
	stringImage = imgToString(nameFile)
	stringToImg(stringImage, nameFile)
	img = Image.open(nameFile).convert('LA')
	img.save(nameFile + "-greyscale.png")

def stringToImg(stringImage, nameFile):
	fh = open(nameFile, "wb")	
	fh.write(stringImage.decode('base64'))
	fh.close()
	
def imgToString(nameFile):
	with open(nameFile, "rb") as imageFile:
		result = base64.b64encode(imageFile.read())
		return result	

if __name__ == '__main__':
	cluster = dispy.JobCluster(conv)
	jobs = []
	nameFile = 'ktp-1.jpg'
	#nameFile = 'D:/Novita Laksmi Devi 5112100007/coba-dispy/images/ktp-1.jpg'
	job = cluster.submit(conv)
	#stringRecv = job
	#print nameFile
	#print imgToString(nameFile) 
	conv(nameFile)
