# # Coding=utf-8
# from tkinter import *
# import tkinter as tk
# from tkinter import ttk
# # from ttk import *
# import threading
# import time
# import sys
# import queue
# def fmtTime(timeStamp):
#     timeArray = time.localtime(timeStamp)
#     dateTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#     return dateTime
# #自定义re_Text,用于将stdout映射到Queue
# class re_Text():
#     def __init__(self, queue):
#         self.queue = queue
#     def write(self, content):
#         self.queue.put(content)
# class GUI():
#     def __init__(self, root):
#         #new 一个Quue用于保存输出内容
#         self.msg_queue = queue.Queue()
#         self.initGUI(root)
#     #在show_msg方法里，从Queue取出元素，输出到Text
#     def show_msg(self):
#         while not self.msg_queue.empty():
#             content = self.msg_queue.get()
#             self.text.insert(INSERT, content)
#             self.text.see(END)
#         #after方法再次调用show_msg
#         self.root.after(100, self.show_msg)
#     def initGUI(self, root):
#         self.root = root
#         self.root.title("test")
#         self.root.geometry("400x200+700+500")
#         self.root.resizable = False
#         self.button = Button(self.root, text="click", width=10, command=self.show)
#         self.button.pack(side="top")
#         self.scrollbar = Scrollbar(self.root)
#         self.scrollbar.pack(side="right", fill="y")
#         self.text = Text(self.root, height=10, width=45, yscrollcommand=self.scrollbar.set)
#         self.text.pack(side="top", fill=BOTH, padx=10, pady=10)
#         self.scrollbar.config(command=self.text.yview)
#         #启动after方法
#         self.root.after(100, self.show_msg)
#         #将stdout映射到re_Text
#         sys.stdout = re_Text(self.msg_queue)
#         root.mainloop()
#     def __show(self):
#         i = 0
#         while i < 3:
#             print(fmtTime(time.time()))
#             time.sleep(1)
#             i += 1
#     def show(self):
#         T = threading.Thread(target=self.__show, args=())
#         T.start()
# if __name__ == "__main__":
#     root = tk.Tk()
#     myGUI = GUI(root)

# import queue
# import time
#
# q = queue.Queue()
# for i in range(0, 4):
#     time.sleep(0.5)
#     element = 'element %s'%i
#     print('put', element)
#     q.put(element)
# while not q.empty():
#     time.sleep(0.5)
#     print('get', q.get())

# from tkinter import *
# from tkinter import ttk
#
# class GUI():
#     def __init__(self, root):
#         self.initGUI(root)
#     def loop(self):
#         print('loop proc running')
#         self.root.after(1000, self.loop)
#     def initGUI(self, root):
#         self.root = root
#         self.root.title('test')
#         self.root.geometry('400x200+80+600')
#         self.root.resizable = False
#         self.root.after(1000, self.loop)
#
#         self.root.mainloop()
# if __name__ == '__main__':
#     root = Tk()
#     myGUI = GUI(root)


# from tkinter import *
# from tkinter import ttk
# import threading
# import time
#
# class GUI():
#     def __init__(self, root):
#         self.initGUI(root)
#     # def loop(self):
#     #     print('loop proc running')
#     #     self.root.after(1000, self.loop)
#     def initGUI(self, root):
#         self.root = root
#         self.root.title('test')
#         self.root.geometry('400x200+700+500')
#         self.root.resizable = False
#
#         self.button_1 = Button(root, text='Run A', width=10, command=self.A)
#         self.button_1.pack(side=TOP)
#         self.button_2 = Button(root, text='Run B', width=10, command=self.B)
#         self.button_2.pack(side=TOP)
#
#         self.root.mainloop()
#     def _A(self):
#         print('start to run proc A')
#         time.sleep(3)
#         print('proc A finished')
#     def A(self):
#         T = threading.Thread(target=self._A)
#         T.start()
#     def _B(self):
#         print('start to run proc B')
#         time.sleep(3)
#         print('proc B finished')
#     def B(self):
#         T = threading.Thread(target=self._B)
#         T.start()
# if __name__ == '__main__':
#     root = Tk()
#     myGUI = GUI(root)

