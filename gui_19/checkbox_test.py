from tkinter import *
class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=TOP, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            # var = StringVar()
            chk = Checkbutton(self, text=pick, variable=var)
            all_buttons.append(chk)
            chk.pack(side=side, anchor=anchor, expand=True)
            self.vars.append(var)
            v.append(IntVar())
    def state(self):
        return map((lambda var: var.get()), self.vars)
    def change_state(self):
        for b in all_buttons:
            b.select()

def all_change(event):
    if v[-1].get():
        for b in all_buttons:
            b.deselect()
    else:
        for b in all_buttons:
            b.select()


if __name__=='__main__':
    root = Tk()
    root.geometry('400x400')
    all_buttons = []
    v = []
    lng = Checkbar(root, ['Python', 'Ruby', 'Perl', 'C++'])
    # tgl = Checkbar(root, ['Chinese', 'English'])
    lng.pack(side=TOP, fill='x')
    # tgl.pack(side=LEFT)
    lng.config(relief=GROOVE, bd=2)
    v.append(IntVar())
    all = Checkbutton(root, text='select all', variable=v[-1], onvalue=1, offvalue=0)
    all.pack()
    all.bind("<Button>", all_change)
    def allstates():
        # print(list(lng.state()), list(tgl.state()))
        print(list(lng.state()))
    def change_all_state():
        lng.change_state()
    #     for button in lng:
    #         button.select()

    Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
    Button(root, text='Peek', command=allstates).pack(side=RIGHT)
    Button(root, text='Select All', command=change_all_state).pack(side=RIGHT)
    root.mainloop()


# import sys
# if sys.version_info.major == 3:
#     import tkinter as tk
# elif sys.version_info.major == 2:
#     import Tkinter as tk
# import random
# class DemoApplication(tk.Frame):
#     def on_checkbox_changed(self):
#         if self.check_box_var1.get()==1 and self.check_box_var2.get()==1:
#             main_win.title(u"都被选中了")
#         elif self.check_box_var1.get():
#             main_win.title(u"C 被选中了")
#         elif self.check_box_var2.get():
#             main_win.title(u"Python 被选中了")
#         else:
#             main_win.title(u"都没有被选中")
#     def createWidgets(self):
#         self.check_box_var1 = tk.IntVar()
#         self.check_box_var2 = tk.IntVar()
#         # 创建一个多选框
#         self.check_box1 = tk.Checkbutton(main_win, text=u'C', variable = self.check_box_var1, onvalue = 1, offvalue = 0, command=self.on_checkbox_changed)
#         self.check_box1.pack()
#         # 创建一个多选框
#         self.check_box2 = tk.Checkbutton(main_win, text=u'Python', variable = self.check_box_var2, onvalue = 1, offvalue = 0, command=self.on_checkbox_changed)
#         self.check_box2.pack()
# def __init__(self, master=None):
#     tk.Frame.__init__(self, master)
#     self.createWidgets()
#     main_win = tk.Tk()
#     main_win.title(u"多选框演示")
#     main_win.geometry("300x100")
#     app = DemoApplication(master=main_win)
#     app.mainloop()

# from tkinter import *
#
#
# def create_cbuts():
#     for index, item in enumerate(cbuts_text):
#         cbuts.append(Checkbutton(root, text=item, variable=IntVar()))
#         cbuts[index].pack()
#
#
# def select_all():
#     for i in cbuts:
#         i.select()
#
#
# def deselect_all():
#     for i in cbuts:
#         i.deselect()
#
#
# def all_state():
#     state = []
#     for i in cbuts:
#         # return map((lambda s:i.get()), state)
#         # state.append(if i.select: )
#         if i.select:
#             state.append(1)
#         else:
#             state.append(0)
#     print(state)
#
#
# root = Tk()
#
# cbuts_text = ['a', 'b', 'c', 'd']
# cbuts = []
# create_cbuts()
# Button(root, text='all', command=select_all).pack()
# Button(root, text='none', command=deselect_all).pack()
# Button(root, text='state', command=all_state).pack()
# mainloop()
