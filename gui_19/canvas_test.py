# import tkinter as tk
# from tkinter import *
#
# root = tk.Tk()
# root.minsize(400, 200)
#
# root.rowconfigure(0, weight=1)
# root.columnconfigure(0, weight=1)
# frame1 = Frame(root, width=200, height=200)
# frame1.grid(row=0, column=0, sticky=NSEW)
#
# # frame1.rowconfigure(0, weight=1)
# # frame1.columnconfigure(0, weight=1)
# frame1.columnconfigure(1, weight=1)
#
# left = Label(frame1, text='left', bg='red')
# left.grid(row=0, column=0, sticky=NSEW)
# right = Label(frame1, text='right', bg='blue')
# right.grid(row=0, column=1, sticky=NSEW)
# b = Label(frame1, text='bottom', bg='green')
# b.grid(row=1, column=0, columnspan=2, sticky=NSEW)
# # root.geometry("800x600")
# # frame1 = Frame(root, width=200, height=200)
# # frame1.pack()
# # screenwidth = frame1.winfo_screenwidth()  # 屏幕宽度
# # screenheight = frame1.winfo_screenheight()  # 屏幕高度
# # cv = Canvas(root, height=screenheight, width=screenwidth, bg='green')
# # cv.pack()
# root.mainloop()
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont

class Canvas_Button:
    def __init__(self, canvas:Canvas, x1:int, y1:int, x2:int, y2:int, text:str, fontsize:int=15, d_outline:str='gray', d_fill:str='gray'):
        self.canvas = canvas
        self.value = text
        self.tag = text

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.d_outline = d_outline
        self.d_fill = d_fill
        # self.px = (x2 - x1) / 2 + x1
        # self.py = (y2 - y1) / 2 + y1

        self.rec = self.canvas.create_rectangle(x1, y1, x2, y2, width=2, outline=self.d_outline, tags=self.tag)
        self.text = self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=self.value, font=fontsize, justify='center', fill=self.d_fill, tags=self.tag)

    def focus_on(self, color:str):
        self.canvas.itemconfig(self.rec, fill=color)

    def focus_off(self):
        self.canvas.itemconfig(self.rec, fill='')

    def Focus(self,event:Event,color:str ):
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.focus_on(color)
        else:
            self.focus_off()

    def move_on(self, color:str):
        self.canvas.itemconfig(self.rec, outline=color)
        self.canvas.itemconfig(self.text, fill=color)

    def move_off(self):
        self.canvas.itemconfig(self.rec, outline=self.d_outline)
        self.canvas.itemconfig(self.text, fill=self.d_fill)

    def Move(self,event:Event,color:str):
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.move_on(color)
        else:
            self.move_off()

    def execute(self,event:Event, function=None):
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.focus_off()
            self.move_off()

            if function != None:
                return function()



# f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 200     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class Button_Canvas(tk.Button):
    # def __init__(self, cv, x1, y1, text, id, color=None, **kwargs):
    def __init__(self, cv, x1, y1, text, id, font=25, *args, **kwargs):
        super().__init__(cv, font=font)
        self.text = text
        self.id = id
        self.cv = cv
        self.x = x1
        self.y = y1

        self['text'] = self.text
        # self['id'] = self.id
        # self.cv.create_window(x1, y1, window=self)


def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)
    widget.bind("<ButtonRelease>", on_drag_end)

def on_drag_start(event):
    global lines, dic, deleted, texts
    deleted = []
    print("lines: ", lines)
    for i in lines:
        if event.widget.id in dic[i]:
            cv.delete(i)
            deleted.append(i)
            # lines.remove(i)
            print("lines: ", lines)
    for j in deleted:
        # cv.delete(dic[j][2])
        cv.delete(dic[j][2])
        lines.remove(j)
    # print('1 dic: ', dic)
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    # print('id: ', event.widget.id)

def on_drag_motion(event):
    global lines, dic, deleted, texts
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
    # cv.create_window(x, y, height=40, width=40, window=event.widget)


