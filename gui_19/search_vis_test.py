# import tkinter as tk  # 使用Tkinter前需要先导入
#
# # 第1步，实例化object，建立窗口window
# window = tk.Tk()
#
# # 第2步，给窗口的可视化起名字
# window.title('My Window')
#
# # 第3步，设定窗口的大小(长 * 宽)
# window.geometry('500x300')  # 这里的乘是小x
#
# # 第4步，在图形界面上创建一个标签label用以显示并放置
# var1 = tk.StringVar()  # 创建变量，用var1用来接收鼠标点击具体选项的内容
# l = tk.Label(window, bg='green', fg='yellow', font=('Arial', 12), width=10, textvariable=var1)
# l.pack()
#
#
# # 第6步，创建一个方法用于按钮的点击事件
# def print_selection():
#     value = lb.get(lb.curselection())  # 获取当前选中的文本
#     var1.set(value)  # 为label设置值
#
#
# # 第5步，创建一个按钮并放置，点击按钮调用print_selection函数
# b1 = tk.Button(window, text='print selection', width=15, height=2, command=print_selection)
# b1.pack()
#
# # 第7步，创建Listbox并为其添加内容
# var2 = tk.StringVar()
# var2.set((1, 2, 3, 4))  # 为变量var2设置值
# # 创建Listbox
# lb = tk.Listbox(window, listvariable=var2)  # 将var2的值赋给Listbox
# # 创建一个list并将值循环添加到Listbox控件中
# list_items = [11, 22, 33, 44]
# for item in list_items:
#     lb.insert('end', item)  # 从最后一个位置开始加入值
# lb.insert(1, 'first')  # 在第一个位置加入'first'字符
# lb.insert(2, 'second')  # 在第二个位置加入'second'字符
# lb.delete(2)  # 删除第二个位置的字符
# lb.pack()
#
# # 第8步，主窗口循环显示
# window.mainloop()
#

import tkinter as tk
from tkinter import Listbox, ttk

# class MyUi(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title('搜索提示框示例')
#         self.geometry("480x320+400+200")
#         ttk.Style().configure('.', font=("仿宋", 15))
#
#         self.myentry_text=''
#         self.mainUi()
#         self.mainloop()
#
#     def mainUi(self):
#         ttk.Label(self,text='这里输入').grid(padx=15, pady=5, row=0,column=0)
#         # def check_digit(content):
#         #     if content.isdigit() or content == "":
#         #         print('1')
#         #         return True
#         #     else:
#         #         print('2')
#         #         return False
#
#         # entry_validate = self.register(check_digit)
#         self.myentry = tk.Entry(self)
#         # self.myentry = tk.Entry(self, validate='key', vcmd=(entry_validate, '%P'))
#         self.myentry.grid(padx=5, pady=5, row=0,column=1)
#         self.myentry.configure(font=("仿宋", 13))
#         self.myentry.configure(validate="key")
#         self.myentry.configure(validatecommand=self.research)
#
#     def research(self):
#         research_content = ['csdn', 'csdn你好', 'csdn你在哪里', 'hahh', 'heihei']
#         current_input = self.myentry.get()
#
#         if current_input != self.myentry_text:
#             self.myentry_text = current_input
#             Listbox_content = []
#             for _c in research_content:
#                 if current_input in _c:
#                     Listbox_content.append(_c)
#
#             mylistbox = tk.Listbox(self)
#             mylistbox.grid(padx=5, pady=5, row=1,column=1)
#             mylistbox.bind("<<ListboxSelect>>", self.show)
#
#             mylistbox.delete(0, tk.END)
#
#             for content in Listbox_content:
#                 mylistbox.insert(tk.END, content)
#
#         self.id = self.after(2000, self.research)
#
#
#     def show(self, event):
#         object = event.widget
#         index = object.curselection()
#         self.myentry.delete(0,tk.END)
#         self.myentry.insert(0, object.get(index))
#         self.after_cancel(self.id)
#         object.grid_forget()
#         self.after_cancel(self.id)
#
# if __name__ == "__main__":
#     MyUi()


# -*- encoding=utf-8 -*-


