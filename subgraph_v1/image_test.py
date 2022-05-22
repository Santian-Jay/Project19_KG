import tkinter as tk

root = tk.Tk()
root.title('subgraph')
root.geometry('1920x1080')

frame1 = tk.Frame(root)
frame1.pack()

img = tk.PhotoImage(file='image/pic-1.png')
label_image = tk.Label(root, image=img, pady=30, padx=30, bd=0)
label_image.image = img
label_image.pack()

root.mainloop()