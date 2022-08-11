from tkinter import ttk, messagebox, Toplevel
from tkinter import *
import tkinter.font as tkFont

# 导入模块
from tkinter import *
from tkinter import messagebox
# import time
# 定义全局变量
sizeX = 0.38
sizeY = 0.15
high = 30
wide = 100
tip = "提示"
temp = False
key = ["姓名:", "电话号码:", "住址:", "E-mail："]


# 返回功能的实现
def back(name):
    # 弹窗
    name.attributes('-topmost', True)           # 让窗口置顶，因为不写这一句的话，弹窗出来，主界面就会覆盖当前查看的窗口
    bk = messagebox.askokcancel(tip, "您确定要返回吗？")
    if bk is True:
        name.withdraw()     # 隐藏窗口


# 新建窗口，括号内为标题，返回窗口的名称变量
def tl(title):
    name = Toplevel()
    name.title(title)
    name.geometry("450x600")
    return name


# 这些增删改查函数，格式都为：先定义局部函数，然后写界面。（但是执行顺序是反着来的）
def add():
    # 添加数据函数
    def add_info():
        if sv_name.get() == '' or sv_tel.get() == '' or sv_addr.get() == '' or sv_mail.get() == '':
            messagebox.showerror(tip, "信息必须全部填上！")
        else:
            name = str.isdigit(sv_name.get())
            tel1 = str.isdigit(sv_tel.get())
            tel2 = str(sv_tel.get())
            tel3 = str(sv_tel.get())[0]
            tel4 = not tel1 or not len(tel2) == 11 or not tel3 == '1'
            mail = str(sv_mail.get())

            if name:
                add_top.attributes('-topmost', True)
                messagebox.showerror(tip, "人名不应该是纯数字，如果您需要，请输入大写数字！")
            else:
                if tel4:
                    add_top.attributes('-topmost', True)
                    messagebox.showerror(tip, "手机号码应该为纯阿拉伯数字，且开头应为1，长度为11位!")
                else:
                    if not mail.find('@') or not mail.endswith('.com'):
                        add_top.attributes('-topmost', True)
                        messagebox.showerror(tip, "请仔细检查邮箱格式！(例如是否有@、.com)")
                    else:
                        add_top.attributes('-topmost', True)
                        ma = messagebox.askokcancel(tip, "您确认添加该联系人吗？")
                        if ma is True:
                            # 对文件内容的添加
                            with open("D:\\Learn\\txl.txt", "a") as f1:
                                f1.write(sv_name.get())
                                f1.write(",")
                                f1.write(sv_tel.get())
                                f1.write(",")
                                f1.write(sv_addr.get())
                                f1.write(",")
                                f1.write(sv_mail.get())
                                f1.write("\n")
                                f1.close()
                            try:
                                add_top.attributes('-topmost', True)
                                messagebox.showinfo(tip, "添加成功！")
                            finally:
                                add_top.withdraw()
    # 不能使用两次Tk（）去创建窗体，因为tkinter中只能有一个主线程，
    # 当需要再次创建一个窗体时，请使用Toplevel()
    add_top = tl("添加联系人")
    # 选择按钮
    back_button = Button(add_top, text="返  回", bg="lightyellow", command=lambda: back(add_top))
    back_button.grid(row=0, column=0)
    back_button = Button(add_top, text="确  定", bg="lightyellow", command=lambda: add_info())
    back_button.grid(row=0, column=1)
    # 标题
    Label(add_top, text="添加联系人", font=("", 16)).place(relx=sizeX*1.2, rely=sizeY*0.3)
    # 文本输入框
    sv_name = StringVar()
    sv_tel = StringVar()
    sv_addr = StringVar()
    sv_mail = StringVar()
    Label(add_top, text=key[0]).place(relx=sizeX-0.1, rely=sizeY)
    Entry(add_top, textvariable=sv_name).place(relx=sizeX, rely=sizeY, width=wide*2)

    Label(add_top, text=key[1]).place(relx=sizeX - 0.15, rely=sizeY*2)
    Entry(add_top, textvariable=sv_tel).place(relx=sizeX, rely=sizeY*2, width=wide*2)

    Label(add_top, text=key[2]).place(relx=sizeX - 0.1, rely=sizeY*3)
    Entry(add_top, textvariable=sv_addr).place(relx=sizeX, rely=sizeY*3, width=wide*2)

    Label(add_top, text=key[3]).place(relx=sizeX - 0.13, rely=sizeY*4)
    Entry(add_top, textvariable=sv_mail).place(relx=sizeX, rely=sizeY*4, width=wide*2)


