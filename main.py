# -*- coding: utf-8 -*-
# @Time    : 2023/4/5 19:22
# @Author  : Tong Huaqing
# @File    : main.py
# @Comment :

# 输入base路径和子路径的正则表达式, 返回所有子路径

import os
import re
import platform
import shutil


def get_all_path(base_path: str, pattern: str):
    all_path = []
    if platform.system().lower() == "windows" and not base_path.endswith("\\"):
        base_path += "\\"
    elif platform.system().lower() == "darwin" and not base_path.endswith("/"):
        base_path += "/"

    # 替换base_path当中需要转移的字符
    base_path_regex = base_path.replace("\\", "\\\\")
    base_path_regex = base_path_regex.replace(".", r"\.")
    base_path_regex = base_path_regex.replace("*", r"\*")
    base_path_regex = base_path_regex.replace("?", r"\?")
    base_path_regex = base_path_regex.replace("+", r"\+")
    base_path_regex = base_path_regex.replace("$", r"\$")
    base_path_regex = base_path_regex.replace("^", r"\^")
    base_path_regex = base_path_regex.replace("[", r"\[")
    base_path_regex = base_path_regex.replace("]", r"\]")
    base_path_regex = base_path_regex.replace("(", r"\(")
    base_path_regex = base_path_regex.replace(")", r"\)")
    base_path_regex = base_path_regex.replace("{", r"\{")
    base_path_regex = base_path_regex.replace("}", r"\}")
    base_path_regex = base_path_regex.replace("|", r"\|")
    base_path_regex = base_path_regex.replace("/", r"\/")
    base_path_regex = base_path_regex.replace(" ", r"\ ")

    pattern = base_path_regex + pattern

    # 递归遍历base_path及其子文件夹下的所有文件
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if re.fullmatch(pattern, os.path.join(root, file)):
                all_path.append(os.path.join(root, file))

    return all_path


if __name__ == '__main__':
    base = input("请输入base路径: ")
    pattern = input("请输入子路径的正则表达式:")

    all_path = get_all_path(base, pattern)
    # 输出all_path当中的所有路径
    if len(all_path) == 0:
        print("没有匹配的路径")
        exit()

    print("所有匹配的路径: ")
    for path in all_path:
        print(path)
    print("共" + str(len(all_path)) + "个")
    # 输入拷贝的目标路径
    target = input("请输入拷贝的目标路径(输入空白退出): ")
    target = target.strip()
    if target == "":
        exit()
    # 如果target不存在, 则创建
    if not os.path.exists(target):
        os.makedirs(target)
    for i, path in enumerate(all_path):
        try:
            print(f"({i + 1}/{len(all_path)})拷贝文件: " + path, end="", flush=True)
            shutil.copy(path, target)
            print(" --成功", flush=True)
        except shutil.SameFileError as e:
            print(" --失败, 原因: " + str(e), flush=True)
            # 如果拷贝的文件和目标文件是同一个文件, 则输出

    input("拷贝完成, 按回车结束")
