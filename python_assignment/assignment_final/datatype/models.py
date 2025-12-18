'''
Author: Nagisa 2964793117@qq.com
Date: 2025-11-21 22:13:02
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2025-12-16 18:59:58
FilePath: \python_assignment\assignment_final\models.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
class Book:
    def __init__(self, index_id, title, author, category, stock=1):
        self.index_id = index_id
        self.title = title
        self.author = author
        self.category = category
        self.stock = stock
        self.borrow_records = []  

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        """从字典创建Book实例"""
        book = cls(
            index_id=data["index_id"],
            title=data["title"],
            author=data["author"],
            category=data["category"],
            stock=data.get("stock", 1)
        )
        book.borrow_records = data.get("borrow_records", [])
        return book


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_type = "user"
        self.borrowed_books = []  
        self.borrow_history = []  
    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        """从字典创建User实例"""
        user = cls(username=data["username"], password=data["password"])
        user.user_type = data.get("user_type", "user")
        user.borrowed_books = data.get("borrowed_books", [])
        user.borrow_history = data.get("borrow_history", [])
        return user


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.user_type = "admin"

    @classmethod
    def from_dict(cls, data):
        admin = cls(username=data["username"], password=data["password"])
        admin.borrowed_books = data.get("borrowed_books", [])
        admin.borrow_history = data.get("borrow_history", [])
        return admin