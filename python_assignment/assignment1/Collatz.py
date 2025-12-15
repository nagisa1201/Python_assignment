'''
Author: Nagisa 2964793117@qq.com
Date: 2025-11-18 11:41:33
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2025-11-18 20:46:31
FilePath: \python_assignment\assignment1\Collatz.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import matplotlib.pyplot as plt
# 设置中文显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False  # 确保负号正常显示
def collatz_sequence(n):
    """生成考拉兹序列"""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2  # 偶数除以2
        else:
            n = 3 * n + 1  # 奇数乘3加1
        sequence.append(n)
    return sequence
def plot_sequence(n):
    '''考拉兹序列折线图绘制函数'''
    seq = collatz_sequence(n)
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(seq)), seq, 'o-', color='purple', linewidth=1.5, markersize=4)
    plt.title(f'考拉兹序列 (n={n})', fontsize=12)  # 中文标题
    plt.xlabel('步骤', fontsize=10)  # 中文x轴标签
    plt.ylabel('数值', fontsize=10)  # 中文y轴标签
    plt.grid(alpha=0.3)
    plt.show()
def main():
    test_numbers = [7, 27, 103]
    for num in test_numbers:
        seq = collatz_sequence(num)
        length = len(seq)
        last_three = seq[-3:] if length >= 3 else seq 
        print(f"n={num}时：")
        print(f"  序列长度：{length}")
        print(f"  最后三个数字：{last_three}\n")
    plot_sequence(27)
if __name__ == "__main__":
    main()