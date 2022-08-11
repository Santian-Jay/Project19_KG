from tkinter import *
class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=TOP, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            # var = StringVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=True)
            self.vars.append(var)
    def state(self):
        return map((lambda var: var.get()), self.vars)

if __name__=='__main__':
    root = Tk()
    lng = Checkbar(root, ['Python', 'Ruby', 'Perl', 'C++'])
    tgl = Checkbar(root, ['Chinese', 'English'])
    lng.pack(side=TOP, fill='x')
    tgl.pack(side=LEFT)
    lng.config(relief=GROOVE, bd=2)

    def allstates():
        print(list(lng.state()), list(tgl.state()))

    Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
    Button(root, text='Peek', command=allstates).pack(side=RIGHT)
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