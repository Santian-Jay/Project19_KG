from tkinter import *
import requests

window = Tk()
window.geometry('1000x600+300+100')
window.title('数据采集')

frame = Frame(window)
frame.pack()

Label(frame, text='请输入网站地址：', font=('黑体', 12)).pack()

var = StringVar()
var.set('https://www.cnblogs.com/zhangyh-blog/p/15940602.html')

address = Entry(frame, width=70, textvariable=var)
address.pack(pady=5)

# 创建一个滚动条
scroll_bar = Scrollbar(frame)
scroll_bar.pack(side=RIGHT, fill=Y)

txt = Text(frame, width=120, height=30)
txt.config(yscrollcommand=scroll_bar.set)  # 在Text组件中使用这个滚动条
txt.pack()
scroll_bar.config(command=txt.yview)  # 让这个滚动条发挥作用


def submit():
    addr = address.get()
    res = requests.get(addr).text
    global txt
    txt.insert(INSERT, res)


def delete():
    global txt
    data = txt.get(1.0, END)

    if len(data) > 1:
        r = messagebox.askokcancel('提示', '确定要清空全部数据吗？')
        if r == True:
            txt.delete(1.0, END)
        else:
            pass
    else:
        messagebox.showwarning('提示', '数据为空，无需清空')


Button(frame, text='开始获取', command=submit).pack()
Button(frame, text='清空数据', command=delete).pack()

from tkinter import messagebox


def save():
    global txt
    result = txt.get(1.0, END)
    with open('result.html', 'w', encoding='utf-8') as f:
        f.write(result)
    messagebox.showinfo('提示', '已经将结果保存为 “result.html”文件，请前往查看')


Button(frame, text='保存', command=save).pack()

window.mainloop()
