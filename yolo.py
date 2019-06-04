import socket
from yoloPydarknet import pydarknetYOLO
import cv2
import imutils
import time

class Yolo():
	def __init__(self, ip="192.168.0.177", port=8080):
		##### YOLO #####
		self.yolo = pydarknetYOLO(obdata="/home/titi/darknet/cfg/coco.data", weights="/home/titi/darknet/yolov3.weights", cfg="/home/titi/darknet/cfg/yolov3.cfg")
		self.results = {
			'labels': [],
			'scores': [],
			'middleX': [],
			'middleY': [],
			'area': []
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
			imgData = client.recv(1024)
			if not imgData:
				break
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
			Area = width * height
			self.results['labels'].append(label)
			self.results['scores'].append(score)
			self.results['middleX'].append(middle_x)
			self.results['middleY'].append(middle_y)
			self.results['area'].append(Area)
		print("Labels:", self.results['labels'])
		print("middleX:", self.results['middleX'])
		print("middleY", self.results['middleY'])
		print("area", self.results['area'])
		cv2.imwrite("results.jpg", img)

	def target(self):
		personScore = []
		personIndex = []
		for index, name in enumerate(self.results['labels']):
			if name == "person":
				personIndex.append(index)
				personScore.append(self.results['scores'][index])
		if not personScore == []:
			maxIndex = personScore.index(max(personScore))
			Index = personIndex[0]
			return (self.results['middleX'][Index], self.results['middleY'][Index], self.results['area'][Index])
		else:
			return (None, None, None)

	def send_results(self, X, Y, A):   
		HOST = "192.168.0.145"
		PORT = 5050
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		pkg = "{} {} {}".format(X, Y, A)
		s.send(bytes(pkg, encoding="utf8"))
		s.close()
		self.clean_results()

	def clean_results(self):
		self.results = {
			'labels': [],
			'scores': [],
			'middleX': [],
			'middleY': [],
			'area': []
		} 

if __name__ == "__main__":
	exe = Yolo(ip="192.168.0.177", port=8080)
	while True:
		print("socket_server")
		exe.socket_server()
		exe.yolo_detect()
		time.sleep(1)
		X, Y, A = exe.target()
		time.sleep(1)
		exe.send_results(X, Y, A)
		time.sleep(1)