def find():
    # 查找数据函数
    def find_info():
        fn = sv_fn.get()

        if fn == '':
            messagebox.showerror(tip, "姓名不能为空！")
        else:
            global temp
            with open("D:\\Learn\\txl.txt", "r") as f2:
                one_info = f2.readline()
                while one_info:
                    oi = one_info.split(',')  # 将每个人的数据，里边的逗号分割一下，这样在下边调用就会方便
                    if str(fn) == oi[0]:              # 判断当前行第一个数据是否为这个名字
                        Label(find_top, text=key[0]+oi[0]).place(relx=sizeX - 0.1, rely=sizeY)
                        Label(find_top, text=key[1]+oi[1]).place(relx=sizeX - 0.15, rely=sizeY * 2)
                        Label(find_top, text=key[2]+oi[2]).place(relx=sizeX - 0.1, rely=sizeY * 3)
                        Label(find_top, text=key[3]+oi[3]).place(relx=sizeX - 0.13, rely=sizeY * 4)
                        try:
                            find_top.attributes('-topmost', True)
                            messagebox.showinfo(tip, "成功查找到！")
                        finally:
                            temp = True
                            break
                    else:
                        one_info = f2.readline()
                f2.close()

            if not temp:
                messagebox.showerror(tip, "没有该联系人！")
                find_top.withdraw()
    # 界面
    find_top = tl("查找联系人")
    # 选择按钮
    back_button = Button(find_top, text="返  回", bg="lightyellow", command=lambda: back(find_top))
    back_button.grid(row=0, column=0)
    back_button = Button(find_top, text="确  定", bg="lightyellow", command=lambda: find_info())
    back_button.grid(row=0, column=1)
    # 标题
    Label(find_top, text="查找联系人", font=("", 16)).place(relx=sizeX*1.2, rely=sizeY*0.3)
    # 文本输入框
    sv_fn = StringVar()
    Label(find_top, text=key[0]).place(relx=sizeX-0.1, rely=sizeY*0.6)
    e_fn = Entry(find_top, textvariable=sv_fn)
    e_fn.place(relx=sizeX, rely=sizeY*0.6, width=wide*2)


def revise():
    def revise_info():
        def writefile():
            data = ''
            with open("D:\\Learn\\txl.txt", 'r') as f4:
                all_info = f4.readlines()
                f4.close()
            for line in all_info:
                if rn in line:
                    line = line.replace(oi[0], str(v_n.get()))
                    line = line.replace(oi[1], str(v_t.get()))
                    line = line.replace(oi[2], str(v_a.get()))
                    line = line.replace(oi[3], str(v_e.get()) + '\n')
                data += line
            with open("D:\\Learn\\txl.txt", 'w+') as f5:
                f5.write(data)
                f5.close()
            messagebox.showinfo(tip, "修改成功！")
            revise_top.withdraw()
        rn = sv_rn.get()
        if rn == '':
            messagebox.showerror(tip, "姓名不能为空！")
        else:
            global temp
            with open("D:\\Learn\\txl.txt", 'r') as f3:
                one_info = f3.readline()
                while one_info:
                    oi = one_info.split(',')
                    if str(rn) == oi[0]:
                        Label(revise_top, text=key[0]+ oi[0]).place(relx=sizeX - 0.1, rely=sizeY)
                        Label(revise_top, text=key[1] + oi[1]).place(relx=sizeX - 0.15, rely=sizeY * 2)
                        Label(revise_top, text=key[2] + oi[2]).place(relx=sizeX - 0.1, rely=sizeY * 3)
                        Label(revise_top, text=key[3] + oi[3]).place(relx=sizeX - 0.13, rely=sizeY * 4)
                        v_n = StringVar()
                        v_t = StringVar()
                        v_a = StringVar()
                        v_e = StringVar()
                        Entry(revise_top, textvariable=v_n).place(relx=sizeX, rely=sizeY+0.05)
                        Entry(revise_top, textvariable=v_t).place(relx=sizeX, rely=sizeY*2+0.05)
                        Entry(revise_top, textvariable=v_a).place(relx=sizeX, rely=sizeY*3+0.05)
                        Entry(revise_top, textvariable=v_e).place(relx=sizeX, rely=sizeY*4+0.05)
                        try:
                            Button(revise_top, text="修改", command=lambda: writefile()).grid(row=1, column=2)
                            temp = True
                            f3.close()
                        finally:
                            break
                    else:
                        one_info = f3.readline()
                f3.close()
        if not temp:
            messagebox.showerror(tip, "没有该联系人！")
    # 界面
    revise_top = tl("修改联系人")
    # 选择按钮
    back_button = Button(revise_top, text="返  回", bg="lightyellow", command=lambda: back(revise_top))
    back_button.grid(row=0, column=0)
    back_button = Button(revise_top, text="确  定", bg="lightyellow", command=lambda: revise_info())
    back_button.grid(row=0, column=1)

    # 标题
    Label(revise_top, text="修改联系人", font=("", 16)).place(relx=sizeX*1.2, rely=sizeY*0.3)
    # 文本输入框
    sv_rn = StringVar()
    Label(revise_top, text=key[0]).place(relx=sizeX-0.1, rely=sizeY*0.6)
    e_fn = Entry(revise_top, textvariable=sv_rn)
    e_fn.place(relx=sizeX, rely=sizeY*0.6, width=wide*2)


