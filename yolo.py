import socket
from yoloPydarknet import pydarknetYOLO
import cv2
import imutils
import time

class Yolo():
	def __init__(self, ip="192.168.0.177", port=8080):
		##### YOLO #####
		self.yolo = pydarknetYOLO(obdata="/home/titi/darknet/cfg/coco.data", weights="/home/titi/darknet/yolov3-tiny.weights", cfg="/home/titi/darknet/cfg/yolov3-tiny.cfg")
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
		##### Start socket server ######
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((self.ip, self.port))
		server.listen(1)
		client, addr = server.accept()
		print("Connected by", addr)

		##### Write image #####
		imgFile = open("socketImage.jpg", 'wb')
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
		server.close()

	def yolo_detect(self):
		img = cv2.imread("socketImage.jpg")
	
		self.yolo.getObject(img, labelWant="", drawBox=True, bold=1, textsize=0.6, bcolor=(0,0,255), tcolor=(255,255,255))
		for i in range(self.yolo.objCounts):
			left, top, width, height, label, score = self.yolo.list_Label(i)
			middle_x = left + width/2
			middle_y = top + height/2
			self.results['labels'].append(label)
			self.results['scores'].append(score)
			self.results['middleX'].append(middle_x)
			self.results['middleY'].append(middle_y)	
		print("Object counts:", self.yolo.objCounts)
		cv2.imwrite("results.jpg", img)

	#def target():
	#		if 

	def send_results(self):
		HOST = "192.168.0.145"
		PORT = 5050
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		s.send(bytes("hello", encoding="utf8"))
		s.close()

if __name__ == "__main__":
	exe = Yolo(ip="192.168.0.177", port=8080)
	while True:
		print("socket_server")
		exe.socket_server()
		exe.yolo_detect()
		time.sleep(1)
		exe.send_results()
		time.sleep(1)