# import tkinter
# from tkinter import *
#
#
# def left_mouse_down(event):
#     print('鼠标左键按下')
#
#     # 事件的属性
#     widget = event.widget
#     print('触发事件的组件:{}'.format(widget))
#     print('组件颜色:{}'.format(widget.cget('bg')))
#     widget_x = event.x  # 相对于组件的横坐标x
#     print('相对于组件的横坐标:{}'.format(widget_x))
#     widget_y = event.y  # 相对于组件的纵坐标y
#     print('相对于组件的纵坐标:{}'.format(widget_y))
#     x_root = event.x_root  # 相对于屏幕的左上角的横坐标
#     print('相对于屏幕的左上角的横坐标:{}'.format(x_root))
#     y_root = event.y_root  # 相对于屏幕的左上角的纵坐标
#     print('相对于屏幕的左上角的纵坐标:{}'.format(y_root))
#
#
# def left_mouse_up(event):
#     print('鼠标左键释放')
#
#
# def moving_mouse(event):
#     print('鼠标左键按下并移动')
#
#
# def moving_into(event):
#     print('鼠标进入')
#
#
# def moving_out(event):
#     print('鼠标移出')
#
#
# def right_mouse_down(event):
#     print('鼠标右键按下')
#
#
# def right_mouse_up(event):
#     print('鼠标右键释放')
#
#
# def pulley_up(event):
#     print('滑轮向上滚动')
#
#
# def focus(event):
#     print('聚焦事件')
#
#
# def unfocus(event):
#     print('失焦事件')
#
#
# if __name__ == '__main__':
#     win = tkinter.Tk()  # 窗口
#     win.title('南风丶轻语')  # 标题
#     screenwidth = win.winfo_screenwidth()  # 屏幕宽度
#     screenheight = win.winfo_screenheight()  # 屏幕高度
#     width = 500
#     height = 300
#     x = int((screenwidth - width) / 2)
#     y = int((screenheight - height) / 2)
#     win.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
#
#     label = Label(text='标签', relief='g', font=('黑体', 20))
#     label.pack(pady=10)
#
#     label.bind('<Button-1>', left_mouse_down)  # 鼠标左键按下
#     label.bind('<ButtonRelease-1>', left_mouse_up)  # 鼠标左键释放
#     label.bind('<Button-3>', right_mouse_down)  # 鼠标右键按下
#     label.bind('<ButtonRelease-3>', right_mouse_up)  # 鼠标右键释放
#     label.bind('<B1-Motion>', moving_mouse)  # 鼠标左键按下并移动
#     label.bind('<Enter>', moving_into)  # 鼠标移入事件
#     label.bind('<Leave>', moving_out)  # 鼠标移出事件
#     label.bind('<FocusIn>', focus)  # 聚焦事件
#     label.bind('<FocusOut>', unfocus)  # 失焦事件
#     label.focus_set()  # 直接聚焦
#     Entry().pack()
#
#     win.mainloop()


# from tkinter import  *
# root = Tk()
# def eventhandler(event):
#     entry.focus()
# entry=Entry(root,bd=4)
# entry.bind_all('<Control-f>', eventhandler ) # 绑定快捷键Ctrl-f
# entry.pack()
# root.mainloop()

# root = tk.Tk()
# root.geometry('300x240')
# def check_digit(content):
#     print(content)
#     # if content.isdigit() or content == "":
#     #     print('1')
#     #     return True
#     # else:
#     #     print('2')
#     #     return False
#
# entry_validate = root.register(check_digit)
# b1 = tk.Entry(root, width=20, validate='key', vcmd=(entry_validate, '%S'))
# b1.pack()
# root.mainloop()

# from tkinter import *
#
# def printkey(event):
#     print('you pressed: ', event.char)
#
# root = tk.Tk()
# entry = Frame(root, width=100, height=100)
# entry.focus_set()
# entry.bind('<Key>', printkey)
# entry.pack()
# root.mainloop()


# from tkinter import *
# from tkinter.ttk import *
#
# class Gui:
#
#     def __init__(self):
#         self.root = Tk()
#
#         # Set up the Combobox
#         self.selections = Combobox(self.root)
#         self.selections['values'] = ['Apples', 'Oranges', 'Blueberries', 'Bananas', 'Custom']
#         self.selections.pack()
#
#         # The Entry to be shown if "Custom" is selected
#         self.custom_field = Entry(self.root)
#         self.show_custom_field = False
#
#         # Check the selection in 100 ms
#         self.root.after(100, self.check_for_selection)
#
#     def check_for_selection(self):
#         '''Checks if the value of the Combobox equals "Custom".'''
#
#
#         # Get the value of the Combobox
#         value = self.selections.get()
#
#         # If the value is equal to "Custom" and show_field is set to False
#         if value == 'Custom' and not self.show_custom_field:
#
#             # Set show_field to True and pack() the custom entry field
#             self.show_custom_field = True
#             self.custom_field.pack()
#
#
#         # If the value DOESNT equal "Custom"
#         elif value != 'Custom':
#
#             # Set show_field to False
#             self.show_custom_field = False
#
#             # Destroy the custom input
#             self.custom_field.destroy()
#
#             # Set up a new Entry object to pack() if we need it later.
#             # Without this line, tkinter was raising an error for me.
#             # This fixed it, but I don't promise that this is the
#             # most efficient method to do this.
#             self.custom_field = Entry(self.root)
#
#         # If the value IS "Custom" and we're showing the custom_feild
#         elif value == 'Custom' and self.show_custom_field:
#             pass
#
#
#         # Call this method again to keep checking the selection box
#         self.root.after(100, self.check_for_selection)
#
#
# app = Gui()
# app.root.mainloop()


