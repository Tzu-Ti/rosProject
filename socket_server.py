import socket

class Socket_server():
	def __init__(self, ip="192.168.0.177", port=8080):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((ip, port))
		self.server.listen(5)

	def getImage(self):
		client, addr = self.server.accept()
		print("Connected by", addr)
		imgFile = open("socketImage.jpg", 'wb')
		while True:
			imgData = client.recv(1024)
			if not imgData:
				break
			imgFile.write(imgData)
		imgFile.close()
		print("image save")
		client.close()
