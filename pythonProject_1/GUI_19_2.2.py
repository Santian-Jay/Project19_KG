import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import multi_graph
import db_conn


# ====================================global variables==============================================
data_folder_path = f"{os.getcwd()}\dataset"
file_entity = f"{data_folder_path}/entity2id.txt"
file_relation = f"{data_folder_path}/relation2id.txt"
file_fact = f"{data_folder_path}/train2id.txt"
dbname = "kit301"
new_entity, new_relation, new_train, feature_1, feature_2, weight, train_1, train_node = [], [], [], [], [], [], [], []
fact_string_list = []

# ====================================global functions==============================================


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


def save_files():
    update_from_file()
    build_statistics_list()


def save_files_g(graphFrame):
    update_from_file()
    build_statistics_list()
    draw_graph_call(graphFrame)


def draw_graph_call(graphFrame):
    multi_graph.draw_graph(new_entity, new_relation, new_train, graphFrame)


# TODO This function needs to convert the data received from the database to the same format as used in the graph data
def update_from_mysql(entities, relations, facts):
    global new_entity, new_relation, new_train

    # Something like this but need conversion?
    new_entity = entities
    new_relation = relations
    new_train = facts


def build_statistics_list():
    # build lists for statistics
    global fact_string_list
    entity_keys, relation_keys = {}, {}
    fact_count = 0
    ent_1, ent_2, rel = [], [], []
    fact_string_list.clear()

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


# ====================================select files window (statistics)==============================================

def select_files_window_b():
    sfwindow = tk.Tk()
    sfwindow.title("Select Files")
    sfwindow.geometry("1333x666")
    global new_entity, new_relation, new_train
    dbname = "kit301"

    def get_relation():
        global file_relation
        file_relation = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                               mode='r')
        # Add success checks
        file_relation = file_relation.name
        relationLabel.config(text=file_relation)

    def get_entity():
        global file_entity
        file_entity = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                             mode='r')
        file_entity = file_entity.name
        entityLabel.config(text=file_entity)

    def get_fact():
        global file_fact
        file_fact = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                           mode='r')
        file_fact = file_fact.name
        factLabel.config(text=file_fact)

    entityFrame = Frame(sfwindow, width=240, height=400, highlightbackground="black", highlightthickness=2)
    entityFrame.grid(row=0, column=0, padx=(200, 100), pady=100)
    entityLabel = Label(entityFrame, wraplength=190, text=file_entity)
    entityLabel.place(x=10, y=160, width=210, height=80)
    entityButton = tk.Button(entityFrame, text="Entity File", command=get_entity)
    entityButton.place(x=37, y=320, width=160, height=33)
    relationFrame = Frame(sfwindow, width=240, height=400, highlightbackground="black", highlightthickness=2)
    relationFrame.grid(row=0, column=1, padx=0, pady=100)
    relationLabel = Label(relationFrame, wraplength=190, text=file_relation)
    relationLabel.place(x=10, y=160, width=210, height=80)
    relationButton = tk.Button(relationFrame, text="Relation File", command=get_relation)
    relationButton.place(x=37, y=320, width=160, height=33)
    factFrame = Frame(sfwindow, width=240, height=400, highlightbackground="black", highlightthickness=2)
    factFrame.grid(row=0, column=2, padx=80, pady=100)
    factLabel = Label(factFrame, wraplength=190, text=file_fact)
    factLabel.place(x=10, y=160, width=210, height=80)
    factButton = tk.Button(factFrame, text="Fact File", command=get_fact)
    factButton.place(x=37, y=320, width=160, height=33)
    cancelButton = tk.Button(sfwindow, text="Cancel", command=lambda: [sfwindow.destroy(), statistics_window()])
    cancelButton.place(x=800, y=600, width=160, height=33)
    saveButton = tk.Button(sfwindow, text="Confirm", command=lambda: [save_files(
        ), sfwindow.destroy(), statistics_window()]) # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    saveButton.place(x=1020, y=600, width=160, height=33)

    uploadButton = tk.Button(sfwindow, text="Upload to Database", command=lambda: [update_from_file(), build_statistics_list(), db_conn.upload_data(dbname, new_relation, new_entity, new_train)])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    uploadButton.place(x=100, y=600, width=240, height=33)

    sfwindow.mainloop()