# import tkinter as tk

# from tkinter import ttk
#
# win = tk.Tk()
#
# win.title("Python GUI") # 添加标题
#
# ttk.Label(win, text="Chooes a number").grid(column=1, row=0) # 添加一个标签0
#
# ttk.Label(win, text="Enter a name:").grid(column=0, row=0) # 设置其在界面中出现的位置
#
# # button被点击之后会被执行
#
# def clickMe(): # 当acction被点击时,该函数则生效
#
#     action.configure(text='Hello ' + name.get() + ' ' + numberChosen.get())#设置button显示的内容
#
#     print('check3 is %d %s' % (chvarEn.get(), type(chvarUn.get())))
#
# action = ttk.Button(win, text="Click Me!", command=clickMe) # 创建一个按钮, text：显示按
#
# action.grid(column=2, row=1) # 设置其在界面中出现的位置
#
# # 文本框
#
# name = tk.StringVar() # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理
#
# #部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
#
# nameEntered = ttk.Entry(win, width=12, textvariable=name) # 创建一个文本框，字符长度为12，
#
# #内容绑定到name,方便clickMe调用
#
# nameEntered.grid(column=0, row=1) # 设置其在界面中出现的位置
#
# nameEntered.focus() # 当程序运行时,光标默认会出现在该文本框中
#
# # 一个下拉列表
#
# number = tk.StringVar()
#
# numberChosen = ttk.Combobox(win, width=12, textvariable=number, state='readonly')
#
# numberChosen['values'] = (1, 2, 4, 42, 100) # 设置下拉列表的值
#
# numberChosen.grid(column=1, row=1) # 设置其在界面中出现的位置 column代表列 row 代表行
#
# numberChosen.current(4) # 设置下拉列表默认显示的值，0为numberChosen['values'] 的下标值
#
# # 复选框
#
# chVarDis = tk.IntVar() # 用来获取复选框是否被勾选，通过chVarDis.get()来获取其的状态,
#
# #其状态值为int类型 勾选为1 未勾选为0
#
# check1 = tk.Checkbutton(win, text="Disabled", variable=chVarDis, state='disabled') # text为复选框
#
# #后面的名称,variable将该复选框的状态赋值给一个变量，当state='disabled'时，
#
# #该复选框为灰色，不能点的状态
#
# check1.select() # 该复选框是否勾选,select为勾选, deselect为不勾选
#
# check1.grid(column=0, row=4, sticky=tk.W) # sticky=tk.W 当该列中其他行或该行中的其他列的
#
# #某一个功能拉长这列的宽度或高度时，设定该值可以保证本行保持左对齐，
#
# #N：北/上对齐 S：南/下对齐 W：西/左对齐 E：东/右对齐
#
# chvarUn = tk.IntVar()
#
# check2 = tk.Checkbutton(win, text="UnChecked", variable=chvarUn)
#
# check2.deselect()
#
# check2.grid(column=1, row=4, sticky=tk.W)
#
# chvarEn = tk.IntVar()
#
# check3 = tk.Checkbutton(win, text="Enabled", variable=chvarEn)
#
# check3.select()
#
# check3.grid(column=2, row=4, sticky=tk.W)
#
# win.mainloop() # 当调用mainloop()时,窗口才会显示出来

# from tkinter import *
# from tkinter import ttk
# import glob
# import os
#
# search = '*log'
#
#
# found_files = []
#
# for dirname, dirnames, filenames in os.walk('./'):
#     for i in glob.glob(dirname+'/'+search+'*'):
#         print(i)
#         found_files.append(i)
#
#
#
# root = Tk()
# root.geometry( "640x480" )
#
#
# listbox = Listbox(root)
#
# for a_file in found_files:
#     listbox.insert(END, a_file)
#
# listbox.pack(fill=BOTH, expand=YES)
#
# root.mainloop()


""" tk_ToolTip_class101.py
gives a Tkinter widget a tooltip as the mouse is above the widget
tested with Python27 and Python34  by  vegaseat  09sep2014
www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

Modified to include a delay time by Victor Zaccardo, 25mar16
"""

try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

