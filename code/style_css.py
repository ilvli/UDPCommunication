class style():
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