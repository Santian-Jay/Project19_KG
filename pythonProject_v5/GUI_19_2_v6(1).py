import datetime
import shutil
import time
import tkinter as tk
# import mttkinter as tk
from mttkinter import *
import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
import os
import glob
from tkinter import Scrollbar, Text, Tk
import multi_graph
from symmetric import symme
from inverse import inver
from entity_feature import efeature
import nnrelation
import db_conn
from degree_test_v2 import deg
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt
from pythonProject_v5.Check_Box import Checkbar
import network1
import json
from PIL import ImageTk, Image
from tkinter.constants import (HORIZONTAL, VERTICAL, RIGHT, LEFT, X, Y, BOTH, BOTTOM, YES, END)
from pythonProject_v5.train.train import start_training
from pythonProject_v5.train.train import args
from pythonProject_v5.Entry_class import Entry_new
from pythonProject_v5.path_test_v5 import subgraph_extra
import threading
import re
import reminder_box
import ttkbootstrap

# ====================================global variables==============================================
data_folder_path = f"{os.getcwd()}\dataset"
file_entity = f"{data_folder_path}/entity2id.txt"
file_relation = f"{data_folder_path}/relation2id.txt"
file_fact = f"{data_folder_path}/train2id.txt"
dbname = "kit301"
new_entity, new_relation, new_train, feature_1, feature_2, weight, train_1, train_node = [], [], [], [], [], [], [], []
fact_string_list = []
subgraphs_rendered = 0
images = None
frames = []
widgets = []
img_out, img_in, img_out_d, img_out_dd, img_out_ddd, img_out_dddd, img0, img1 = None, None, None, None, None, None, None, None

# ====================================global functions==============================================


def get_statistics(statsFrame):
    # TODO get all of the statistics
    multi_graph.data_only_graph(new_entity, new_relation, new_train)
    t_nodes = multi_graph.nx.number_of_nodes(multi_graph.G)
    t_edges = multi_graph.nx.number_of_edges(multi_graph.G)
    in_degree_ave, out_degree_ave = multi_graph.get_degree(multi_graph.G)
    n_relation_head, n_relation_tail = efeature.get_count()
    n_11, n_1n, n_n1, n_nn = nnrelation.nn_categorization(new_train)

    # data list
    data_list = [t_nodes, t_edges, in_degree_ave, out_degree_ave, len(new_relation), n_11, n_1n, n_n1, n_nn, symme.n_sy,
                 inver.n_inver, n_relation_head, n_relation_tail]
    # insert data to json
    with open('data.json', 'r+') as f:
        json_data = json.load(f)
        for i in range(len(data_list)):
            json_data[i]['value'] = data_list[i]
        f.seek(0)
        f.write(json.dumps(json_data))
        f.truncate()


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
    deg.__init__()
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


# ====================================select files window==============================================

def select_files_window():
    sfwindow = tk.Tk()
    sfwindow.title("Select Files")
    sfwindow.geometry("1333x666")
    global new_entity, new_relation, new_train, dbname

    def get_relation():
        global file_relation
        file_relation = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                               mode='r')
        # file_relation = filedialog.askopenfile()
        # Add success checks
        file_relation = file_relation.name
        relationLabel.config(text=file_relation)

    def get_entity():
        global file_entity
        file_entity = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                             mode='r')
        # file_entity = filedialog.askopenfile()
        file_entity = file_entity.name
        entityLabel.config(text=file_entity)

    def get_fact():
        global file_fact
        file_fact = filedialog.askopenfile(initialdir=data_folder_path, filetypes=[("text files", "*.txt")],
                                           mode='r')
        # file_fact = filedialog.askopenfile()
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

    cancelButton = tk.Button(sfwindow, text="Cancel", command=lambda: sfwindow.destroy())
    cancelButton.place(x=800, y=600, width=160, height=33)

    saveButton = tk.Button(sfwindow, text="Confirm", command=lambda: [save_files(
    ), sfwindow.destroy()])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    saveButton.place(x=1020, y=600, width=160, height=33)

    # upload to Database

    dbnameBox = Entry(sfwindow, width=150)
    dbnameBox.place(x=100, y=600, width=240, height=33)
    dbnameBox.insert(0, "Enter a name")

    uploadButton = tk.Button(sfwindow, text="Upload to Database",
                             command=lambda: [update_from_file(), build_fact_list(),
                                              db_conn.upload_data(dbnameBox.get(), new_relation, new_entity,
                                                                  new_train)])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    uploadButton.place(x=350, y=600, width=200, height=33)

    sfwindow.mainloop()


# ====================================visualization window==============================================

