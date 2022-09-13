# from tkinter import *
#
# win = Tk()
# win.geometry('500x500+500+100')
# canvas = Canvas(win)
# canvas.pack(fill=BOTH, expand=True)
# # 画实线,填充橙色,宽度为10
# line = canvas.create_line(150, 100, 150, 200, fill='orange', width=10)
#
#
# def event():
#     # 使用 itemcget 来获取组件的属性
#     fill = canvas.itemcget(line, 'fill')
#     print(fill)
#     width = canvas.itemcget(line, 'width')
#     print(width)
#
#
# btn = Button(win, text='点击获取实线属性', command=event)
#
# canvas.create_window((100, 50), window=btn)
# win.mainloop()

# from tkinter import *
#
# win = Tk()
# win.geometry('500x500+500+100')
# canvas = Canvas(win)
# canvas.pack(fill=BOTH, expand=True)
# # 画实线,填充橙色,宽度为10
# line = canvas.create_line(150, 100, 150, 200, fill='orange', width=10)
#
#
# def move_line():
#     # 使用 coords 来重新设置组件的位置
#     canvas.coords(line, 200, 100, 200, 200)
#
#
# btn = Button(win, text='点击移动实线', command=move_line)
# # 使用 itemconfig 来重新设置组件的属性
# btn1 = Button(win, text='点击切换实线填充颜色', command=lambda: canvas.itemconfig(line, fill='pink'))
# canvas.create_window((100, 50), window=btn)
# canvas.create_window((300, 50), window=btn1)
# win.mainloop()

# from tkinter import *
#
# win = Tk()
# win.geometry('500x500+500+100')
# canvas = Canvas(win)
# canvas.pack(fill=BOTH, expand=True)
# # 画实线,填充橙色,宽度为10
# line = canvas.create_line(150, 100, 150, 200, fill='orange', width=10)
#
#
# def move_line():
#     # 使用 coords 来重新设置组件的位置
#     canvas.coords(line, 200, 100, 200, 200)
#
#
# btn = Button(win, text='点击移动实线', command=move_line)
# # 使用 move 移动组件,参数表示沿XY轴移动的距离
# btn1 = Button(win, text='点击移动实线2', command=lambda: canvas.move(line, 10, 0))
# canvas.create_window((100, 50), window=btn)
# canvas.create_window((300, 50), window=btn1)
# win.mainloop()


from tkinter import *
from PIL import Image, ImageTk

root = Tk()

images = []  # to hold the newly created image

def create_rectangle(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=images[-1], anchor='nw')
    canvas.create_line(x1, y1, x2, y2, **kwargs)

canvas = Canvas(width=300, height=200)
canvas.pack()

create_rectangle(10, 10, 200, 100, fill='blue')
create_rectangle(50, 50, 250, 150, fill='green', alpha=.5)
create_rectangle(80, 80, 150, 120, fill='#800000', alpha=.8)

root.mainloop()