# testing ...
if __name__ == '__main__':
    root = tk.Tk()
    btn1 = tk.Button(root, text="button 1")
    btn1.pack(padx=10, pady=5)
    button1_ttp = CreateToolTip(btn1, \
   'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, '
   'consectetur, adipisci velit. Neque porro quisquam est qui dolorem ipsum '
   'quia dolor sit amet, consectetur, adipisci velit. Neque porro quisquam '
   'est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.')

    btn2 = tk.Button(root, text="button 2")
    btn2.pack(padx=10, pady=5)
    button2_ttp = CreateToolTip(btn2, \
    "First thing's first, I'm the realest. Drop this and let the whole world "
    "feel it. And I'm still in the Murda Bizness. I could hold you down, like "
    "I'm givin' lessons in  physics. You should want a bad Vic like this.")
    root.mainloop()


# import tkinter as tk
# from idlelib.tooltip import Hovertip
#
# app = tk.Tk()
# myBtn = tk.Button(app, text='?')
# myBtn.pack(pady=30)
# myTip = Hovertip(myBtn, 'This is \na multiline tooltip.')
# app.mainloop()


# import tkinter as tk
# import tkinter.ttk as ttk
#
#
# class Tooltip:
#     '''
#     It creates a tooltip for a given widget as the mouse goes on it.
#
#     see:
#
#     http://stackoverflow.com/questions/3221956/
#            what-is-the-simplest-way-to-make-tooltips-
#            in-tkinter/36221216#36221216
#
#     http://www.daniweb.com/programming/software-development/
#            code/484591/a-tooltip-class-for-tkinter
#
#     - Originally written by vegaseat on 2014.09.09.
#
#     - Modified to include a delay time by Victor Zaccardo on 2016.03.25.
#
#     - Modified
#         - to correct extreme right and extreme bottom behavior,
#         - to stay inside the screen whenever the tooltip might go out on
#           the top but still the screen is higher than the tooltip,
#         - to use the more flexible mouse positioning,
#         - to add customizable background color, padding, waittime and
#           wraplength on creation
#       by Alberto Vassena on 2016.11.05.
#
#       Tested on Ubuntu 16.04/16.10, running Python 3.5.2
#
#     TODO: themes styles support
#     '''
#
#     def __init__(self, widget,
#                  *,
#                  bg='#FFFFEA',
#                  pad=(5, 3, 5, 3),
#                  text='widget info',
#                  waittime=400,
#                  wraplength=250):
#
#         self.waittime = waittime  # in miliseconds, originally 500
#         self.wraplength = wraplength  # in pixels, originally 180
#         self.widget = widget
#         self.text = text
#         self.widget.bind("<Enter>", self.onEnter)
#         self.widget.bind("<Leave>", self.onLeave)
#         self.widget.bind("<ButtonPress>", self.onLeave)
#         self.bg = bg
#         self.pad = pad
#         self.id = None
#         self.tw = None
#
#     def onEnter(self, event=None):
#         self.schedule()
#
#     def onLeave(self, event=None):
#         self.unschedule()
#         self.hide()
#
#     def schedule(self):
#         self.unschedule()
#         self.id = self.widget.after(self.waittime, self.show)
#
#     def unschedule(self):
#         id_ = self.id
#         self.id = None
#         if id_:
#             self.widget.after_cancel(id_)
#
#     def show(self):
#         def tip_pos_calculator(widget, label,
#                                *,
#                                tip_delta=(10, 5), pad=(5, 3, 5, 3)):
#
#             w = widget
#
#             s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()
#
#             width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
#                              pad[1] + label.winfo_reqheight() + pad[3])
#
#             mouse_x, mouse_y = w.winfo_pointerxy()
#
#             x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
#             x2, y2 = x1 + width, y1 + height
#
#             x_delta = x2 - s_width
#             if x_delta < 0:
#                 x_delta = 0
#             y_delta = y2 - s_height
#             if y_delta < 0:
#                 y_delta = 0
#
#             offscreen = (x_delta, y_delta) != (0, 0)
#
#             if offscreen:
#
#                 if x_delta:
#                     x1 = mouse_x - tip_delta[0] - width
#
#                 if y_delta:
#                     y1 = mouse_y - tip_delta[1] - height
#
#             offscreen_again = y1 < 0  # out on the top
#
#             if offscreen_again:
#                 # No further checks will be done.
#
#                 # TIP:
#                 # A further mod might automagically augment the
#                 # wraplength when the tooltip is too high to be
#                 # kept inside the screen.
#                 y1 = 0
#
#             return x1, y1
#
#         bg = self.bg
#         pad = self.pad
#         widget = self.widget
#
#         # creates a toplevel window
#         self.tw = tk.Toplevel(widget)
#
#         # Leaves only the label and removes the app window
#         self.tw.wm_overrideredirect(True)
#
#         win = tk.Frame(self.tw,
#                        background=bg,
#                        borderwidth=0)
#         label = tk.Label(win,
#                           text=self.text,
#                           justify=tk.LEFT,
#                           background=bg,
#                           relief=tk.SOLID,
#                           borderwidth=0,
#                           wraplength=self.wraplength)
#
#         label.grid(padx=(pad[0], pad[2]),
#                    pady=(pad[1], pad[3]),
#                    sticky=tk.NSEW)
#         win.grid()
#
#         x, y = tip_pos_calculator(widget, label)
#
#         self.tw.wm_geometry("+%d+%d" % (x, y))
#
#     def hide(self):
#         tw = self.tw
#         if tw:
#             tw.destroy()
#         self.tw = None
#
#
# if __name__ == '__main__':
#
#     import random
#
#     def further_text():
#         # texts generated at http://lorem-ipsum.perbang.dk/
#         short_text = ('Lorem ipsum dolor sit amet, mauris tellus, '
#                      'porttitor torquent eu. Magna aliquet lorem, '
#                      'cursus sit ac, in in. Dolor aliquet, cum integer. '
#                      'Proin aliquet, porttitor pulvinar mauris. Tellus '
#                      'lectus, amet cras, neque lacus quis. Malesuada '
#                      'nibh. Eleifend nam, in eget a. Nec turpis, erat '
#                      'wisi semper')
#         medium_text = ('Lorem ipsum dolor sit amet, suspendisse aenean '
#                        'ipsum sollicitudin, pellentesque nunc ultrices ac '
#                        'ut, arcu elit turpis senectus convallis. Ac orci '
#                        'pretium sed gravida, tortor nulla felis '
#                        'consectetuer, mauris egestas est erat. Ut enim '
#                        'tellus at diam, ac sagittis vel proin. Massa '
#                        'eleifend orci tortor sociis, scelerisque in pede '
#                        'metus phasellus, est tempor gravida nam, ante '
#                        'fusce sem tempor. Mi diam auctor vel pede, mus '
#                        'non mi luctus luctus, lectus sit varius repellat '
#                        'eu')
#         long_text = ('Lorem ipsum dolor sit amet, velit eu nam cursus '
#                      'quisque gravida sollicitudin, felis arcu interdum '
#                      'error quam quis massa, et velit libero ligula est '
#                      'donec. Suspendisse fringilla urna ridiculus dui '
#                      'volutpat justo, quisque nisl eget sed blandit '
#                      'egestas, libero nullam magna sem dui nam, auctor '
#                      'vehicula nunc arcu vel sed dictum, tincidunt vitae '
#                      'id tristique aptent platea. Lacus eros nec proin '
#                      'morbi sollicitudin integer, montes suspendisse '
#                      'augue lorem iaculis sed, viverra sed interdum eget '
#                      'ut at pulvinar, turpis vivamus ac pharetra nulla '
#                      'maecenas ut. Consequat dui condimentum lectus nulla '
#                      'vitae, nam consequat fusce ac facilisis eget orci, '
#                      'cras enim donec aenean sed dolor aliquam, elit '
#                      'lorem in a nec fringilla, malesuada curabitur diam '
#                      'nonummy nisl nibh ipsum. In odio nunc nec porttitor '
#                      'ipsum, nunc ridiculus platea wisi turpis praesent '
#                      'vestibulum, suspendisse hendrerit amet quis vivamus '
#                      'adipiscing elit, ut dolor nec nonummy mauris nec '
#                      'libero, ad rutrum id tristique facilisis sed '
#                      'ultrices. Convallis velit posuere mauris lectus sit '
#                      'turpis, lobortis volutpat et placerat leo '
#                      'malesuada, vulputate id maecenas at a volutpat '
#                      'vulputate, est augue nec proin ipsum pellentesque '
#                      'fringilla. Mattis feugiat metus ultricies repellat '
#                      'dictum, suspendisse erat rhoncus ultricies in ipsum, '
#                      'nulla ante pellentesque blandit ligula sagittis '
#                      'ultricies, sed tortor sodales pede et duis platea')
#
#         text = random.choice([short_text, medium_text, long_text, long_text])
#
#         return '\nFurther info: ' + text
#
#     def main_01(wraplength=200):
#
#         # alias
#         stuff = further_text
#
#         root = tk.Tk()
#         frame = ttk.Frame(root)
#
#         btn_ne = ttk.Button(frame, text='North East')
#         btn_se = ttk.Button(frame, text='South East')
#         btn_sw = ttk.Button(frame, text='South West')
#         btn_nw = ttk.Button(frame, text='North West')
#         btn_center = ttk.Button(frame, text='Center')
#         btn_n = ttk.Button(frame, text='North')
#         btn_e = ttk.Button(frame, text='East')
#         btn_s = ttk.Button(frame, text='South')
#         btn_w = ttk.Button(frame, text='West')
#
#         Tooltip(btn_nw, text='North West' + stuff(), wraplength=wraplength)
#         Tooltip(btn_ne, text='North East' + stuff(), wraplength=wraplength)
#         Tooltip(btn_se, text='South East' + stuff(), wraplength=wraplength)
#         Tooltip(btn_sw, text='South West' + stuff(), wraplength=wraplength)
#         Tooltip(btn_center, text='Center' + stuff(), wraplength=wraplength)
#         Tooltip(btn_n, text='North' + stuff(), wraplength=wraplength)
#         Tooltip(btn_e, text='East' + stuff(), wraplength=wraplength)
#         Tooltip(btn_s, text='South' + stuff(), wraplength=wraplength)
#         Tooltip(btn_w, text='West' + stuff(), wraplength=wraplength)
#
#         r = 0
#         c = 0
#         pad = 10
#         btn_nw.grid(row=r, column=c, padx=pad, pady=pad, sticky=tk.NW)
#         btn_n.grid(row=r, column=c + 1, padx=pad, pady=pad, sticky=tk.N)
#         btn_ne.grid(row=r, column=c + 2, padx=pad, pady=pad, sticky=tk.NE)
#
#         r += 1
#         btn_w.grid(row=r, column=c + 0, padx=pad, pady=pad, sticky=tk.W)
#         btn_center.grid(row=r, column=c + 1, padx=pad, pady=pad,
#                     sticky=tk.NSEW)
#         btn_e.grid(row=r, column=c + 2, padx=pad, pady=pad, sticky=tk.E)
#
#         r += 1
#         btn_sw.grid(row=r, column=c, padx=pad, pady=pad, sticky=tk.SW)
#         btn_s.grid(row=r, column=c + 1, padx=pad, pady=pad, sticky=tk.S)
#         btn_se.grid(row=r, column=c + 2, padx=pad, pady=pad, sticky=tk.SE)
#
#         frame.grid(sticky=tk.NSEW)
#         for i in (0, 2):
#             frame.rowconfigure(i, weight=1)
#             frame.columnconfigure(i, weight=1)
#
#         root.rowconfigure(0, weight=1)
#         root.columnconfigure(0, weight=1)
#
#         root.title('Tooltip wraplength = {}'.format(wraplength))
#         root.mainloop()
#
#     def main():
#         print('Trying out three different wraplengths:')
#         for i, wl in enumerate((200, 250, 400), 1):
#             print(' ', i)
#             main_01(wl)
#         print('Done.')
#
#     main()


