# import tkinter as tk
# import tkinter.ttk as ttk
# from tktooltip import ToolTip
#
#
# app = tk.Tk()
# b = ttk.Button(app, text="Button")
# b.pack()
# ToolTip(b, msg="Hover info", follow=True)   # True by default
# app.mainloop()

# import tkinter as tk
# from idlelib.tooltip import Hovertip
#
# app = tk.Tk()
# myBtn = tk.Button(app, text='?')
# myBtn.pack(pady=30)
# myTip = Hovertip(myBtn, 'This is \na multiline tooltip.')
# app.mainloop()

from tkinter import *
from tkinter.tix import *
root = Tk()
btn1 = Button(root, text="hello")
btn1.grid(row=0, column=0)
balloon = Balloon(root, bg="white", title="Help")
balloon.bind_widget(btn1, balloonmsg="Click to Exit")
root.mainloop()