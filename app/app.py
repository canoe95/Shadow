# coding:utf-8

import sys
import window
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
# import pymysql
import threading


import pymysql

path = "./"


class Controller:
    def __init__(self):
        pass

    def show_login(self):
        self.login = LoginDialog()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        self.login.close()
        self.window = MainDialog()
        self.window.switch_window.connect(self.shutdown)
        self.window.show()
        from shadow import shadow;
        self.p = threading.Thread(target=shadow)
        # 设置为守护进程，当父进程结束时，将被强制终止
        self.p.daemon = True
        self.p.start()

    def shutdown(self):
        print("-------- 结束接收数据 -----------")
        sys.exit()



class MainDialog(QDialog):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = window.Ui_Dialog_Main()
        self.setWindowIcon(QIcon(path + "logo.ico"))
        self.ui.setupUi(self)

    # 传递信号，调用新一层函数
    def close(self):
        self.switch_window.emit()

    def ask(self):
        query = self.ui.textEdit.toPlainText().strip()
        print("收到询问: " + query)
        from shadow import chat
        back = chat(query)
        print("处理结果: " + back)
        self.ui.textEdit.setText(back)





class LoginDialog(QDialog):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = window.Ui_Dialog_Login()
        self.setWindowIcon(QIcon(path + "logo.ico"))
        self.ui.setupUi(self)


    # 调用后端接口登录判断
    def verily(self, name, email):
        conn = pymysql.connect(host = '43.163.218.127' # 连接名称，默认127.0.0.1
            ,user = 'root' # 用户名
            ,passwd='011026' # 密码
            ,port= 3306 # 端口，默认为3306
            ,db='aides' # 数据库名称
            ,charset='utf8' # 字符编码
        )
        cur = conn.cursor() # 生成游标对象
        sql = "select * from `user` where `name`= " + '\'' + name + '\'' # SQL语句
        #print(sql)
        cur.execute(sql) # 执行SQL语句
        data = cur.fetchall() # 通过fetchall方法获得数据
        cur.close()
        conn.close()
        if len(data) > 1 or len(data) == 0:
            return False
        elif data[0][1] != email:
            return False
        return True

    
    def write_conf(self, name, email, pwd, mode):
        with open(path+"shadow.conf", 'w') as f:
            f.write("name: " + name + "\n")
            f.write("email: " + email + "\n")
            f.write("password: " + pwd + "\n")
            f.write("mode: " + mode + "\n")

    def start(self):
        name = self.ui.name.text()
        email = self.ui.email.text()
        pwd = self.ui.pwd.text()
        mode = self.ui.mode.text()
        if self.verily(name, email):
            self.write_conf(name, email, pwd, mode)
            # 跳转主页面
            self.switch_window.emit()


    
    def clear(self):
        self.ui.name.clear()
        self.ui.email.clear()
        self.ui.pwd.clear()




if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = Controller()
    myDlg.show_login()
    sys.exit(myapp.exec_())