"""useful code"""
# from tkinter import *
# root = tk.Tk()
# root.geometry("500x300")
# def update(data):
#     my_list.delete(0, END)
#
#     for item in data:
#         my_list.insert(END, item)
#
# # def update_1(data):
# #     my_list_1.delete(0, END)
# #
# #     for item in data:
# #         my_list_1.insert(END, item)
#
# def fillout(e):
#     my_entry.delete(0, END)
#     my_entry.insert(0, my_list.get(ACTIVE))
#
# # def fillout_1(e):
# #     my_entry_1.delete(0, END)
# #     my_entry_1.insert(0, my_list_1.get(ACTIVE))
#
#
# def check(e):
#     # my_list_1.pack_forget()
#     # my_list.pack()
#     typed = my_entry.get()
#     # if ',' in typed:
#     #     first, second = typed.strip().split(',')
#     #     typed = second
#     #     print(typed)
#
#     if typed == "":
#         data = toppings
#     else:
#         data = []
#         for item in toppings:
#             if typed.lower() in item.lower():
#                 data.append(item)
#     update(data)
#
# # def check_1(e):
# #     # my_list.pack_forget()
# #     # my_list_1.pack()
# #     typed = my_entry_1.get()
# #     # if ',' in typed:
# #     #     first, second = typed.strip().split(',')
# #     #     typed = second
# #     #     print(typed)
# #
# #     if typed == "":
# #         data = toppings
# #     else:
# #         data = []
# #         for item in toppings:
# #             if typed.lower() in item.lower():
# #                 data.append(item)
# #     update_1(data)
#
# my_label = Label(root, text='Start Typing...')
# my_label.pack(pady=20)
#
# my_entry = Entry(root)
# my_entry.pack()
#
# # my_entry_1 = Entry(root)
# # my_entry_1.pack()
#
# # self.bind("<FocusIn>", self.on_focus_in)
# # self.bind("<FocusOut>", self.on_focus_out)
# # def on_focus_in(event):
# #     # my_list_1.pack_forget()
# #     my_list.pack()
# #     print('on_focus_in')
# #
# # def on_focus_out(event):
# #     # my_list_1.pack_forget()
# #     # my_list.pack_forget()
# #     print('on_focus_out')
#
# # def on_focus_in_1(event):
# #     my_list.pack_forget()
# #     my_list_1.pack()
# #     print('on_focus_in_1')
# #
# # def on_focus_out_1(event):
# #     # my_list_1.pack_forget()
# #     # my_list_1.pack_forget()
# #     print('on_focus_out_1')
#
# # my_entry.bind("<FocusIn>", on_focus_in)
# # my_entry.bind("<FocusOut>", on_focus_out)
#
# # my_entry_1.bind("<FocusIn>", on_focus_in_1)
# # my_entry_1.bind("<FocusOut>", on_focus_out_1)
#
# my_list = Listbox(root, width=50)
# my_list.pack(pady=40)
#
# # my_list_1 = Listbox(root, width=50)
# # my_list_1.pack(pady=40)
#
# toppings = ['TransE', 'TransD', 'TransH', 'DistMult', 'ComplEx', 'SimplE']
#
# update(toppings)
#
# my_list.bind("<<ListboxSelect>>", fillout)
# # my_list_1.bind("<<ListboxSelect>>", fillout_1)
#
# my_entry.bind("<KeyRelease>", check)
# # my_entry_1.bind("<KeyRelease>", check_1)
#
# root.mainloop()


