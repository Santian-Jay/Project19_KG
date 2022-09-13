import tkinter as tk
import tkinter.font as tkFont
class Entry_new(tk.Entry):
    def __init__(self, master, placeholder, **kw):
        super().__init__(master, **kw)
        f1 = tkFont.Font(family='microsoft yahei', size=15)
        self.placeholder = placeholder
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self._state = 'placeholder'
        self.insert(0, self.placeholder)

    def on_focus_in(self, event):
        # if self._state == 'placeholder':
        self._state = ''
        self.delete('0', 'end')

    def on_focus_out(self, event):
        if not self.get():
            self._state == 'placeholder'
            self.insert(0, self.placeholder)

# if __name__ == '__main__':
#     root = tk.Tk()
#     root.geometry("300x200+600+250")
#
#     username = Entry(root, "username")
#     username.pack()
#
#     password = Entry(root, "password")
#     password.pack()
#
#     root.mainloop()


