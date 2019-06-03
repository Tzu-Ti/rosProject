import socket

ip = "192.168.0.177"
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(5)

print("[*] Listening on %s:%d" %(ip, port))

while True:
	client, addr = server.accept()
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
server.close()
