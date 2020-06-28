import time
import socket
import argparse

def connect(proxy_ip, proxy_port, host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((proxy_ip, int(proxy_port)))
    except socket.error as e:
        print("Failed to create socket.")

    print("Connect to proxy")
    time.sleep(1)
    sock.send(host)
    time.sleep(1)
    sock.send(port)

    while True:
        msg = raw_input("-> ")
        sock.send(msg)
    s.close()

parser = argparse.ArgumentParser(description="Client arguments")
parser.add_argument('-Pi', '--proxy_ip', type=str, metavar='', required=True, help='Specify proxy ip')
parser.add_argument('-Pp', '--proxy_port', type=str, metavar='', required=True, help='Specif proxy port')
parser.add_argument('-i', '--host', type=str, metavar='', required=True, help='Specify host ip')
parser.add_argument('-p', '--port', type=str, metavar='', required=True, help='Specify host port')
args = parser.parse_args()

connect(args.proxy_ip, args.proxy_port, args.host, args.port)