def delete():
    def del_info():
        dn = sv_dn.get()
        if dn == '':
            messagebox.showerror(tip, "姓名不能为空！")
        else:
            ma = messagebox.askokcancel(tip, "确定删除该联系人吗？")
            if ma:
                global temp
                with open("D:\\Learn\\txl.txt", 'r') as f6:
                    one_info = f6.readline()
                    while one_info:
                        oi = one_info.split(',')
                        if str(dn) == oi[0]:
                            data = ''
                            with open("D:\\Learn\\txl.txt", 'r') as f7:
                                all_info = f7.readlines()
                                f7.close()
                            for line in all_info:
                                if dn in line:
                                    line = line.replace(one_info[0:len(one_info)], '')
                                data += line
                            with open("D:\\Learn\\txl.txt", 'w+') as f8:
                                f8.write(data)
                                f8.close()
                            messagebox.showinfo(tip, '删除成功！')
                            del_top.withdraw()
                            break
                        else:
                            one_info = f6.readline()
                    f6.close()
                if not temp:
                    messagebox.showerror(tip, '没有该联系人，无法删除！')

    # 界面
    del_top = tl("删除联系人")
    # 选择按钮
    back_button = Button(del_top, text="返  回", bg="lightyellow", command=lambda: back(del_top))
    back_button.grid(row=0, column=0)
    back_button = Button(del_top, text="确  定", bg="lightyellow", command=lambda: del_info())
    back_button.grid(row=0, column=2)

    # 标题
    Label(del_top, text="删除联系人", font=("", 16)).place(relx=sizeX*1.2, rely=sizeY*0.3)
    # 文本输入框
    sv_dn = StringVar()
    Label(del_top, text=key[0]).place(relx=sizeX-0.1, rely=sizeY*0.6)
    e_fn = Entry(del_top, textvariable=sv_dn)
    e_fn.place(relx=sizeX, rely=sizeY*0.6, width=wide*2)


def look_all():
    # 界面
    look_top = tl("查看所有联系人")
    # 选择按钮
    back_button = Button(look_top, text="返  回", command=lambda: back(look_top))
    back_button.pack(anchor=NW)
    # 标题
    Label(look_top, text="查看所有联系人", font=("", 16)).pack(side=TOP, fill=X)
    # 滚动条、列表
    frame = Frame(look_top)
    frame.pack(pady=8)
    num_k = Frame(look_top)
    num_k.pack(pady=8, side=LEFT)
    num_label = Label(num_k, text='【现没有联系人！】')
    num_label.pack()
    lb = Listbox(frame, font=("", 16), height=20, width=30, borderwidth=0)
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.config(command=lb.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    lb.config(yscrollcommand=scrollbar.set, activestyle='none')
    scrollbar2 = Scrollbar(frame, orient=HORIZONTAL)
    scrollbar2.config(command=lb.xview)
    scrollbar2.pack(side=BOTTOM, fill=X)
    lb.config(xscrollcommand=scrollbar2.set, activestyle='none')
    lb.pack(fill=BOTH)
    # 联系人数据
    with open("D:\\Learn\\txl.txt", 'r') as f8:
        one_info = f8.readline()
        while one_info:
            i = 0
            oi = one_info.split(',')
            contacts = [oi[0], oi[1], oi[2], oi[3]]
            for item in contacts:
                lb.insert(END, key[i] + item)
                i += 1
            lb.insert(END, "\n")
            one_info = f8.readline()
        f8.close()
    if len(contacts) != 0:
        num_label.config(text='【现共有 %d 位联系人！】' % (len(contacts)+1))


class MainGUI:
    def __init__(self, root_name):
        self.root_name = root_name

        self.root_name.title("个人通讯录")           # 窗口名
        self.root_name.geometry("450x600")

    def main(self):
        # 按钮                                                                           # ↓调用内部方法，加()为直接调用
        self.add_button = Button(self.root_name, text="添 加 联 系 人", command=lambda: add())
        self.add_button.place(relx=sizeX, rely=sizeY, height=high, width=wide)
        self.find_button = Button(self.root_name, text="查 找 联 系 人", command=lambda: find())
        self.find_button.place(relx=sizeX, rely=sizeY*2, height=high, width=wide)
        self.add_button = Button(self.root_name, text="修 改 联 系 人", command=lambda: revise())
        self.add_button.place(relx=sizeX, rely=sizeY*3, height=high, width=wide)
        self.del_button = Button(self.root_name, text="删 除 联 系 人", command=lambda: delete())
        self.del_button.place(relx=sizeX, rely=sizeY*4, height=high, width=wide)
        self.look_button = Button(self.root_name, text="查 看 所 有 联 系 人", command=lambda: look_all())
        self.look_button.place(relx=sizeX*0.85, rely=sizeY*5, height=high, width=wide*1.5)

    # def get_current_time(self):
    #     current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    #     self.root_name.after(100, self.get_current_time)
    #     # 标签
    #     self.current_time_label = Label(self.root_name, text=current_time, bg="yellow")
    #     self.current_time_label.place(relx=sizeX*0.4, rely=0, height=high, width=wide*3)


def gui_start():
    root = Tk()
    book = MainGUI(root)
    book.main()
    # book.get_current_time()
    root.mainloop()


gui_start()