import threading
from datatype.models import Book, User, Admin
from datatype.utils import (
    MAX_BORROW, BORROW_DAYS, DATA_FILE, LOCK,
    load_json_file, save_json_file, get_current_date, calculate_overdue_days,
    ServiceSignals
)

class LibrarySystem:
    def __init__(self):
        self.books = {}  
        self.users = {}  
        self.current_user = None
        self.signals = ServiceSignals()  
        self.load_data()  

    # 数据持久化
    def load_data(self):
        """异步加载数据"""
        def _load():
            with LOCK:
                try:
                    data = load_json_file(DATA_FILE)
                    if data:
                        # 加载图书
                        for book_data in data["books"]:
                            self.books[book_data["index_id"]] = Book.from_dict(book_data)
                        # 加载用户
                        for user_data in data["users"]:
                            if user_data["user_type"] == "admin":
                                self.users[user_data["username"]] = Admin.from_dict(user_data)
                            else:
                                self.users[user_data["username"]] = User.from_dict(user_data)

                    # 确保admin存在
                    if "admin" not in self.users:
                        self.users["admin"] = Admin("admin", "admin123")
                        self.signals.data_loaded.emit(True, "初始化默认管理员：admin/admin123")
                    else:
                        self.signals.data_loaded.emit(True, "数据加载成功！")


                except Exception as e:
                    # 加载失败时也强制创建admin
                    self.users["admin"] = Admin("admin", "admin123")
                    self.signals.data_loaded.emit(False, f"加载失败：{str(e)}，已初始化默认管理员")

        threading.Thread(target=_load, daemon=True).start()


    def save_data(self):
        """异步保存数据"""
        def _save():
            with LOCK:
                try:
                    data = {
                        "books": [book.to_dict() for book in self.books.values()],
                        "users": [user.to_dict() for user in self.users.values()]
                    }
                    save_json_file(DATA_FILE, data)
                    self.signals.data_saved.emit(True, "数据已保存！")
                except Exception as e:
                    self.signals.data_saved.emit(False, f"保存失败：{str(e)}")

        threading.Thread(target=_save, daemon=True).start()

    # 用户管理
    def register_user(self, username, password):
        if username in self.users:
            self.signals.user_operation.emit(False, "用户名已存在！")
            return
        self.users[username] = User(username, password)
        self.save_data()
        self.signals.user_operation.emit(True, f"用户 {username} 注册成功！")

    def login(self, username, password):
        # 确保admin一定存在
        # if "admin" not in self.users:
        #     self.users["admin"] = Admin("admin", "admin123")
        #     print("Admin账号已强制创建！")  # 调试信息
        
        # 打印当前用户列表
        print("当前用户列表：", list(self.users.keys()))
        
        if username not in self.users:
            self.signals.user_operation.emit(False, "用户名不存在！")
            return False
        user = self.users[username]
        if user.password != password:
            self.signals.user_operation.emit(False, "密码错误！")
            return False
        self.current_user = user
        self.signals.user_operation.emit(True, f"欢迎 {username} 登录！")
        return True

    def logout(self):
        self.current_user = None

    # 图书管理（管理员）
    def add_book(self, index_id, title, author, category, stock=1):
        if not self._is_admin():
            self.signals.book_operation.emit(False, "只有管理员可添加图书！")
            return
        if index_id in self.books:
            self.signals.book_operation.emit(False, "索引号已存在！")
            return
        self.books[index_id] = Book(index_id, title, author, category, stock)
        self.save_data()
        self.signals.book_operation.emit(True, f"图书《{title}》添加成功！")

    def modify_book(self, index_id,** kwargs):
        if not self._is_admin():
            self.signals.book_operation.emit(False, "只有管理员可修改图书！")
            return
        if index_id not in self.books:
            self.signals.book_operation.emit(False, "图书不存在！")
            return
        book = self.books[index_id]
        for k, v in kwargs.items():
            if hasattr(book, k) and v is not None:
                setattr(book, k, v)
        self.save_data()
        self.signals.book_operation.emit(True, f"图书 {index_id} 修改成功！")

    def delete_book(self, index_id):
        if not self._is_admin():
            self.signals.book_operation.emit(False, "只有管理员可删除图书！")
            return
        if index_id not in self.books:
            self.signals.book_operation.emit(False, "图书不存在！")
            return
        del self.books[index_id]
        self.save_data()
        self.signals.book_operation.emit(True, f"图书 {index_id} 删除成功！")

    # 图书查询
    def search_book(self, **kwargs):
        results = []
        for book in self.books.values():
            match = True
            for k, v in kwargs.items():
                if not hasattr(book, k) or str(getattr(book, k)).lower() != v.lower():
                    match = False
                    break
            if match:
                results.append(book)
        return results

    # 借阅归还
    def borrow_book(self, index_id):
        if not self.current_user:
            self.signals.user_operation.emit(False, "请先登录！")
            return False
        if index_id not in self.books:
            self.signals.book_operation.emit(False, "图书不存在！")
            return False
        book = self.books[index_id]
        if book.stock <= 0:
            self.signals.book_operation.emit(False, "图书无库存！")
            return False
        if len(self.current_user.borrowed_books) >= MAX_BORROW:
            self.signals.user_operation.emit(False, f"最多只能借阅{MAX_BORROW}本！")
            return False

        # 执行借阅逻辑
        borrow_date = get_current_date()
        book.stock -= 1
        book.borrow_records.append((self.current_user.username, borrow_date, None))
        self.current_user.borrowed_books.append(index_id)
        self.current_user.borrow_history.append((book.to_dict(), borrow_date, None))
        self.save_data()
        self.signals.book_operation.emit(True, f"借阅《{book.title}》成功！\n借阅期限{BORROW_DAYS}天。")
        return True

    def return_book(self, index_id):
        if not self.current_user:
            self.signals.user_operation.emit(False, "请先登录！")
            return False
        if index_id not in self.current_user.borrowed_books:
            self.signals.book_operation.emit(False, "你未借阅该图书！")
            return False
        book = self.books[index_id]
        return_date = get_current_date()

        # 更新图书借阅记录
        for i, record in enumerate(book.borrow_records):
            if record[0] == self.current_user.username and record[2] is None:
                book.borrow_records[i] = (record[0], record[1], return_date)
                break

        # 更新用户记录
        book.stock += 1
        self.current_user.borrowed_books.remove(index_id)
        overdue_days = 0
        for i, history in enumerate(self.current_user.borrow_history):
            if history[0]["index_id"] == index_id and history[2] is None:
                self.current_user.borrow_history[i] = (history[0], history[1], return_date)
                overdue_days = calculate_overdue_days(history[1], return_date)
                break

        self.save_data()
        if overdue_days > 0:
            self.signals.book_operation.emit(True, f"归还《{book.title}》成功！\n逾期{overdue_days}天！")
        else:
            self.signals.book_operation.emit(True, f"归还《{book.title}》成功！")
        return True

    def _is_admin(self):   
        return self.current_user and self.current_user.user_type == "admin"