import wx
from socket import *
import threading
from faker import Faker

class Client(wx.Frame):
    def __init__(self):
        #实例属性
        self.name = Faker('zh_CN').name()  #客户端的名字
        self.isConnected = False  #是否连接服务器
        self.client_socket = None
        wx.Frame.__init__(self,None,title=self.name+'聊天室客户端',size=(450,680),pos=(100,50))
        # 界面布局
        # 加入聊天室、离开聊天室、发送信息、清空信息，展示聊天记录、输入文字
        self.pl = wx.Panel(self)
        #创建按钮
        self.conn_btn = wx.Button(self.pl,label = '加入聊天室',pos=(10,10),size=(200,40))
        # 创建按钮
        self.dis_btn = wx.Button(self.pl, label='离开聊天室', pos=(220, 10), size=(200, 40))
        # 创建按钮
        self.clear_btn = wx.Button(self.pl, label='清空信息', pos=(10, 580), size=(200, 40))
        # 创建按钮
        self.send_btn = wx.Button(self.pl, label='发送信息', pos=(220, 580), size=(200, 40))
        #创建聊天内容文本框
        self.text = wx.TextCtrl(self.pl,size=(400,400),pos=(10,60),style=wx.TE_READONLY|wx.TE_MULTILINE)
        #创建输入文本框
        self.input_text = wx.TextCtrl(self.pl,size=(400,100),pos=(10,470),style=wx.TE_MULTILINE)

        #按钮事件绑定
        self.Bind(wx.EVT_BUTTON,self.clear,self.clear_btn)
        self.Bind(wx.EVT_BUTTON, self.conn,self.conn_btn)
        self.Bind(wx.EVT_BUTTON, self.dis,self.dis_btn)
        self.Bind(wx.EVT_BUTTON, self.send,self.send_btn)
    #点击加入聊天室触发
    def conn(self,event):
        if self.isConnected==False:
            self.isConnected=True
            self.client_socket = socket()
            self.client_socket.connect(('127.0.0.1',8999))
            #发送自己的用户名
            self.client_socket.send(self.name.encode('utf-8'))
            #创建线程接收服务器发送的信息
            # 创建线程
            main_thread = threading.Thread(target=self.recv_data)
            # 设置为守护线程
            main_thread.daemon = True
            # 启动线程
            main_thread.start()

    def recv_data(self):
        while self.isConnected:
            text = self.client_socket.recv(1024).decode('utf-8')
            self.text.AppendText(text+'\n')


    # 点击清空按钮触发
    def clear(self,event):
        self.input_text.Clear()

    # 点击离开聊天室触发
    def dis(self,event):
        self.client_socket.send('断开连接'.encode('utf-8'))
        self.isConnected=False


    # 点击发送信息触发
    def send(self,event):
        if self.isConnected:
            text = self.input_text.GetValue()
            if text != '':
                self.client_socket.send(text.encode('utf-8'))
                self.input_text.Clear()



#程序入口
if __name__ =='__main__':
    #创建应用程序对象
    app = wx.App()
    client = Client()
    client.Show()
    app.MainLoop()