# 根据“章节排序.txt”来对“/章节”中的文件进行重命名。
# “章节排序.txt”中的每一行的格式为：章节名，以顺序作为章节号，从1开始计数。
# “/章节”目录中的文件名格式为：三位章节号数字（可能没有）+章节名+文件后缀+_数字（避免文件名重复的编号，正常情况下没有）。
# 例如：“章节排序.txt”中“章节名”的顺序是1。那么“/章节”目录中如果有文件名为“章节名.txt”
# 则会被重命名为“001章节名.txt”。或者“/章节”目录中如果有文件名为“002章节名.txt”，由
# 于章节号不匹配，则重命名为“001章节名.txt”以匹配章节号。若是遇到文件名已经存在的情况，
# 则会在文件名后加上“_1”、“_2”等等来避免文件被覆盖。

import os
import re

# 定义文件路径
base_dir = os.path.dirname(__file__)
chapters_dir = os.path.join(base_dir, "章节")
sort_file_path = os.path.join(base_dir, "章节排序.txt")

# 读取章节排序文件
with open(sort_file_path, "r", encoding="utf-8") as f:
    sort_lines = f.readlines()

# 解析章节排序
chapter_mapping = {}
for index, line in enumerate(sort_lines, start=1):
    chapter_name = line.strip()
    if chapter_name:
        chapter_mapping[chapter_name] = f"{index:03d}"

# 遍历章节目录中的文件
for filename in os.listdir(chapters_dir):
    file_path = os.path.join(chapters_dir, filename)
    if not os.path.isfile(file_path):
        continue

    # 提取文件名和扩展名，并去除章节号和_后缀
    match = re.match(r"^\d{0,3}(.*?)(?:_\d+)?(\.\w+)$", filename)
    if match:
        name = match.group(1)  # 提取章节名
        ext = match.group(2)   # 提取扩展名
    else:
        name, ext = os.path.splitext(filename)  # 默认处理

    # 查找章节名对应的编号
    for chapter_name, chapter_number in chapter_mapping.items():
        if chapter_name == name:
            new_name = f"{chapter_number}{chapter_name}{ext}"
            new_path = os.path.join(chapters_dir, new_name)

            # 如果新的文件名与旧的文件名相同，则跳过重命名
            if new_name == filename:
                print(f"文件名相同，跳过重命名: {filename}")
                break

            # 如果文件名冲突，添加后缀避免覆盖
            counter = 1
            while os.path.exists(new_path):
                new_name = f"{chapter_number}{chapter_name}_{counter}{ext}"
                new_path = os.path.join(chapters_dir, new_name)
                counter += 1

            # 重命名文件
            os.rename(file_path, new_path)
            print(f"重命名: {filename} -> {new_name}")
            break