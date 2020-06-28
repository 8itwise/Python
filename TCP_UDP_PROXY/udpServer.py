import socket

host = '127.0.0.1'
port = 2000

def udpMsg():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        sock.setblocking(0)
    except socket.error as e:
        print(str(e))

    print "Server running......"

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print data
        except:
            pass
    s.close()

udpMsg()
