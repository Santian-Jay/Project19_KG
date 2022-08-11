from tkinter import *
root = Tk()
l1 = Label(root, text='pack_forget')
b3 = Button(root, text='button')

b1 = Button(root, text='Hide', command=b3.pack_forget)
b2 = Button(root, text='Show', command=b3.pack)

l1.pack(fill='x')
b1.pack(fill='x')
b2.pack(fill='x')
b3.pack()

root.mainloop()