# Key press prototype
# Tracks keys as pressed, ignoring the keyboard repeater
# Current keys down are kept in a dictionary.
# That a key is pressed is flagged, and the last key pressed is tracked

# import tkinter
#
# winWid = 640
# winHei = 480
# keyDown = False
# lastKey = "none"
# keyChange = keyDown
# keyList = {}
#
#
# def onKeyDown(event):
#     global keyDown, lastKey, keyList
#     if (event.char in keyList) != True:
#         keyList[event.char] = "down"
#         print(keyList)
#     keyDown = True
#     lastKey = event.char
#
#
# def onKeyUp(event):
#     global keyDown
#     if (event.char in keyList) == True:
#         keyList.pop(event.char)
#     if len(keyList) == 0:
#         keyDown = False
#     print(keyList)
#
#
# # onTimer is present to show keyboard action as it happens.
# # It is not needed to track the key changes, and it can be
# # removed.
# def onTimer():
#     global keyChange, timerhandle
#     if keyDown != keyChange:
#         keyChange = keyDown
#         if keyDown:
#             print("Key down, last key pressed - " + lastKey)
#         else:
#             print("Key up, last key pressed - " + lastKey)
#     timerhandle = window.after(20, onTimer)
#
#
# def onShutdown():
#     window.after_cancel(timerhandle)
#     window.destroy()
#
#
# window = tkinter.Tk()
# frame = tkinter.Canvas(window, width=winWid, height=winHei, bg="black")
# frame.pack()
#
# frame.bind("<KeyPress>", onKeyDown)
# frame.bind("<KeyRelease>", onKeyUp)
# frame.focus_set()
#
# timerhandle = window.after(20, onTimer)
# window.protocol("WM_DELETE_WINDOW", onShutdown)
# window.mainloop()


