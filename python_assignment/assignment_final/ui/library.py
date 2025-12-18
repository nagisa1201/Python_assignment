# 主窗口UI
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QTabWidget, QMessageBox,
                             QComboBox, QSpinBox, QMenuBar, QAction, QGridLayout,QHeaderView)
from PyQt5.QtCore import Qt
from datatype.utils import MAX_BORROW
from ui.login import LoginDialog

class MainWindow(QMainWindow):
    def __init__(self, library_service):
        super().__init__()
        self.library_service = library_service
        self.current_user = library_service.current_user
        if self.current_user.username == "admin":
            self.current_user.user_type = "admin"
        print("当前登录用户：", self.current_user.username if self.current_user else "未登录")
        print("当前用户类型：", self.current_user.user_type if self.current_user else "无")
        self._init_ui()
        self._bind_signals()
        self.update_book_table()

    def _init_ui(self):
        self.setWindowTitle(f"图书管理系统 - {self.current_user.username}")
        self.setMinimumSize(800, 600)
        self._init_menubar()  

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 普通用户标签页
        self.book_tab = self._create_book_tab()
        self.tabs.addTab(self.book_tab, "图书查询/浏览")

        self.borrow_tab = self._create_borrow_tab()
        self.tabs.addTab(self.borrow_tab, "借阅/归还")

        self.history_tab = self._create_history_tab()
        self.tabs.addTab(self.history_tab, "借阅历史")
        print(self.library_service._is_admin())

        if self.library_service._is_admin():
            self.manage_tab = self._create_manage_tab()
            self.tabs.addTab(self.manage_tab, "图书管理（管理员）")

    def _init_menubar(self):
        menubar = self.menuBar()
        menubar.clear()  

        file_menu = menubar.addMenu("文件")
        self.logout_action = QAction("退出登录", self)
        self.exit_action = QAction("退出系统", self)
        file_menu.addAction(self.logout_action)
        file_menu.addAction(self.exit_action)

        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "关于", "图书管理系统 v1.0"))

    def _create_book_tab(self):
        """图书查询/浏览页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        search_layout = QHBoxLayout()
        self.search_type = QComboBox()
        self.search_type.addItems(["索引号", "书名", "作者", "分类"])
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("请输入搜索内容")
        search_btn = QPushButton("搜索")
        show_all_btn = QPushButton("显示所有在馆图书")

        search_layout.addWidget(QLabel("搜索条件："))
        search_layout.addWidget(self.search_type)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(show_all_btn)

        self.book_table = QTableWidget()
        self.book_table.setColumnCount(5)
        self.book_table.setHorizontalHeaderLabels(["索引号", "书名", "作者", "分类", "库存"])
        self.book_table.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(search_layout)
        layout.addWidget(self.book_table)

        search_btn.clicked.connect(self.search_book)
        show_all_btn.clicked.connect(self.show_all_books)

        return widget

    def _create_borrow_tab(self):
        """借阅/归还页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 借阅区
        borrow_layout = QHBoxLayout()
        borrow_layout.addWidget(QLabel("借阅图书（输入索引号）："))
        self.borrow_edit = QLineEdit()
        borrow_btn = QPushButton("借阅")
        borrow_layout.addWidget(self.borrow_edit)
        borrow_layout.addWidget(borrow_btn)

        # 归还区
        return_layout = QHBoxLayout()
        return_layout.addWidget(QLabel("归还图书（输入索引号）："))
        self.return_edit = QLineEdit()
        return_btn = QPushButton("归还")
        return_layout.addWidget(self.return_edit)
        return_layout.addWidget(return_btn)

        # 当前借阅表格
        layout.addLayout(borrow_layout)
        layout.addLayout(return_layout)
        layout.addWidget(QLabel("当前借阅图书："))
        self.borrowed_table = QTableWidget()
        self.borrowed_table.setColumnCount(5)
        self.borrowed_table.setHorizontalHeaderLabels(["索引号", "书名", "作者", "分类", "借阅日期"])
        self.borrowed_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.borrowed_table)

        # 绑定事件
        borrow_btn.clicked.connect(self.borrow_book)
        return_btn.clicked.connect(self.return_book)

        return widget

    def _create_history_tab(self):
        """借阅历史页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["索引号", "书名", "作者", "借阅日期", "归还日期", "状态"])
        self.update_history_table()
        layout.addWidget(self.history_table)

        return widget


# ===================================管理员页面============================================
    def _create_manage_tab(self):
        """管理员图书管理页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        add_layout = QVBoxLayout()
        add_layout.addWidget(QLabel("=== 添加新图书 ==="))
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("索引号："), 0, 0)
        self.add_index = QLineEdit()
        form_layout.addWidget(self.add_index, 0, 1)

        form_layout.addWidget(QLabel("书名："), 1, 0)
        self.add_title = QLineEdit()
        form_layout.addWidget(self.add_title, 1, 1)

        form_layout.addWidget(QLabel("作者："), 2, 0)
        self.add_author = QLineEdit()
        form_layout.addWidget(self.add_author, 2, 1)

        form_layout.addWidget(QLabel("分类："), 3, 0)
        self.add_category = QLineEdit()
        form_layout.addWidget(self.add_category, 3, 1)

        form_layout.addWidget(QLabel("库存："), 4, 0)
        self.add_stock = QSpinBox()
        self.add_stock.setMinimum(1)
        self.add_stock.setValue(1)
        form_layout.addWidget(self.add_stock, 4, 1)

        add_btn = QPushButton("添加图书")
        add_layout.addLayout(form_layout)
        add_layout.addWidget(add_btn)

        edit_layout = QVBoxLayout()
        edit_layout.addWidget(QLabel("=== 修改/删除图书 ==="))
        edit_form_layout = QGridLayout()

        edit_form_layout.addWidget(QLabel("目标索引号："), 0, 0)
        self.edit_index = QLineEdit()
        edit_form_layout.addWidget(self.edit_index, 0, 1)

        edit_form_layout.addWidget(QLabel("新书名："), 1, 0)
        self.edit_title = QLineEdit()
        self.edit_title.setPlaceholderText("不修改则留空")
        edit_form_layout.addWidget(self.edit_title, 1, 1)

        edit_form_layout.addWidget(QLabel("新作者："), 2, 0)
        self.edit_author = QLineEdit()
        self.edit_author.setPlaceholderText("不修改则留空")
        edit_form_layout.addWidget(self.edit_author, 2, 1)

        edit_form_layout.addWidget(QLabel("新分类："), 3, 0)
        self.edit_category = QLineEdit()
        self.edit_category.setPlaceholderText("不修改则留空")
        edit_form_layout.addWidget(self.edit_category, 3, 1)

        edit_form_layout.addWidget(QLabel("新库存："), 4, 0)
        self.edit_stock = QSpinBox()
        self.edit_stock.setMinimum(0)
        self.edit_stock.setSpecialValueText("不修改")
        edit_form_layout.addWidget(self.edit_stock, 4, 1)

        btn_layout = QHBoxLayout()
        modify_btn = QPushButton("修改图书")
        delete_btn = QPushButton("删除图书")
        btn_layout.addWidget(modify_btn)
        btn_layout.addWidget(delete_btn)

        edit_layout.addLayout(edit_form_layout)
        edit_layout.addLayout(btn_layout)
        layout.addLayout(add_layout)
        layout.addSpacing(30)
        layout.addLayout(edit_layout)

        add_btn.clicked.connect(self.add_book)
        modify_btn.clicked.connect(self.modify_book)
        delete_btn.clicked.connect(self.delete_book)

        return widget

    def _bind_signals(self):
        try:
            self.library_service.signals.book_operation.disconnect(self._show_book_msg)
        except (RuntimeError, TypeError):
            pass 

        try:
            self.library_service.signals.data_saved.disconnect()
        except (RuntimeError, TypeError):
            pass

        self.logout_action.triggered.connect(self.logout)
        self.exit_action.triggered.connect(self.close)

        self.library_service.signals.book_operation.connect(self._show_book_msg)
        self.library_service.signals.data_saved.connect(lambda s, m: QMessageBox.information(self, "数据保存", m))

    def update_book_table(self, books=None):
        books = books or self.library_service.books.values()
        self.book_table.setRowCount(0)
        for row, book in enumerate(books):
            self.book_table.insertRow(row)
            self.book_table.setItem(row, 0, QTableWidgetItem(book.index_id))
            self.book_table.setItem(row, 1, QTableWidgetItem(book.title))
            self.book_table.setItem(row, 2, QTableWidgetItem(book.author))
            self.book_table.setItem(row, 3, QTableWidgetItem(book.category))
            self.book_table.setItem(row, 4, QTableWidgetItem(str(book.stock)))
        self.book_table.resizeColumnsToContents()

    def update_borrowed_table(self):
        borrowed_books = self.current_user.borrowed_books
        self.borrowed_table.setRowCount(0)
        for row, index_id in enumerate(borrowed_books):
            book = self.library_service.books.get(index_id)
            if not book:
                continue
            borrow_date = "未知"
            for history in self.current_user.borrow_history:
                if history[0]["index_id"] == index_id and history[2] is None:
                    borrow_date = history[1]
                    break
            self.borrowed_table.insertRow(row)
            self.borrowed_table.setItem(row, 0, QTableWidgetItem(index_id))
            self.borrowed_table.setItem(row, 1, QTableWidgetItem(book.title))
            self.borrowed_table.setItem(row, 2, QTableWidgetItem(book.author))
            self.borrowed_table.setItem(row, 3, QTableWidgetItem(book.category))
            self.borrowed_table.setItem(row, 4, QTableWidgetItem(borrow_date))
        self.borrowed_table.resizeColumnsToContents()

    def update_history_table(self):
        history_list = self.current_user.borrow_history
        self.history_table.setRowCount(0)
        for row, history in enumerate(history_list):
            book_info, borrow_date, return_date = history
            status = "已归还" if return_date else "未归还"
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(book_info["index_id"]))
            self.history_table.setItem(row, 1, QTableWidgetItem(book_info["title"]))
            self.history_table.setItem(row, 2, QTableWidgetItem(book_info["author"]))
            self.history_table.setItem(row, 3, QTableWidgetItem(borrow_date))
            self.history_table.setItem(row, 4, QTableWidgetItem(return_date or "——"))
            self.history_table.setItem(row, 5, QTableWidgetItem(status))
        self.history_table.resizeColumnsToContents()

    # 业务操作UI回调
    def search_book(self):
        search_type = self.search_type.currentText()
        search_key = self.search_edit.text().strip()
        if not search_key:
            QMessageBox.warning(self, "警告", "搜索内容不能为空！")
            return
        type_map = {"索引号": "index_id", "书名": "title", "作者": "author", "分类": "category"}
        results = self.library_service.search_book(**{type_map[search_type]: search_key})
        self.update_book_table(results)
        QMessageBox.information(self, "搜索结果", f"找到 {len(results)} 本匹配图书！")

    def show_all_books(self): 
        in_stock_books = [b for b in self.library_service.books.values() if b.stock > 0] #####
        self.update_book_table(in_stock_books)

    def borrow_book(self):
        index_id = self.borrow_edit.text().strip()
        if not index_id:
            QMessageBox.warning(self, "警告", "请输入图书索引号！")
            return
        if self.library_service.borrow_book(index_id):
            self.update_book_table()
            self.update_borrowed_table()
            self.update_history_table()
            self.borrow_edit.clear()

    def return_book(self):
        index_id = self.return_edit.text().strip()
        if not index_id:
            QMessageBox.warning(self, "警告", "请输入图书索引号！")
            return
        if self.library_service.return_book(index_id):
            self.update_book_table()
            self.update_borrowed_table()
            self.update_history_table()
            self.return_edit.clear()

    def add_book(self):
        index_id = self.add_index.text().strip()
        title = self.add_title.text().strip()
        author = self.add_author.text().strip()
        category = self.add_category.text().strip()
        stock = self.add_stock.value()
        if not (index_id and title and author and category):
            QMessageBox.warning(self, "警告", "索引号、书名、作者、分类不能为空！")
            return
        self.library_service.add_book(index_id, title, author, category, stock)
        self.update_book_table()
        self.add_index.clear()
        self.add_title.clear()
        self.add_author.clear()
        self.add_category.clear()
        self.add_stock.setValue(1)

    def modify_book(self):
        index_id = self.edit_index.text().strip()
        if not index_id:
            QMessageBox.warning(self, "警告", "请输入目标索引号！")
            return
        kwargs = {
            "title": self.edit_title.text().strip() or None,
            "author": self.edit_author.text().strip() or None,
            "category": self.edit_category.text().strip() or None,
            "stock": self.edit_stock.value() if self.edit_stock.value() != 0 else None
        }
        self.library_service.modify_book(index_id,** kwargs)
        self.update_book_table()
        self.edit_index.clear()
        self.edit_title.clear()
        self.edit_author.clear()
        self.edit_category.clear()
        self.edit_stock.setValue(0)

    def delete_book(self):
        index_id = self.edit_index.text().strip()
        if not index_id:
            QMessageBox.warning(self, "警告", "请输入目标索引号！")
            return
        if QMessageBox.question(self, "确认", f"是否删除图书 {index_id}？", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.library_service.delete_book(index_id)
            self.update_book_table()
            self.edit_index.clear()

    def logout(self):
        self.library_service.logout()
        self.close()
        login_dialog = LoginDialog(self.library_service)
        login_dialog.login_success.connect(self._restart)
        login_dialog.exec_()

    def _restart(self):
        self.current_user = self.library_service.current_user

        if hasattr(hasattr(self, 'tabs')):
            self.tabs.deleteLater()  # 销毁旧标签页容器
        self._init_ui()  # 重新初始化UI
        self._bind_signals()
        self.show()

    def _show_book_msg(self, success, msg):
        if success:
            QMessageBox.information(self, "提示", msg)
        else:
            QMessageBox.warning(self, "警告", msg)