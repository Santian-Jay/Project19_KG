# import tkinter as tk
# from tkinter import *
#
# class Button_Canvas(Button):
#     def __init__(self, id=None, **kwargs):
#         self.id = id
#         super().__init__()
#
#
# b1= Button_Canvas(text="test", id=111)
# b2= Button_Canvas(text="test", id=2222)
# b3 = Button_Canvas(text="test", id=3333)
# b4 = Button_Canvas(text="test", id=4444)
#
# print(b1.id)
# print(b2.id)
# print(b3.id)
# print(b4.id)


from tkinter import *

# class My_Button(Button):
#     def __init__(self, text, id, command, color=None, **kwargs):
#         self.text = text
#         self.id = id
#         self.command = command
#         self.color = color
#         super().__init__()
#         self['bg'] = self.color
#         self['text'] = self.text
#         self['command'] = self.command
#
#     def get_id(self):
#         return self.id
#
#
# def dothings():
#     print('Button class worked')
#     print(btn1.id)
#
# window = Tk()
# window.title("Test Button Class")
# window.geometry('400x200')
#
# btn1 = My_Button("Click Me", 11111, dothings,  'green')
# btn1.pack()
#
#
# window.mainloop()
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# window = Tk()
# window.title("Test Button Class")
# window.geometry('600x400')
#
# def event(e):
#     # canvas.delete('current')
#     widget = e.widget
#     print(canvas('current'))
#
# canvas = Canvas(window, width=600, height=400)
# canvas.pack()
# x = ["A", "B", "C", "D", "E", "F", "G", "H"]
# y = [150, 85.2, 65.2, 85, 45, 120, 51, 64]
# #
# # fig, ax = plt.subplots(figsize=(10, 7))
# # ax.bar(x=x, height=y)
# # ax.set_title("Simple Bar Plot", fontsize=15)
#
# # canvas_l = FigureCanvasTkAgg(fig, canvas)
# # canvas_l.draw()
#
# # canvas_l.get_tk_widget().pack()
#
# canvas.create_line(40, 360, 560, 360, width=2, fill="orange")
# canvas.create_line(40, 40, 40, 360, width=2, fill="orange")
#
# x_list = []
# for i in range(80, 540, 60):
#     canvas.create_line(i, 360, i, 364, width=4, fill='orange')
#     x_list.append(i)
#
# # for j in range(80, 540, 60):
# #     count = 0
# #     y2 = 360 - y[count]
# #     print("y2: ", y2)
# #     canvas.create_line(j, 360, j, y2, width=40, fill="green")
# #     count += 1
#
# for j in range(len(x_list)):
#     # y2 = 360 - y[j]
#     p_x = x_list[j]
#     p_y = 360 - y[j]
#     print("y2: ", y[j])
#     canvas.create_line(p_x, 360, p_x, p_y, width=40, fill="green")
# canvas.bind('<Button-1>', event)
#
#
# window.mainloop()


# from tkinter import *
# import time
#
#
# def ok():  # 点击按钮，由yn变量决定是暂停还是继续动起来
#     global yn
#     if yn == True:
#         yn = False
#         but1['text'] = '  动起来  '
#     else:
#         yn = True
#         but1['text'] = '  暂 停  '
#         ballmove()  # 小球继续动起来
#
#
# def ballmove():  # 小球在画布四周不停反弹
#     global x, y
#     while yn:  # 由yn变量来控制小球是否移动
#         can1.move(xq, x, y)  # 初始化,小球向右下角移动
#         weizhi = can1.coords(xq)  # 获取小球的位置，一个4个元素的元组
#
#         if weizhi[0] <= 0:  # 侦测球是否超过画布左方
#             x = step
#         if weizhi[1] <= 0:  # 侦测球是否超过画布上方
#             y = step
#         if weizhi[2] >= can1width:  # 侦测球是否超过画布右方
#             x = -step
#         if weizhi[3] >= can1height:  # 侦测球是否超过画布下方
#             y = -step
#
#         can1.update()  # 刷新画布
#         time.sleep(speed)  # 可以控制移动速度
#
#
# root = Tk()
#
# can1width = 200  # 定义画布宽度
# can1height = 150  # 定义画布高度
# step = 3  # 小于移动的步长,3个像素
# x, y = 3, 3  # 小球移动的初始步长
# speed = 0.03  # 设置移动速度
# yn = False  # yn的值来控制球是否移动
#
# can1 = Canvas(root, background='lightblue', width=can1width, height=can1height)  # 创建画布
# can1.pack()
#
# but1 = Button(root, text="  动起来  ", command=ok)  # 创建按钮
# but1.pack()
#
# xq = can1.create_oval(20, 20, 40, 40, fill='red', outline='green')  # 绘制小球
#
#
# def xq_move(event):  # 鼠标拖动小球
#     can1.coords(xq, event.x - 10, event.y - 10, event.x + 10, event.y + 10)
#     # 将鼠标当前位置转为小球的外接正方形的左上角和右下角坐标（小球的半径为10）
#
#
# can1.tag_bind(xq, "<B1-Motion>", xq_move)  # 小球,鼠标按住移动事件
#
# root.mainloop()


