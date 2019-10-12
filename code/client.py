import socket
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

HOST = ""
PORT = 10888
NickName = ""


class logindialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('登录界面')
        self.resize(250, 200)
        self.setFixedSize(self.width(), self.height())
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 设置界面控件
        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入用户名")
        self.lineEdit_IP = QLineEdit()
        self.lineEdit_IP.setPlaceholderText("请输入主机IP地址")
        self.pushButton_get_ip = QPushButton()
        self.pushButton_get_ip.setText("获取本机IP")
        pushButton_enter = QPushButton()
        pushButton_enter.setText("确定")
        pushButton_quit = QPushButton()
        pushButton_quit.setText("退出")

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit_account)
        layout.addWidget(self.lineEdit_IP)
        layout.addWidget(self.pushButton_get_ip)
        layout.addWidget(pushButton_enter)
        layout.addWidget(pushButton_quit)
        self.setLayout(layout)

        # 绑定按钮事件
        pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        pushButton_quit.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton_get_ip.clicked.connect(self.click_get_ip)

    def on_pushButton_enter_clicked(self):
        # 用户名判断
        if self.lineEdit_account.text() == "":
            return
        else:
            global NickName
            NickName = self.lineEdit_account.text()
        # IP地址判断
        if self.lineEdit_IP.text() == "":
            return
        else:
            global HOST
            HOST = self.lineEdit_IP.text()
        # 通过验证，关闭对话框并返回1
        self.accept()

    def click_get_ip(self):
        """
        pushbutton_get_ip控件点击触发的槽
        :return: None
        """
        # 获取本机ip
        self.lineEdit_IP.clear()
        try:
            self.s1.connect(('8.8.8.8', 80))
            my_addr = self.s1.getsockname()[0]
            self.lineEdit_IP.setText(str(my_addr))
        except Exception as ret:
            # 若无法连接互联网使用，会调用以下方法
            try:
                my_addr = socket.gethostbyname(socket.gethostname())
            except Exception as ret_e:
                QMessageBox.information(self, '提示', "无法获取ip，请连接网络！", QMessageBox.Yes)
        finally:
            self.s1.close()


class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.iniUI()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.sendto(NickName.encode('utf-8'), (HOST, PORT))
        # 初始化线程
        self.my_thread = MyThread(self.s)  # 实例化线程对象
        self.my_thread.my_signal.connect(self.append_message_func)
        self.my_thread.start()  # 启动线程

    def iniUI(self):
        self.resize(800, 500)
        self.center()
        self.setWindowTitle('UDPCommunication')
        # 设置控件
        self.messageWindow = QTextBrowser()
        self.inputWindow = QLineEdit(self)
        self.btn = QPushButton('发送', self)
        self.btn.move(230, 380)
        self.qbtn = QPushButton('退出', self)
        self.qbtn.move(550, 380)

        # 设置布局
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout1.addWidget(self.btn)
        layout1.addWidget(self.qbtn)
        layout2.addWidget(self.inputWindow)
        layout2.addLayout(layout1)
        layout3.addWidget(self.messageWindow)
        layout3.addLayout(layout2)
        self.setLayout(layout3)

        self.btn.clicked.connect(self.send)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', "确定要退出吗?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def send(self):
        if self.inputWindow.text() == "":
            self.messageWindow.insertHtml(self.toHtml("red", "请先输入信息！"))
        else:
            try:
                send_msg = (str(self.inputWindow.text())).encode('utf-8')
                self.s.sendto(send_msg, (HOST, PORT))
                self.messageWindow.insertHtml(self.toHtml("black", self.inputWindow.text()))
            except Exception as ret:
                print(ret)
                self.messageWindow.insertHtml(self.toHtml("red", "发送失败！"))
        self.inputWindow.clear()
        time.sleep(1)

    def append_message_func(self, messagae):
        self.messageWindow.insertHtml(self.toHtml("black", messagae))

    def toHtml(self, c, s):
        return "<font color='"+c+"' font-size='20'>" + s + "</font><br>"


class MyThread(QThread):  # 线程类
    my_signal = pyqtSignal(str)  # 自定义信号对象。参数str就代表这个信号可以传一个字符串

    def __init__(self, socket):
        super(MyThread, self).__init__()
        self.s = socket

    def run(self):  # 线程执行函数
        print('UDP服务端正在监听端口:{}\n'.format(PORT))
        while True:
            (data, addr) = self.s.recvfrom(1024)
            print(data.decode('utf-8'))
            self.my_signal.emit(data.decode('utf-8'))  # 释放自定义的信号
            time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = logindialog()
    if dialog.exec_() == QDialog.Accepted:
        window = ClientWindow()
        window.show()
    sys.exit(app.exec_())