# from tkinter import ttk, Tk, Toplevel
#
# root = Tk()
# welcome_window = Toplevel(root)
# welcome_window.title('Welcome')
#
# lab_window = Toplevel(root)
# lab_window.title('Lab')
#
# root.withdraw() # hide root window
# lab_window.withdraw() # hide lab window
#
# def goto_lab():
#     welcome_window.destroy()
#     lab_window.deiconify() # show lab window
#
# button1 = ttk.Button(welcome_window, text='Close',\
#                      command=goto_lab)
# button1.pack(padx=100, pady=50)
#
# button2 = ttk.Button(lab_window, text='Close',\
#                      command=quit)
# button2.pack(padx=100, pady=50)
#
# root.mainloop()


# # from "Python Coobook 2nd Edition", section 11.9, page 439.
# # Modified to work in Python 2 & 3.
# from __future__ import print_function
#
# try:
#     import Tkinter as tk, time, threading, random, Queue as queue
# except ModuleNotFoundError:   # Python 3
#     import tkinter as tk, time, threading, random, queue
#
# class GuiPart(object):
#     def __init__(self, master, queue, end_command):
#         self.queue = queue
#         # Set up the GUI
#         tk.Button(master, text='Done', command=end_command).pack()
#         # Add more GUI stuff here depending on your specific needs
#
#     def processIncoming(self):
#         """ Handle all messages currently in the queue, if any. """
#         while self.queue.qsize():
#             try:
#                 msg = self.queue.get_nowait()
#                 # Check contents of message and do whatever is needed. As a
#                 # simple example, let's print it (in real life, you would
#                 # suitably update the GUI's display in a richer fashion).
#                 print(msg)
#             except queue.Empty:
#                 # just on general principles, although we don't expect this
#                 # branch to be taken in this case, ignore this exception!
#                 pass
#
#
# class ThreadedClient(object):
#     """
#     Launch the main part of the GUI and the worker thread. periodic_call()
#     and end_application() could reside in the GUI part, but putting them
#     here means that you have all the thread controls in a single place.
#     """
#     def __init__(self, master):
#         """
#         Start the GUI and the asynchronous threads.  We are in the main
#         (original) thread of the application, which will later be used by
#         the GUI as well.  We spawn a new thread for the worker (I/O).
#         """
#         self.master = master
#         # Create the queue
#         self.queue = queue.Queue()
#
#         # Set up the GUI part
#         self.gui = GuiPart(master, self.queue, self.end_application)
#
#         # Set up the thread to do asynchronous I/O
#         # More threads can also be created and used, if necessary
#         self.running = True
#         self.thread1 = threading.Thread(target=self.worker_thread1)
#         self.thread1.start()
#
#         # Start the periodic call in the GUI to check the queue
#         self.periodic_call()
#
#     def periodic_call(self):
#         """ Check every 200 ms if there is something new in the queue. """
#         self.master.after(200, self.periodic_call)
#         self.gui.processIncoming()
#         if not self.running:
#             # This is the brutal stop of the system.  You may want to do
#             # some cleanup before actually shutting it down.
#             import sys
#             sys.exit(1)
#
#     def worker_thread1(self):
#         """
#         This is where we handle the asynchronous I/O.  For example, it may be
#         a 'select()'.  One important thing to remember is that the thread has
#         to yield control pretty regularly, be it by select or otherwise.
#         """
#         while self.running:
#             # To simulate asynchronous I/O, create a random number at random
#             # intervals. Replace the following two lines with the real thing.
#             time.sleep(rand.random() * 1.5)
#             msg = rand.random()
#             self.queue.put(msg)
#
#     def end_application(self):
#         self.running = False  # Stops worker_thread1 (invoked by "Done" button).
#
# rand = random.Random()
# root = tk.Tk()
# client = ThreadedClient(root)
# root.mainloop()


