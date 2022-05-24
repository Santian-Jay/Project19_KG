import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import network
from test_dir import db_conn, multi_graph

# ====================================global variables==============================================
data_folder_path = f"{os.getcwd()}\dataset"
file_entity = f"{data_folder_path}/entity2id.txt"
file_relation = f"{data_folder_path}/relation2id.txt"
file_fact = f"{data_folder_path}/train2id.txt"
dbname = "kit301"
new_entity, new_relation, new_train, feature_1, feature_2, weight, train_1, train_node = [], [], [], [], [], [], [], []
fact_string_list = []
subgraphs_rendered = 0

# ====================================global functions==============================================


def get_statistics(statsFrame):
    # TODO get all of the statistics
    multi_graph.data_only_graph(new_entity, new_relation, new_train)
    total_nodes = f'Total number of entities is {multi_graph.nx.number_of_nodes(multi_graph.G)}'
    total_edges = f'Total number of relations is {multi_graph.nx.number_of_edges(multi_graph.G)}'
    deg_ave = multi_graph.get_degree(multi_graph.G)
    degrees_ave = f'Average degrees is {deg_ave}'

    statsLabel = Label(statsFrame, wraplength=400, text='Statistics', font='Arial', pady=10)
    statsLabel.pack()
    num_nodeLabel = Label(statsFrame, wraplength=400, text=total_nodes, font='Arial', pady=10)
    num_nodeLabel.pack()
    num_edgesLabel = Label(statsFrame, wraplength=400, text=total_edges, font='Arial', pady=10)
    num_edgesLabel.pack()
    num_relationsLabel = Label(statsFrame, wraplength=400, text=degrees_ave, font='Arial', pady=10)
    num_relationsLabel.pack()

    # tv2 = ttk.Treeview(statsFrame)
    # tv2['columns'] = ('Statistic', 'Value')
    # tv2.column("#0", width=0, stretch=NO)
    # tv2.column("Statistic", anchor=CENTER, width=200)
    # tv2.column("Value", anchor=CENTER, width=200)
    # tv2.heading("#0", text="", anchor=CENTER)
    # tv2.heading("Statistic", text="Statistic", anchor=CENTER)
    # tv2.column("Value", text="Value", anchor=CENTER)
    # tv2.insert(parent='', index='end', iid=0,text='', values=('Number of entities', '1'))
    # tv2.insert(parent='', index='end', iid=1, text='', values=('Number of relations', '2'))
    #
    # tv2.pack()


def update_from_file():
    f_entity = open(file_entity, 'r', encoding='UTF-8')
    f_relation = open(file_relation, 'r', encoding='UTF-8')
    f_train = open(file_fact, 'r', encoding='UTF-8')

    all_entity = f_entity.readlines()
    all_relation = f_relation.readlines()
    all_train = f_train.readlines()

    multi_graph.clear_dataset(all_entity, new_entity)
    multi_graph.clear_dataset(all_relation, new_relation)
    multi_graph.clear_dataset(all_train, new_train)


def save_files():
    update_from_file()
    build_fact_list()


def save_files_g(extraFrame):
    update_from_file()
    build_fact_list()
    # draw_graph_call(extraFrame)


def draw_graph_call(extraFrame):
    multi_graph.draw_graph(new_entity, new_relation, new_train, extraFrame)
    # multi_graph.data_only_graph(new_entity, new_relation, new_train)


# TODO This function needs to convert the data received from the database to the same format as used in the graph data
def update_from_mysql(entities, relations, facts):
    global new_entity, new_relation, new_train

    # Something like this but need conversion?
    new_entity = entities
    new_relation = relations
    new_train = facts


def build_fact_list():
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
    entityLabel = Label(entityFrame, wraplength=190, text='file_entity')
    entityLabel.place(x=10, y=160, width=210, height=120)
    entityButton = tk.Button(entityFrame, text="Entity File", command=get_entity)
    entityButton.place(x=37, y=320, width=160, height=33)
    relationFrame = Frame(sfwindow, width=240, height=400, highlightbackground="black", highlightthickness=2)
    relationFrame.grid(row=0, column=1, padx=0, pady=100)
    relationLabel = Label(relationFrame, wraplength=190, text='file_relation')
    relationLabel.place(x=10, y=160, width=210, height=120)
    relationButton = tk.Button(relationFrame, text="Relation File", command=get_relation)
    relationButton.place(x=37, y=320, width=160, height=33)
    factFrame = Frame(sfwindow, width=240, height=400, highlightbackground="black", highlightthickness=2)
    factFrame.grid(row=0, column=2, padx=80, pady=100)
    factLabel = Label(factFrame, wraplength=190, text='file_fact')
    factLabel.place(x=10, y=160, width=210, height=120)
    factButton = tk.Button(factFrame, text="Fact File", command=get_fact)
    factButton.place(x=37, y=320, width=160, height=33)
    cancelButton = tk.Button(sfwindow, text="Cancel", command=lambda: [sfwindow.destroy(), statistics_window()])
    cancelButton.place(x=800, y=600, width=160, height=33)
    saveButton = tk.Button(sfwindow, text="Confirm", command=lambda: [save_files(
        ), sfwindow.destroy(), statistics_window()]) # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    saveButton.place(x=1020, y=600, width=160, height=33)

    uploadButton = tk.Button(sfwindow, text="Upload to Database", command=lambda: [update_from_file(), build_fact_list(), db_conn.upload_data(dbname, new_relation, new_entity, new_train)])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    uploadButton.place(x=100, y=600, width=240, height=33)

    sfwindow.mainloop()