# from tkinter import *
# from tkinter import colorchooser
# import threading
# # 创建窗口
# root = Tk()
# root.title('操作图形项')
# # 创建并添加Canvas
# cv = Canvas(root, background='white', width=400, height=350)
# cv.pack(fill=BOTH, expand=YES)
# # 该变量用于保存当前选中的图形项
# current = None
# # 该变量用于保存当前选中的图形项的边框颜色
# current_outline = None
# # 该变量用于保存当前选中的图形项的边框宽度
# current_width = None
# # 该函数用于高亮显示选中图形项（边框颜色会red、yellow之间切换）
# def show_current():
#     # 如果当前选中项不为None
#     if current is not None:
#         # 如果当前选中图形项的边框色为red，将它改为yellow
#         if cv.itemcget(current, 'outline') == 'red':
#             cv.itemconfig(current, width=2,
#             outline='yellow')
# # 否则，将颜色改为red
#     else:
#         cv.itemconfig(current, width=2,
#         outline='red')
# global t
# # 通过定时器指定0.2秒之后执行show_current函数
# t = threading.Timer(0.2, show_current)
# t.start()
# # 通过定时器指定0.2秒之后执行show_current函数
# t = threading.Timer(0.2, show_current)
# t.start()
# # 分别创建矩形、椭圆、和圆
# rect = cv.create_rectangle(30, 30, 250, 200,
# fill='magenta', width='0')
# oval = cv.create_oval(180, 50, 380, 180,
# fill='yellow', width='0')
# circle = cv.create_oval(120, 150, 300, 330,
# fill='pink', width='0')
# bottomF = Frame(root)
# bottomF.pack(fill=X,expand=True)
# liftbn = Button(bottomF, text='向上',
# # 将椭圆移动到它上面的item之上
# command=lambda : cv.tag_raise(oval, cv.find_above(oval)))
# liftbn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# lowerbn = Button(bottomF, text='向下',
# # 将椭圆移动到它下面的item之下
# command=lambda : cv.tag_lower(oval, cv.find_below(oval)))
# lowerbn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# def change_fill():
# # 弹出颜色选择框,让用户选择颜色
#     fill_color = colorchooser.askcolor(parent=root,
#     title='选择填充颜色',
# # 初始颜色设置为椭圆当前的填充色（fill选项值）
#     color = cv.itemcget(oval, 'fill'))
#     if fill_color is not None:
#         cv.itemconfig(oval, fill=fill_color[1])
#         fillbn = Button(bottomF, text='改变填充色',
#         # 该按钮触发change_fill函数
#         command=change_fill)
#         fillbn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# def change_outline():
#     # 弹出颜色选择框,让用户选择颜色
#     outline_color = colorchooser.askcolor(parent=root,
#     title='选择边框颜色',
#     # 初始颜色设置为椭圆当前的边框色（outline选项值）
#     color = cv.itemcget(oval, 'outline'))
#     if outline_color is not None:
#         cv.itemconfig(oval, outline=outline_color[1],
#         width=4)
#         outlinebn = Button(bottomF, text='改变边框色',
#         # 该按钮触发change_outline函数
#         command=change_outline)
#         outlinebn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
#         movebn = Button(bottomF, text='右下移动',
#         # 调用move方法移动图形项
#         command=lambda : cv.move(oval, 15, 10))
#         movebn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# coordsbn = Button(bottomF, text='位置复位',
# # 调用coords方法重设图形项的大小和位置
# command=lambda : cv.coords(oval, 180, 50, 380, 180))
# coordsbn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# # 再次添加Frame容器
# bottomF = Frame(root)
# bottomF.pack(fill=X,expand=True)
# zoomoutbn = Button(bottomF, text='缩小',
# # 调用scale方法对图形项进行缩放
# # 前面两个坐标指定缩放中心，后面两个参数指定横向、纵向的缩放比
# command=lambda : cv.scale(oval, 180, 50, 0.8, 0.8))
# zoomoutbn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# zoominbn = Button(bottomF, text='放大',
# # 调用scale方法对图形项进行缩放
# # 前面两个坐标指定缩放中心，后面两个参数指定横向、纵向的缩放比
# command=lambda : cv.scale(oval, 180, 50, 1.2, 1.2))
# zoominbn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# def select_handler(ct):
#     global current, current_outline, current_width
#     # 如果ct元组包含了选中项
#     if ct is not None and len(ct) > 0:
#         ct = ct[0]
# # 如果current对应的图形项不为空
#     if current is not None:
#          # 恢复current对应的图形项的边框
#         cv.itemconfig(current, outline=current_outline,
#         width = current_width)
#     # 获取当前选中图形项的边框信息
#     current_outline = cv.itemcget(ct, 'outline')
#     current_width = cv.itemcget(ct, 'width')
#     # 使用current保存当前选中项
#     current = ct
# def click_handler(event):
#     # 获取当前选中的图形项
#     ct = cv.find_closest(event.x, event.y)
#     # 调用select _handler处理选中图形项
#     select_handler(ct)
# def click_select():
#     # 取消为“框选”绑定的两个事件处理函数
#     cv.unbind('<B1-Motion>')
#     cv.unbind('<ButtonRelease-1>')
#     # 为“点选”绑定鼠标点击的事件处理函数
#     cv.bind('<Button-1>', click_handler)
#     clickbn = Button(bottomF, text='点选图形项',
#     # 该按钮触发click_select函数
#     command=click_select)
#     clickbn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# # 记录鼠标拖动的第一个点的x、y坐标
#     firstx = firsty = None
# # 记录前一次绘制的、代表选择区的虚线框
#     prev_select = None
# def drag_handler(event):
#     global firstx, firsty, prev_select
# # 刚开始拖动时，用鼠标位置为firstx、firsty赋值
#     if firstx is None and firsty is None:
#         firstx, firsty = event.x, event.y
#         leftx, lefty = min(firstx, event.x), min(firsty, event.y)
#         rightx, righty = max(firstx, event.x), max(firsty, event.y)
# # 删除上一次绘制的虚线选择框
#     if prev_select is not None:
#         cv.delete(prev_select)
# # 重新绘制虚线选择框
#         prev_select = cv.create_rectangle(leftx, lefty, rightx, righty,
#         dash=2)
# def release_handler(event):
#     global firstx, firsty
#     if prev_select is not None:
#         cv.delete(prev_select)
#     if firstx is not None and firsty is not None:
#         leftx, lefty = min(firstx, event.x), min(firsty, event.y)
#         rightx, righty = max(firstx, event.x), max(firsty, event.y)
#         firstx = firsty = None
# # 获取当前选中的图形项
#     ct = cv.find_enclosed(leftx, lefty, rightx, righty)
# # 调用select _handler处理选中图形项
#     select_handler(ct)
# def rect_select():
# # 取消为“点选”绑定的事件处理函数
#     cv.unbind('<Button-1>')
# # 为“框选”绑定鼠标拖动、鼠标释放的事件处理函数
#     cv.bind('<B1-Motion>', drag_handler)
#     cv.bind('<ButtonRelease-1>', release_handler)
# rectbn = Button(bottomF, text='框选图形项',
# # 该按钮触发rect_select函数
# command=rect_select)
# rectbn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# deletebn = Button(bottomF, text='删除',
# # 删除图形项
# command=lambda : cv.delete(oval))
# deletebn.pack(side=LEFT, ipadx=10, ipady=5, padx=3)
# root.mainloop()


