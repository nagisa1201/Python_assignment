'''
Author: Nagisa 2964793117@qq.com
Date: 2025-11-18 11:53:58
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2025-11-20 19:19:47
FilePath: \python_assignment\assignment1\Shape.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle as mpl_Circle
# 防止中文乱码
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False
class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self, ax):
        rect_patch = Rectangle(
            (self.x, self.y),
            self.width, self.height,
            edgecolor='blue',
            facecolor='none',
            linewidth=2
        )
        ax.add_patch(rect_patch)
class Circle(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    def draw(self, ax):
        circle_patch = mpl_Circle(
            (self.x, self.y),
            self.radius,
            edgecolor='red',
            facecolor='none',
            linewidth=2
        )
        ax.add_patch(circle_patch)

def draw(shape, ax):
    shape.draw(ax)

def main():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title('图形绘制工具')
    ax.set_xlabel('X轴')
    ax.set_ylabel('Y轴')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_aspect('equal', adjustable='box')  # 新增这一行
    print("===== 图形绘制菜单 =====")
    print("1. 绘制长方形")
    print("2. 绘制圆形")
    print("3. 退出程序并显示图形")
    while True:
        try:
            choice = input("请选择操作（1/2/3）：")
            if choice == '1':
                x = float(input("请输入长方形左下角X坐标（0-90）："))
                y = float(input("请输入长方形左下角Y坐标（0-90）："))
                width = float(input("请输入长方形宽度（5-100-x）："))
                height = float(input("请输入长方形高度（5-100-y）："))
                if not (0 <= x <= 90 and 0 <= y <= 90 and 5 <= width <= 100 - x and 5 <= height <= 100 - y):
                    print("参数超出范围，请重新输入！")
                    continue
                rect = Rect(x, y, width, height)
                draw(rect, ax)
                print("长方形已绘制！")
            elif choice == '2':
                x = float(input("请输入圆心X坐标（10-90）："))
                y = float(input("请输入圆心Y坐标（10-90）："))
                radius = float(input("请输入圆半径（5-10）：")) 
                if not (10 <= x <= 90 and 10 <= y <= 90 and 5 <= radius <= 10):
                    print("参数超出范围，请重新输入！")
                    continue
                circle = Circle(x, y, radius)
                draw(circle, ax)
                print("圆形已绘制！")

            elif choice == '3':
                print("程序退出，正在显示图形...")
                break
            else:
                print("无效选择，请输入1、2或3！")
        except ValueError:
            print("输入错误，请输入数字！")
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()