# ====================================statistics window==============================================

def statistics_window():
    statistics_window = tk.Tk()
    statistics_window.title("Knowledge Graph Visualization Tool")
    statistics_window.configure(bg="#f7f3f2")
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


    # SubGraphButton = tk.Button(statistics_window, text="Select files", font=f1,
                            # command=lambda: [network.draw_subgraph(file_entity, file_relation, file_fact)])
    # SubGraphButton.place(x=1170, y=30, width=150, height=50)

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
        # update_from_mysql(new_relation, new_entity, new_train)S
        build_fact_list()

    # Database selection combobox
    selected_db = StringVar(statistics_window)
    selected_db.set("Select your database")
    selected_db.trace('w', load_database)
    selectDatabase = ttk.Combobox(statistics_window, textvariable=selected_db, values=selectedDatabases, width=30, font=f1)
    selectDatabase.place(x=650, y=30, width=450, height=50)

    def beginsearch():
        result = "result"

    # frame for table
    statsFrame = Frame(statistics_window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    statsFrame.place(x=250, y=150, width=700, height=800)

    # frame for table
    factsFrame = Frame(statistics_window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    factsFrame.place(x=1000, y=550, width=700, height=400)

    # frame for distribution
    distributionFrame = Frame(statistics_window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    distributionFrame.place(x=1000, y=150, width=700, height=400)

    # scrollbar
    statsScroll = Scrollbar(factsFrame)
    statsScroll.pack(side=RIGHT, fill=Y)

    # table
    columns = ("entity1", "relationship", "entity2")
    headers = ("Entity", "Relationship", "Entity")
    widthes = (200, 200, 200)

    tv = ttk.Treeview(factsFrame, yscrollcommand=statsScroll.set, show="headings", columns=columns)

    for (column, header, width) in zip(columns, headers, widthes):
        tv.column(column, width=width, anchor="w")
        tv.heading(column, text=header, anchor="w")

    def insert_data():
        for i, person in enumerate(fact_string_list):
            tv.insert('', i, values=person)

    update_from_file()
    build_fact_list()
    insert_data()
    get_statistics(statsFrame)

    tv.place(x=0, y=0, width=680, height=399)

    # tv.pack()

    def get_data():
        item = tv.get_children()[0]
        print(tv.item(item, "values"))

    # button of statistics and visualization
    # statistics_window.protocol('WM_DELETE_WINDOW', lambda: [statistics_window.destroy(), enter()])
    statistics_page_button = Button(statistics_window, text="Statistics", background="#9e9796", activebackground="#d6cece", relief=SUNKEN, font=f3)
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

    uploadButton = tk.Button(sfwindow, text="Upload to Database", command=lambda: [update_from_file(), build_fact_list(), db_conn.upload_data(dbname, new_relation, new_entity, new_train)])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    uploadButton.place(x=100, y=600, width=240, height=33)

    sfwindow.mainloop()


# ====================================visualization window==============================================
def visualisation_window():
    global new_entity, new_relation, new_train, dbname
    window = tk.Tk()
    window.title("Knowledge Graph Visualization Tool")
    window.configure(bg="#f7f3f2")
    window.geometry("1920x1080")
    window.maxsize(width=1920, height=1080)
    window.minsize(width=920, height=1080)
    window.resizable(width=True, height=True)
    f1 = tkFont.Font(family='microsoft yahei', size=15)
    f2 = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
    f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')
    global subgraphs_rendered
    subgraphs_rendered = 0

    # Select Database Bar
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
        build_fact_list()

    # Database selection combobox
    selected_db = StringVar(window)
    selected_db.set("Select your database")
    selected_db.trace('w', load_database)
    selectDatabase = ttk.Combobox(window, textvariable=selected_db, values=selectedDatabases, width=30, font=f1)
    selectDatabase.place(x=650, y=30, width=450, height=50)

    def test_db():
        result = "result"
        print(file_entity)
        print(file_relation)
        print(file_fact)
        print(data_folder_path)
        db_name = "kit301"
        db_conn.download_data(db_name, new_relation, new_entity, new_train)

    def begin_search():
        global subgraphs_rendered
        max_hops = 2
        max_entities = 2
        if ent_checked.get() == 1:
            print('box 1 checked')
            max_entities = num_entities.get()

        if hop_checked.get() == 1:
            print('box 2 checked')
            max_hops = hop_count.get()

        network.draw_subgraph(graphFrame, subgraphs_rendered, entityBox.get(), relationBox.get(), max_hops, max_entities, file_entity, file_relation, file_fact)
        subgraphs_rendered += 1

    # frame for graph
    graphFrame = Frame(window, highlightbackground="black", highlightthickness=1, bg="#f7f3f2")
    graphFrame.place(x=200, y=120, width=1398, height=960)

    extraFrame = Frame(window, highlightbackground="black", highlightthickness=1, bg="#f7f3f2")
    extraFrame.place(x=200, y=120, width=0, height=0)

    # scrollbar
    # graphScroll = Scrollbar(graphFrame)
    # graphScroll.pack(side=RIGHT, fill=Y)

    # Update data files and draw graph
    update_from_file()
    build_fact_list()
    # draw_graph_call(extraFrame)

    # Frame for Rangebox
    subgraphFrame = Frame(window, highlightbackground="black", highlightthickness=1, bg="#ded5d5")
    subgraphFrame.place(x=1600, y=0, width=320, height=1080)

    # Subgraph Frame lLabel
    var = tk.StringVar()
    label = tk.Label(subgraphFrame, background="#9e9796", width=20, height=2, text="Subgraph", font=f2)
    label.pack(fill=X, pady=50)

    # Entity Search Entry Box
    entityBox = Entry(subgraphFrame, width=100, font=f1)
    entityBox.pack(fill=X, pady=15, padx=30)
    entityBox.insert(0, "Entity")

    # Relation Search Entry Box
    relationBox = Entry(subgraphFrame, width=100, font=f1)
    relationBox.pack(fill=X, pady=15, padx=30)
    relationBox.insert(0, "Relation")

    subgraphOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    # Select number of entities, checkbutton and combobox
    ent_checked = IntVar()
    num_entities = IntVar()
    Checkbutton(subgraphFrame, text="No. of Entities", variable=ent_checked, font=f1, bg="#ded5d5").pack(fill=X, pady=15, padx=30)
    selectNumEntities = ttk.Combobox(subgraphFrame,  textvariable=num_entities, values=subgraphOptions, width=1, font=f1)
    selectNumEntities.pack()

    # Select Hop Count, checkbutton and combobox
    hop_checked = IntVar()
    hop_count = IntVar()
    Checkbutton(subgraphFrame, text="Hop Count", variable=hop_checked, font=f1, bg="#ded5d5").pack(fill=X, pady=15, padx=30)
    selectHopCount = ttk.Combobox(subgraphFrame, textvariable=hop_count, values=subgraphOptions, width=1, font=f1)
    selectHopCount.pack()

    # # Select No. of Subgraphs, checkbutton and combobox
    # var3 = IntVar()
    # Checkbutton(subgraphFrame, text="No. of Subgraphs", variable=var3, font=f1).pack(fill=X, pady=15, padx=30)
    # selectNumSubGraphs = ttk.Combobox(subgraphFrame, values=subgraphOptions, width=1, font=f1)
    # selectNumSubGraphs.pack()

    # Search Button
    search_button = Button(subgraphFrame, text="Search", command=lambda: [begin_search()], font=f1)
    search_button.pack(fill=X, pady=15, padx=30)

    # DB Test Button
    db_test_button = Button(subgraphFrame, text="Test DB download", command=test_db, font=f1)
    db_test_button.pack(fill=X, pady=15, padx=30)

    # Select Files Button
    FilesButton = tk.Button(window, text="Select files", font=f1, command=lambda: [window.destroy(), select_files_window()])  #command=select_files_window
    FilesButton.place(x=30, y=30, width=150, height=50)

    # Tab Page Buttons
    statistics_page_button = Button(window, text="Statistics", font=f3,
                                    command=lambda: [window.destroy(), statistics_window()])
    statistics_page_button.place(x=0, y=810, width=170, height=90)
    visualization_page_button = Button(window, text="Visualisation", font=f3, background="#9e9796", activebackground="#d6cece", relief=SUNKEN)
    visualization_page_button.place(x=0, y=710, width=170, height=90)
    window.mainloop()

visualisation_window()