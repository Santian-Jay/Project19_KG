import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self.pack()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.select = tk.StringVar()
        root.geometry('250x145')
        #root.minsize()
        root.maxsize(650, 480)  #设置最大的可以手动缩放窗口
        root.title('Login')     #设置窗口title

        self.intWind()

    def button_active(self):
        u = self.username.get()
        p = self.password.get()

        if len(u) == 0 or len(p) == 0:
            messagebox.showinfo('ERROR', 'Please enter full information')
            return

        messagebox.showinfo('Notification', 'You entered account is: %s\npassword is: %s\nYour account type is %s'% (u, p, self.select.get()))

    def selector_linstener(self, *args):
        self.select.set(self.selector.get())

    def intWind(self):
        # Label(self, text='123', fg='red', bg='green', width=1).grid(row=0, column=0)   #pack()change to grid
        # Entry(self, textvariable=self.envar, fg='#000', bg='#ff0', width=5).grid(row=0, column=1)
        # text = Text(self, fg='#ff0', bg='#000', width=12)
        # text.grid(columnspan=2, rowspan=2, pady=15, padx=50, ipadx=50)  #pady y轴填充，padx x轴填充，ipadx 两个组件内部填充
        # text.insert('end', '123')
        # text.insert('end', '123')
        # text.insert('end', '123')
        frame1 = Frame(self)
        Label(frame1, text='Account:').grid(row=0, column=0)
        Entry(frame1, textvariable=self.username).grid(row=0, column=1)

        frame2 = Frame(self)
        Label(frame2, text='Password:').grid(row=0, column=0)
        Entry(frame2,show='*', textvariable=self.password).grid(row=0, column=1)

        frame3 = Frame(self)
        Label(frame3, text='Type').grid(row=0, column=0)
        self.selector = ttk.Combobox(frame3, values=('General User', 'Manager'), width=18)
        self.selector.grid(row=0, column=1)
        self.selector.current(0)
        self.selector.bind('<<ComboboxSelected>>', self.selector_linstener())

        frame3.grid(pady=6)
        frame1.grid(pady=10)
        frame2.grid(pady=6)

        Button(self, text='Login', width=15, command=self.button_active).grid(pady=5)
        # print(self.selector.cget('values'))
        # print(self.selector.cget('width'))

        # self.clipboard_append('jay')   #粘贴板
        # self.clipboard_clear()         #清空粘贴板


if __name__ == '__main__':
    root = tk.Tk()
    application = Application(root=root)
    application.mainloop()