# #!/usr/bin/env python3
#
# import tkinter as tk
#
# def on_keypress(event):
#
#     print(event)
#     print(event.state & 4) # Control
#     print(event.keysym == 'a')
#     # get text from entry
#     if event.keysym == 'BackSpace':
#         # remove last char
#         value = event.widget.get()[:-1]
#     elif (event.state & 4): # and (event.keysym in ('a', 'c', 'x', 'e')):
#         value = event.widget.get()
#     else:
#         # add new char at the end
#         value = event.widget.get() + event.char
#     #TODO: other special keys
#
#     value = value.strip().lower()
#
#     # get data from test_list
#     if value == '':
#         data = test_list
#     else:
#         data = []
#         for item in test_list:
#             if value in item.lower():
#                 data.append(item)
#
#     # update data in listbox
#     listbox_update(data)
#
#
# def listbox_update(data):
#     # delete previous data
#     listbox.delete(0, 'end')
#
#     # sorting data
#     data = sorted(data, key=str.lower)
#
#     # put new data
#     for item in data:
#         listbox.insert('end', item)
#
#
# def on_select(event):
#     # display element selected on list
#     print('(event) previous:', event.widget.get('active'))
#     print('(event)  current:', event.widget.get(event.widget.curselection()))
#     print('---')
#
#
# # --- main ---
#
# test_list = ('apple', 'banana', 'Cranberry', 'dogwood', 'alpha', 'Acorn', 'Anise', 'Strawberry' )
#
# root = tk.Tk()
#
# entry = tk.Entry(root)
# entry.pack()
# entry.bind('<KeyPress>', on_keypress)
#
# listbox = tk.Listbox(root)
# listbox.pack()
# #listbox.bind('<Double-Button-1>', on_select)
# listbox.bind('<<ListboxSelect>>', on_select)
# listbox_update(test_list)
#
# root.mainloop()

