import socket
import sys
import time
import argparse

def proxy(host, port):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock1 = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
	except socket.error as e:
		print("Failed to create socket.")

	sock.bind((host, port))
	sock.listen(2)
	c, addr = sock.accept()
	print("applying proxy for ", addr)

	time.sleep(1)
	destip = c.recv(16)
	destport = c.recv(4)

	sock1.connect((str(destip),int(destport)))

	while(True):
		data = c.recv(1024)
		if not data:
			break
		print("Message received: ", data)
		print("Sending data to udp server...")
		sock1.send(data)
	c.close()
	sock.close()
	sock1.close()


parser = argparse.ArgumentParser(description="Proxy arguments")
parser.add_argument('-i', '--host', type=str, metavar='', required=True, help='Specify host ip')
parser.add_argument('-p', '--port', type=str, metavar='', required=True, help='Specif port')
args = parser.parse_args()


proxy(args.host, int(args.port))
