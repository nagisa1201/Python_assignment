'''
Author: Nagisa 2964793117@qq.com
Date: 2025-12-15 22:22:25
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2025-12-15 22:24:21
FilePath: \Python_assignment\python_assignment\assignment_final\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
from PyQt5.QtWidgets import QApplication
from services import LibrarySystem
from ui.login import LoginDialog
from ui.main import MainWindow

def main():
    # 初始化Qt应用
    app = QApplication(sys.argv)
    
    # 创建图书馆系统实例
    library_system = LibrarySystem()
    
    # 显示登录窗口
    login_dialog = LoginDialog(library_system)
    
    # 定义登录成功后的回调函数
    def on_login_success():
        # 关闭登录窗口
        login_dialog.close()
        # 显示主窗口
        main_window = MainWindow(library_system)
        main_window.show()
    
    # 连接登录成功信号
    login_dialog.login_success.connect(on_login_success)
    
    # 显示登录窗口并启动应用循环
    login_dialog.exec_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()