def on_drag_end(event):
    global f_l, dic, name_list, deleted, texts
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    for i in deleted:
        index = dic[i].index(event.widget.id)
        print('i', i)
        if index == 0:
            # dic[i][index].x = x
            # dic[i][index].y = y
            dic[dic[i][index]][0] = x
            dic[dic[i][index]][1] = y
            j = cv.create_line(x, y, dic[dic[i][1]][0], dic[dic[i][1]][1], fill='red', tags="1", arrow=LAST)
            if x >= dic[dic[i][1]][0]:
                target_x = (x - dic[dic[i][1]][0]) / 2 + dic[dic[i][1]][0]
            else:
                target_x = (dic[dic[i][1]][0] - x) / 2 + x
            if y >= dic[dic[i][1]][1]:
                target_y = (y - dic[dic[i][1]][1]) / 2 + dic[dic[i][1]][1]
            else:
                target_y = (dic[dic[i][1]][1] - y) / 2 + y
            k = cv.create_text(target_x, target_y, text=dic[dic[i][2]], font=f3, anchor="nw")
            dic[k] = dic[dic[i][2]]
            print('delete: ', dic[i][2])
            del dic[dic[i][2]]
            print('deleted')
            dic[j] = [dic[i][index], dic[i][1], k]
            del dic[i]
            lines.append(j)
        elif index == 1:
            dic[dic[i][1]][0] = x
            dic[dic[i][1]][1] = y
            j = cv.create_line(dic[dic[i][0]][0], dic[dic[i][0]][1], x, y, fill='red', tags="1", arrow=LAST)
            if x >= dic[dic[i][1]][0]:
                target_x = (x - dic[dic[i][0]][0]) / 2 + dic[dic[i][0]][0]
            else:
                target_x = (dic[dic[i][0]][0] - x) / 2 + x
            if y >= dic[dic[i][0]][1]:
                target_y = (y - dic[dic[i][0]][1]) / 2 + dic[dic[i][0]][1]
            else:
                target_y = (dic[dic[i][0]][1] - y) / 2 + y
            k = cv.create_text(target_x, target_y, text=dic[dic[i][2]], font=f3, anchor="nw")
            dic[k] = dic[dic[i][2]]
            print('delete: ', dic[i][2])
            del dic[dic[i][2]]
            print('deleted')
            dic[j] = [dic[i][0], dic[i][index], k]
            del dic[i]
            lines.append(j)
    print('lines: ', lines)
    print('dic: ', dic)


main = tk.Tk()
main.geometry("800x600")

f3 = tkFont.Font(family='microsoft yahei', size=15)
# cv = Canvas(main, height=800, width=600, bg='green')
cv = Canvas(main, bg='white')
cv.pack(fill=BOTH, expand=True)

notes1 = Button_Canvas(cv,320, 250, text='drag', id=1, font=f3)
notes1.pack()
# notes1_ttp = CreateToolTip(notes1, 'dragoooooooo')
# notes.bind("<ButtonRelease>",stopV)
notes2 = Button_Canvas(cv, 32, 20, text='drag1', id=2, font=f3)
notes2.pack()
# notes.bind("<ButtonRelease>",stopV)
notes3 = Button_Canvas(cv, 120, 250, text='drag3', id=3, font=f3)
notes3.pack()
# notes.bind("<ButtonRelease>",stopV)
# notes4 = Canvas_Button(cv, 10, 20, 100, 120,  text='drag4')
# notes4.pack()
# notes.bind("<ButtonRelease>",stopV)

make_draggable(notes1)
make_draggable(notes2)
make_draggable(notes3)
# make_draggable(notes4)

n1 = cv.create_window(320, 250, window=notes1)
n2 = cv.create_window(32, 20, window=notes2)
n3 = cv.create_window(120, 250,window=notes3)
# n4 = cv.create_window(120, 20, height=100, width=100, window=notes4)

buttons = []
buttons.append(notes1)
buttons.append(notes2)
buttons.append(notes3)

# cv.pack()
lines = []
f_l = cv.create_line(320, 250, 32, 20, fill='red', tags=("notes1", "notes2"), arrow=LAST)
f_2 = cv.create_line(32, 20, 120, 250, fill='red', tags=("notes2", "notes3"), arrow=LAST)
f_3 = cv.create_line(320, 250, 120, 250, fill='red', tags=("notes1", "notes3"), arrow=LAST)
# f_l = cv.create_line(120, 250, 120, 20, fill='red', tags=("3", "4"))
lines.append(f_l)
lines.append(f_2)
lines.append(f_3)

