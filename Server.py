import socket
from sys import exit

# Hosted By markjuruo(Linzhihan)
# To view more, please visit
# https://github.com/markjuruo/Python-UDP-Chating

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = input("Please input IP address: ")
PORT = 10888

s.bind((HOST, PORT))

user = {}

while True:
    (data, addr) = s.recvfrom(1024)
    if (user.get(addr, False) == False):
        user[addr] = data.decode('utf-8')
        print("IP(%s) NickName(%s) Join" % (addr, data.decode('utf-8')))
    else:
        print(addr, " : ", data.decode('utf-8'))
        data = user[addr] + " : " + data.decode('utf-8')
        for key, value in user.items():
            if key != addr:
                s.sendto(data.encode('utf-8'), key)
