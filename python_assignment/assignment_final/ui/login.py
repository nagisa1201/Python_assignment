# 登录界面
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal

class LoginDialog(QDialog):
    login_success = pyqtSignal()
    def __init__(self, library_service):
        super().__init__()

        self.library_service = library_service  # 存放业务逻辑层实例，ui和业务逻辑分离

        self._init_ui()
        self._bind_signals()

    def _init_ui(self):
        self.setWindowTitle("图书管理系统 - 登录")
        self.setMinimumSize(550, 350) 
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 20)

        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("用户名："))
        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("请输入用户名")
        user_layout.addWidget(self.user_edit)

        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(QLabel("密码："))
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.pwd_edit.setPlaceholderText("请输入密码")
        pwd_layout.addWidget(self.pwd_edit)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("登录")
        self.register_btn = QPushButton("注册")
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)

        layout.addLayout(user_layout)
        layout.addLayout(pwd_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _bind_signals(self):
        self.login_btn.clicked.connect(self._login)
        self.register_btn.clicked.connect(self._register)
        self.library_service.signals.user_operation.connect(self._show_msg)

    def _login(self):
        username = self.user_edit.text().strip()
        password = self.pwd_edit.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空！")
            return
        success = self.library_service.login(username, password)
        if success:
            self.login_success.emit()
            self.close()

    def _register(self):
        username = self.user_edit.text().strip()
        password = self.pwd_edit.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空！")
            return
        self.library_service.register_user(username, password)

    def _show_msg(self, success, msg):
        if success:
            QMessageBox.information(self, "提示", msg)
        else:
            QMessageBox.warning(self, "警告", msg)