# r_1 = cv.create_text(320/2+30, 250/2, text='parent_of', font=f3, anchor="nw", angle=315)
r_1 = cv.create_text(320/2, 250/2, text='parent_of', font=f3, anchor="nw")
r_2 = cv.create_text(320/2+30, 230, text='sub_of', font=f3, anchor="nw")
r_3 = cv.create_text(120/2, 230/2, text='son_of', font=f3, anchor="nw")

texts = []
texts.append(r_1)
texts.append(r_2)
texts.append(r_3)

name_list = [0, n1, n2, n3]
# dic = {f_l:[notes1, notes2, r_1], f_2:[notes2, notes3, r_3], f_3:[notes1, notes3, r_2], r_1:'parent_of', r_2:'sub_of', r_3:'son_of'}
dic = {f_l:[n1, n2, r_1], f_2:[n2, n3, r_3], f_3:[n1, n3, r_2], r_1:'parent_of', r_2:'sub_of', r_3:'son_of', n1:[320, 250], n2:[32, 20], n3:[120, 250]}
print('dic: ', dic)
# print()
#
# for i in lines:
#     print(dic[i][0].x, dic[i][0].y)
#
# print('test: ', dic[5][2])
# d = dic[5][2]
# del d
# print('删除以后：', dic)
# dic = {}
# name_list = []
# for i in range(10):
#     temp_str = str(i) + '_line'
#     dic[temp_str] = ''
#     name_list.append(temp_str)
# print(dic)
# print(name_list)
# dic[name_list[0]] = (n1, n2)
# dic[name_list[1]] = (n3, n4)
# print(dic)
#
# print(f_l)
# print(f_2)

main.mainloop()



# import tkinter
#
# win = tkinter.Tk()
# win.title("鼠标拖动事件")
# win.geometry("800x600+600+100")
#
# #<B1-Motion> 拖动左键触发事件
# #<B2-Motion> 拖动中键触发事件
# #<B3-Motion> 拖动右键触发事件
#
# label=tkinter.Label(win,text="red orange yellow green cyan blue violet拖动鼠标打印")
# label.pack()
# def func(event):
#     print(event.x,event.y)
# label.bind("<B1-Motion>",func)
#
# win.mainloop()



# from tkinter import *
#
# win = Tk()
# win.geometry('500x500+500+100')
# canvas = Canvas(win)
# canvas.pack(fill=BOTH, expand=True)
# # 画实线,填充橙色
# canvas.create_line(100, 100, 100, 200, fill='red')
# # 画实线,填充橙色,设置宽度为10
# canvas.create_line(150, 100, 150, 200, fill='green', width=10)
# # 画虚线,填充橙色
# canvas.create_line(200, 100, 200, 200, fill='orange', dash=(2, 2))
# win.mainloop()


# from tkinter import *
# from tkinter import ttk
#
# def up(event):
#     print("up")
# def down(event):
#     print("down")
# def left(event):
#     print("left")
# def right(event):
#     print("right")
# def stopV(event):
#     print("stopV")
# def stopH(event):
#     print("stopH")
#
# root = Tk()
# root.title("Telescope Controller")
#
# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# mainframe.columnconfigure(0, weight=1)
# mainframe.rowconfigure(0, weight=1)
#
# Bup = ttk.Button(mainframe, text="Up")
# Bup.grid(column=2, row=1, sticky=(W, E))
# Bup.bind("<ButtonPress>",up)
# Bup.bind("<ButtonRelease>",stopV)
# Bdwn = ttk.Button(mainframe, text="Down")
# Bdwn.grid(column=2, row=3, sticky=W)
# Bdwn.bind("<ButtonPress>",down)
# Bdwn.bind("<ButtonRelease>",stopV)
# Bl = ttk.Button(mainframe, text="Left")
# Bl.grid(column=1, row=2, sticky=E)
# Bl.bind("<ButtonPress>",left)
# Bl.bind("<ButtonRelease>",stopH)
# Br = ttk.Button(mainframe, text="Right")
# Br.grid(column=3, row=2, sticky=W)
# Br.bind("<ButtonPress>",right)
# Br.bind("<ButtonRelease>",stopH)
#
# for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
#
# root.mainloop()


