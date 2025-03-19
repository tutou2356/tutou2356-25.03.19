from threading import main_thread
from 硅基智能机器人 import chat_g

import wx
from socket import *
import threading
from concurrent.futures import ThreadPoolExecutor

class Server(wx.Frame):
    def __init__(self):
        self.isOn = False
        #创建socket
        self.server_socket = socket()
        #绑定ip和端口号
        self.server_socket.bind(('0.0.0.0',8999))
        #监听
        self.server_socket.listen(5)
        #保存所有的客户端
        self.client_thread_dict = {}
        #创建线程池
        self.pool = ThreadPoolExecutor(max_workers=15)

        #界面布局
        #调用父类的init
        wx.Frame.__init__(self,None,title='智能问答聊天室',pos=(0,50),size=(450,600))
        #创建面板
        self.pl=wx.Panel(self)
        #创建按钮  启动服务，保存聊天记录
        self.start_server_btn = wx.Button(self.pl,pos=(10,10),size=(200,40),label='启动服务器')
        #保存聊天记录
        self.save_text_btn = wx.Button(self.pl, pos=(220, 10), size=(200, 40), label='保存聊天记录')
        # 创建聊天内容文本框
        self.text = wx.TextCtrl(self.pl, size=(400, 400), pos=(10, 60), style=wx.TE_READONLY | wx.TE_MULTILINE)
        #给按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.start_server, self.start_server_btn)
        self.Bind(wx.EVT_BUTTON, self.save_text, self.save_text_btn)

    #启动服务器
    def start_server(self,event):
        print('start server')
        if self.isOn==False:
            self.isOn=True
            #创建线程
            main_thread = threading.Thread(target=self.main_thread_fun)
            #设置为守护线程
            main_thread.daemon = True
            #启动线程
            main_thread.start()

    def main_thread_fun(self):
        while self.isOn:
            client_socket,client_address = self.server_socket.accept()
            print(client_address)
            client_name=client_socket.recv(1024).decode('utf-8')
            print(client_name)
            client_thread = ClientThread(client_socket,client_name,self)
            #保存客户端
            self.client_thread_dict[client_name] = client_thread
            self.pool.submit(client_thread.run)
            self.send('【服务器通知】欢迎%s进入聊天室'%client_name)

    def send(self,text,is_user_message=True):
        self.text.AppendText(text + '\n')
        # 如果是用户消息，才需要机器人回复
        if is_user_message:
            # 提取实际问题内容(去掉用户名标记)
            # 假设格式是"【用户名】消息内容"
            question = text.split('】', 1)[1] if '】' in text else text
            # 获取机器人回复
            result_text = chat_g(question)
            # 在服务器显示机器人回复
            self.text.AppendText("【机器人】" + result_text + '\n')
            # 发送给所有客户端，并标记这是机器人的回复
            for client in self.client_thread_dict.values():
                if client.isOn:
                    client.client_socket.send(("【机器人】" + result_text).encode('utf-8'))
        else:
            # 如果不是用户消息(如系统通知)，直接转发
            for client in self.client_thread_dict.values():
                if client.isOn:
                    client.client_socket.send(text.encode('utf-8'))

            #保存聊天记录
    def save_text(self,event):
        print('save_text')
        record = self.text.GetValue()
        with open('record.log','a+',encoding = 'GBK') as f:
            f.write(record)

class ClientThread(threading.Thread):
    def __init__(self,socket,name,server):
        threading.Thread.__init__(self)
        self.client_socket = socket
        self.client_name = name
        self.server = server
        self.isOn = True

    def run(self):
        while self.isOn:
            text = self.client_socket.recv(1024).decode('utf-8')
            if text == '断开连接':
                self.isOn = False
                self.server.send('【服务器消息】%s离开了聊天室'%self.client_name,is_user_message=False)
            else:
                self.server.send('【%s】%s'%(self.client_name,text),is_user_message=True)
        self.client_socket.close()








#程序入口
if __name__ == '__main__':
    #创建应用程序对象
    app = wx.App()
    #创建服务器窗口
    server = Server()
    #显示服务器窗口
    server.Show()
    #循环显示
    app.MainLoop()


