import tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
from database import db
from insert_graph import insert
from tkinter.messagebox import *



class VisualFrame(tk.Frame):  # 继承Frame类

    def __init__(self, root):
        super().__init__(root)
        self.hop_count = IntVar()
        self.hop_checked = IntVar()
        self.num_entities = IntVar()
        self.ent_checked = IntVar()
        self.createPage()

    def createPage(self):
        framea = tk.Frame(self, bg='green')   #
        framea.pack(side='top', fill='both', ipadx=10, ipady=10, expand=True)

        frameb = tk.Frame(framea, height=60, bg='yellow')
        frameb.pack(side='top', fill='x', ipadx=0, ipady=0, expand=0)

        framed = tk.Frame(framea, bg='pink')
        framed.pack(side='left', fill='both', ipadx=10, ipady=10, expand=True)

        framec = tk.Frame(framea, width=300, bg='gray')    # 右边的部分
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
        label = tk.Label(framec, background="light grey", width=20, height=2, text="Subgraph", font=140)
        label.pack(pady=50)

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


        tk.Button(self, text='Select Files', command=self.upload_file).place(x=0, y=0, width=200, height=50)

        selected_db = StringVar(self)
        selected_db.set("Select your database")
        selectDatabase = ttk.Combobox(self, textvariable=selected_db, width=30, font=80)
        selectDatabase.place(x=735, rely=0, width=450, height=50)

    def upload_file(self):
        print('select your files')

    def begin_search(self):
        print('begin search')
        print(self.entityBox.get(), self.relationBox.get())
        print(self.num_entities.get(), self.hop_count.get())
        # print(self.ent_checked, self.num_entities, self.hop_checked, self.hop_count)
        # print(self.num_entities)

    def test_db(self):
        print('begin test_db')


class StatisticFrame(tk.Frame):  # 继承Frame类

    def __init__(self, root):
        super().__init__(root)
        self.table_view = tk.Frame()
        self.table_view.pack()

        self.createPage()

    def createPage(self):

        columns = ('n_entity', "n_relation", "n_edge", "n_n", "n_1", "1_1", "1_n", "inverse", "symmetric", "in_degree",
                   "out_degree")
        self.tree_view = ttk.Treeview(self, show='headings', columns=columns)
        self.tree_view.column('n_entity', width=80, anchor='center')
        self.tree_view.column('n_relation', width=80, anchor='center')
        self.tree_view.column('n_edge', width=80, anchor='center')
        self.tree_view.column('n_n', width=80, anchor='center')
        self.tree_view.column('n_1', width=80, anchor='center')
        self.tree_view.column('1_1', width=80, anchor='center')
        self.tree_view.column('1_n', width=80, anchor='center')
        self.tree_view.column('inverse', width=80, anchor='center')
        self.tree_view.column('symmetric', width=80, anchor='center')
        self.tree_view.column('in_degree', width=80, anchor='center')
        self.tree_view.column('out_degree', width=80, anchor='center')

        self.tree_view.heading('n_entity', text='n_entity')
        self.tree_view.heading('n_relation', text='n_relation')
        self.tree_view.heading('n_edge', text='n_edge')
        self.tree_view.heading('n_n', text='n_n')
        self.tree_view.heading('n_1', text='n_1')
        self.tree_view.heading('1_1', text='1_1')
        self.tree_view.heading('1_n', text='1_n')
        self.tree_view.heading('inverse', text='inverse')
        self.tree_view.heading('symmetric', text='symmetric')
        self.tree_view.heading('in_degree', text='in_degree')
        self.tree_view.heading('out_degree', text='out_degree')

        self.tree_view.pack(fill=tkinter.BOTH, expand=True)

        insert.insert_json()

        self.show_data()

        tk.Button(self, text='Refresh Table', command=self.show_data).pack(anchor=tk.E, pady=5)

    def show_data(self):

        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        graph = db.all_graph()
        index = 0
        for g in graph:
            self.tree_view.insert('', index + 1, values=(
                g['n_entity'],
                g['n_relation'],
                g['n_edge'],
                g['n_n'],
                g['n_1'],
                g['1_1'],
                g['1_n'],
                g['inverse'],
                g['symmetric'],
                g['in_degree'],
                g['out_degree']
            ))
