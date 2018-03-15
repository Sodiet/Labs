import socket
import os

TCP_IP = 'localhost'
TCP_PORT = 8000
BUFFER_SIZE = 1024
CUR_DIR = os.getcwd()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    conn, address = s.accept()
    data = conn.recv(BUFFER_SIZE)
    request = str(data).split('\r\n', 1)[0].split(' ')[1]

    if request == "/about/aboutme.html":
        file = open(CUR_DIR + request, mode='r')
        conn.send(("HTTP/1.1 200 OK \n Content type:text HTML\n\n\n " + file.read()).encode())
        file.close()

    elif request == "/index.html" or request == "/":
        file = open(CUR_DIR + "/index.html", mode='r')
        conn.send(("HTTP/1.1 200 OK \n Content type:text HTML\n\n\n " + file.read()).encode())
        file.close()
    else:
        file = open(CUR_DIR + "/404.html", mode='r')
        conn.send(("HTTP/1.1 404 Not found \n Content type:text HTML\n\n\n " + file.read()).encode())
        file.close()

conn.close()
s.close()