# ====================================statistics window==============================================

def statistics_window():
    statistics_window = tk.Tk()
    statistics_window.title("Knowledge Graph Visualization Tool")
    statistics_window.geometry("1920x1080")
    f1 = tkFont.Font(family='microsoft yahei', size=15)
    f2 = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
    f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')
    s = ttk.Style()
    s.configure('Treeview', rowheight=40)
    s.configure('Treeview.Heading', font=f2)

    FilesButton = tk.Button(statistics_window, text="Select files", font=f1,
                            command=lambda: [statistics_window.destroy(), select_files_window_b()])
    FilesButton.place(x=30, y=30, width=150, height=50)

    # DatabaseBar
    selectedDatabases = [
        "kit301"
        #"Database 2",
        #"Database 3"
    ]

    # runs when a database is selected
    def load_database(*args):
        dbname = selectDatabase.get()
        db_conn.download_data(dbname, new_relation, new_entity, new_train)
        #update_from_mysql(new_relation, new_entity, new_train)S
        build_statistics_list()

    # Database selection combobox
    selected_db = StringVar(statistics_window)
    selected_db.set("Select your database")
    selected_db.trace('w', load_database)
    selectDatabase = ttk.Combobox(statistics_window, textvariable=selected_db, values=selectedDatabases, width=30, font=f1)
    selectDatabase.place(x=650, y=30, width=450, height=50)

    def beginsearch():
        result = "result"

    # frame for table
    statsFrame = Frame(statistics_window, highlightbackground="black", highlightthickness=2)
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
    build_statistics_list()
    insert_data()

    tv.place(x=0, y=0, width=1380, height=799)

    # tv.pack()

    def get_data():
        item = tv.get_children()[0]
        print(tv.item(item, "values"))

    # button of statistics and visualization
    # statistics_window.protocol('WM_DELETE_WINDOW', lambda: [statistics_window.destroy(), enter()])
    statistics_page_button = Button(statistics_window, text="Statistics", background="grey", activebackground="white", font=f3)
    statistics_page_button.place(x=0, y=810, width=170, height=90)

    visualization_page_button = Button(statistics_window, text="Visualisation", font=f3, command=lambda: [statistics_window.destroy(),
                                                                                                          visualisation_window()])
    visualization_page_button.place(x=0, y=710, width=170, height=90)

    statistics_window.mainloop()


# ====================================select files window (visualisation)==============================================

def select_files_window():
    sfwindow = tk.Tk()
    sfwindow.title("Select Files")
    sfwindow.geometry("1333x666")
    global new_entity, new_relation, new_train, dbname


    def get_relation():
        global file_relation
        file_relation = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                               mode='r')
        # Add success checks
        file_relation = file_relation.name
        relationLabel.config(text=file_relation)

    def get_entity():
        global file_entity
        file_entity = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                             mode='r')
        file_entity = file_entity.name
        entityLabel.config(text=file_entity)

    def get_fact():
        global file_fact
        file_fact = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                           mode='r')
        file_fact = file_fact.name
        factLabel.config(text=file_fact)

    entityFrame = Frame(sfwindow, width=240, height=400, highlightbackground="black", highlightthickness=2)
    entityFrame.grid(row=0, column=0, padx=(200, 100), pady=100)
    entityLabel = Label(entityFrame, wraplength=190, text=file_entity)
    entityLabel.place(x=10, y=160, width=210, height=80)
    entityButton = tk.Button(entityFrame, text="Entity File", command=get_entity)
    entityButton.place(x=37, y=320, width=160, height=33)
    relationFrame = Frame(sfwindow, width=240, height=400, highlightbackground="black", highlightthickness=2)
    relationFrame.grid(row=0, column=1, padx=0, pady=100)
    relationLabel = Label(relationFrame, wraplength=190, text=file_relation)
    relationLabel.place(x=10, y=160, width=210, height=80)
    relationButton = tk.Button(relationFrame, text="Relation File", command=get_relation)
    relationButton.place(x=37, y=320, width=160, height=33)
    factFrame = Frame(sfwindow, width=240, height=400, highlightbackground="black", highlightthickness=2)
    factFrame.grid(row=0, column=2, padx=80, pady=100)
    factLabel = Label(factFrame, wraplength=190, text=file_fact)
    factLabel.place(x=10, y=160, width=210, height=80)
    factButton = tk.Button(factFrame, text="Fact File", command=get_fact)
    factButton.place(x=37, y=320, width=160, height=33)

    cancelButton = tk.Button(sfwindow, text="cancel", command=lambda: [sfwindow.destroy(), visualisation_window()])
    cancelButton.place(x=800, y=600, width=160, height=33)

    saveButton = tk.Button(sfwindow, text="Confirm", command=lambda: [save_files(
        ), sfwindow.destroy(), visualisation_window()]) # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    saveButton.place(x=1020, y=600, width=160, height=33)

    uploadButton = tk.Button(sfwindow, text="Upload to Database", command=lambda: [update_from_file(), build_statistics_list(), db_conn.upload_data(dbname, new_relation, new_entity, new_train)])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    uploadButton.place(x=100, y=600, width=240, height=33)

    sfwindow.mainloop()