from tkinter import *
# 创建窗口
root = Tk()
root.title('操作标签')
# 创建并添加Canvas
cv = Canvas(root, background='white', width=620, height=250)
cv.pack(fill=BOTH, expand=YES)
# 绘制一个矩形框
rt = cv.create_rectangle(40, 40, 300, 220,
outline='blue', width=2,
tag = ('t1', 't2', 't3', 'tag4')) # 为该图形项指定标签
# 访问图形项的id，也就是编号
print(rt) # 1
# 绘制一个椭圆
oval = cv.create_oval(350, 50, 580, 200,
fill='yellow', width=0,
tag = ('g1', 'g2', 'g3', 'tag4')) # 为该图形项指定标签
# 访问图形项的id，也就是编号
print(oval) # 2
# 根据指定tag该tag对应的所有图形项
print(cv.find_withtag('tag4')) # (1, 2)
# 获取指定图形项的所有tag
print(cv.gettags(rt)) # ('t1', 't2', 't3', 'tag4')
print(cv.gettags(2)) # ('g1', 'g2', 'g3', 'tag4')
cv.dtag(1, 't1') # 删除id为1的图形项上名为t1的tag
cv.dtag(oval, 'g1') # 删除id为oval的图形项上名为g1的tag
# 获取指定图形项的所有tag
print(cv.gettags(rt)) # ('tag4', 't2', 't3')
print(cv.gettags(2)) # ('tag4', 'g2', 'g3')
# 为所有图形项添加tag
cv.addtag_all('t5')
print(cv.gettags(1)) # ('tag4', 't2', 't3', 't5')
print(cv.gettags(oval)) # ('tag4', 'g2', 'g3', 't5')
# 为指定图形项添加tag
cv.addtag_withtag('t6', 'g2')
# 获取指定图形项的所有tag
print(cv.gettags(1)) # ('tag4', 't2', 't3', 't5')
print(cv.gettags(oval)) # ('tag4', 'g2', 'g3', 't5', 't6')
# 为指定图形项上面的图形项添加tag, t2上面的就是oval图形项
cv.addtag_above('t7', 't2')
print(cv.gettags(1)) # ('tag4', 't2', 't3', 't5')
print(cv.gettags(oval)) # ('tag4', 'g2', 'g3', 't5', 't6', 't7')
# 为指定图形项下面的图形项添加tag, g2下面的就是rt图形项
cv.addtag_below('t8', 'g2')
print(cv.gettags(1)) # ('tag4', 't2', 't3', 't5', 't8')
print(cv.gettags(oval)) # ('tag4', 'g2', 'g3', 't5', 't6', 't7')
# 为最接近指定点的图形项添加tag，最接近360、90的图形项是oval
cv.addtag_closest('t9', 360, 90)
print(cv.gettags(1)) # ('tag4', 't2', 't3', 't5', 't8')
print(cv.gettags(oval)) # ('tag4', 'g2', 'g3', 't5', 't6', 't7', 't9')
# 为位于指定区域内（几乎覆盖整个图形区）的最上面的图形项添加tag
cv.addtag_closest('t10', 30, 30, 600, 240)
print(cv.gettags(1)) # ('tag4', 't2', 't3', 't5', 't8')
print(cv.gettags(oval)) # ('tag4', 'g2', 'g3', 't5', 't6', 't7', 't9', 't10')
# 为与指定区域内重合的最上面的图形项添加tag
cv.addtag_closest('t11', 250, 30, 400, 240)
print(cv.gettags(1)) # ('tag4', 't2', 't3', 't5', 't8')
print(cv.gettags(oval)) # ('tag4', 'g2', 'g3', 't5', 't6', 't7', 't9', 't10', 't11')
root.mainloop()