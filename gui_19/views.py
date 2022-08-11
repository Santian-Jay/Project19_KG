import os
import shutil
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import glob
from PIL import ImageTk, Image
import image
import tkinter.font as tkFont
import nnrelation
import json
from degree_test import deg
import path_test_v3

from database import db
from insert_graph import insert
from tkinter.messagebox import *


class VisualFrame(tk.Frame):  # 继承Frame类

    def __init__(self, root):
        super().__init__(root)
        self.framed = None
        self.txt = Text()
        self.hop_count = IntVar()
        self.hop_checked = IntVar()
        self.num_entities = IntVar()
        self.ent_checked = IntVar()
        self.createPage()

    def createPage(self):
        global framed, txt
        framea = tk.Frame(self, bg='green')  #
        framea.pack(side='top', fill='both', ipadx=10, ipady=10, expand=True)

        frameb = tk.Frame(framea, height=60, bg='yellow')
        frameb.pack(side='top', fill='x', ipadx=0, ipady=0, expand=0)

        framed = tk.Frame(framea, bg='pink')
        framed.pack(side='left', fill='both', ipadx=10, ipady=10, expand=True)

        framec = tk.Frame(framea, width=300, bg='gray')  # 右边的部分
        framec.pack(side='right', fill='y', ipadx=10, ipady=10, expand=0)

        """
        测试代码
        Label(framec, width=20, height=2, text='Subgraph', font=120).place(x=80, y=0)
        entity_box = Entry(framec, width=20, font=140)
        entity_box.place(x=80, y=80)
        entity_box.insert(0, 'Entity')

        relation_box = Entry(framec, width=20, font=140)
        relation_box.place(x=80, y=120)
        relation_box.insert(0, 'Relation')
        """

        var = tk.StringVar()
        self.label = tk.Label(framec, background="light grey", width=20, height=2, text="Subgraph", font=140)
        self.label.pack(pady=50)

        # Entity Search Entry Box
        self.entityBox = Entry(framec, width=20, font=140)
        self.entityBox.pack(pady=25, padx=10)
        self.entityBox.insert(0, "Entity")

        # Relation Search Entry Box
        self.relationBox = Entry(framec, width=20, font=140)
        self.relationBox.pack(pady=25, padx=10)
        self.relationBox.insert(0, "Relation")

        subgraphOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        # Select number of entities, checkbutton and combobox
        # self.ent_checked = IntVar()
        # self.num_entities = IntVar()
        Checkbutton(framec, text="No. of Entities", variable=self.ent_checked, font=140).pack(pady=15, padx=10)
        selectNumEntities = ttk.Combobox(framec, textvariable=self.num_entities, values=subgraphOptions, width=4,
                                         font=140)
        selectNumEntities.pack()

        # Select Hop Count, checkbutton and combobox
        # self.hop_checked = IntVar()
        # self.hop_count = IntVar()
        Checkbutton(framec, text="Hop Count", width=18, variable=self.hop_checked, font=140).pack(pady=15, padx=10)
        selectHopCount = ttk.Combobox(framec, textvariable=self.hop_count, values=subgraphOptions, width=4, font=140)
        selectHopCount.pack()

        # Search Button
        search_button = Button(framec, text="Search", width=20, command=self.begin_search, font=140)
        search_button.pack(pady=15, padx=10)

        # DB Test Button
        db_test_button = Button(framec, text="Test DB download", width=20, command=self.test_db, font=140)
        db_test_button.pack(pady=5, padx=10)

        search_button = Button(framec, text="Clear Images", width=20, command=self.clear_images, font=140)
        search_button.pack(pady=15, padx=10)

        tk.Button(self, text='Select Files', command=self.upload_file).place(x=0, y=0, width=200, height=50)

        selected_db = StringVar(self)
        selected_db.set("Select your database")
        selectDatabase = ttk.Combobox(self, textvariable=selected_db, width=30, font=80)
        selectDatabase.place(x=735, rely=0, width=450, height=50)
        # self.image_view(framed)

    def upload_file(self):
        print('select your files')

    def begin_search(self):
        global framed

        self.image_view(framed)
        print('begin search')
        print(self.entityBox.get(), self.relationBox.get())
        print(self.num_entities.get(), self.hop_count.get())
        # print(self.ent_checked, self.num_entities, self.hop_checked, self.hop_count)
        # print(self.num_entities)
        deg.__init__()

    def test_db(self):
        print('begin test_db')

    def image_view(self, frame):
        global txt, scroll_bar, images
        scroll_bar = Scrollbar(frame)
        scroll_bar.pack(side=RIGHT, fill=Y)

        # txt = Text(graphFrame, width=200, height=300)
        txt = Text(frame, height=220)
        txt.config(yscrollcommand=scroll_bar.set)  # 在Text组件中使用这个滚动条
        txt.pack(fill='both')

        scroll_bar.config(command=txt.yview)  # 让这个滚动条发挥作用

        images = glob.glob('subgraph_images/*.png')
        images = [ImageTk.PhotoImage(Image.open(photo)) for photo in images]
        # print(len(images))
        for i in range(len(images)):
            txt.image_create(END, image=images[i])
            txt.insert(tk.INSERT, 'the %dth image' % (i + 1))

    def clear_images(self):
        global txt, scroll_bar
        data = txt.get(1.0, END)
        if not os.path.exists('subgraph_images'):
            os.mkdir('subgraph_images')
        else:
            shutil.rmtree('subgraph_images')
            os.mkdir('subgraph_images')
        if len(data) > 1:
            r = messagebox.askokcancel('Warning', 'Confirm to clear?')
            if r:
                txt.delete(1.0, END)
                txt.pack_forget()
                scroll_bar.pack_forget()
            else:
                pass
        else:
            messagebox.showwarning('Warning', 'nothing to clear.')