# ====================================visualization window==============================================
def visualisation_window():
    global new_entity, new_relation, new_train, dbname
    window = tk.Tk()
    window.title("Knowledge Graph Visualization Tool")
    window.geometry("1920x1080")
    f1 = tkFont.Font(family='microsoft yahei', size=15)
    f2 = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
    f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')

    # DatabaseBar
    selectedDatabases = [
        "kit301"
        #"Database 2",
        #"Database 3"
    ]

    # runs when a database is selected
    def load_database(*args):
        dbname = selectDatabase.get()
        db_conn.download_data(dbname, new_relation, new_entity, new_train)
        # update_from_mysql()
        build_statistics_list()

    # Database selection combobox
    selected_db = StringVar(window)
    selected_db.set("Select your database")
    selected_db.trace('w', load_database)
    selectDatabase = ttk.Combobox(window, textvariable=selected_db, values=selectedDatabases, width=30, font=f1)
    selectDatabase.place(x=650, y=30, width=450, height=50)

    def beginsearch():
        result = "result"
        print("Search will happen...")
        print(file_entity)
        print(file_relation)
        print(file_fact)
        print(data_folder_path)
        dbname = "kit301"
        db_conn.download_data(dbname, new_relation, new_entity, new_train)

    # frame for graph
    graphFrame = Frame(window, highlightbackground="black", highlightthickness=1)
    graphFrame.place(x=200, y=120, width=1401, height=960)

    # scrollbar
    graphScroll = Scrollbar(graphFrame)
    graphScroll.pack(side=RIGHT, fill=Y)

    # Update data files and draw graph
    update_from_file()
    build_statistics_list()
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

    # search button
    search_button = Button(subgraphFrame, text="Batch search", command=beginsearch, font=f1)
    search_button.pack(fill=X, pady=15, padx=30)

    subgraphOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    var1 = IntVar()
    Checkbutton(subgraphFrame, text="No. of Entities", variable=var1, font=f1).pack(fill=X, pady=15, padx=30)
    selectNumEntities = ttk.Combobox(subgraphFrame, values=subgraphOptions, width=1, font=f1)
    selectNumEntities.pack()

    var2 = IntVar()
    Checkbutton(subgraphFrame, text="Hop Count", variable=var2, font=f1).pack(fill=X, pady=15, padx=30)
    selectHopCount = ttk.Combobox(subgraphFrame, values=subgraphOptions, width=1, font=f1)
    selectHopCount.pack()

    var3 = IntVar()
    Checkbutton(subgraphFrame, text="No. of Subgraphs", variable=var3, font=f1).pack(fill=X, pady=15, padx=30)
    selectNumSubGraphs = ttk.Combobox(subgraphFrame, values=subgraphOptions, width=1, font=f1)
    selectNumSubGraphs.pack()

    FilesButton = tk.Button(window, text="Select files", font=f1, command=lambda: [window.destroy(), select_files_window()])  #command=select_files_window
    FilesButton.place(x=30, y=30, width=150, height=50)

    statistics_page_button = Button(window, text="Statistics", font=f3,
                                    command=lambda: [window.destroy(), statistics_window()])
    statistics_page_button.place(x=0, y=810, width=170, height=90)

    visualization_page_button = Button(window, text="Visualisation", font=f3, background="grey",
                                       activebackground="white")
    visualization_page_button.place(x=0, y=710, width=170, height=90)

    window.mainloop()


visualisation_window()
