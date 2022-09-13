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
        print(i)
        if event.widget.id in dic[i]:
            cv.delete(i)
            deleted.append(i)
            # lines.remove(i)
            print("lines: ", lines)
    for j in deleted:
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
        if index == 0:
            dic[i][index].x = x
            dic[i][index].y = y
            j = cv.create_line(x, y, dic[i][1].x, dic[i][1].y, fill='red', tags="1", arrow=LAST)
            if x >= dic[i][1].x:
                target_x = (x - dic[i][1].x) / 2 + dic[i][1].x
            else:
                target_x = (dic[i][1].x - x) / 2 + x
            if y >= dic[i][1].y:
                target_y = (y - dic[i][1].y) / 2 + dic[i][1].y
            else:
                target_y = (dic[i][1].y - y) / 2 + y
            k = cv.create_text(target_x, target_y, text=dic[dic[i][2]], font=f3, anchor="nw")
            dic[k] = dic[dic[i][2]]
            print('delete: ', dic[i][2])
            del dic[dic[i][2]]
            print('deleted')
            dic[j] = [dic[i][index], dic[i][1], k]
            del dic[i]
            lines.append(j)
        elif index == 1:
            dic[i][index].x = x
            dic[i][index].y = y
            j = cv.create_line(dic[i][0].x, dic[i][0].y, x, y, fill='red', tags="1", arrow=LAST)
            if x >= dic[i][0].x:
                target_x = (x - dic[i][0].x) / 2 + dic[i][0].x
            else:
                target_x = (dic[i][0].x - x) / 2 + x
            if y >= dic[i][0].y:
                target_y = (y - dic[i][0].y) / 2 + dic[i][0].y
            else:
                target_y = (dic[i][0].y - y) / 2 + y
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
dic = {f_l:[notes1, notes2, r_1], f_2:[notes2, notes3, r_3], f_3:[notes1, notes3, r_2], r_1:'parent_of', r_2:'sub_of', r_3:'son_of'}
# dic = {f_l:[n1, n2, r_1], f_2:[n2, n3, r_3], f_3:[n1, n3, r_2], r_1:'parent_of', r_2:'sub_of', r_3:'son_of'}
print('dic: ', dic)