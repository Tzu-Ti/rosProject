import socket
from yoloPydarknet import pydarknetYOLO
import cv2
import imutils
import time

class Yolo():
	def __init__(self, ip="192.168.0.177", port=8080):
		##### YOLO #####
		self.yolo = yolo = pydarknetYOLO(obdata="/home/titi/darknet/cfg/coco.data", weights="/home/titi/darknet/yolov3-tiny.weights", cfg="/home/titi/darknet/cfg/yolov3-tiny.cfg")
		self.results = {
			'labels': [],
			'scores': [],
			'middleX': [],
			'middleY': []
		}

		##### Socket server #####
		self.ip = ip
		self.port = port
		
		

	def socket_server(self):
		imgFile = open("socketImage.jpg", 'wb')
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((self.ip, self.port))
		server.listen(5)
		client, addr = server.accept()
		print("Connected by", addr)
		while True:
			#print("enter while")
			imgData = client.recv(1024)
			if not imgData:
				break
			#print("write over")
			imgFile.write(imgData)
		imgFile.close()
		print("image save")
		client.close()

if __name__ == "__main__":
	exe = Yolo(ip="192.168.0.177", port=8080)
	while True:
		print("socket_server")
		exe.socket_server()
		time.sleep(2)
	#exe.socket_server()
	exe.server.close()