# !/usr/bin/python3
# -*- coding: utf-8 -*-

# import tkinter
# import threading
# import time
#
#
# class section:
#     def onPaste(self):
#         print("显示AI机器人一天的工作")
#
#     def onCopy(self):
#         print("如果要现在开始工作，就点开始，否则会根据日常的安排工作")
#
#     def onCut(self):
#         print("学习新的工作技术，只要教过AI一次，就会了，以后的工作都可以交给他")
#
#
#
# def move(event):
#     global x,y,root
#     new_x = (event.x-x)+root.winfo_x()
#     new_y = (event.y-y)+root.winfo_y()
#     s = "300x300+" + str(new_x)+"+" + str(new_y)
#     root.geometry(s)
#     print("当把我放到左上角200*200的区域时我会走人的,当前是x:%s,y:%s"%(new_x,new_y))
#     if new_x<50 and new_y<50:
#         exit()
#
# def button_1(event):
#     global x,y
#     x,y = event.x,event.y
#     print("event.x, event.y = ",event.x,event.y)
# '右键菜单设置'
# def button_3(event):
#     global menu
#     print(event.x_root, event.y_root)
#     menu.post(event.x_root, event.y_root)
#     '''
#     global root
#     root.Menu(root.abc,tearoff=0)
#     root.Menu.post(event.x_root, event.y_root)
#     '''
#
# global x,y,root,menu
# def aiui():
#     global root,menu
#     root = tkinter.Tk()
#     root.overrideredirect(True)
#     root.wm_attributes('-topmost',1)
#     sw=root.winfo_screenwidth()
#     sh=root.winfo_screenheight()
#     root_x=sw-300
#     root_y=sh-300-50
#     root.attributes("-alpha", 0.4)#窗口透明度60 %
#
#     root.geometry("300x300+%d+%d"%(root_x,root_y))
#
#     canvas = tkinter.Canvas(root)
#     canvas.configure(width = 300)
#     canvas.configure(height = 300)
#     #canvas.configure(bg = "red")
#     canvas.configure(highlightthickness = 0)
#
#
#     filename = tkinter.PhotoImage(file = "./subgraph_images/picture-1.png")
#     canvas.create_image(150,150, image=filename)
#
#     canvas.bind("<B1-Motion>",move)
#     canvas.bind("<Button-1>",button_1)
#     canvas.bind("<Button-3>",button_3)
#
#     canvas.pack()
#
#
#     section_obj = section()
#     menu = tkinter.Menu(canvas,tearoff=0)
#     menu.add_command(label="我的工作", command=section_obj.onCopy)
#     menu.add_separator()
#     menu.add_command(label="开始工作", command=section_obj.onPaste)
#     menu.add_separator()
#     menu.add_command(label="技能学习", command=section_obj.onCut)
#     menu.add_separator()
#     menu.add_command(label="退出", command=root.quit)
#
#     root.mainloop()
#
#
#
# '''线程控制'''
# exitFlag = 0
# class threadControl(threading.Thread):
#     def __init__(self,threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#
#     def run(self):
#         print ("开始线程：" + self.name)
#         if self.name=='aiui':
#             aiui()
#         print_time(self.name, self.counter, 5)
#         print ("退出线程：" + self.name)
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threadName.exit()
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
#
#
# if __name__ == '__main__':
#     thread1=threadControl(1,'thread_1',1)
#     thread2=threadControl(2,'thread_2',2)
#     aiui_obj=threadControl(3,'aiui',3)
#
#     aiui_obj.start()
#
#     thread1.start()
#     thread2.start()
#     thread1.join()
#     thread2.join()
#
#     aiui_obj.join()
#     print ("退出主线程")


