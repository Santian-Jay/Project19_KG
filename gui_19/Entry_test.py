import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
import re

root = tk.Tk()
root.geometry("400x600")
v = tk.StringVar()
e = tk.Entry(root, textvariable=v)
v.set('1,2,3,4,5')
e.pack()

def show():
    temp = e.get().strip().split(',')
    temp_list = []
    for n in temp:
        if n != '':
            temp_list.append(n)
    print(temp_list)
    str_obj.set('Lamb')


select_Model = [
    'TransE', 'TransD', 'TransH', 'DistMult', 'ComplEx', 'SimplE'
]
select_loss_function = ['pair', 'point', 'sigmoid']

model = 'TransE'

data1 = 'pair, sigmoid'
data2 = 'point'
margin1 = '2, 4, 6, 8'
margin2 = '4, 8, 12, 16, 20, 24'
lamb = '0.1, 0.01, 0.001'


def choose(event):
    if select_model() not in ['TransE', 'TransD', 'TransH']:
        print('1')
        v1.set(data2)
        str_obj.set('Lamb')
        print('3')
        selectLoss_function['value'] = ['point']
        selectLoss_function.set('point')
        update_lf()
    else:
        print('2')
        v1.set(data1)
        str_obj.set('Margin')
        selectLoss_function['value'] = ['pair', 'sigmoid']
        selectLoss_function.set('sigmoid')
        print('4')
        update_lf()

def update_lf():
    if loss_function() == 'pair':
        v2.set('2,4,6,8')
    elif loss_function() == 'sigmoid':
        v2.set('4, 8, 12, 16, 20, 24')
    else:
        v2.set('0.1, 0.01, 0.001')

def choose1(event):
    if loss_function() == 'pair':
        v2.set('2,4,6,8')
    elif loss_function() == 'sigmoid':
        v2.set('4, 8, 12, 16, 20, 24')
    else:
        v2.set('0.1, 0.01, 0.001')

def select_model():
    return selected_Model.get()


selected_Model = StringVar()
selected_Model.set("TransE")
selectModel = Combobox(root, textvariable=selected_Model, values=select_Model, width=20)
selectModel.configure(state='readonly')
selectModel.bind('<<ComboboxSelected>>', choose)
selectModel.pack()


def loss_function():
    return selected_loss_function.get()
LossFunctionLabel = Label(root, text='Loss Function', bg="#f7f3f2", anchor='w')
LossFunctionLabel.pack()

select_loss_function = ['pair', 'point', 'sigmoid']
selected_loss_function = StringVar()
selected_loss_function.set("pair")
selectLoss_function = Combobox(root, textvariable=selected_loss_function, values=select_loss_function, width=30)
selectLoss_function.configure(state='readonly')
selectLoss_function.bind('<<ComboboxSelected>>', choose1)
selectLoss_function.pack()



v1 = tk.StringVar()
e1 = tk.Entry(root, textvariable=v1)
v1.set(data1)
e1.pack()


b = tk.Button(text='get result', command=show)
b.pack()

str_obj = tk.StringVar()
str_obj.set('Margin')
selectModelLabel = tk.Label(root, textvariable=str_obj, bg="green", anchor='w')
selectModelLabel.pack()


v2 = tk.StringVar()
e2 = tk.Entry(root, textvariable=v2)
v2.set(margin1)
e2.pack()

t = '2, 4, 6, 8,'
h = 'True,False'
# t_list = t.strip().split(', ')
# # t_list.remove('')
# print(t_list)
t_list2 = re.split(', | | ,|,', t)
# t_list2.remove('')
t_list2 = list(set(t_list2))
t_list2.remove('')
print(t_list2)
root.mainloop()

# import tkinter as tk
#
# class Test():
#     def __init__(self):
#         self.root = tk.Tk()
#         self.text = tk.StringVar()
#         self.text.set("Test")
#         self.label = tk.Label(self.root, textvariable=self.text)
#
#         self.button = tk.Button(self.root,
#                                 text="Click to change text below",
#                                 command=self.changeText)
#         self.button.pack()
#         self.label.pack()
#         self.root.mainloop()
#
#     def changeText(self):
#         self.text.set("Text updated")
#
# app=Test()