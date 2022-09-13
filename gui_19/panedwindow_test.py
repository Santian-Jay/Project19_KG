from tkinter import *
import ttkbootstrap
from ttkbootstrap import *
import pythonProject_v5.ttkbootstrap as ttk
from pythonProject_v5.ttkbootstrap.constants import *
from pythonProject_v5.ttkbootstrap import style
# from tkinter import ttk
def add():

    a = int(e1.get())

    b = int(e2.get())

    leftdata = str(a+b)

    left.insert(1,leftdata)

root = ttk.Window()

w1 = PanedWindow()

w1.pack(fill = BOTH, expand = 1)

left = Entry(w1, bd = 5)

w1.add(left)

w2 = PanedWindow(w1, orient = VERTICAL)

w1.add(w2)

e1 = Entry(w2)

e2 = Entry(w2)

w2.add(e1)

w2.add(e2)

bottom = Button(w2, text="Add", command=add)

w2.add(bottom)

mainloop()


# import tkinter as tk
# import ttkbootstrap
# import pythonProject_v5.ttkbootstrap as ttk
# from pythonProject_v5.ttkbootstrap.constants import *
# from pythonProject_v5.ttkbootstrap import style
#
# root = ttk.Window(themename="superhero")
#
# b1 = ttk.Button(root, text="Submit", bootstyle="success")
# b1.pack(side=LEFT, padx=5, pady=10)
#
# b2 = ttkbootstrap.ttk.Checkbutton(root, bootstyle="success")
# b2.pack(side=LEFT, padx=5, pady=10)
#
# root.mainloop()