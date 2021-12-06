#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 13:55
# @Author  : bjl
# @Version : V1.2
# @File    : PythonCommentRate.py

import os
import sys
import re

"""
计算本程序所在目录下各python源代码文件的注释率，以及本程序所在目录下全部python源代码文件合计的注释率
1. 本程序可对"#"标识的单行注释、"三双引号"标识的多行注释一并进行统计
2. 本程序使用了正则表达式进行匹配
3. 注释率=注释行数/总行数*100%
4. 注释率不足20%的，相应统计结果以 ***** 标识结尾
5. 最后一行给出本程序所在目录下全部python源代码文件合计的注释率
6. 可支持多层目录结构的递归查找、统计
7. 剔除PythonCommentRate.py文件本身
"""


def show_files(path, all_files):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for cur_file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, cur_file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            show_files(cur_path, all_files)
        else:
            if re.match(r".*py$", cur_file) and cur_path != os.path.join(os.getcwd(), "PythonCommentRate.py"):
                all_files.append(cur_path)
    return all_files


# 获取代码文件所在路径
files = show_files(os.getcwd(), [])
# print(files)

# 本程序所在目录下全部python源代码文件合计的总行数
ttl_code_sum = 0
# 本程序所在目录下全部python源代码文件合计的注释行数
ttl_comment_sum = 0

for file in files:
    # print("=="*10)
    # print(file)

    # 当前python源代码文件的总行数
    code_sum = 0
    with open(file, "r", encoding="utf-8") as my_code:
        my_lines = my_code.readlines()
        serial_num_list = [[], []]

        for serial_num, line in enumerate(my_lines):
            serial_num = serial_num + 1
            code_sum += 1
            if re.match(r"\s*#+.*", line):
                serial_num_list[0].append(serial_num)

            if re.match(r".*\"\"\".*", line):
                serial_num_list[1].append(serial_num)

    if code_sum == 0:
        print("%s空文件!自动跳过!" % file)
        continue

    serial_num_sum1 = 0
    serial_num_sum2 = 0

    for ser in serial_num_list[0]:
        serial_num_sum1 += 1
    try:
        for ser_num, value in enumerate(serial_num_list[1]):
            if ser_num % 2 == 0:
                top_num = value
            else:
                end_num = value
                serial_num_sum2 += (int(end_num) - int(top_num) + 1)
    except:
        print("%s源码注释不规范!自动跳过!" % file)
        continue

    # 当前python源代码文件的注释行数
    serial_num_sum = serial_num_sum1 + serial_num_sum2
    # 当前python源代码文件的注释率
    exp_rate = 100 * (serial_num_sum / code_sum)

    ttl_comment_sum += serial_num_sum
    ttl_code_sum += code_sum

    if exp_rate < 20:
        print("%s | 注释行数为%d，总行数为%d | 注释率为%f%% *****" % (file, serial_num_sum, code_sum, exp_rate))
    else:
        print("%s | 注释行数为%d，总行数为%d | 注释率为%f%%" % (file, serial_num_sum, code_sum, exp_rate))

# 本程序所在目录下全部python源代码文件合计的注释率
ttl_exp_rate = 100 * (ttl_comment_sum / ttl_code_sum)
if ttl_exp_rate < 20:
    print("合计 | 注释行数为%d，总行数为%d | 注释率为%f%% *****" % (ttl_comment_sum, ttl_code_sum, ttl_exp_rate))
else:
    print("合计 | 注释行数为%d，总行数为%d | 注释率为%f%%" % (ttl_comment_sum, ttl_code_sum, ttl_exp_rate))