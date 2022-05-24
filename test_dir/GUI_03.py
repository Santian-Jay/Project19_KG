#辞职信
import tkinter as tk
from PIL import Image
from tkinter import messagebox
from random import random

root = tk.Tk()
root.geometry('600x300+100+100')
root.title('Resign')

frame1 = tk.Frame(root)   #frame1 可以看做是本子的第一页
frame1.pack()             #显示第一页

tk.Label(frame1, text='尊敬的各位领导：', font=24, padx=30, pady=30).pack(side=tk.LEFT, anchor=tk.N)

img = tk.PhotoImage(file='../image/gaoci.png')
label_img = tk.Label(frame1, image=img, pady=30, padx=30, bd=0)
label_img.pack(side=tk.LEFT, anchor=tk.N)

tk.Label(frame1, text='辞职人：小星星', height=25, font=24, padx=30, pady=30, anchor=tk.S).pack(side=tk.LEFT)

#yes_img = tk.PhotoImage(file='image/yes01.png')
#no_img = tk.PhotoImage(file='image/no.png')

yes_button = tk.Button(frame1, text='yes',font=40, bd=0)
no_button = tk.Button(frame1, text='no',font=40, bd=0)


yes_button.place(relx=0.3, rely=0.8, anchor=tk.CENTER)
no_button.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

frame2 = tk.Frame(root)
frame2.pack()
tk.Label(frame2, text='老板大人，臣告退了\n这一退，可能就是一辈子了\n!!!! ^_^ !!!',
         font=('black', 18),
         justify=tk.LEFT,
         height=300,
         fg='red',
         padx=50
         ).pack()

tk.Button(frame2, text='exit', font=30, command=root.quit).place(relx=0.9, rely=0.8)
# tk.Button(frame2, text="later", font=30, command=root.quit).place(relx=0.4, rely=0.8)

back_button = tk.Button(frame2, text="later", font=40, bd=0)
back_button.place(relx=0.4, rely=0.8)

def on_exit():
    messagebox.showwarning(title='Notification', message='此路不通')

#不允许直接关闭窗口
root.protocol('WM_DELETE_WINDOW', on_exit)

#随机移动
def move(event):
    no_button.place(relx=random(), rely=random(), anchor=tk.CENTER)

no_button.bind('<Enter>', move)


# yes按钮
def sure():
    frame1.pack_forget()   #关闭第一个页面
    frame2.pack()          #开启第二个页面


# back to first screen
def back2main():
    frame2.pack_forget()
    frame1.pack()

yes_button.config(command=sure)
back_button.config(command=back2main)

root.mainloop()