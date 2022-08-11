import tkinter as tk
from tkinter import ttk
from tkinter import *

app = tk.Tk()

frames = []
widgets = []

def createwidgets():
    global widgetNames
    global frameNames
    frame = tk.Frame(app, relief="groove")
    frames.append(frame)

    frame1 = tk.Frame(app, borderwidth=2, relief="groove")
    frames.append(frame1)

    frame.pack(side="top", fill="x")
    frame1.pack(side="top", fill="x")

    for i in range(3):
        # widget = tk.Entry(frame)
        selectModelLabel = Label(frame, text='KGE Model', bg="#f7f3f2", anchor='w', width=10)
        # selectModelLabel.place(x=18, y=43, width=230, height=30)
        selectModelLabel.pack(side='left')
    for i in range(3):
        select_Model = ['TransE', 'TransD', 'TransH', 'DistMult', 'ComplEx', 'SimplE']
        selected_Model = tk.StringVar(app)
        selected_Model.set("TransE")
        # selected_Model.trace('w', select_model)
        widget = ttk.Combobox(frame1, textvariable=selected_Model, values=select_Model, width=10)
        widgets.append(widget)
        widget.pack(side="left")

createWidgetButton = tk.Button(app, text="createWidgets", command=createwidgets)
createWidgetButton.pack(side="bottom", fill="x")

app.mainloop()

# selectModelLabel = Label(frame, text='Select a KGE Model', font=f1, bg="#f7f3f2", anchor='w')
# # selectModelLabel.place(x=18, y=43, width=230, height=30)
# selectModelLabel.pack(side='left')
#
# select_Model = ['TransE', 'TransD', 'TransH', 'DistMult', 'ComplEx', 'SimplE']
# selected_Model = StringVar(training_window)
# selected_Model.set("TransE")
# # selected_Model.trace('w', select_model)
# selectModel = ttk.Combobox(frame, textvariable=selected_Model, values=select_Model, width=20,
#                            font=f0)
# selectModel.bind('<<ComboboxSelected>>', choose)
# selectModelLabel.pack(side='left')

