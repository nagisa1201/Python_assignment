'''
Author: Nagisa 2964793117@qq.com
Date: 2025-11-19 17:23:05
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2025-11-20 21:08:24
FilePath: \python_assignment\assignment3\web_crawler.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests
from bs4 import BeautifulSoup
import os
import re
def crawl_wallpapers():
    url = "http://www.netbian.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    save_dir = "netbian_wallpapers"
    os.makedirs(save_dir, exist_ok=True)
    resp = requests.get(url, headers=headers, timeout=15)
    resp.encoding = "gbk" 
    soup = BeautifulSoup(resp.text, "html.parser")
    img_links = []
    crawl_num = 10 # 爬10张
    # 选择器限定为壁纸列表ul里的img
    for img in soup.select("ul.clearfix img[src*='img.netbian.com/file/']"):
        src = img.get("src")
        if src and (src.endswith(".jpg") or src.endswith(".png")):
            if src not in img_links:
                img_links.append(src)
                if len(img_links) >= crawl_num:
                    break
    for i, link in enumerate(img_links, 1):
        try:
            img_data = requests.get(link, headers=headers, timeout=15).content
            with open(f"{save_dir}/wallpaper_{i}.jpg", "wb") as f:
                f.write(img_data)
            print(f"已下载第{i}张")
        except:
            print(f"第{i}张失败，跳过")

    print(f"\n完成！共下载{len(os.listdir(save_dir))}张，路径：{os.path.abspath(save_dir)}")

if __name__ == "__main__":
    crawl_wallpapers()