# from tkinter import *
#
#
# def event(w):
#     #  current 表示删除鼠标下的组件
#     canvas.delete('current')
#
#
# win = Tk()
# win.geometry('500x500+500+100')
# canvas = Canvas(win)
# canvas.pack(fill=BOTH, expand=True)
# # 画实线,填充橙色,设置宽度为10
# for i in range(10, 200, 20):
#     canvas.create_line(i, 100, i, 200, width=10, fill='orange')
# #  绑定鼠标左键点击事件
# canvas.bind('<Button-1>', event)
# win.mainloop()


# import tkinter as tk
# import tkinter.scrolledtext as scrolledtext
#
# from tkinter import *
#
#
# class MyButton(Button):
#     def __init__(self, parent=None, d_btns={}, *args, **kwargs):
#         Button.__init__(self, parent, *args, **kwargs)
#         self.parent = parent
#         self.dialog = None
#         self.d_btns = d_btns
#
#     def click(self):
#         print('button click:', self.dialog)
#         if not self.dialog:
#             self.dialog = MyDialog(self.parent, self.d_btns)
#         else:
#             self.dialog.show()
#
#
# class MyDialog(Toplevel):
#     def __init__(self, parent, d_btns={}, title='My Dialog'):
#         Toplevel.__init__(self, parent)
#
#         self.parent = parent
#         self.name = title
#         self.text_area = None
#         self.btns = []
#         self.text_size = (60, 20)
#         self.btn_size = (16, 1)
#
#         self.transient(parent)  # 去掉最大最小化按钮
#         self.title(title)
#
#         self.protocol("WM_DELETE_WINDOW", self.cancel)
#         if not d_btns:
#             d_btns = {'OK': self.ok, 'Cancel': self.cancel}
#         self.init_input_box(d_btns)
#
#     def ok(self):
#         print('ok')
#         self.cancel()
#
#     def cancel(self):
#         print('cancel')
#         self.withdraw()
#         self.parent.grab_set()
#
#     def init_input_box(self, d_btns):
#         w, h = self.text_size
#         # 初始化文本框
#         if self.text_area: self.text_area.destroy()
#         self.text_area = scrolledtext.ScrolledText(self, width=w, height=h)
#         self.text_area.grid(row=0, column=0, columnspan=len(d_btns), padx=10, pady=5)
#         self.text_area.focus()
#         w, h = self.btn_size
#         i = 0
#         for name, cmd in d_btns.items():
#             # 初始化按钮
#             btn = Button(self, text=name, width=w, height=h)
#             btn.grid(row=1, column=i, pady=5)
#             btn.configure(command=cmd)
#             self.btns.append(btn)
#             i += 1
#
#     def change_btn_names(self, btn_names):
#         for i, btn in enumerate(self.btns):
#             btn.configure(text=btn_names[i])
#
#     def bind_btn_cmds(self, btn_cmds):
#         for i, btn in enumerate(self.btns):
#             btn.configure(command=btn_cmds[i])
#
#     def hide(self):
#         self.update()
#         self.withdraw()
#         self.parent.grab_set()
#
#     def show(self):
#         print('dialog show:', self)
#         self.grab_set()
#         self.deiconify()
#         self.update()
#
#
# def cmd1():
#     print('111')
#
#
# def cmd2():
#     print('222')
#
#
# def cmd3(btn, names):
#     print('333')
#     btn.dialog.change_btn_names(names)
#
#
# def main_window():
#     window = Tk()
#
#     mbtn = MyButton(window, text='click me', width=10, height=1)
#     mbtn.configure(command=mbtn.click)
#     mbtn.grid(row=0, column=0)
#
#     d_pairs = {'a': cmd1, 'b': cmd2, 'c': lambda: cmd3(mbtn, ['x', 'y'])}
#     mbtn2 = MyButton(window, d_pairs, text='←click', width=10, height=1)
#     mbtn2.configure(command=mbtn2.click)
#     mbtn2.grid(row=0, column=1)
#
#     d_pairs = {'1': cmd1, '2': cmd2, '3': lambda: cmd3(mbtn, ['yy', 'xx']), '4': lambda: print(444)}
#     mbtn3 = MyButton(window, d_pairs, text='←click', width=10, height=1)
#     mbtn3.configure(command=mbtn3.click)
#     mbtn3.grid(row=0, column=2)
#     return window
#
#
# if __name__ == '__main__':
#     window = main_window()
#     window.mainloop()
