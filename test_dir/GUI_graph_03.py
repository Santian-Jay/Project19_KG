import glob
import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import networkx as nx
import matplotlib.pyplot as plt

root = tk.Tk()   #创建tk主窗口
root.title("在tkinter中显示matplotlib")

frame1 = tk.Frame(root)   #frame1 可以看做是本子的第一页
frame1.pack()             #显示第一页

img = tk.PhotoImage(file='../image/Figure_1.png')

label_img = tk.Label(frame1, image=img, pady=30, padx=30, bd=0)
label_img.pack(side=tk.LEFT, anchor=tk.N)

tk.Label(frame1, text='辞职人：小星星', height=25, font=24, padx=30, pady=30, anchor=tk.S).pack(side=tk.LEFT)


# root = tk.Tk()
#
# # Typical matplotlib code
#
# f = Figure(figsize = (4,3), dpi = 100)
#
# a = f.add_subplot(111)
#
# a.plot([1,2,4,3,5,7,6,7,8,8,9,6,7,8,7,5,6,4,3,4,3,2,1])
#
# canvas = FigureCanvasTkAgg(f, root)
#
# canvas.draw()
#
# canvas.get_tk_widget().pack()
#
# canvas._tkcanvas.pack()



root.mainloop()


