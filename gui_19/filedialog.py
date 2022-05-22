import tkinter as tk
from tkinter import filedialog


def select_file():
    global name
    selected_file_path = filedialog.askopenfilename()
    filename.set(selected_file_path)
    name = filename.get()
    # print(name)


def print_data():
    # text.insert(tk.INSERT, name)
    print(name)
    with open(file=name, mode='r', encoding='utf-8') as file:  # 读取路径文件的内容
        file_text = file.readlines()
        strs = ''
        for f in file_text:
            strs += f
        text.insert(tk.INSERT, strs)


root = tk.Tk()
root.geometry('400x400')
filename = tk.StringVar()
root.title("Select files")
tk.Label(root, text='file path').pack()
entry = tk.Entry(root, textvariable=filename)
entry.pack(pady=10, padx=10)

tk.Button(root, text='single', command=select_file).pack()

text_area = tk.Frame(root, bg='green', height=200)
text_area.pack(side='bottom', fill='both', ipadx=10, ipady=10, expand=True)
print_button = tk.Button(text_area, text='print', command=print_data)
print_button.pack()

text = tk.Text(root, width=100, height=60)
text.pack()

# text.insert(tk.INSERT, content)

root.mainloop()
