import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = ""
PORT = 10888

# 获取本机ip
try:
    s.connect(('8.8.8.8', 80))
    my_addr = s.getsockname()[0]
    HOST = str(my_addr)
except Exception as ret:
    # 若无法连接互联网使用，会调用以下方法
    print("无法获取ip，请连接网络！\n")
finally:
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定地址和端口
try:
    s.bind((HOST, PORT))
except Exception as ret:
    print("启动时遇到错误！\n")
    quit()

print("启动成功\n正在监听中...")
user = {}

while True:
    try:
        (data, addr) = s.recvfrom(1024)
        if (user.get(addr, False) == False):
            user[addr] = data.decode('utf-8')
            print("IP:%s NickName:%s Join" % (addr, data.decode('utf-8')))
        else:
            data = user[addr] + " : " + data.decode('utf-8')
            print(data)
            for key, value in user.items():
                if key != addr:
                    s.sendto(data.encode('utf-8'), key)
    except Exception as ret:
        print(ret)
        continue