# from tkinter import *
# root=Tk()
# # # 设置主窗口区的背景颜色以区别画布区的颜色
# root.config(bg='#8DB6CD')
# root.title("C语言中文网")
# root.geometry('800x600')
# # root.iconbitmap('./subgraph_images/picture-1.png')
# # # 将画布设置为白色
# cv = Canvas(root,bg='white')
# # tkinter 提供的内置位图名称
# bitmaps = ["error", "gray75", "gray50", "gray25", "gray12",
# "hourglass", "info", "questhead", "question", "warning"]
# # 列出所有的位图样式
# for i in range(len(bitmaps)):
#     # 前两个参数指定一个位图的位置，后续依次排列
#     cv.create_bitmap((i+1)*30,30,bitmap=bitmaps[i])
# #并在画布上添加文本
# # 参数说明，前两个参数（x0，y0）参照点，指定文字字符串的左上角坐标
# # anchor 指定了文本的对于参照点的相对位置，以方位来指定,比如 W/E/N/S等
# cv.create_text(30,80,text = "tkinter内置位图预览",fill ='#7CCD7C',anchor = W,font =('微软雅黑',15,'bold'))
# # 展示图片，使用 PhotoImage()来加载图片
# img = PhotoImage (file="./subgraph_images/picture-1.png")
# cv.create_image(300,150,image = img,anchor =W)
# cv.create_text(30,220,text = "图片预览",fill ='#7CCD7C',anchor = W,font =('微软雅黑',15,'bold'))
# cv.pack()
# mainloop()



# import tkinter
# from tkinter import *
#
# class section:
#     def onPaste(self):
#         print("显示AI机器人一天的工作")
#
#     def onCopy(self):
#         print("如果要现在开始工作，就点开始，否则会根据日常的安排工作")
#
#     def onCut(self):
#         print("学习新的工作技术，只要教过AI一次，就会了，以后的工作都可以交给他")
#
# root = Tk()
# # # 设置主窗口区的背景颜色以区别画布区的颜色
# root.config(bg='#8DB6CD')
# root.title("C语言中文网")
# root.geometry('800x600')
# # root.iconbitmap("C:/Users/Jay/Desktop/image_transfer/no.png")
#
# # 定义移动函数
# def move_img():
#     # 定义移动坐标
#     cv.move(image1, 50, 30)
#
#
# # # 将画布设置为白色
# cv = Canvas(root, height=600, width=400, bg='white')
# def move(event):
#     global x,y,root
#     new_x = (event.x-x)+root.winfo_x()
#     new_y = (event.y-y)+root.winfo_y()
#     s = "300x300+" + str(new_x)+"+" + str(new_y)
#     root.geometry(s)
#     print("当把我放到左上角200*200的区域时我会走人的,当前是x:%s,y:%s"%(new_x,new_y))
#     if new_x<50 and new_y<50:
#         exit()
#
# def button_1(event):
#     global x,y
#     x,y = event.x,event.y
#     print("event.x, event.y = ",event.x,event.y)
# '右键菜单设置'
# def button_3(event):
#     global menu
#     print(event.x_root, event.y_root)
#     menu.post(event.x_root, event.y_root)
# cv.bind("<B1-Motion>",move)
# cv.bind("<Button-1>",button_1)
# cv.bind("<Button-3>",button_3)
# section_obj = section()
# menu = tkinter.Menu(cv,tearoff=0)
# menu.add_command(label="我的工作", command=section_obj.onCopy)
# menu.add_separator()
# menu.add_command(label="开始工作", command=section_obj.onPaste)
# menu.add_separator()
# menu.add_command(label="技能学习", command=section_obj.onCut)
# menu.add_separator()
# menu.add_command(label="退出", command=root.quit)
# # 使用 PhotoImage()来加载图片
# img = PhotoImage(file="C:/Users/Jay/Desktop/image_transfer/no.png")
# image1 = cv.create_image(30, 150, image=img, anchor=W)
# # 将按钮放置在画布中
# btn = Button(cv, text="点击移动画布", bg="#8A8A8A", activebackground="#7CCD7C", command=move_img)
# # 在指定位置创建一个窗口控件，tags来添加标签
# cv.create_window(320, 250, height=40, width=100, window=btn)
# # 调用delete() 删除画布对象,若传入ALL，则删除所有的画布对象
# # cv.delete(image1)
# cv.pack()
# # 显示窗口
# root.mainloop()


