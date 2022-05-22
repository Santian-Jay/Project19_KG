from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk

dbstr = "H:\mydb.db"

root = Tk()
root.geometry('700x1000')
root.title('学生管理系统')

Label(root, text="学号：").place(relx=0, rely=0.05, relwidth=0.1)
Label(root, text="姓名：").place(relx=0.5, rely=0.05, relwidth=0.1)
Label(root, text="电话：").place(relx=0, rely=0.1, relwidth=0.1)
Label(root, text="地址：").place(relx=0.5, rely=0.1, relwidth=0.1)

sid = StringVar()
name = StringVar()
phone = StringVar()
address = StringVar()
Entry(root, textvariable=sid).place(relx=0.1, rely=0.05, relwidth=0.37, height=25)
Entry(root, textvariable=name).place(relx=0.6, rely=0.05, relwidth=0.37, height=25)

Entry(root, textvariable=phone).place(relx=0.1, rely=0.1, relwidth=0.37, height=25)
Entry(root, textvariable=address).place(relx=0.6, rely=0.1, relwidth=0.37, height=25)

Label(root, text='学生信息管理', bg='white', fg='red', font=('宋体', 15)).pack(side=TOP, fill='x')


def showAllInfo():
    x = dataTreeview.get_children()
    for item in x:
        dataTreeview.delete(item)
    con = sqlite3.connect(dbstr)
    cur = con.cursor()
    cur.execute("select * from student")
    lst = cur.fetchall()
    for item in lst:
        dataTreeview.insert("", 1, text="line1", values=item)
    cur.close()
    con.close()


def appendInfo():
    if sid.get() == "":
        showerror(title='提示', message='输入不能为空')
    elif name.get() == "":
        showerror(title='提示', message='输入不能为空')
    elif phone.get() == "":
        showerror(title='提示', message='输入不能为空')
    elif address.get() == "":
        showerror(title='提示', message='输入不能为空')
    else:
        x = dataTreeview.get_children()
        for item in x:
            dataTreeview.delete(item)
        list1 = []
        list1.append(sid.get())
        list1.append(name.get())
        list1.append(phone.get())
        list1.append(address.get())
        con = sqlite3.connect(dbstr)
        cur = con.cursor()
        cur.execute("insert into student values(?,?,?,?)", tuple(list1))
        con.commit()
        cur.execute("select * from student")
        lst = cur.fetchall()
        for item in lst:
            dataTreeview.insert("", 1, text="line1", values=item)
        cur.close()
        con.close()


def deleteInfo():
    con = sqlite3.connect(dbstr)
    cur = con.cursor()
    cur.execute("select * from student")
    studentList = cur.fetchall()
    cur.close()
    con.close()
    print(studentList)

    num = sid.get()
    flag = 0
    if num.isnumeric() == False:
        showerror(title='提示', message='删除失败')
    for i in range(len(studentList)):
        for item in studentList[i]:
            if int(num) == item:
                flag = 1
                con = sqlite3.connect(dbstr)
                cur = con.cursor()
                cur.execute("delete from student where id = ?", (int(num),))
                con.commit()
                cur.close()
                con.close()
                break
    if flag == 1:
        showinfo(title='提示', message='删除成功！')
    else:
        showerror(title='提示', message='删除失败')

    x = dataTreeview.get_children()
    for item in x:
        dataTreeview.delete(item)

    con = sqlite3.connect(dbstr)
    cur = con.cursor()
    cur.execute("select * from student")
    lst = cur.fetchall()
    for item in lst:
        dataTreeview.insert("", 1, text="line1", values=item)
    cur.close()
    con.close()


Button(root, text="显示所有信息", command=showAllInfo).place(relx=0.2, rely=0.2, width=100)
Button(root, text="追加信息", command=appendInfo).place(relx=0.4, rely=0.2, width=100)
Button(root, text="删除信息", command=deleteInfo).place(relx=0.6, rely=0.2, width=100)

dataTreeview = ttk.Treeview(root, show='headings', column=('sid', 'name', 'phone', 'address'))
dataTreeview.column('sid', width=150, anchor="center")
dataTreeview.column('name', width=150, anchor="center")
dataTreeview.column('phone', width=150, anchor="center")
dataTreeview.column('address', width=150, anchor="center")

dataTreeview.heading('sid', text='学号')
dataTreeview.heading('name', text='名字')
dataTreeview.heading('phone', text='电话')
dataTreeview.heading('address', text='地址')

dataTreeview.place(rely=0.3, relwidth=0.97)

root.mainloop()
