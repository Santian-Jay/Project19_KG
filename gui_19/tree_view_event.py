# import tkinter
# from tkinter import ttk  # 导入内部包
#
# li = ['王记', '12', '男']
# root = tkinter.Tk()
# root.title('测试')
# tree = ttk.Treeview(root, columns=['1', '2', '3'], show='headings')
# tree.column('1', width=100, anchor='center')
# tree.column('2', width=100, anchor='center')
# tree.column('3', width=100, anchor='center')
# tree.heading('1', text='姓名')
# tree.heading('2', text='学号')
# tree.heading('3', text='性别')
# tree.insert('', 'end', values=li)
# tree.grid()
#
#
# def treeviewClick(event):  # 单击
#     print('单击')
#     for item in tree.selection():
#         item_text = tree.item(item, "values")
#         print(item_text[0])  # 输出所选行的第一列的值
#
#
# tree.bind('<ButtonRelease-1>', treeviewClick)  # 绑定单击离开事件===========
#
# root.mainloop()

# import random
# from tkinter import ttk
# from tkinter import *
#
# root = Tk()  # 初始旷的声明
# columns = ("a", "b", "c")
# treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)  # 表格
#
# treeview.column('a', width=50, anchor='center')
# treeview.column('b', width=100, anchor='center')
# treeview.column('c', width=80, anchor='center')
# treeview.heading('a', text='列1')
# treeview.heading('b', text='列2')
# treeview.heading('c', text='列3')
# treeview.pack(side=LEFT, fill=BOTH)
# for i in range(10):
#     treeview.insert('', i, values=(str(random.randint(0, 9)), str(random.randint(0, 9)), str(random.randint(0, 9))))
#
#
# def treeview_sort_column(tv, col, reverse):  # Treeview、列名、排列方式
#     l = [(tv.set(k, col), k) for k in tv.get_children('')]
#     print(tv.get_children(''))
#     l.sort(reverse=reverse)  # 排序方式
#     # rearrange items in sorted positions
#     for index, (val, k) in enumerate(l):  # 根据排序后索引移动
#         tv.move(k, '', index)
#         print(k)
#     tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
#
#
# '''
# #莫名其妙？？？？写循环的话只有最后一列管用,看论坛说的好像是python2.7管用
# for col in columns:
#     treeview.heading(col, text=col, command=lambda: treeview_sort_column(treeview, col, False))
# '''
#
# '''
# #基本用法（上边注释的只有最后一列管用、索性手工试验一下可用性，证实可行）
# treeview.heading('a', text='123', command=lambda: treeview_sort_column(tree, 'a', False))#重建标题，添加控件排序方法
# treeview.heading('b', text='111', command=lambda: treeview_sort_column(tree, 'b', False))#重建标题，添加控件排序方法
# treeview.heading('c', text='223', command=lambda: treeview_sort_column(tree, 'c', False))#重建标题，添加控件排序方法
# '''
#
# # 这个代码对于python3就管用了
# for col in columns:  # 给所有标题加（循环上边的“手工”）
#     treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))
#
# root.mainloop()  # 进入消息循环


from tkinter import *
from tkinter.ttk import *

root = Tk()

tree1 = Treeview(root, columns=('qy', 'dz'))
# 创建树表格组件，栏目有3个：#0, qy, dz

tree1.column('#0', width=90, anchor=CENTER, stretch=False)
tree1.column('qy', width=90, anchor=CENTER)
tree1.column('dz', width=160, anchor=CENTER)
# 定义3个栏目的宽度，对齐方法，宽度是否窗体变化

tree1.heading('#0', text='')
tree1.heading('qy', text='区域')
tree1.heading('dz', text='地址')
# 定义3个栏目的表头文字

sf1 = tree1.insert('', END, text='广东', open=True)
sf2 = tree1.insert('', END, text='湖南', open=True)
# 在根节点‘’下添加2个子节点：广东，湖南

tree1.insert(sf1, END, text='广州市', values=('海珠区', '阅江中路380号'))
tree1.insert(sf1, END, text='深圳市', values=('南山区', '华侨城侨香路11号'))
tree1.insert(sf1, END, text='东莞市', values=('南城区', '元美东路3号济亨网'))
# 在广州（sf1）节点下，插入3条记录：#0栏 = text,其它栏 = values()

tree1.insert(sf2, END, text='长沙市', values=('雨花区', '韶山中路108号'))
tree1.insert(sf2, END, text='湘潭市', values=('岳塘区', '书院路42号云峰工作室'))
tree1.insert(sf2, END, text='衡阳市', values=('蒸湘区', '祝融路名都花园B9栋107室'))
# 在湖南（sf2）节点下，插入3条记录：#0栏 = text,其它栏 = values()

tree1.insert(sf2, END, text='长沙市', values=('岳麓区', '梅溪湖路复兴小区709号'))
tree1.insert(sf1, END, text='广州市', values=('白云区', '下塘西路545号'))
# 以同样方法插入2条记录，它们会根据父节点找到自己的位置

tree1.pack(fill=BOTH, expand=True)

root.mainloop()