# import threading
# import time
# import PySimpleGUI as sg
#
# """
#     Threaded Demo - Uses Window.write_event_value communications
#
#     Requires PySimpleGUI.py version 4.25.0 and later
#
#     This is a really important demo  to understand if you're going to be using multithreading in PySimpleGUI.
#
#     Older mechanisms for multi-threading in PySimpleGUI relied on polling of a queue. The management of a communications
#     queue is now performed internally to PySimpleGUI.
#
#     The importance of using the new window.write_event_value call cannot be emphasized enough.  It will hav a HUGE impact, in
#     a positive way, on your code to move to this mechanism as your code will simply "pend" waiting for an event rather than polling.
#
#     Copyright 2020 PySimpleGUI.org
# """
#
# THREAD_EVENT = '-THREAD-'
#
# cp = sg.cprint
#
#
# def the_thread(window):
#     """
#     The thread that communicates with the application through the window's events.
#
#     Once a second wakes and sends a new event and associated value to the window
#     """
#     i = 0
#     while True:
#         time.sleep(1)
#         window.write_event_value('-THREAD-', (
#         threading.current_thread().name, i))  # Data sent is a tuple of thread name and counter
#         cp('This is cheating from the thread', c='white on green')
#         i += 1
#
#
# def main():
#     """
#     The demo will display in the multiline info about the event and values dictionary as it is being
#     returned from window.read()
#     Every time "Start" is clicked a new thread is started
#     Try clicking "Dummy" to see that the window is active while the thread stuff is happening in the background
#     """
#
#     layout = [[sg.Text('Output Area - cprint\'s route to here', font='Any 15')],
#               [sg.Multiline(size=(65, 20), key='-ML-', autoscroll=True, reroute_stdout=True, write_only=True,
#                             reroute_cprint=True)],
#               [sg.T('Input so you can see data in your dictionary')],
#               [sg.Input(key='-IN-', size=(30, 1))],
#               [sg.B('Start A Thread'), sg.B('Dummy'), sg.Button('Exit')]]
#
#     window = sg.Window('Window Title', layout, finalize=True)
#
#     while True:  # Event Loop
#         event, values = window.read()
#         cp(event, values)
#         if event == sg.WIN_CLOSED or event == 'Exit':
#             break
#         if event.startswith('Start'):
#             threading.Thread(target=the_thread, args=(window,), daemon=True).start()
#         if event == THREAD_EVENT:
#             cp(f'Data from the thread ', colors='white on purple', end='')
#             cp(f'{values[THREAD_EVENT]}', colors='white on red')
#     window.close()
#
#
# if __name__ == '__main__':
#     main()

from tkinter import *
from threading import Thread
from time import sleep
from random import randint

class GUI():

    def __init__(self):
        self.root = Tk()
        self.root.geometry("200x200")

        self.btn = Button(self.root,text="lauch")
        self.btn.pack(expand=True)

        self.btn.config(command=self.action)

    def run(self):
        self.root.mainloop()

    def add(self,string,buffer):
        while  self.txt:
            msg = str(randint(1,100))+string+"\n"
            self.txt.insert(END,msg)
            sleep(0.5)

    def reset_lbl(self):
        self.txt = None
        self.second.destroy()

    def action(self):
        self.second = Toplevel()
        self.second.geometry("100x100")
        self.txt = Text(self.second)
        self.txt.pack(expand=True,fill="both")

        self.t = Thread(target=self.add,args=("new",None))
        self.t.setDaemon(True)
        self.t.start()

        self.second.protocol("WM_DELETE_WINDOW",self.reset_lbl)

a = GUI()
a.run()

