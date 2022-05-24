import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import networkx as nx
import matplotlib.pyplot as plt

root = tk.Tk()   #创建tk主窗口
root.title("在tkinter中显示matplotlib")

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)  #添加子图，1行1列第一个
#
# #生成图的数据
# G = nx.Graph()  #无向图
#
# #添加节点
# G.add_nodes_from([1, 2, 3, 4])
# #添加边
# G.add_edges_from([(1,2), (1,3), (2,3), (2,4)])
#
# #可视化
# nx.draw(G, node_size=500, with_labels=True)


#将绘制的图显示到tk上：创建属于root的canvas的画布，并将图f置于画布上
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP,  #上对齐
                            fill=tk.BOTH,  #填充方式
                            expand=tk.YES)  #随窗口大小调整而调整

# #matplotlib的导航工具栏显示上来（默认不显示）
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas._tkcanvas.pack(side=tk.TOP,  #上对齐  #get_tk_widget()得到的就是——tkcanvas
#                       fill=tk.BOTH,  #填充方式
#                       expand=tk.YES)  #随窗口大小调整而调整)

def on_key_enent(event):
    """"键盘事件处理"""
    print("你按了%s" % event.key)
    #key_press_handler(event, canvas, toolbar)
    key_press_handler(event, canvas)

#绑定上面定义的键盘事件处理函数
canvas.mpl_connect('key_press_event', on_key_enent)

def _quit():
    """点击退出按钮时调用这个函数"""
    root.quit()   #主循环结束
    root.destroy()   #销毁窗口

#创建一个按钮，并把上面那个函数绑定过来
button = tk.Button(master=root, text="退出", command=_quit)
#按钮放在下边
button.pack(side=tk.BOTTOM)

#主循环
root.mainloop()