def visualisation_window():
    global new_entity, new_relation, new_train, dbname
    window = tk.Tk()
    window.title("Knowledge Graph Visualization Tool")
    window.configure(bg="#f7f3f2")
    window.geometry("1920x1080")
    # window.maxsize(width=1920, height=1080)
    # window.minsize(width=920, height=1080)
    window.resizable(width=True, height=True)
    f1 = tkFont.Font(family='microsoft yahei', size=15)
    f2 = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
    f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')
    global subgraphs_rendered
    cate_tree_view = ttk.Treeview()

    subgraphs_rendered = 0
    txt = Text()
    images = None
    graph_data_1 = {}
    graph_data_2 = {}
    graph_data_3 = {}
    graph_data_4 = {}
    graph_data_5 = {}
    result_image = None
    im = None
    # image_label = tk.Label()
    # Select Database Bar
    selectedDatabases = [
        "kit301"
        "Database 2",
        "Database 3"
    ]

    def select_window(selection):
        graphFrame.place_forget()
        extraFrame.place_forget()
        statsFrame.place_forget()
        factsFrame.place_forget()
        distributionFrame.place_forget()
        resultFrame.place_forget()
        optionsFrame.place_forget()
        subgraphFrame.place_forget()
        historyFrame.place_forget()
        psLabel.place_forget()
        KG.place_forget()
        KGE.place_forget()
        modelsFrame.place_forget()

        if selection == 0:
            graphFrame.place(x=200, y=120, width=1398, height=960)
            extraFrame.place(x=200, y=120, width=0, height=0)
            subgraphFrame.place(x=1600, y=0, width=320, height=1080)

        elif selection == 1:
            statsFrame.place(x=220, y=150, width=600, height=900)
            factsFrame.place(x=822, y=650, width=1000, height=400)
            distributionFrame.place(x=822, y=150, width=1000, height=500)

        elif selection == 2:
            resultFrame.place(x=442, y=150, width=1378, height=650)
            optionsFrame.place(x=220, y=803, width=1600, height=250)
            modelsFrame.place(x=220, y=150, width=220, height=650)

        elif selection == 3:
            historyFrame.place(x=220, y=150, width=1600, height=800)
            KGE.place(x=480, y=110, width=200, height=30)
            KG.place(x=250, y=110, width=200, height=30)

            # KGE.place(x=250, y=110, width=200, height=30)
            # KG.place(x=480, y=110, width=200, height=30)
            psLabel.place(x=300, y=980, width=1230, height=30)

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

    # def _subgraph_extra(file_entity, file_relation, file_fact, temp_list, max_entities):
    #     T = threading.Thread(target=subgraph_extra(file_entity, file_relation, file_fact, temp_list, max_entities))
    #     T.setDaemon(True)
    #     T.start()
    def _begin_search():
        global subgraphs_rendered
        max_entities = int(num_entities.get())

        temp = entityBox.get().strip().split(',')

        temp_list = []
        for n in temp:
            temp_list.append(n)
        print(temp_list)

        # network.draw_subgraph(graphFrame, subgraphs_rendered, entityBox.get(), relationBox.get(), max_hops, max_entities, file_entity, file_relation, file_fact)
        subgraphs_rendered += 1
        # network1.first_func(entityBox.get(), relationBox.get(), max_hops, max_entities, file_entity, file_relation, file_fact)
        # network1.first_func(temp_list, relationBox.get(), max_entities, file_entity, file_relation, file_fact)
        if len(temp_list) == 2:
            # subgraph_extra(data_folder_path, temp_list)
            subgraph_extra(file_entity, file_relation, file_fact, temp_list, max_entities)
            # _subgraph_extra(file_entity, file_relation, file_fact, temp_list, max_entities)
            deg.__init__()  # ======================
            _image_view()
        else:
            messagebox.showerror('Warning', "Two entities are required, please try again!")

    # def begin_search():
    #     T = threading.Thread(target=_begin_search)
    #     T.setDaemon(True)
    #     T.start()
        # global subgraphs_rendered
        # max_hops = 2
        # max_entities = 2
        # if ent_checked.get() == 1:
        #     print('box 1 checked')
        #     max_entities = num_entities.get()
        #
        # if hop_checked.get() == 1:
        #     print('box 2 checked')
        #     max_hops = hop_count.get()
        #
        # temp = entityBox.get().strip().split(',')
        #
        # temp_list = []
        # for n in temp:
        #     temp_list.append(n)
        # print(temp_list)
        #
        # # network.draw_subgraph(graphFrame, subgraphs_rendered, entityBox.get(), relationBox.get(), max_hops, max_entities, file_entity, file_relation, file_fact)
        # subgraphs_rendered += 1
        # # network1.first_func(entityBox.get(), relationBox.get(), max_hops, max_entities, file_entity, file_relation, file_fact)
        # # network1.first_func(temp_list, relationBox.get(), max_entities, file_entity, file_relation, file_fact)
        # if len(temp_list) == 2:
        #     # subgraph_extra(data_folder_path, temp_list)
        #     subgraph_extra(file_entity, file_relation, file_fact, temp_list)
        #     deg.__init__()  # ======================
        #     image_view()
        # else:
        #     messagebox.showerror('Warning', "Two entities are required, please try again!")

    # frame for graph
    graphFrame = Frame(window, highlightbackground="black", highlightthickness=1, bg="#f7f3f2")
    graphFrame.place(x=200, y=120, width=1398, height=960)

    extraFrame = Frame(window, highlightbackground="black", highlightthickness=1, bg="#f7f3f2")
    extraFrame.place(x=200, y=120, width=0, height=0)

    def _image_view():
        global txt, scroll_bar, images
        scroll_bar = Scrollbar(graphFrame)
        scroll_bar.pack(side=RIGHT, fill=Y)

        # txt = Text(graphFrame, width=200, height=300)
        txt = Text(graphFrame, width=260, height=220)
        txt.config(yscrollcommand=scroll_bar.set)  #
        txt.pack()

        scroll_bar.config(command=txt.yview)  #

        images = glob.glob('subgraph_images/*.png')
        images = [ImageTk.PhotoImage(Image.open(photo)) for photo in images]
        print(len(images))
        for i in range(len(images)):
            txt.image_create(END, image=images[i])
            txt.insert(tk.INSERT, 'the %dth image' % (i + 1))

    def image_view():
        T = threading.Thread(target=_image_view)
        T.setDaemon(True)
        T.start()
        # global txt, scroll_bar, images
        # scroll_bar = Scrollbar(graphFrame)
        # scroll_bar.pack(side=RIGHT, fill=Y)
        #
        # # txt = Text(graphFrame, width=200, height=300)
        # txt = Text(graphFrame, width=260, height=220)
        # txt.config(yscrollcommand=scroll_bar.set)  #
        # txt.pack()
        #
        # scroll_bar.config(command=txt.yview)  #
        #
        # images = glob.glob('subgraph_images/*.png')
        # images = [ImageTk.PhotoImage(Image.open(photo)) for photo in images]
        # print(len(images))
        # for i in range(len(images)):
        #     txt.image_create(END, image=images[i])
        #     txt.insert(tk.INSERT, 'the %dth image' % (i + 1))
        # txt.image = images

    def clear_images():
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

    # def on_focus_in(event):
    #     entityBox.delete('0', END)
    # Entity Search Entry Box
    # entityBox = Entry(subgraphFrame, width=100, font=f1)
    entityBox = Entry_new(subgraphFrame, 'entry', font=f1)
    entityBox.pack(fill=X, pady=15, padx=30)
    # entityBox.insert(0, "Entity")
    # entityBox.bind("<<FocusIn>>", entityBox.on_focus_in)

    # Relation Search Entry Box
    # relationBox = Entry(subgraphFrame, width=100, font=f1)
    relationBox = Entry_new(subgraphFrame, 'relation', font=f1)
    relationBox.pack(fill=X, pady=15, padx=30)
    # relationBox.insert(0, "Relation")

    subgraphOptions = ["4", "5", "6", "7", "8", "9", "10"]

    # Select number of entities, checkbutton and combobox
    ent_checked = IntVar()
    num_entities = IntVar()
    # Checkbutton(subgraphFrame, text="No. of Entities", variable=ent_checked, font=f1, bg="#ded5d5").pack(fill=X,
    #                                                                                                      pady=15,
    #                                                                                                      padx=30)
    Label(subgraphFrame, text="No. of Entities", font=f1).pack(fill=X, padx=30, pady=15)
    selectNumEntities = ttk.Combobox(subgraphFrame, textvariable=num_entities, values=subgraphOptions, width=20, font=f1)
    selectNumEntities.set('10')
    selectNumEntities.config(state="readonly")
    selectNumEntities.pack()

    # Select Hop Count, checkbutton and combobox
    # hop_checked = IntVar()
    # hop_count = IntVar()
    # Checkbutton(subgraphFrame, text="Hop Count", variable=hop_checked, font=f1, bg="#ded5d5").pack(fill=X, pady=15,
    #                                                                                                padx=30)
    # selectHopCount = ttk.Combobox(subgraphFrame, textvariable=hop_count, values=subgraphOptions, width=1, font=f1)
    # selectHopCount.pack()

    # # Select No. of Subgraphs, checkbutton and combobox
    # var3 = IntVar()
    # Checkbutton(subgraphFrame, text="No. of Subgraphs", variable=var3, font=f1).pack(fill=X, pady=15, padx=30)
    # selectNumSubGraphs = ttk.Combobox(subgraphFrame, values=subgraphOptions, width=1, font=f1)
    # selectNumSubGraphs.pack()

    # Search Button
    search_button = Button(subgraphFrame, text="Search", command=lambda: [_begin_search()], font=f1)
    search_button.pack(fill=X, pady=15, padx=30)

    # DB Test Button
    db_test_button = Button(subgraphFrame, text="Test DB download", command=test_db, font=f1)
    db_test_button.pack(fill=X, pady=15, padx=30)

    # empty image view Button
    search_button = Button(subgraphFrame, text="Clear Images", command=lambda: [clear_images()], font=f1)
    search_button.pack(fill=X, pady=15, padx=30)

    # Select Files Button
    FilesButton = tk.Button(window, text="Select files", font=f1,
                            command=lambda: [select_files_window()])  # window.destroy(), command=select_files_window
    FilesButton.place(x=30, y=30, width=150, height=50)

    # Tab Radio Buttons
    tag = tk.IntVar()
    tagWidth = 23
    tk.Radiobutton(window, text="Visualization", font=f3, command=lambda: select_window(0), width=tagWidth,
                   variable=tag, value=0, bd=1,
                   indicatoron=0).place(x=0, y=710, width=170, height=70)
    tk.Radiobutton(window, text="Statistics", font=f3, command=lambda: select_window(1), variable=tag, width=tagWidth,
                   value=1, bd=1,
                   indicatoron=0).place(x=0, y=790, width=170, height=70)
    tk.Radiobutton(window, text="Training", font=f3, command=lambda: select_window(2), variable=tag, width=tagWidth,
                   value=2, bd=1,
                   indicatoron=0).place(x=0, y=870, width=170, height=70)
    tk.Radiobutton(window, text="Traceable", font=f3, command=lambda: select_window(3), variable=tag, width=tagWidth,
                   value=3, bd=1,
                   indicatoron=0).place(x=0, y=950, width=170, height=70)

    # ====================================statistics window==============================================

    s = ttk.Style()
    s.configure('Treeview', rowheight=40)
    s.configure('Treeview.Heading', font=f1)
    cate_text_view = Text()
    img_in, img_out, img_out_d, img_out_dd, img_out_ddd, img_out_dddd, img0, img1 = None, None, None, None, None, None, None, None

    def beginsearch():
        result = "result"

    # frame for table
    statsFrame = Frame(window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    # statsFrame.place(x=220, y=150, width=600, height=900)

    # frame for table
    factsFrame = Frame(window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    # factsFrame.place(x=822, y=650, width=1000, height=400)

    # frame for distribution
    distributionFrame = Frame(window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")

    # distributionFrame.place(x=822, y=150, width=1000, height=500)

    # nnLabel = tk.Label(factsFrame, wraplength=400, text='n-n==========================================', font='Arial', pady=10)
    # nnLabel.pack()

    # category view

    def show_category1():
        global cate_text_view
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

    def show_category2():
        global cate_text_view
        data = cate_text_view.get(1.0, END)
        if len(data) > 1:
            cate_text_view.delete(1.0, END)
        else:
            pass
        cate2_content = ''
        fSymmetric = open('symmetric.txt', 'r')
        n_symm = int(fSymmetric.readline())
        cate2_content += 'symmetric has %d \n' % n_symm
        for index in range(n_symm):
            content = fSymmetric.readline().strip()
            cate2_content += (content + ', ')
        cate2_content += '\n\n'

        fInverse = open('inverse.txt', 'r')
        n_inve = int(fInverse.readline())
        cate2_content += 'inverse has %d \n' % n_inve
        for index in range(n_inve):
            content = fInverse.readline().strip()
            cate2_content += (content + ', ')
        cate2_content += '\n\n'
        cate_text_view.insert(tk.INSERT, cate2_content)

    def create_cate_view():
        global cate_text_view
        mb = tk.Menubutton(factsFrame, text='Show Details', relief='raised', font=f1, width=120)
        mb.pack(anchor=tk.NW)
        show_button = tk.Menu(mb, tearoff=False)
        show_button.add_command(label='                Category 1                ', command=show_category1, font=f1)
        show_button.add_command(label='                Category 2                ', command=show_category2, font=f1)
        # show_button.add_separator()
        # show_button.add_command(label='Quit', command=factsFrame.quit())
        mb.config(menu=show_button)

        # 右边滚动条
        r_scroll_bar = Scrollbar(factsFrame)
        r_scroll_bar.pack(side=RIGHT, fill=Y)
        # 底部滚动条
        b_scroll_bar = Scrollbar(factsFrame, orient=HORIZONTAL)
        b_scroll_bar.pack(side=BOTTOM, fill=X)

        cate_text_view = tk.Text(factsFrame, width=200, height=200)
        cate_text_view.config(yscrollcommand=r_scroll_bar.set, xscrollcommand=b_scroll_bar.set, font=f1)  # 绑定
        cate_text_view.pack()

        style_value = ttk.Style()
        style_value.configure("Text", rowheight=60, font=f1)

        r_scroll_bar.config(command=cate_text_view.yview)  #
        b_scroll_bar.config(command=cate_text_view.xview)  #

    # category base view
    def create_base_tree_view():
        style_value = ttk.Style()
        style_value.configure("Treeview", rowheight=60, font=f1)
        style_value.configure("Treeview.Heading", rowheight=60, font=f1)

        columns = ('Entry', 'Value')
        cate_tree_view = ttk.Treeview(statsFrame, show='headings', columns=columns)
        cate_tree_view.column('Entry', width=160, anchor='w')
        cate_tree_view.column('Value', width=40, anchor='center')

        cate_tree_view.heading('Entry', text='Entry')
        cate_tree_view.heading('Value', text='Value')
        cate_tree_view.pack(fill='both', expand=True)

        with open('data.json', 'r') as f:
            json_data = json.load(f)
            for jd in json_data:
                cate_tree_view.insert('', index=13, values=(
                    jd['title'],
                    jd['value']
                ))

    # distribution graph view
    def create_dis_image_view():
        global img_out, img_in, img_out_d, img_out_dd, img_out_ddd, img_out_dddd
        mb1 = tk.Menubutton(distributionFrame, text='Show Distribution Graph', relief='raised', font=f1, width=120)
        mb1.pack(anchor=tk.NW)

        dis_frame1 = tk.Frame(distributionFrame, bg='red', width=150)
        dis_frame1.pack(side='left', fill='y', expand=True)
        indegree_image = Image.open('dis_images/in-d.png')
        img_in = ImageTk.PhotoImage(indegree_image.resize((1000, 500), Image.ANTIALIAS))
        in_img_label = tk.Label(dis_frame1, image=img_in)
        in_img_label.pack()

    update_from_file()
    build_fact_list()
    # insert_data()
    get_statistics(statsFrame)
    create_cate_view()
    create_base_tree_view()
    create_dis_image_view()

    # ====================================Training window==============================================

    f0 = tkFont.Font(family='microsoft yahei', size=12)
    f1 = tkFont.Font(family='microsoft yahei', size=12)
    f2 = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
    f3 = tkFont.Font(family='times', size=18, slant='italic', weight='bold')
    s = ttk.Style()
    s.configure('Treeview', rowheight=40)
    s.configure('Treeview.Heading', font=f2)

    img_in, img_out, img_out_d, img_out_dd, img_out_ddd, img_out_dddd, img0, img1 = None, None, None, None, None, None, None, None
    global model_result, margin_result, lamb_result, bernoulli_result, learning_rate_result, batch_size_result, loss_function_result, negative_sampling_result, negative_sample_no_result, result_text_view
    result_text_view = Text()
    text_view = Text()

    # runs when a database is selected
    def load_database(*args):
        dbname = selectDatabase.get()
        db_conn.download_data(dbname, new_relation, new_entity, new_train)
        # update_from_mysql(new_relation, new_entity, new_train)S
        build_fact_list()

    # frame for train result
    resultFrame = Frame(window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2",
                        width=1600, height=950)
    resultFrame.pack()
    # resultFrame.place(x=220, y=100, width=1600, height=800)
    # image_label = tk.Label(resultFrame)
    # image_label.pack()

    # frame for table
    optionsFrame = Frame(window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    # optionsFrame.place(x=220, y=805, width=1600, height=250)

    # frame to select models
    modelsFrame = Frame(window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")

    def create_options_view():
        # global option_text_view, model_result, margin_result, lamb_result, bernoulli_result, learning_rate_result, batch_size_result, loss_function_result, negative_sampling_result, negative_sample_no_result
        mb = tk.Menubutton(optionsFrame, text='Training Options', relief='raised', font=f1, width=201)
        # mb.pack(anchor=tk.NW)
        mb.place(x=0, y=0, width=1597, height=40)
        image_label = tk.Label(resultFrame)
        image_label.pack()
        float_treeview_list = []
        # global selectMargin, selectLamb

        def choose(event):
            if select_model() not in ['TransE', 'TransD', 'TransH']:
                str_obj.set('Select Lamb')
                selectLoss_function['value'] = ['point']
                selectLoss_function.set('point')
                update_lf()
            else:
                str_obj.set('Select Margin')
                selectLoss_function['value'] = ['pair', 'sigmoid']
                selectLoss_function.set('pair')
                update_lf()

        def update_lf():
            if loss_function() == 'pair':
                selected_margin.set('2, 4, 6, 8')
            elif loss_function() == 'sigmoid':
                selected_margin.set('4, 8, 12, 16, 20, 24')
            else:
                selected_margin.set('0.1, 0.01, 0.001')

        def choose1(event):
            if loss_function() == 'pair':
                selected_margin.set('2,4,6,8')
            elif loss_function() == 'sigmoid':
                selected_margin.set('4, 8, 12, 16, 20, 24')
            else:
                selected_margin.set('0.1, 0.01, 0.001')

        def select_model():
            model_result = selected_Model.get()
            return selected_Model.get()

        selectModelLabel = Label(optionsFrame, text='Select a KGE Model', font=f1, bg="#f7f3f2", anchor='w')
        selectModelLabel.place(x=18, y=43, width=230, height=30)

        select_Model = [
            'TransE', 'TransD', 'TransH', 'DistMult', 'ComplEx', 'SimplE'
        ]
        selected_Model = StringVar(window)
        selected_Model.set("TransE")
        # selected_Model.trace('w', select_model)
        selectModel = ttk.Combobox(optionsFrame, textvariable=selected_Model, values=select_Model, width=20,
                                   font=f0)
        selectModel.configure(state='readonly')
        selectModel.bind('<<ComboboxSelected>>', choose)
        selectModel.place(x=20, y=70, width=230, height=30)
        # selectModel.pack(padx=20, ipady=10)

        str_obj = tk.StringVar()
        str_obj.set('Select Margin')
        selectMarginLabel = Label(optionsFrame, textvariable=str_obj, font=f1, bg="#f7f3f2", anchor='w')
        selectMarginLabel.place(x=18, y=173, width=230, height=30)


        def margin():
            margin_result = selectMargin.get()
            print(margin_result)
            return selectMargin.get()
            #return margin_text.get()
        # pair set default[2, 4, 6, 8], sigmoid set default[4, 8, 12, 16, 20, 24]
        # select_margin = ["0", "4", "8", "12", "16", "24"]
        select_margin = '2, 4, 6, 8'
        selected_margin = StringVar()
        margin_text = tk.StringVar()
        margin_text.set('2')
        selected_margin.set(select_margin)
        # selected_margin.trace('w', margin)
        # selectMargin = ttk.Combobox(optionsFrame, textvariable=selected_margin, values=select_margin, width=100,
        #                             font=f1, state='normal')
        # selectMargin.configure(state='readonly')
        selectMargin = ttk.Entry(optionsFrame, textvariable=selected_margin, font=f1)
        # selectMargin.insert(0, select_margin)
        selectMargin.place(x=20, y=200, width=230, height=30)

        # selectMargin.pack(side=LEFT)

        selectLambLabel = Label(optionsFrame, text='Select Lamb', font=f1, bg="#f7f3f2", anchor='w')
        # selectLambLabel.place(x=268, y=173, width=230, height=30)

        def lamb():
            lamb_result = selected_lamb.get()
            return selected_lamb.get()
            #return selected_lamb.get()
        # 'DistMult', 'ComplEx', 'SimplE' use point function, lamb default:[0.1, 01, 0.001]
        select_lamb = '0.1, 0.01, 0.001'
        selected_lamb = StringVar(window)
        selected_lamb.set("0.1")
        # selected_lamb.trace('w', lamb)
        # # if select_model() not in ['TransE', 'TransD', 'TransH']:
        # # selected_lamb.state = 'normal'
        # selectLamb = ttk.Combobox(optionsFrame, textvariable=selected_lamb, values=select_lamb, width=100, font=f1,
        #                           state='disable')
        # selectLamb.configure(state='readonly')

        selectLamb = ttk.Entry(optionsFrame, textvariable=select_lamb, font=f1)
        selectLamb.insert(0, select_lamb)
        # selectLamb.place(x=270, y=200, width=230, height=30)
        # selectLamb.pack(side=LEFT)

        def bernoulli():
            bernoulli_result = selected_Bernoulli.get()
            print(bernoulli_result)
            return selectBernoulli.get()
            #return selected_Bernoulli.get()

        BernoulliLabel = Label(optionsFrame, text='Select Bernoulli', font=f1, bg="#f7f3f2", anchor='w')
        BernoulliLabel.place(x=18, y=108, width=230, height=30)

        select_Bernoulli = 'True, False'
        selected_Bernoulli = StringVar(window)
        selected_Bernoulli.set("True")
        # elected_Bernoulli.trace('w', bernoulli)

        # selectBernoulli = ttk.Combobox(optionsFrame, textvariable=selected_Bernoulli, values=select_Bernoulli,
        #                                width=30,
        #                                font=f0)
        # selectBernoulli.configure(state='readonly')
        selectBernoulli = ttk.Entry(optionsFrame, textvariable=select_Bernoulli, font=f1)
        selectBernoulli.insert(0, select_Bernoulli)
        selectBernoulli.place(x=20, y=135, width=230, height=30)

        def learning_rate():
            learning_rate_result = selected_learning_rate.get()
            return selectLearning_rate.get()
            #return selected_learning_rate.get()

        LearningRateLabel = Label(optionsFrame, text='Learning Rate', font=f1, bg="#f7f3f2", anchor='w')
        LearningRateLabel.place(x=268, y=108, width=230, height=30)

        select_learning_rate = '0.1, 0.001, 0.0001, 0.00001'
        selected_learning_rate = StringVar(window)
        selected_learning_rate.set("0.1")
        # selected_learning_rate.trace('w', learning_rate)
        # selectLearning_rate = ttk.Combobox(optionsFrame, textvariable=selected_learning_rate,
        #                                    values=select_learning_rate, width=30,
        #                                    font=f0)
        # selectLearning_rate.configure(state='readonly')

        selectLearning_rate = ttk.Entry(optionsFrame, textvariable=select_learning_rate, font=f1)
        selectLearning_rate.insert(0, select_learning_rate)
        selectLearning_rate.place(x=270, y=135, width=260, height=30)

        def batch_size():
            batch_size_result = selected_batch_size.get()
            return selectBatch_size.get()
            #return selected_batch_size.get()

        BatchSizeLabel = Label(optionsFrame, text='Batch Size', font=f1, bg="#f7f3f2", anchor='w')
        BatchSizeLabel.place(x=548, y=108, width=230, height=30)

        select_batch_size = '512, 1024, 2048, 4096'
        selected_batch_size = StringVar(window)
        selected_batch_size.set("512")
        # selected_batch_size.trace('w', batch_size)
        # selectBatch_size = ttk.Combobox(optionsFrame, textvariable=selected_batch_size, values=select_batch_size,
        #                                 width=30,
        #                                 font=f0)
        # selectBatch_size.configure(state='readonly')
        selectBatch_size = ttk.Entry(optionsFrame, textvariable=select_batch_size, font=f1)
        selectBatch_size.insert(0, select_batch_size)
        selectBatch_size.place(x=550, y=135, width=260, height=30)

        def loss_function():
            loss_function_result = selected_loss_function.get()
            return selected_loss_function.get()

        LossFunctionLabel = Label(optionsFrame, text='Loss Function', font=f1, bg="#f7f3f2", anchor='w')
        LossFunctionLabel.place(x=268, y=43, width=230, height=30)

        select_loss_function = ['pair', 'point', 'sigmoid']
        # select_loss_function = 'pair, point, sigmoid'
        selected_loss_function = StringVar(window)
        selected_loss_function.set("pair")
        # selected_loss_function.trace('w', loss_function)
        selectLoss_function = ttk.Combobox(optionsFrame, textvariable=selected_loss_function,
                                           values=select_loss_function, width=30,
                                           font=f0)
        selectLoss_function.configure(state='readonly')
        selectLoss_function.bind('<<ComboboxSelected>>', choose1)
        # selectLoss_function = ttk.Entry(optionsFrame, textvariable=select_loss_function, font=f1)
        # selectLoss_function.insert(0, select_loss_function)
        selectLoss_function.place(x=270, y=70, width=230, height=30)

        def negative_sampling():
            negative_sampling_result = selected_negative_sampling.get()
            return selected_negative_sampling.get()

        NegativeSamplingLabel = Label(optionsFrame, text='Negative Sampling', font=f1, bg="#f7f3f2", anchor='w')
        NegativeSamplingLabel.place(x=548, y=43, width=230, height=30)

        select_negative_sampling = 'Bernoulli'
        selected_negative_sampling = StringVar(window)
        selected_negative_sampling.set("Bernoulli")
        # selected_negative_sampling.trace('w', negative_sampling)
        # selectNegative_sampling = ttk.Combobox(optionsFrame, textvariable=selected_negative_sampling,
        #                                        values=select_negative_sampling, width=30,
        #                                        font=f0)
        # selectNegative_sampling.configure(state='readonly')
        selectNegative_sampling = ttk.Entry(optionsFrame, textvariable=select_negative_sampling, font=f1)
        selectNegative_sampling.insert(0, select_negative_sampling)
        selectNegative_sampling.place(x=550, y=70, width=260, height=30)

        def negative_sample_no():
            negative_sample_no_result = selected_negative_sample_no.get()
            return selectNegative_sample_no.get()
            #return selected_negative_sample_no.get()

        NegativeSampleLabel = Label(optionsFrame, text='Number of Negative Samples', font=f1, bg="#f7f3f2",
                                    anchor='w')
        NegativeSampleLabel.place(x=548, y=173, width=290, height=30)

        select_negative_sample_no = '1, 50, 100, 500'
        selected_negative_sample_no = StringVar(window)
        selected_negative_sample_no.set('1')
        # selected_negative_sample_no.trace('w', negative_sample_no)
        # selectNegative_sample_no = ttk.Combobox(optionsFrame, textvariable=selected_negative_sample_no,
        #                                         values=select_negative_sample_no, width=30,
        #                                         font=f0)
        # selectNegative_sample_no.configure(state='readonly')
        selectNegative_sample_no = ttk.Entry(optionsFrame, textvariable=select_negative_sample_no, font=f1)
        selectNegative_sample_no.insert(0, select_negative_sample_no)
        selectNegative_sample_no.place(x=550, y=200, width=310, height=30)

        def _get_parameters_list():
            TrainingButton.configure(state='disabled')
            T1 = threading.Thread(target=get_parameters_list)
            # T1.setDaemon(True)
            T1.start()

        def _create_float_window():
            T3 = threading.Thread(target=create_float_window)
            T3.start()
        def create_float_window():
            top_level = Toplevel(window)
            top_level.title('training...')
            top_level.geometry('600x400+1000+500')
            top_level.overrideredirect(True)
            Label(top_level, anchor='center', font=f1, text='Training...').pack()
            time.sleep(2)
            top_level.destroy()

        def create_result_float_window(data_list):
            top_level_result = Toplevel(window)
            top_level_result.title('training finished')
            top_level_result.geometry('1200x800+1000+500')
            # right scrollbar
            h_r_scroll_bar = Scrollbar(top_level_result)
            h_r_scroll_bar.pack(side=RIGHT, fill=Y)

            h_b_scroll_bar = Scrollbar(top_level_result, orient=HORIZONTAL)
            h_b_scroll_bar.pack(side=BOTTOM, fill=X)

            # historyColumns = ('Time', 'Params', 'Performance', 'File')
            historyColumns = ('Time', 'Params', 'Performance')
            result_tree_view = ttk.Treeview(top_level_result, show='headings', columns=historyColumns,
                                          yscrollcommand=h_r_scroll_bar.set, xscrollcommand=h_b_scroll_bar.set)
            result_tree_view.column('Time', width=100, anchor='w')
            result_tree_view.column('Params', width=400, anchor='w')
            result_tree_view.column('Performance', width=400, anchor='center')
            # cate_tree_view.column('File', width=60, anchor='center')

            result_tree_view.heading('Time', text='Time')
            result_tree_view.heading('Params', text='Parameter Content')
            result_tree_view.heading('Performance', text='Best Performance')
            # cate_tree_view.heading('File', text='Trained Model')
            result_tree_view.pack(fill='both', expand=True)

            h_b_scroll_bar.config(command=result_tree_view.xview)
            h_r_scroll_bar.config(command=result_tree_view.yview)

            style_value = ttk.Style()
            style_value.configure("Treeview", rowheight=50, font=f1)

            result_tree_view.tag_configure('oddrow', background='white')
            result_tree_view.tag_configure('evenrow', background='lightblue')
            count = 0
            max_mrr = 0
            for jd in data_list:
                if jd['Index'] >= max_mrr:
                    max_mrr = jd['Index']
                if count % 2 == 0:
                    result_tree_view.insert('', index=4, values=(
                        jd['Time'], jd['Hyper_Params'], jd['Best_Perfor']
                    ), tags='evenrow')
                else:
                    result_tree_view.insert('', index=4, values=(
                        jd['Time'], jd['Hyper_Params'], jd['Best_Perfor']
                    ), tags='oddrow')
                count += 1

            print(max_mrr)


        def get_parameters_list():
            _create_float_window()
            global cate_tree_view
            bernoulli_list = bernoulli()
            ber_list = re.split(', | | ,|,', bernoulli_list)
            ber_list = list(set(ber_list))
            if '' in ber_list:
                ber_list.remove('')

            lr_list_str = learning_rate()
            lr_list_float = re.split(', | | ,|,', lr_list_str)
            lr_list_float = list(set(lr_list_float))
            if '' in lr_list_float:
                lr_list_float.remove('')
            lr_list_float = sorted(lr_list_float)
            bs_list_str = batch_size()
            bs_list_int = re.split(', | | ,|,', bs_list_str)
            bs_list_int = list(set(bs_list_int))
            if '' in bs_list_int:
                bs_list_int.remove('')
            bs_list_int = sorted(bs_list_int)
            ns_list_str = negative_sample_no()
            ns_list_int = re.split(', | | ,|,', ns_list_str)
            ns_list_int = list(set(ns_list_int))
            if '' in ns_list_int:
                ns_list_int.remove('')
            ns_list_int = sorted(ns_list_int)
            margin_list_str = margin()
            margin_list_int = re.split(', | | ,|,', margin_list_str)
            margin_list_int = list(set(margin_list_int))
            if '' in margin_list_int:
                margin_list_int.remove('')
            margin_list_int = sorted(margin_list_int)

            para_list = [(a, b, c, d, e) for a in ber_list for b in lr_list_float for c in bs_list_int for d in ns_list_int for e in margin_list_int]
            print(para_list)
            print(len(para_list))

            for t in range(len(para_list)):
                with open('config.json', 'r+') as f:
                    json_data = json.load(f)
                    json_data['Models'] = select_model()
                    json_data['Bern'] = para_list[t][0]
                    json_data['Lr'] = float(para_list[t][1])
                    json_data['N_batch'] = int(para_list[t][2])
                    json_data['N_Ns'] = int(para_list[t][3])
                    if select_model() not in ['TransE', 'TransD', 'TransH']:
                        json_data['Lamb'] = float(para_list[t][4])
                    else:
                        json_data['Margin'] = int(para_list[t][4])
                    json_data['Ns'] = negative_sampling()
                    json_data['Loss'] = loss_function()
                    f.seek(0)
                    f.write(json.dumps(json_data))
                    f.truncate()
                _train(t, para_list)
            print('11111')
            print(float_treeview_list)
            create_result_float_window(float_treeview_list)
                # T = threading.Thread(target=_train)
                # T.start()

        # get_parameters_list()

        def print_config():
            # show_training_result()
            print(negative_sample_no(), negative_sampling(), loss_function(), batch_size(), learning_rate(),
                  bernoulli(), lamb(), margin(), select_model())
            with open('config.json', 'r+') as f:
                json_data = json.load(f)
                json_data['Models'] = select_model()
                json_data['Bern'] = bernoulli()
                json_data['Lr'] = float(learning_rate())
                json_data['Lamb'] = float(lamb())
                json_data['Margin'] = int(margin())
                json_data['N_Ns'] = int(negative_sample_no())
                json_data['Ns'] = negative_sampling()
                json_data['Loss'] = loss_function()
                json_data['N_batch'] = int(batch_size())
                f.seek(0)
                f.write(json.dumps(json_data))
                f.truncate()

        def set_data(graph_list):
            with open('mrr.json', 'r+') as f1:
                json_data = json.load(f1)
                if select_model() == 'TransE':
                    if graph_list[0] > json_data[0]['TransE']:
                        json_data[0]['TransE'] = graph_list[0]
                        json_data[1]['TransE'] = graph_list[1]
                        json_data[2]['TransE'] = graph_list[2]
                        json_data[3]['TransE'] = graph_list[3]
                        json_data[4]['TransE'] = graph_list[4]
                elif select_model() == 'TransD':
                    if graph_list[0] > json_data[0]['TransD']:
                        json_data[0]['TransD'] = graph_list[0]
                        json_data[1]['TransD'] = graph_list[1]
                        json_data[2]['TransD'] = graph_list[2]
                        json_data[3]['TransD'] = graph_list[3]
                        json_data[4]['TransD'] = graph_list[4]
                elif select_model() == 'TransH':
                    if graph_list[0] > json_data[0]['TransH']:
                        json_data[0]['TransH'] = graph_list[0]
                        json_data[1]['TransH'] = graph_list[1]
                        json_data[2]['TransH'] = graph_list[2]
                        json_data[3]['TransH'] = graph_list[3]
                        json_data[4]['TransH'] = graph_list[4]
                elif select_model() == 'DisMult':
                    if graph_list[0] > json_data[0]['DisMult']:
                        json_data[0]['DisMult'] = graph_list[0]
                        json_data[1]['DisMult'] = graph_list[1]
                        json_data[2]['DisMult'] = graph_list[2]
                        json_data[3]['DisMult'] = graph_list[3]
                        json_data[4]['DisMult'] = graph_list[4]
                elif select_model() == 'CompIEx':
                    if graph_list[0] > json_data[0]['CompIEx']:
                        json_data[0]['CompIEx'] = graph_list[0]
                        json_data[1]['CompIEx'] = graph_list[1]
                        json_data[2]['CompIEx'] = graph_list[2]
                        json_data[3]['CompIEx'] = graph_list[3]
                        json_data[4]['CompIEx'] = graph_list[4]
                elif select_model() == 'SimpIE':
                    if graph_list[0] > json_data[0]['SimpIE']:
                        json_data[0]['SimpIE'] = graph_list[0]
                        json_data[1]['SimpIE'] = graph_list[1]
                        json_data[2]['SimpIE'] = graph_list[2]
                        json_data[3]['SimpIE'] = graph_list[3]
                        json_data[4]['SimpIE'] = graph_list[4]
                f1.seek(0)
                f1.write(json.dumps(json_data))
                f1.truncate()

        def _train(p_index, para_list):
            # global para_list
            # print_config()
            graph_data, total_time = start_training()
            set_data(graph_data)
            # graph_data = [0.675, 2.2, 0.5, 0.8, 1.0]
            # total_time = '2022-09-18_21-23-31'
            # temp_str = 'lf: ' + loss_function() + ', ns: ' + negative_sampling() + ', b: ' + bernoulli() + ', lr: ' \
            #            + learning_rate() + ', bs: ' + batch_size() + ', magin: ' + margin() + ', lamb: ' + lamb() + ', nns: ' + negative_sample_no()
            if select_model() not in ['TransE', 'TransD', 'TransH']:
                temp_str = 'lf: ' + loss_function() + ', ns: ' + negative_sampling() + ', b: ' + para_list[p_index][
                            0] + ', lr: ' + para_list[p_index][1] + ', bs: ' + para_list[p_index][2] + ', lamb: ' + \
                           para_list[p_index][4] + ', nns: ' + para_list[p_index][3]
            else:
                temp_str = 'lf: ' + loss_function() + ', ns: ' + negative_sampling() + ', b: ' + para_list[p_index][0] + \
                           ', lr: ' + para_list[p_index][1] + ', bs: ' + para_list[p_index][2] + ', magin: ' + para_list[p_index][
                               4] + ', nns: ' + para_list[p_index][3]
            # temp_str = 'lf: ' + loss_function() + ', ns: ' + negative_sampling() + ', b: ' + para_list[index][0] + ', lr: ' \
            #            + para_list[index][1] + ', bs: ' + para_list[index][2] + ', magin: ' + para_list[index][4] + ', lamb: ' \
            #            + lamb() + ', nns: ' + para_list[index][3]
            best_perfor = "mrr: %.2f, mr: %.2f, test1: %.2f, test3: %.2f, test10: %.2f" % (
            graph_data[0], graph_data[1], graph_data[2], graph_data[3], graph_data[4])
            #
            new_data = {"Index": graph_data[0], "Time": total_time, "Hyper_Params": temp_str,
                        "Best_Perfor": best_perfor}
            float_treeview_list.append(new_data)

            file_path = args.task_dir + '/' + select_model() + '.json'
            if not os.path.exists(file_path):
                f = open(file_path, 'w')
                f.write('[]')
                f.close()

            with open(file_path, 'r') as f:
                jsondata = json.load(f)
                if len(jsondata) == 0:
                    jsondata.insert(0, new_data)
                else:
                    for index, value in enumerate(jsondata):
                        insert = False
                        if index <= len(jsondata) - 1:
                            print(index, value)
                            if value['Index'] > new_data['Index']:
                                jsondata.insert(index, new_data)
                                insert = True
                                break
                        if index == len(jsondata) - 1 and insert is False:
                            jsondata.insert(index + 1, new_data)
                            break
            f.close()
            with open(file_path, 'w') as f_new:
                json.dump(jsondata, f_new)
                print('insert')
            f_new.close()
            if p_index+1 == len(para_list):
                TrainingButton.configure(state='normal')
                show_graph()
                print('22222')
            # else:
            #     messagebox.showerror('Warning', "An error occurred, please restart the application!")


        def train():
            # print_config()
            # graph_data, total_time = start_training()
            # T = threading.Thread(target=_train)
            T2 = threading.Thread(target=_train)
            T2.setDaemon(True)
            T2.start()
            # set_data(graph_data)
            # temp_str = 'lf: ' + loss_function() + ', ns: ' + negative_sampling() + ', b: ' + bernoulli() + ', lr: ' \
            #            + learning_rate() + ', bs: ' + batch_size() + ', magin: ' + margin() + ', lamb: ' + lamb() + ', nns: ' + negative_sample_no()
            # # # temp_str = 'loss function:' + loss_function() + ', negative sampling:' + negative_sampling() + ', select bernoulli:' + bernoulli() + ', learning rate:' \
            # # #            + learning_rate() + ', batch size:' + batch_size() + ', magin:' + margin() + ', lamb:' + lamb() + ', number of negative samples:' + negative_sample_no()
            # # # best_Perfor = 'mrr:' + str(graph_data[0]) + ', mr:' + str(graph_data[1]) + ', test1:' + str(graph_data[2]), ', test3:' + str(graph_data[3]) + ', test10:' + str(graph_data[4])
            # best_perfor = "mrr: %.2f, mr: %.2f, test1: %.2f, test3: %.2f, test10: %.2f" % (
            # graph_data[0], graph_data[1], graph_data[2], graph_data[3], graph_data[4])
            # #
            # new_data = {"Index": graph_data[0], "Time": total_time, "Hyper_Params": temp_str,
            #             "Best_Perfor": best_perfor}
            # # with open('traceable.json', 'r') as f:
            # #     jsondata = json.load(f)
            # #     for index, value in enumerate(jsondata):
            # #         insert = False
            # #         if index <= len(jsondata) - 1:
            # #             print(index, value)
            # #             if value['Index'] > new_data['Index']:
            # #                 jsondata.insert(index, new_data)
            # #                 insert = True
            # #                 break
            # #         if index == len(jsondata) - 1 and insert is False:
            # #             jsondata.insert(index + 1, new_data)
            # #             break
            # # with open('traceable.json', 'w') as f_new:
            # #     json.dump(jsondata, f_new)
            # #     print('insert')
            #
            # file_path = args.task_dir + '/' + select_model() + '.json'
            # if not os.path.exists(file_path):
            #     f = open(file_path, 'w')
            #     f.write('[]')
            #     f.close()
            #
            # with open(file_path, 'r') as f:
            #     jsondata = json.load(f)
            #     if len(jsondata) == 0:
            #         jsondata.insert(0, new_data)
            #     else:
            #         for index, value in enumerate(jsondata):
            #             insert = False
            #             if index <= len(jsondata) - 1:
            #                 print(index, value)
            #                 if value['Index'] > new_data['Index']:
            #                     jsondata.insert(index, new_data)
            #                     insert = True
            #                     break
            #             if index == len(jsondata) - 1 and insert is False:
            #                 jsondata.insert(index + 1, new_data)
            #                 break
            # f.close()
            # with open(file_path, 'w') as f_new:
            #     json.dump(jsondata, f_new)
            #     print('insert')
            # f_new.close()
            # show_graph()

        def show_graph():
            # global image_label
            received_list = list(check_box_list.state())
            if 1 in received_list:
                image_label.pack()
                x_labels = []
                for i in range(len(received_list)):
                    if received_list[i] == 1:
                        x_labels.append(select_Model[i])
                print('received_list: ', received_list)
                print('x_labels: ', x_labels)
                chart_data_1 = []
                chart_data_2 = []
                chart_data_3 = []
                chart_data_4 = []
                chart_data_5 = []

                print(graph_data_1)
                for m in x_labels:
                    with open('mrr.json') as f:
                        json_data = json.load(f)
                    chart_data_1.append(json_data[0][m])
                    chart_data_2.append(json_data[1][m])
                    chart_data_3.append(json_data[2][m])
                    chart_data_4.append(json_data[3][m])
                    chart_data_5.append(json_data[4][m])
                fig1 = plt.figure(dpi=240, figsize=(12, 8))

                plt.subplot(321)
                plt.bar(x_labels, chart_data_1, width=0.4, color='steelblue')
                plt.xlim(-1, len(select_Model))
                for a, b in zip(x_labels, chart_data_1):
                    plt.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=10)
                plt.ylabel('MRR')
                plt.subplot(322)
                plt.bar(x_labels, chart_data_2, width=0.4, color='steelblue')
                plt.xlim(-1, len(select_Model))
                for a, b in zip(x_labels, chart_data_2):
                    plt.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=10)
                plt.ylabel('MR')
                plt.subplot(323)
                plt.bar(x_labels, chart_data_3, width=0.4, color='steelblue')
                plt.xlim(-1, len(select_Model))
                for a, b in zip(x_labels, chart_data_3):
                    plt.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=10)
                plt.ylabel('Test_1')
                plt.subplot(324)
                plt.bar(x_labels, chart_data_4, width=0.4, color='steelblue')
                plt.xlim(-1, len(select_Model))
                for a, b in zip(x_labels, chart_data_4):
                    plt.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=10)
                plt.ylabel('Test_3')
                plt.subplot(325)
                plt.bar(x_labels, chart_data_5, width=0.4, color='steelblue')
                plt.xlim(-1, len(select_Model))
                for a, b in zip(x_labels, chart_data_5):
                    plt.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=10)
                plt.ylabel('Test_10')
                plt.tight_layout()
                save_path = 'training_result_image/tr_image.png'
                plt.savefig(save_path, bbox_inches='tight', dpi=240)  # remove whitespace around
                print('33333')
                create_result_view()
                print('show 5 graph')
            else:
                image_label.pack_forget()

        def create_result_view():
            global result_text_view, result_image, im, image_label1
            im = None
            result_image = None
            result_image = Image.open('training_result_image/tr_image.png')
            im = ImageTk.PhotoImage(result_image.resize((1300, 640), Image.ANTIALIAS))
            image_label.configure(image=im)
            print('44444')

        TrainingButton = tk.Button(optionsFrame, text="Begin Training", font=f1,
                                   command=lambda: _get_parameters_list())
        TrainingButton.place(x=1230, y=140, width=200, height=50)

        def all_change(event):
            if v[0].get():
                for b in all_buttons:
                    b.deselect()
            else:
                for b in all_buttons:
                    b.select()

        all_buttons = []
        v = []
        v.append(IntVar())
        all = Checkbutton(modelsFrame, text='select all', variable=v[0], onvalue=1, offvalue=0, font=f1)
        all.pack(side=TOP, anchor=W)
        all.bind("<Button>", all_change)

        check_box_list = Checkbar(modelsFrame, select_Model, all_buttons, v)
        check_box_list.pack(side=TOP, fill='x')

        UploadButton = tk.Button(modelsFrame, text="Update Charts", font=f1,
                                 command=lambda: show_graph())
        UploadButton.pack(side=BOTTOM, fill='x')

    # ====================================traceable window==============================================

    # frame
    historyFrame = Frame(window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    psLabel = Label(window, text='PS: lf=Loss Fction, ns=Negative Sampling, b=Bernoulli, lr=Learning Rate, '
                                 'bs=Batch Size, m=Margin, l=Lamb, nns=No.of Negative Samples', font=f1, bg="#f7f3f2",
                    anchor='w')

    # KG and KGE DropDown
    # selectKGELabel = Label(optionsFrame, text='KGE', font=f1, bg="#f7f3f2", anchor='w')
    # selectKGELabel.place(x=18, y=43, width=230, height=30)

    def selectKGE():
        KGE_result = selected_KGE.get()
        print(KGE_result)
        return selected_KGE.get()

    KGElist = [
        'TransE', 'TransD', 'TransH', 'DistMult', 'ComplEx', 'SimplE'
    ]
    selected_KGE = StringVar(window)
    selected_KGE.set("TransE")
    # selected_KGE.trace('w', selectKGE)
    KGE = ttk.Combobox(window, textvariable=selected_KGE, values=KGElist, width=10,
                       font=f0)

    # selectModel.pack(padx=20, ipady=10)

    def selectKG():
        KG_result = selected_KG.get()
        print(KG_result)
        return selected_KG.get()

    input_path = '../pythonProject_v5/KG_Data'

    dir_list = []

    for root, dirs, files in os.walk(input_path):
        dir_list = dirs
        break

    # KGlist = [
    # 'TransE', 'TransD', 'TransH', 'DistMult', 'ComplEx', 'SimplE'
    # ]
    selected_KG = StringVar(window)
    selected_KG.set(dir_list[0])
    # selected_KG.trace('w', selectKG)
    KG = ttk.Combobox(window, textvariable=selected_KG, values=dir_list, width=10, font=f0)

    # selectModel.pack(padx=20, ipady=10)
    # category base view

    def create_history_table():

        # style_value = ttk.Style()
        # style_value.configure("Treeview", rowheight=60, font=f1)
        # style_value.configure("Treeview.Heading", rowheight=60, font=f1)

        # right scrollbar
        h_r_scroll_bar = Scrollbar(historyFrame)
        h_r_scroll_bar.pack(side=RIGHT, fill=Y)

        h_b_scroll_bar = Scrollbar(historyFrame, orient=HORIZONTAL)
        h_b_scroll_bar.pack(side=BOTTOM, fill=X)

        # historyColumns = ('Time', 'Params', 'Performance', 'File')
        historyColumns = ('Time', 'Params', 'Performance')
        cate_tree_view = ttk.Treeview(historyFrame, show='headings', columns=historyColumns,
                                      yscrollcommand=h_r_scroll_bar.set, xscrollcommand=h_b_scroll_bar.set)
        cate_tree_view.column('Time', width=100, anchor='w')
        cate_tree_view.column('Params', width=400, anchor='w')
        cate_tree_view.column('Performance', width=400, anchor='center')
        # cate_tree_view.column('File', width=60, anchor='center')

        cate_tree_view.heading('Time', text='Time')
        cate_tree_view.heading('Params', text='Parameter Content')
        cate_tree_view.heading('Performance', text='Best Performance')
        # cate_tree_view.heading('File', text='Trained Model')
        cate_tree_view.pack(fill='both', expand=True)

        h_b_scroll_bar.config(command=cate_tree_view.xview)
        h_r_scroll_bar.config(command=cate_tree_view.yview)

        style_value = ttk.Style()
        style_value.configure("Treeview", rowheight=50, font=f1)

        cate_tree_view.tag_configure('oddrow', background='white')
        cate_tree_view.tag_configure('evenrow', background='lightblue')
        # temp_ = cate_tree_view.insert('', END, text='2022-09-19', open=True)
        def delButton(tree):
            x = tree.get_children()
            for item in x:
                tree.delete(item)

        def show_trace_table():
            delButton(cate_tree_view)
            print(data_folder_path)
            global count
            count = 0
            # file_path = args.task_dir + '/' + selectKGE() + '.json'
            file_path = './KG_Data/' + selectKG() + '/' + selectKGE() + '.json'
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    for jd in json_data:
                        if count % 2 == 0:
                            cate_tree_view.insert('', index=4, values=(
                                jd['Time'], jd['Hyper_Params'], jd['Best_Perfor']
                            ), tags='evenrow')
                        else:
                            cate_tree_view.insert('', index=4, values=(
                                jd['Time'], jd['Hyper_Params'], jd['Best_Perfor']
                            ), tags='oddrow')
                        count += 1
                f.close()
            else:
                messagebox.showerror('Warning', "File does not exist or file is empty!")

        def delete_history():
            selected_history = cate_tree_view.selection()
            for item in selected_history:
                cate_tree_view.delete(item)

        show_Button = tk.Button(historyFrame, text="Update Table", font=f0, command=lambda: show_trace_table())
        show_Button.pack(side=LEFT)
        delete_Button = tk.Button(historyFrame, text="Delete History", font=f0, command=lambda: delete_history())
        delete_Button.pack(padx=20, side=LEFT)

    create_history_table()
    update_from_file()
    build_fact_list()
    create_options_view()
    # create_result_view()
    # show_training_result()

    window.mainloop()


visualisation_window()
