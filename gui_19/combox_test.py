# -*- encoding=utf-8 -*-
# import tkinter
# from tkinter import *
# from tkinter import ttk
#
#
# def choose(event):
#     # 选中事件
#     print('选中的数据:{}'.format(combobox.get()))
#     print('value的值:{}'.format(value.get()))
#
#
# if __name__ == '__main__':
#     win = tkinter.Tk()  # 窗口
#     win.title('南风丶轻语')  # 标题
#     screenwidth = win.winfo_screenwidth()  # 屏幕宽度
#     screenheight = win.winfo_screenheight()  # 屏幕高度
#     width = 600
#     height = 500
#     x = int((screenwidth - width) / 2)
#     y = int((screenheight - height) / 2)
#     win.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
#     value = StringVar()
#     value.set('CCC')  # 默认选中CCC==combobox.current(2)
#
#     values = ['AAA', 'BBB', 'CCC', 'DDD']
#     combobox = ttk.Combobox(
#             master=win,  # 父容器
#             height=10,  # 高度,下拉显示的条目数量
#             width=20,  # 宽度
#             state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
#             cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
#             font=('', 20),  # 字体
#             textvariable=value,  # 通过StringVar设置可改变的值
#             values=values,  # 设置下拉框的选项
#             )
#     combobox.bind('<<ComboboxSelected>>', choose)
#     # print(combobox.keys())  # 可以查看支持的参数
#     combobox.pack()
#     win.mainloop()

import tkinter

win = tkinter.Tk()
win.title("Listbox列表框（单击多选）")
win.geometry("800x600+600+100")
#MULTIPLE   支持不用按shift和ctrl可以多选
lb=tkinter.Listbox(win,selectmode=tkinter.MULTIPLE)
lb.pack()
for item in["good","nice","handsome","very good","verynice"]:
    lb.insert(tkinter.END,item)
def delete_item():
    lb.delete('active')

# deleteButton = tkinter.Button(win, text='Delete', command=lambda x=lb: x.delete('active'))
deleteButton = tkinter.Button(win, text='Delete', command=lambda: delete_item())
deleteButton.pack()

win.mainloop()