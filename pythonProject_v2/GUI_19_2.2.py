import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import multi_graph

data_folder_path = f"{os.getcwd()}\dataset"
file_entity = f"{data_folder_path}/entity2id.txt"
file_relation = f"{data_folder_path}/relation2id.txt"
file_fact = f"{data_folder_path}/train2id.txt"
new_entity, new_relation, new_train, feature_1, feature_2, weight, train_1, train_node = [], [], [], [], [], [], [], []
fact_string_list = []


def save_files():
    update_from_file()


def save_files_g(graphFrame):
    update_from_file()
    draw_graph_call(graphFrame)


def draw_graph_call(graphFrame):
    multi_graph.draw_graph(new_entity, new_relation, new_train, graphFrame)


def update_from_file():
    f_entity = open(file_entity, 'r')
    f_relation = open(file_relation, 'r')
    f_train = open(file_fact, 'r')
    all_entity = f_entity.readlines()
    all_relation = f_relation.readlines()
    all_train = f_train.readlines()

    multi_graph.clear_dataset(all_entity, new_entity)
    multi_graph.clear_dataset(all_relation, new_relation)
    multi_graph.clear_dataset(all_train, new_train)

    global fact_string_list
    entity_keys, relation_keys = {}, {}
    fact_count = 0
    ent_1, ent_2, rel = [], [], []

    for entity in new_entity:
        if len(entity) != 1:
            entity_keys[int(entity[1])] = entity[0]  # ent_dict.append(int(entity[1]), str(entity[0]))

    for relation in new_relation:
        if len(relation) != 1:
            relation_keys[int(relation[1])] = relation[0]  # rel_dict.append(int(relation[1]), str(relation[0]))

    for train in new_train:
        if len(train) != 1:
            ent_1.append(int(train[0]))
            ent_2.append(int(train[1]))
            rel.append(int(train[2]))
        else:
            fact_count = int(train[0])

    for i in range(0, fact_count):
        t1 = entity_keys[ent_1[i]]
        t2 = relation_keys.get((rel[i]))
        t3 = entity_keys.get((ent_2[i]))
        this_tuple = (t1, t2, t3)
        fact_string_list.append(tuple(this_tuple))


def sub_window():
    sub_window = tk.Tk()
    sub_window.title("Knowledge Graph Visualization Tool")
    sub_window.geometry("1920x1080")
    f1 = tkFont.Font(family='microsoft yahei', size=15)
    f2 = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
    f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')
    s = ttk.Style()
    s.configure('Treeview', rowheight=40)
    s.configure('Treeview.Heading', font=f2)

    def create_sub_Window():
        def get_relation():
            global file_relation
            file_relation = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                                   mode='r')
            file_relation = file_relation.name

        def get_entity():
            global file_entity
            file_entity = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                                 mode='r')
            file_entity = file_entity.name

        def get_fact():
            global file_fact
            file_fact = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                               mode='r')
            file_fact = file_fact.name

        sfwindow = tk.Toplevel(sub_window)
        sfwindow.title("Select Files")
        sfwindow.geometry("1000x500")
        entityFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        entityFrame.grid(row=0, column=0, padx=(150, 80), pady=100)
        entityButton = tk.Button(entityFrame, text="Entity", command=get_entity)
        entityButton.place(x=28, y=240, width=120, height=25)
        relationFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        relationFrame.grid(row=0, column=1, padx=0, pady=100)
        relationButton = tk.Button(relationFrame, text="Relation", command=get_relation)
        relationButton.place(x=28, y=240, width=120, height=25)
        factFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        factFrame.grid(row=0, column=2, padx=80, pady=100)
        factButton = tk.Button(factFrame, text="Fact", command=get_fact)
        factButton.place(x=28, y=240, width=120, height=25)
        cancelButton = tk.Button(sfwindow, text="cancel")
        cancelButton.place(x=600, y=450, width=120, height=25)
        saveButton = tk.Button(sfwindow, text="Save",
                               command=save_files)
        saveButton.place(x=770, y=450, width=120, height=25)

    FilesButton = tk.Button(sub_window, text="Select files", font=f1, command=create_sub_Window)
    FilesButton.place(x=30, y=30, width=150, height=50)

    # DatabaseBar
    selectedDatabases = [
        "Database 1",
        "Database 2",
        "Database 3"
    ]

    selectDatabase = ttk.Combobox(sub_window, values=selectedDatabases, width=30, font=f1)
    selectDatabase.place(x=650, y=30, width=450, height=50)
    selectDatabase.set("Select your database")

    # search bar_1
    # searchBox = Entry(sub_window, width=100)
    # searchBox.place(x=570, y=30, width=250, height=35)
    # searchBox.pack(padx=5, pady=15, side=LEFT)
    # searchBox.insert(0, "Entity")

    # search bar_2
    # searchBox = Entry(sub_window, width=100)
    # searchBox.place(x=830, y=30, width=250, height=35)
    # searchBox.pack(padx=5, pady=15, side=LEFT)
    # searchBox.insert(0, "Relation")

    def beginsearch():
        result = "result"

    # button of batch search
    # search_button = Button(sub_window, text="Batch search", command=beginsearch)
    # search_button.place(x=1100, y=30, width=100, height=35)
    # searchButton.pack(padx=5, pady=15, side=LEFT)

    # frame for table
    statsFrame = Frame(sub_window, highlightbackground="black", highlightthickness=2)
    statsFrame.place(x=250, y=150, width=1400, height=800)

    # scrollbar
    statsScroll = Scrollbar(statsFrame)
    statsScroll.pack(side=RIGHT, fill=Y)

    # table
    columns = ("entity1", "relationship", "entity2")
    headers = ("Entity", "Relationship", "Entity")
    widthes = (293, 293, 293)

    tv = ttk.Treeview(statsFrame, yscrollcommand=statsScroll.set, show="headings", columns=columns)

    for (column, header, width) in zip(columns, headers, widthes):
        tv.column(column, width=width, anchor="w")
        tv.heading(column, text=header, anchor="w")

    def insert_data():
        for i, person in enumerate(fact_string_list):
            tv.insert('', i, values=person)

    update_from_file()
    insert_data()

    tv.place(x=0, y=0, width=1380, height=799)

    # tv.pack()

    def get_data():
        item = tv.get_children()[0]
        print(tv.item(item, "values"))

    # button of statistics and visualization
    # sub_window.protocol('WM_DELETE_WINDOW', lambda: [sub_window.destroy(), enter()])
    statisticsPageButton = Button(sub_window, text="Statistics", background="grey", activebackground="white", font=f3)
    statisticsPageButton.place(x=0, y=810, width=170, height=90)

    visualizationPageButton = Button(sub_window, text="Visualisation", font=f3,
                                     command=lambda: [sub_window.destroy()])
    visualizationPageButton.place(x=0, y=710, width=170, height=90)


    sub_window.mainloop()