# # !/usr/bin/env python3
#
# import tkinter as tk
#
#
# def on_change(*args):
#     # print(args)
#
#     value = var_text.get()
#     value = value.strip().lower()
#
#     # get data from test_list
#     if value == '':
#         data = test_list
#     else:
#         data = []
#         for item in test_list:
#             if value in item.lower():
#                 data.append(item)
#
#                 # update data in listbox
#     listbox_update(data)
#
#
# def listbox_update(data):
#     # delete previous data
#     listbox.delete(0, 'end')
#
#     # sorting data
#     data = sorted(data, key=str.lower)
#
#     # put new data
#     for item in data:
#         listbox.insert('end', item)
#
#
# def on_select(event):
#     # display element selected on list
#     print('(event) previous:', event.widget.get('active'))
#     print('(event)  current:', event.widget.get(event.widget.curselection()))
#     print('---')
#
#
# # --- main ---
#
# test_list = ('apple', 'banana', 'Cranberry', 'dogwood', 'alpha', 'Acorn', 'Anise', 'Strawberry')
#
# root = tk.Tk()
#
# var_text = tk.StringVar()
# var_text.trace('w', on_change)
#
# entry = tk.Entry(root, textvariable=var_text)
# entry.pack()
#
# listbox = tk.Listbox(root)
# listbox.pack()
# # listbox.bind('<Double-Button-1>', on_select)
# listbox.bind('<<ListboxSelect>>', on_select)
# listbox_update(test_list)
#
# root.mainloop()

# from ttkwidgets.autocomplete import AutocompleteEntryListbox
# from tkinter import *
#
# countries = [
#         'Antigua and Barbuda', 'Bahamas','Barbados','Belize', 'Canada',
#         'Costa Rica ', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador ',
#         'Grenada', 'Guatemala ', 'Haiti', 'Honduras ', 'Jamaica', 'Mexico',
#         'Nicaragua', 'Saint Kitts and Nevis', 'Panama ', 'Saint Lucia',
#         'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States of America'
#         ]
#
# ws = Tk()
# ws.title('PythonGuides')
# ws.geometry('400x300')
# ws.config(bg='#DFE7F2')
#
# frame = Frame(ws, bg='#DFE7F2')
# frame.pack(expand=True)
#
# Label(
#     frame,
#     bg='#DFE7F2',
#     font = ('Times',21),
#     text='Countries in North America '
#     ).pack()
#
# entry = AutocompleteEntryListbox(
#     frame,
#     width=30,
#     font=('Times', 18),
#     completevalues=countries
#     )
# entry.pack()
#
# ws.mainloop()

# from ttkwidgets.autocomplete import AutocompleteEntry
# from tkinter import *
#
# countries = [
#         'Antigua and Barbuda', 'Bahamas','Barbados','Belize', 'Canada',
#         'Costa Rica ', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador ',
#         'Grenada', 'Guatemala ', 'Haiti', 'Honduras ', 'Jamaica', 'Mexico',
#         'Nicaragua', 'Saint Kitts and Nevis', 'Panama ', 'Saint Lucia',
#         'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States of America'
#         ]
#
# ws = Tk()
# ws.title('PythonGuides')
# ws.geometry('400x300')
# ws.config(bg='#f25252')
#
# frame = Frame(ws, bg='#f25252')
# frame.pack(expand=True)
#
# Label(
#     frame,
#     bg='#f25252',
#     font = ('Times',21),
#     text='Countries in North America '
#     ).pack()
#
# entry = AutocompleteEntry(
#     frame,
#     width=30,
#     font=('Times', 18),
#     completevalues=countries
#     )
# entry.pack()
#
# ws.mainloop()


# -*- coding: utf8 -*-
# from tkinter import *
#
#
# #####################################
# ###--------------tk----------------
# class App:
#     def __init__(self, master):
#         frame = Frame(master)
#         frame.pack(expand=1)
#         self.e1 = Entry(frame)
#         self.e1.pack()
#         self.e2 = Entry(frame)
#         self.e2.pack()
#
#         self.e1.bind("<Return>", handlerAdaptor(focus_cg, e2=self.e2))  # tk类不能直接传递参数，需要lambda
#
#
# def focus_cg(event, e2):
#     e2.focus_set()  # 焦点移到e2
#     print('entry 2')
#
#
# def handlerAdaptor(fun, **kwds):
#     print('entry 22')
#     # 事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧
#     return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)
#
#
# if __name__ == '__main__':
#     root = Tk()
#     app = App(root)
#     root.mainloop()