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
from service.services import LibrarySystem
from ui.login import LoginDialog
from ui.library import MainWindow

def main():
    app = QApplication(sys.argv)
    
    library_system = LibrarySystem()

    login_dialog = LoginDialog(library_system)
    
    def on_login_success():
        login_dialog.close()
        main_window = MainWindow(library_system)
        main_window.show()
    
    login_dialog.login_success.connect(on_login_success)
    
    login_dialog.exec_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()