import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import random
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
        if event.widget in dic[i]:
            cv.delete(i)
            deleted.append(i)
            print("lines: ", lines)
    for j in deleted:
        cv.delete(dic[j][2])
        lines.remove(j)

    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    print(event.widget.id)


def on_drag_motion(event):
    global lines, dic, deleted, texts
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)


def on_drag_end(event):
    global f_l, dic, name_list, deleted, texts
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    for i in deleted:
        index = dic[i].index(event.widget)
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


main = tk.Tk()
main.geometry("1600x1200+400+400")

f3 = tkFont.Font(family='microsoft yahei', size=15)
# cv = Canvas(main, height=800, width=600, bg='green')
cv = Canvas(main, bg='green')
cv.pack(fill=BOTH, expand=True)

dic = {}
position = []
lines = []
name_list = []
buttons = []
entity_list = ['Thyra', 'GunhildeOfWenden', 'SweynForkbeard', 'HaraldTheSecond', 'Harthacnut', 'GormTheOld']
# Thyra	4
# GunhildeOfWenden	5
# SweynForkbeard	6
# HaraldTheSecond	8
# Harthacnut	10
# GormTheOld	12


# GrandparentOf	4
# HusbandOf	5
# SuceededBy	6
# SucceededBy	7
# ParentOf	8
relation_list = ['GrandparentOf	', 'HusbandOf', 'HusbandOf', 'GrandparentOf', 'ParentOf', 'SucceededBy']

# f_l = cv.create_line(320, 250, 32, 20, fill='red', tags=("notes1", "notes2"), arrow=LAST)
# f_2 = cv.create_line(32, 20, 120, 250, fill='red', tags=("notes2", "notes3"), arrow=LAST)
# f_3 = cv.create_line(320, 250, 120, 250, fill='red', tags=("notes1", "notes3"), arrow=LAST)
temp = [(4, 6), (6, 5), (12, 4), (12, 6), (5, 8), (10, 12)]
for t in temp:
    for item in t:
        if item not in name_list:
            name_list.append(item)
name_list = sorted(name_list)
print('name list: ', name_list)  # name list:  [4, 6, 5, 12, 8, 10]

for i in range(10):
    x = random.randint(100, 1100)
    y = random.randint(60, 800)
    if (x, y) not in position:
        position.append((x, y))

for i in range(6):
    name = 'r_' + str(i)
    b = Button_Canvas(cv, position[i][0], position[i][1], text=entity_list[i], id=name_list[i], font=f3)
    b.pack()
    buttons.append(b)
    make_draggable(b)
    n1 = cv.create_window(position[i][0], position[i][1], window=b)
    # dic[n1] = [0]
# print('buttons: ',  buttons)
# for tuple in temp:
for i in range(len(temp)):
    tuple = temp[i]
    # for number1, number2 in tuple:
    index1 = name_list.index(tuple[0])
    index2 = name_list.index(tuple[1])

    if buttons[index1].x >= buttons[index2].x:
        target_x = (buttons[index1].x - buttons[index2].x) / 2 + buttons[index2].x
    else:
        target_x = (buttons[index2].x - buttons[index1].x) / 2 + buttons[index1].x
    if buttons[index1].y >= buttons[index2].y:
        target_y = (buttons[index1].y - buttons[index2].y) / 2 + buttons[index2].y
    else:
        target_y = (buttons[index2].y - buttons[index1].y) / 2 + buttons[index1].y

    l_1 = cv.create_line(buttons[index1].x, buttons[index1].y, buttons[index2].x, buttons[index2].y, fill='red', tags=(str(index1), str(index2)), arrow=LAST)
    lines.append(l_1)

    r_1 = cv.create_text(target_x, target_y, text=relation_list[i], font=f3, anchor="nw")   # fetch relation by tuple
    dic[l_1] = [buttons[index1], buttons[index2], r_1]
    dic[r_1] = relation_list[i]

print(dic)

main.mainloop()