class StatisticFrame(tk.Frame):  # 继承Frame类
    def __init__(self, root):
        super().__init__(root)
        self.framee = None
        self.framef = None
        self.frameg = None
        self.frameh = None
        self.cate_text_view = Text()
        self.f1 = tkFont.Font(family='microsoft yahei', size=15)
        self.f2 = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
        self.f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')
        s = ttk.Style()
        s.configure('Treeview', rowheight=40)
        s.configure('Treeview.Heading', font=self.f2)
        self.table_view = tk.Frame()
        self.table_view.pack()

        self.createPage()

    def createPage(self):
        global cate_text_view, framee, frameg, frameh, f1

        frameb = tk.Frame(self, height=60, bg='yellow')
        frameb.pack(side='top', fill='x', ipadx=0, ipady=0, expand=0)

        framee = tk.Frame(self, bg='green')  # statistics frame, left
        framee.pack(side='left', fill='both', ipadx=10, ipady=10, expand=True)

        framef = tk.Frame(self, bg='yellow')  # right frame
        framef.pack(side='right', fill='both', ipadx=0, ipady=0, expand=True)

        frameg = tk.Frame(framef, bg='red')  # distribution frame
        frameg.pack(side='top', fill='both', ipadx=10, ipady=10, expand=True)

        frameh = tk.Frame(framef, bg='pink')  # relation category frame
        frameh.pack(side='bottom', fill='both', ipadx=10, ipady=10, expand=True)

        tk.Button(self, text='Select Files', command=self.upload_file).place(x=0, y=4, width=200, height=50)

        selected_db = StringVar(self)
        selected_db.set("Select your database")
        selectDatabase = ttk.Combobox(self, textvariable=selected_db, width=30, font=80)
        selectDatabase.place(x=735, y=4, width=450, height=50)

        self.create_base_tree_view()
        self.create_cate_view()
        self.create_dis_image_view()

    def upload_file(self):
        print('select your files')

    def show_category1(self):
        global cate_text_view, framee, frameg, frameh, f1
        f1 = tkFont.Font(family='microsoft yahei', size=15)
        data = cate_text_view.get(1.0, END)
        if len(data) > 1:
            cate_text_view.delete(1.0, END)
        else:
            pass
        cate1_content = ''
        f11 = open('dataset/1-1.txt', 'r')
        n_11 = int(f11.readline())
        cate1_content += '1-1 has %d \n' % n_11
        for index in range(n_11):
            content = f11.readline().strip()
            cate1_content += (content + ', ')
        cate1_content += '\n\n'

        f1n = open('dataset/1-n.txt', 'r')
        n_1n = int(f1n.readline())
        cate1_content += '1-n has %d \n' % n_1n
        for index in range(n_1n):
            content = f1n.readline().strip()
            cate1_content += (content + ', ')
        cate1_content += '\n\n'

        fn1 = open('dataset/n-1.txt', 'r')
        n_n1 = int(fn1.readline())
        cate1_content += 'n-1 has %d \n' % n_n1
        for index in range(n_n1):
            content = fn1.readline().strip()
            cate1_content += (content + ', ')
        cate1_content += '\n\n'

        fnn = open('dataset/n-n.txt', 'r')
        n_nn = int(fnn.readline())
        cate1_content += 'n-n has %d \n' % n_nn
        for index in range(n_nn):
            content = fnn.readline().strip()
            cate1_content += (content + ', ')
        cate1_content += '\n\n'

        cate_text_view.insert(tk.INSERT, cate1_content)

    def show_category2(self):
        global cate_text_view
        data = cate_text_view.get(1.0, END)
        if len(data) > 1:
            cate_text_view.delete(1.0, END)
        else:
            pass
        cate2_content = ''
        fSymmetric = open('symmetric_v1.txt', 'r')
        n_symm = int(fSymmetric.readline())
        cate2_content += 'symmetric has %d \n' % n_symm
        for index in range(n_symm):
            content = fSymmetric.readline().strip()
            cate2_content += (content + ', ')
        cate2_content += '\n\n'

        fInverse = open('inverse_v1.txt', 'r')
        n_inve = int(fInverse.readline())
        cate2_content += 'inverse has %d \n' % n_inve
        for index in range(n_inve):
            content = fInverse.readline().strip()
            cate2_content += (content + ', ')
        cate2_content += '\n\n'
        cate_text_view.insert(tk.INSERT, cate2_content)

    def create_cate_view(self):
        global cate_text_view, framee, frameg, frameh, f1
        # f1 = tkFont.Font(family='microsoft yahei', size=15)
        mb = tk.Menubutton(frameh, text='Show Details', relief='raised', font=f1)
        mb.pack(fill='x', anchor=tk.NW)
        show_button = tk.Menu(mb, tearoff=False)
        show_button.add_command(label='                Category 1                ', command=self.show_category1,
                                font=f1)
        show_button.add_command(label='                Category 2                ', command=self.show_category2,
                                font=f1)
        mb.config(menu=show_button)

        # 右边滚动条
        r_scroll_bar = Scrollbar(frameh)
        r_scroll_bar.pack(side=RIGHT, fill=Y)
        # 底部滚动条
        b_scroll_bar = Scrollbar(frameh, orient=HORIZONTAL)
        b_scroll_bar.pack(side=BOTTOM, fill=X)

        cate_text_view = tk.Text(frameh, width=200, height=200)
        cate_text_view.config(yscrollcommand=r_scroll_bar.set, xscrollcommand=b_scroll_bar.set, font=f1)  # 绑定
        cate_text_view.pack()

        style_value = ttk.Style()
        style_value.configure("Text", rowheight=60, font=f1)

        r_scroll_bar.config(command=cate_text_view.yview)  # 绑定
        b_scroll_bar.config(command=cate_text_view.xview)  # 绑定

    # category base view
    def create_base_tree_view(self):
        global cate_text_view, framee, frameg, frameh, f1
        f1 = tkFont.Font(family='microsoft yahei', size=15)

        columns = ('Entry', 'Value')
        cate_tree_view = ttk.Treeview(framee, show='headings', columns=columns)
        cate_tree_view.column('Entry', width=540, anchor='w')
        cate_tree_view.column('Value', anchor='center')

        cate_tree_view.heading('Entry', text='Entry')
        cate_tree_view.heading('Value', text='Value')
        cate_tree_view.pack(fill='both', expand=True)

        style_value = ttk.Style()
        style_value.configure("Treeview", rowheight=60, font=f1)

        with open('data.json', 'r') as f:
            json_data = json.load(f)
            for jd in json_data:
                cate_tree_view.insert('', index=13, values=(
                    jd['title'],
                    jd['value']
                ))

    # distribution graph view
    def create_dis_image_view(self):
        global img_out, img_in, img_out_d, img_out_dd, img_out_ddd, img_out_dddd, cate_text_view, framee, frameg, frameh, f1
        mb1 = tk.Menubutton(frameg, text='Show Distribution Graph', relief='raised', font=f1)
        mb1.pack(fill='x', anchor=tk.NW)

        dis_frame1 = tk.Frame(frameg, bg='red')
        dis_frame1.pack(side='left', fill='both', expand=True)
        # indegree_image = Image.open('dis_images/in-d.png')
        indegree_image = Image.open('./subgraph_images/picture-1.png')
        img_in = ImageTk.PhotoImage(indegree_image.resize((1000, 500), Image.ANTIALIAS))
        in_img_label = tk.Label(dis_frame1, image=img_in)
        in_img_label.pack(fill='both', expand=True)