# ====================================main window==============================================

def enter():
    window = tk.Tk()
    window.title("Knowledge Graph Visualization Tool")
    window.geometry("1920x1080")
    f1 = tkFont.Font(family='microsoft yahei', size=15)
    f2 = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
    f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')

    # Upload files
    def create_Window():
        def get_relation():
            global file_relation
            file_relation = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                                   mode='r')
            # Add success checks
            file_relation = file_relation.name

        def get_entity():
            global file_entity
            file_entity = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                                 mode='r')
            file_entity = file_entity.name

        def get_fact():
            global file_fact
            file_fact = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                               mode='r')
            file_fact = file_fact.name

        sfwindow = tk.Toplevel(window)
        sfwindow.title("Select Files")
        sfwindow.geometry("1000x500")
        entityFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        entityFrame.grid(row=0, column=0, padx=(150, 80), pady=100)
        entityLabel = Label(entityFrame, wraplength=140, text=file_entity)
        entityLabel.place(x=0, y=120, width=165, height=60)
        entityButton = tk.Button(entityFrame, text="Entity File", command=get_entity)
        entityButton.place(x=28, y=240, width=120, height=25)
        relationFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        relationFrame.grid(row=0, column=1, padx=0, pady=100)
        relationLabel = Label(relationFrame, wraplength=140, text=file_relation)
        relationLabel.place(x=0, y=120, width=165, height=60)
        relationButton = tk.Button(relationFrame, text="Relation File", command=get_relation)
        relationButton.place(x=28, y=240, width=120, height=25)
        factFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        factFrame.grid(row=0, column=2, padx=80, pady=100)
        factLabel = Label(factFrame, wraplength=140, text=file_fact)
        factLabel.place(x=0, y=120, width=165, height=60)
        factButton = tk.Button(factFrame, text="Fact File", command=get_fact)
        factButton.place(x=28, y=240, width=120, height=25)
        cancelButton = tk.Button(sfwindow, text="cancel")
        cancelButton.place(x=600, y=450, width=120, height=25)
        saveButton = tk.Button(sfwindow, text="Save", command=lambda: save_files_g(
            graphFrame))  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
        saveButton.place(x=770, y=450, width=120, height=25)

    FilesButton = tk.Button(window, text="Select files", font=f1, command=create_Window)
    FilesButton.place(x=30, y=30, width=150, height=50)

    # DatabaseBar
    selectedDatabases = [
        "Database 1",
        "Database 2",
        "Database 3"
    ]

    selectDatabase = ttk.Combobox(window, values=selectedDatabases, width=30, font=f1)
    selectDatabase.place(x=650, y=30, width=450, height=50)
    selectDatabase.set("Select your database")

    def beginsearch():
        result = "result"
        print("Search will happen...")
        print(file_entity)
        print(file_relation)
        print(file_fact)
        print(data_folder_path)

    # frame for graph
    graphFrame = Frame(window, highlightbackground="black", highlightthickness=1)
    graphFrame.place(x=200, y=120, width=1401, height=960)

    # scrollbar
    graphScroll = Scrollbar(graphFrame)
    graphScroll.pack(side=RIGHT, fill=Y)

    # Update data files and draw graph
    update_from_file()
    draw_graph_call(graphFrame)

    # frame for rangeBox
    subgraphFrame = Frame(window, highlightbackground="black", highlightthickness=1)
    subgraphFrame.place(x=1600, y=0, width=320, height=1080)

    # subgraph frame label
    var = tk.StringVar()
    label = tk.Label(subgraphFrame, background="light grey", width=20, height=2, text="Subgraph", font=f2)
    label.pack(fill=X, pady=50)

    # entity search entry
    searchBox = Entry(subgraphFrame, width=100, font=f1)
    searchBox.pack(fill=X, pady=15, padx=30)
    searchBox.insert(0, "Entity")

    # relation search entry
    searchBox = Entry(subgraphFrame, width=100, font=f1)
    searchBox.pack(fill=X, pady=15, padx=30)
    searchBox.insert(0, "Relation")

    # batch search entry
    # searchBox = Entry(subgraphFrame, width=100, font=f1)
    # searchBox.pack(fill=X, pady=15, padx=30) #.place(x=670, y=30, width=400, height=25)
    # searchBox.pack(padx=5, pady=15, side=LEFT)
    # searchBox.insert(0, "Batch search")

    # search button
    search_button = Button(subgraphFrame, text="Batch search", command=beginsearch, font=f1)
    search_button.pack(fill=X, pady=15, padx=30)

    # RangeButton1 = tk.Radiobutton(subgraphFrame, text="No. of Entities", variable=var, value="Entities", font=f1)
    # RangeButton1.pack(fill=X, pady=15)

    subgraphOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    var1 = IntVar()
    Checkbutton(subgraphFrame, text="No. of Entities", variable=var1, font=f1).pack(fill=X, pady=15, padx=30)
    selectNumEntities = ttk.Combobox(subgraphFrame, values=subgraphOptions, width=1, font=f1)
    selectNumEntities.pack()
    # selectDatabase.set("Select your database")

    var2 = IntVar()
    Checkbutton(subgraphFrame, text="Hop Count", variable=var2, font=f1).pack(fill=X, pady=15, padx=30)
    selectHopCount = ttk.Combobox(subgraphFrame, values=subgraphOptions, width=1, font=f1)
    selectHopCount.pack()

    var3 = IntVar()
    Checkbutton(subgraphFrame, text="No. of Subgraphs", variable=var3, font=f1).pack(fill=X, pady=15, padx=30)
    selectNumSubGraphs = ttk.Combobox(subgraphFrame, values=subgraphOptions, width=1, font=f1)
    selectNumSubGraphs.pack()

    # RangeButton2 = tk.Radiobutton(subgraphFrame, text="Hop Count", variable=var, value="Count", font=f1)
    # RangeButton2.pack(fill=X, pady=15)
    # RangeButton3 = tk.Radiobutton(subgraphFrame, text="No. of Subgraphs", variable=var, value="Entities", font=f1)
    # RangeButton3.pack(fill=X, pady=15)

    # frame for subGraphs
    # subgraphFrame = Frame(window, highlightbackground="black", highlightthickness=1)
    # subgraphFrame.place(x=1100, y=630, width=180, height=140)

    # label2 = tk.Label(subgraphFrame, background="grey", width=20, text="SubGraphs")
    # label2.pack()

    # var1 = tk.IntVar()
    # var2 = tk.IntVar()
    # var3 = tk.IntVar()

    # subGraph1 = tk.Checkbutton(subgraphFrame, text='search 1', variable=var1, onvalue=1, offvalue=0, )
    # subGraph2 = tk.Checkbutton(subgraphFrame, text='search 2', variable=var2, onvalue=1, offvalue=0, )
    # subGraph3 = tk.Checkbutton(subgraphFrame, text='search 3', variable=var3, onvalue=1, offvalue=0, )
    # subGraph1.pack(fill=X, pady=3)
    # subGraph2.pack(fill=X, pady=3)
    # subGraph3.pack(fill=X, pady=3)

    statisticsPageButton = Button(window, text="Statistics", font=f3, command=lambda: [window.quit(), sub_window()])
    statisticsPageButton.place(x=0, y=810, width=170, height=90)

    visualizationPageButton = Button(window, text="Visualisation", font=f3, background="grey", activebackground="white",
                                     command=beginsearch)
    visualizationPageButton.place(x=0, y=710, width=170, height=90)

    window.mainloop()


enter()
