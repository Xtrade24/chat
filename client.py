import socket

import threading

import time

key = 8194

shutdown = False
join = False

def receving (name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                print(data.decode('utf-8'))

                decrypt = ""; k = False
                for i in data.decode("utf-8"):
                    if i == ":":
                        k = True
                        decrypt += i
                    elif k == False or i == " ":
                        decrypt += i
                    else:
                        decrypt += chr(ord(i)^key)
                print(decrypt)

                time.sleep(0.2)
        except:
            pass

host = socket.gethostbyname(socket.gethostname())
port = 0

server = ("192.168.1.155", 9090)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = input("Введи свое имя, котрое будет использоваться в чате:    ")

rT = threading.Thread(target = receving, args = ("RecvThread", s))
rT.start()

while shutdown == False:
    if join == False:
        s.sendto(("["+alias+"] ==> ПРИСОЕДИНИЛСЯ ").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()

            crypt = ""
            for i in message:
                crypt += chr(ord(i)^key)
            message = crypt

            if message != "":
                s.sendto(("["+alias+"] :: "+message).encode("utf-8"), server)

            time.sleep(0.2)

        except:
            s.sendto(("["+alias+"] <== ОТКЛЮЧИЛСЯ "+message).encode("utf-8"), server)
            shutdown = True

rT.join()
s.close()
