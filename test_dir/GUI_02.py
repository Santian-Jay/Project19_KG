#图片查看器

import glob
import tkinter as tk
from PIL import Image, ImageTk


root = tk.Tk()
root.geometry('906x687+100+100')   #+100+100 表示距离上下间距为100
root.title('Photo Viewer')

photos = glob.glob('dataset/train/ants/*.jpg')
photos = [ImageTk.PhotoImage(Image.open(photo)) for photo in photos]


current_photo_no = 0
photo_label = tk.Label(root, image=photos[current_photo_no], width=900, height=600)
photo_label.pack()

total_n = len(photos)
first_n = 1

number_var = tk.StringVar()
number_var.set('1 of 122')
tk.Label(root, textvariable=number_var, bd=1, relief=tk.SUNKEN, anchor=tk.CENTER).pack(fill=tk.X)

button_frame = tk.Frame(root)
button_frame.pack()
prev_photo = tk.Button(button_frame, text='previous')
next_photo = tk.Button(button_frame, text='next')
prev_photo.pack(side=tk.LEFT, anchor=tk.CENTER)
next_photo.pack(side=tk.RIGHT, anchor=tk.CENTER)

def change_photos(num):
    global current_photo_no
    current_photo_no += num

    if current_photo_no >= total_n:
        current_photo_no = 0
    if current_photo_no < 0:
        current_photo_no = total_n - 1

    number_var.set(f'{current_photo_no + 1} of {total_n}')

    photo_label.configure(image=photos[current_photo_no])

prev_photo.config(command=lambda: change_photos(-1))
next_photo.config(command=lambda: change_photos(1))


root.mainloop()