import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x600")

    framea = tk.Frame(root, height=130,  bg='blue')
    framea.pack(side='top', fill='x', ipadx=10, ipady=10, expand=0)

    frameb = tk.Frame(root, bg='green')
    frameb.pack(side='top', fill='both', ipadx=10, ipady=10, expand=True)

    framec = tk.Frame(framea, height=60,  bg='gray')
    framec.pack(side='top', fill='x', ipadx=10, ipady=10, expand=0)

    framed = tk.Frame(framea, bg='yellow')
    framed.pack(side='top', fill='x', ipadx=10, ipady=10, expand=True)

    root.mainloop()