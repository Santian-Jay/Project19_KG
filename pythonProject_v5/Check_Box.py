from tkinter import *
import tkinter.font as tkFont
class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], all_buttons=[], v=[], side=TOP, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            f0 = tkFont.Font(family='microsoft yahei', size=12)
            # var = StringVar()
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var, font=f0, onvalue=1, offvalue=0)
            all_buttons.append(chk)
            chk.pack(side=side, anchor=anchor, expand=True)
            self.vars.append(var)
            v.append(IntVar())
    def state(self):
        return map((lambda var: var.get()), self.vars)
    
    # def change_state(self, all_buttons=None):
    #     for b in all_buttons:
    #         b.select()