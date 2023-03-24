
'''
作者：ZS QQ536957230
此程序需配合“字典破解WiFi密码.py”使用，请先运行本文件。
以下代码仅用于生成1000顺序数（用于测试WiFi密码连接）。
请勿将本程序用于非法行为或活动。如有违反，作者保留追究法律责任的权利。
'''

def generate_sequential_number(number):
    return str(number).zfill(8)  # 将数字转换为字符串并用0填充至8位

def write_sequential_numbers_to_file(start_number, count):
    filename = f'sequential_numbers_{count}.txt'  # 使用 count 构造文件名
    with open(filename, 'w') as file:
        for i in range(start_number, start_number + count):
            file.write(generate_sequential_number(i) + '\n')  # 将生成的顺序数写入文件
            print(f"第{i - start_number + 1}个成功")
    print("全部生成成功")

count = 1000
write_sequential_numbers_to_file(12345678, count)


# 导入python内置模块random

# 初版作废
'''
# 生成一个8位随机数
def generate_sequential_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

# 将随机数写入文件
# def write_random_numbers_to_file(filename, count):
#     with open(filename, 'w') as file:
#         for _ in range(count):
#             file.write(generate_random_number() + '\n')  # 将生成的随机数写入文件

def write_sequential_numbers_to_file(filename, start_number, count):
    with open(filename, 'w') as file:
        for i in range(start_number, start_number + count):
            file.write(generate_sequential_number(i) + '\n')  # 将生成的顺序数写入文件

# 生成100000个随机数并写入文件
# write_random_numbers_to_file('D:\\编程\\Python\\random_numbers.txt', 100000)
# 从11111111开始生成100000个顺序数并写入文件

write_sequential_numbers_to_file('sequential_numbers_100000.txt', 12345678, 100000) 

import random

# 生成一个8位随机数
# def generate_random_number():
#     return ''.join([str(random.randint(0, 9)) for _ in range(8)])

# 生成一个8位顺序数
def generate_sequential_number(number):
    return str(number).zfill(8)

# 将随机数写入文件
# def write_random_numbers_to_file(filename, count):
#     with open(filename, 'w') as file:
#         for _ in range(count):
#             file.write(generate_random_number() + '\n')  # 将生成的随机数写入文件

# 将顺序数写入文件
def write_sequential_numbers_to_file(filename, start_number, count):
    with open(filename, 'w') as file:
        for i in range(start_number, start_number + count):
            file.write(generate_sequential_number(i) + '\n')  # 将生成的顺序数写入文件

# 生成100个随机数并写入文件
# write_random_numbers_to_file('D:\\编程\\Python\\random_numbers.txt', 10000)  # 调用函数，生成100个随机数并写入文件

'''

