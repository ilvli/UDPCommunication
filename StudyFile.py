import threading
from time import ctime, sleep


def music(musicName):
    for i in range(2):
        print("I was listening to %s. %s" % (musicName, ctime()))
        sleep(1)


def move(moveName):
    for i in range(2):
        print("I was at the %s! %s" % (moveName, ctime()))
        sleep(3)


threads = []
t1 = threading.Thread(target=music, args=('爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=move, args=('阿凡达',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        # setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。
        t.setDaemon(True)
        t.start()
    # join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
    t.join()

    print("all over %s" % ctime())
