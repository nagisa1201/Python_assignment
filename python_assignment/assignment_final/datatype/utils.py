'''
Author: Nagisa 2964793117@qq.com
Date: 2025-11-22 16:25:03
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2025-12-15 22:27:30
FilePath: /python_assignment/assignment_final/utils.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import datetime
import os
import threading
from PyQt5.QtCore import pyqtSignal, QObject

MAX_BORROW = 5
BORROW_DAYS = 30
DATA_FILE = "./python_assignment/assignment_final/library_data.json"
LOCK = threading.Lock()

def load_json_file(file_path):
    """加载JSON文件"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_file(file_path, data):
    """保存JSON文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_current_date():
    """获取当前日期字符串"""
    return datetime.date.today().strftime("%Y-%m-%d")

def calculate_overdue_days(borrow_date_str, return_date_str):
    """计算逾期天数"""
    borrow_date = datetime.datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
    return_date = datetime.datetime.strptime(return_date_str, "%Y-%m-%d").date()
    return (return_date - borrow_date).days - BORROW_DAYS

class ServiceSignals(QObject):
    data_loaded = pyqtSignal(bool, str)
    data_saved = pyqtSignal(bool, str)
    book_operation = pyqtSignal(bool, str)
    user_operation = pyqtSignal(bool, str)