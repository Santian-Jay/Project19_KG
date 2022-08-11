import tkinter as tk

# if __name__ == '__main__':
#     root = tk.Tk()
#     root.geometry("600x600")
#
#     framea = tk.Frame(root, height=130,  bg='blue')
#     framea.pack(side='top', fill='x', ipadx=10, ipady=10, expand=0)
#
#     frameb = tk.Frame(root, bg='green')
#     frameb.pack(side='top', fill='both', ipadx=10, ipady=10, expand=True)
#
#     framec = tk.Frame(framea, height=60,  bg='gray')
#     framec.pack(side='top', fill='x', ipadx=10, ipady=10, expand=0)
#
#     framed = tk.Frame(framea, bg='yellow')
#     framed.pack(side='top', fill='x', ipadx=10, ipady=10, expand=True)
#
#     tk.Button(root, text='Select Files').place(x=0, y=0, width=200, height=50)
#
#     root.mainloop()
import numpy as np
import matplotlib.mlab as mlab


# import matplotlib.pyplot as plt
# x = ['TransE', 'TransD', 'TransH', 'DistMult', 'ComplEx', 'SimplE']
# y = [827, 647, 611, 369, 155.72, 500]
# fig1 = plt.figure()
# plt.bar(x, y, 0.4, color='steelblue')
#
# for a, b in zip(x, y):
#     plt.text(a, b, '%.4f' % b, ha='center', va='bottom')
#
# plt.xlabel('Models')
# plt.ylabel('')
# plt.title('Training result')
#
# plt.show()
# import numpy as np
# import matplotlib.pyplot as plt
#
# x = np.arange(10) + 1
# y1 = np.random.randint(1, 3, 10)
#
# y2 = np.full(x.shape, 2)
#
# #在左下的子图绘制 y1 的条形图
#
# plt.subplot(223)
#
# plt.bar(x, y1, color='yellow')
#
# plt.ylabel('y1')
#
# #在右下的子图中绘制 y2 的条形图
#
# plt.subplot(224)
#
# plt.bar(x, y2, color='green')
#
# plt.ylabel('y2')
#
# #在左上的子图中绘制堆积柱形图
#
# plt.subplot(221)
#
# plt.bar(x, y1, color='k', alpha=0.3)
#
# plt.bar(x, y2, bottom=y1)
#
# plt.ylabel('y1 + y2')
#
# #在右上的子图中绘制堆积柱形图
#
# plt.subplot(222)
#
# plt.bar(x, y2, color='gray')
#
# plt.bar(x, y1, bottom=y2, color='b')
#
# plt.ylabel('y2 + y1')
#
# plt.show()

# from tkinter import *
# win = Tk()
# win.title("C语言中文网")
# win.geometry('500x200')
# win.resizable(0,0)
# lb = Label(text='C语言中文网答疑辅导班',font=('微软雅黑', 18,'bold'),fg='#CD7054')
# lb.pack()
# # win.iconbitmap('C:/Users/Administrator/Desktop/C语言中文网logo.ico')
# # 新建整型变量
# CheckVar1 = IntVar()
# CheckVar2 = IntVar()
# CheckVar3 = IntVar()
# # 设置三个复选框控件，使用variable参数来接收变量
# check1 = Checkbutton(win, text="Python",font=('微软雅黑', 15,'bold'),variable = CheckVar1,onvalue=1,offvalue=0)
# check2 = Checkbutton(win, text="C语言",font=('微软雅黑', 15,'bold'),variable = CheckVar2,onvalue=1,offvalue=0)
# check3 = Checkbutton(win, text="Java",font=('微软雅黑', 15,'bold'),variable = CheckVar3,onvalue=1,offvalue=0)
# # 选择第一个为默认选项
# # check1.select ()
# check1.pack (side = LEFT)
# check2.pack (side = LEFT)
# check3.pack (side = LEFT)
# # 定义执行函数
# def study():
#     # 没有选择任何项目的情况下
#     if (CheckVar1.get() == 0 and CheckVar2.get() == 0 and CheckVar3.get() == 0):
#         s = '您还没选择任语言'
#     else:
#         s1 = "Python" if CheckVar1.get() == 1 else ""
#         s2 = "C语言" if CheckVar2.get() == 1 else ""
#         s3 = "Java" if CheckVar3.get() == 1 else ""
#         s = "您选择了%s %s %s" % (s1, s2, s3)
#      #设置标签lb2的字体
#     lb2.config(text=s)
# btn = Button(win,text="选好了",bg='#BEBEBE',command=study)
# btn.pack(side = LEFT)
# # 该标签，用来显示选择的文本
# lb2 = Label(win,text='',bg ='#9BCD9B',font=('微软雅黑', 11,'bold'),width = 5,height=2)
# lb2.pack(side = BOTTOM, fill = X)
# # 显示窗口
# win.mainloop()


import sys
if sys.version_info.major == 3:
    import tkinter as tk
elif sys.version_info.major == 2:
    import Tkinter as tk
import random
class DemoApplication(tk.Frame):
    def on_checkbox_changed(self):
        if self.check_box_var1.get()==1 and self.check_box_var2.get()==1:
            main_win.title(u"都被选中了")
        elif self.check_box_var1.get():
            main_win.title(u"C 被选中了")
        elif self.check_box_var2.get():
            main_win.title(u"Python 被选中了")
        else:
            main_win.title(u"都没有被选中")
    def createWidgets(self):
        self.check_box_var1 = tk.IntVar()
        self.check_box_var2 = tk.IntVar()
        # 创建一个多选框
        self.check_box1 = tk.Checkbutton(main_win,
                                       text=u'C',
                                       variable = self.check_box_var1,
                                       onvalue = 1,
                                       offvalue = 0,
                                       command=self.on_checkbox_changed)
        self.check_box1.pack()
        # 创建一个多选框
        self.check_box2 = tk.Checkbutton(main_win,
                                       text=u'Python',
                                       variable = self.check_box_var2,
                                       onvalue = 1,
                                       offvalue = 0,
                                       command=self.on_checkbox_changed)
        self.check_box2.pack()
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.createWidgets()
main_win = tk.Tk()
main_win.title(u"多选框演示")
main_win.geometry("300x100")
app = DemoApplication(master=main_win)
app.mainloop()