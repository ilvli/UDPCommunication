import socket
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont

HOST = ""
PORT = 10888
NickName = ""


class logindialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("..\\src\\sun.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('登录')
        self.resize(280, 230)
        self.setFixedSize(self.width(), self.height())
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sty = style

        # 添加界面控件
        self.lineEdit_account = QLineEdit()
        self.lineEdit_IP = QLineEdit()
        self.pushButton_get_ip = QPushButton("获取本机IP")
        self.pushButton_enter = QPushButton("确定")
        self.pushButton_quit = QPushButton("退出")
        # 设置控件提示文本
        self.lineEdit_account.setPlaceholderText("请输入用户名")
        self.lineEdit_IP.setPlaceholderText("请输入主机IP地址")
        # 设置控件大小
        self.lineEdit_account.setFixedSize(250, 30)
        self.lineEdit_IP.setFixedSize(250, 30)
        self.pushButton_get_ip.setFixedSize(250, 25)
        self.pushButton_enter.setFixedSize(250, 25)
        self.pushButton_quit.setFixedSize(250, 25)
        # 设置按键样式
        self.pushButton_get_ip.setStyleSheet(self.sty.buttonStyle())
        self.pushButton_enter.setStyleSheet(self.sty.buttonStyle())
        self.pushButton_quit.setStyleSheet(self.sty.buttonStyle())
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit_account, alignment=Qt.AlignCenter)
        layout.addWidget(self.lineEdit_IP, alignment=Qt.AlignCenter)
        layout.addWidget(self.pushButton_get_ip, alignment=Qt.AlignCenter)
        layout.addWidget(self.pushButton_enter, alignment=Qt.AlignCenter)
        layout.addWidget(self.pushButton_quit, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # 绑定按钮事件
        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton_get_ip.clicked.connect(self.click_get_ip)

    def on_pushButton_enter_clicked(self):
        # 用户名判断
        if self.lineEdit_account.text() == "":
            QMessageBox.information(self, '提示', "请输入用户名！", QMessageBox.Yes)
            return
        else:
            global NickName
            NickName = self.lineEdit_account.text()
        # IP地址判断
        if self.lineEdit_IP.text() == "":
            QMessageBox.information(self, '提示', "请输入IP地址！", QMessageBox.Yes)
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
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.sendto(NickName.encode('utf-8'), (HOST, PORT))
        # 初始化线程
        self.my_thread = MyThread(self.s)  # 实例化线程对象
        self.my_thread.my_signal.connect(self.append_message_func)
        self.my_thread.start()  # 启动线程
        self.sty = style
        self.iniUI()

    def iniUI(self):
        self.resize(800, 500)
        self.center()
        self.setWindowTitle('UDPCommunication')
        self.setWindowIcon(QIcon("..\\src\\plane.png"))
        # 添加控件
        self.messageWindow = QTextBrowser()
        self.inputWindow = QLineEdit(self)
        self.btn = QPushButton('发送', self)
        self.qbtn = QPushButton('退出', self)
        self.btn.move(230, 380)
        self.qbtn.move(550, 380)
        # 设置按键样式
        self.btn.setStyleSheet(self.sty.buttonStyle())
        self.qbtn.setStyleSheet(self.sty.buttonStyle())

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
            # self.messageWindow.setStyleSheet(self.sty.buttonStyle())
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

        return "<font color='" + c + "' font-size='20'>" + s + "</font><br>"


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


class style():
    # 按键样式
    def buttonStyle():
        fm = "QPushButton{font-family:'Microsoft YaHei'}"  # 字体样式
        fs = "QPushButton{font-size:18px}"  # 字体大小
        fw = "QPushButton{font-weight:bold}"  # 字体加粗
        c = "QPushButton{color:#DCDCDC}"  # 按键前景色
        bc = "QPushButton{background-color:#00BFFF}"  # 按键背景色
        hc = "QPushButton:hover{color:#FFFFFF}"  # 光标移动到上面后的前景色
        hbc = "QPushButton:hover{background-color:#6495ED}"  # 光标移动到上面后的背景色
        br = "QPushButton{border-radius:5px}"  # 圆角半径
        pbr = "QPushButton:pressed{background-color:rgb(180,180,180);border: 5px;}"  # 按下时的样式
        res = fm + fs + fw + c + bc + hc + hbc + br + pbr
        return res


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = logindialog()
    if dialog.exec_() == QDialog.Accepted:
        window = ClientWindow()
        window.show()
    sys.exit(app.exec_())

