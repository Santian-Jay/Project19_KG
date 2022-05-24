import io
import shutil
import tkinter as tk
import networkx as nx
import tkinter.font as tkFont
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import time
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
from PIL import Image, ImageTk
import network1
import json
from PIL import ImageTk, Image
from tkinter.constants import (HORIZONTAL, VERTICAL, RIGHT, LEFT, X, Y, BOTH, BOTTOM, YES, END)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ====================================global variables==============================================
data_folder_path = f"{os.getcwd()}\dataset"
file_entity = f"{data_folder_path}/entity2id.txt"
file_relation = f"{data_folder_path}/relation2id.txt"
file_fact = f"{data_folder_path}/train2id.txt"
dbname = "kit301"
new_entity, new_relation, new_train, feature_1, feature_2, weight, train_1, train_node = [], [], [], [], [], [], [], []
fact_string_list = []
subgraphs_rendered = 0
img_out, img_in,img_out_d, img_out_dd, img0, img1 = None, None, None, None, None, None
# txt = Text()
images = None


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
    ), sfwindow.destroy(),
        statistics_window()])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    saveButton.place(x=1020, y=600, width=160, height=33)

    uploadButton = tk.Button(sfwindow, text="Upload to Database",
                             command=lambda: [update_from_file(), build_fact_list(),
                                              db_conn.upload_data(dbname, new_relation, new_entity,
                                                                  new_train)])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
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
    cate_text_view = Text()
    img_in, img_out, img_out_d, img_out_d, img0, img1 = None, None, None, None, None, None

    FilesButton = tk.Button(statistics_window, text="Select files", font=f1,
                            command=lambda: [statistics_window.destroy(), select_files_window_b()])
    FilesButton.place(x=30, y=30, width=150, height=50)

    # SubGraphButton = tk.Button(statistics_window, text="Select files", font=f1,
    # command=lambda: [network.draw_subgraph(file_entity, file_relation, file_fact)])
    # SubGraphButton.place(x=1170, y=30, width=150, height=50)

    # DatabaseBar
    selectedDatabases = [
        "kit301"
        # "Database 2",
        # "Database 3"
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
    selectDatabase = ttk.Combobox(statistics_window, textvariable=selected_db, values=selectedDatabases, width=30,
                                  font=f1)
    selectDatabase.place(x=650, y=30, width=450, height=50)

    def beginsearch():
        result = "result"

    # frame for table
    statsFrame = Frame(statistics_window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    statsFrame.place(x=220, y=150, width=600, height=900)

    # frame for table
    factsFrame = Frame(statistics_window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    factsFrame.place(x=822, y=650, width=1000, height=400)

    # frame for distribution
    distributionFrame = Frame(statistics_window, highlightbackground="black", highlightthickness=2, bg="#f7f3f2")
    distributionFrame.place(x=822, y=150, width=1000, height=500)

    # dis_frame1 = tk.Frame(distributionFrame, width=500)
    # dis_frame1.pack(side='left', fill='y', expand=True)
    # dis_frame2 = tk.Frame(distributionFrame, width=500)
    # dis_frame2.pack(side='left', fill='y', expand=True)

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

        r_scroll_bar.config(command=cate_text_view.yview)  # 绑定
        b_scroll_bar.config(command=cate_text_view.xview)  # 绑定

    # category base view
    def create_base_tree_view():
        columns = ('Entry', 'Value')
        cate_tree_view = ttk.Treeview(statsFrame, show='headings', columns=columns)
        cate_tree_view.column('Entry', width=160, anchor='w')
        cate_tree_view.column('Value', width=40, anchor='center')

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

    def draw_dis(graph):
        global img_in, img_out
        As_1 = nx.adjacency_matrix(graph, weight=None)  # Ignore weights when converting to matrix 'weight=None'
        A_1 = As_1.todense()
        new_arr = np.array(A_1)  # covert matrix to array

        outd = np.sum(new_arr, axis=1)
        out_data = pd.DataFrame({'outdegree': outd})
        sns.kdeplot(data=out_data)
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='PNG')
        img0 = Image.open(io.BytesIO(buffer1.getvalue()))
        img1 = img0.resize((500, 500))
        img_in = ImageTk.PhotoImage(img1)
        # save_path1 = 'dis_images/out-d.jpg'
        # plt.savefig(save_path1)
        plt.close()

        ind = np.sum(new_arr, axis=0)
        in_data = pd.DataFrame({'indegree': ind})
        sns.kdeplot(data=in_data)
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='PNG')
        img2 = Image.open(io.BytesIO(buffer2.getvalue()))
        img4 = img2.resize((500, 500))
        img_out = ImageTk.PhotoImage(img4)

        # save_path2 = 'dis_images/in-d.jpg'
        # plt.savefig(save_path2)
        plt.close()

    def show_dis_graph():
        # dis_frame1.pack(side='left', fill='both', expand=True)
        # dis_frame2.pack(side='left', fill='both', expand=True)
        #
        # out_data = pd.DataFrame({'outdegree': outd})
        # sns.kdeplot(data=out_data)
        # buffer1 = io.BytesIO()
        # plt.savefig(buffer1, format='PNG')
        # img0 = Image.open(io.BytesIO(buffer1.getvalue()))
        # img1 = img0.resize((500, 500))
        # img_in = ImageTk.PhotoImage(img1)
        # save_path1 = 'dis_images/out-d.jpg'
        # plt.savefig(save_path1)
        # plt.close()
        #
        # in_data = pd.DataFrame({'indegree': ind})
        # # sns.kdeplot(data=in_data)
        # data = pd.DataFrame({'indegree': ind, 'outdegree': outd})
        # sns.kdeplot(data=data)
        # buffer2 = io.BytesIO()
        # plt.savefig(buffer2, format='PNG')
        # img2 = Image.open(io.BytesIO(buffer2.getvalue()))
        # img4 = img2.resize((1000, 500))
        # img_out = ImageTk.PhotoImage(img4)
        #
        # f = plt.figure(figsize=(5, 5), dpi=100)
        # a = f.add_subplot(111)
        # canvas = FigureCanvasTkAgg(f, master=dis_frame2)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill='both', expand=1)

        # save_path2 = 'dis_images/in-d.jpg'
        # plt.savefig(save_path2)
        # plt.close()

        indegree_image = Image.open('dis_images/in-d.png')
        outdegree_image = Image.open('dis_images/out-d.png')

        img_in = ImageTk.PhotoImage(indegree_image.resize((500, 500), Image.ANTIALIAS))
        img_out = ImageTk.PhotoImage(outdegree_image.resize((500, 500), Image.ANTIALIAS))

        # in_img_label = tk.Label(dis_frame1, image=img_in)
        # out_img_label = tk.Label(dis_frame2, image=img_out)
        in_img_label = tk.Label(dis_frame1, image=img_in)
        out_img_label = tk.Label(dis_frame2, image=img_out)
        in_img_label.image = img_in
        out_img_label.image = img_out
        in_img_label.pack()
        out_img_label.pack()

    def refresh_dis_graph():
        global dis_frame1, dis_frame2
        # for widget in dis_frame1.winfo_children():
        #     # widget.destory()
        #     # widget.pack_forget()
        #     dis_frame1.pack_forget()

        # for widget1 in dis_frame2.winfo_children():
        #     # widget1.destory()
        #     # widget1.pack_forget()
        #     dis_frame2.pack_forget()
        dis_frame2.pack_forget()
        dis_frame2.pack(side='left', fill='both', expand=True)
        # statistics_window.after(1000, show_dis_graph)
        # show_dis_graph()

    # distribution graph view
    def create_dis_image_view():
        global img_out, img_in, img_out_d, img_out_dd
        # global dis_frame1, dis_frame2, img0, img1
        #
        # mb1 = tk.Menubutton(distributionFrame, text='Show Distribution Graph', relief='raised', font=f1, width=120)
        # mb1.pack(anchor=tk.NW)
        #
        # show_dis_button = tk.Menu(mb1, tearoff=False)
        # show_dis_button.add_command(label='                Show Distribution Graph                ', command=show_dis_graph, font=f1)
        # show_dis_button.add_command(label='                Refresh Distribution Graph                 ', command=refresh_dis_graph, font=f1)
        #
        # mb1.config(menu=show_dis_button)

        # dis_frame1 = tk.Frame(distributionFrame, width=500)
        # dis_frame1.pack(side='left', fill='y', expand=True)
        # dis_frame2 = tk.Frame(distributionFrame, width=500)
        # dis_frame2.pack(side='left', fill='y', expand=True)

        dis_frame2 = tk.Frame(distributionFrame,width=0.1)  # empty
        dis_frame2.pack(side='left', fill='y', expand=True)

        dis_frame1 = tk.Frame(distributionFrame, bg='red', width=500)
        dis_frame1.pack(side='left', fill='both', expand=True)

        dis_frame3 = tk.Frame(distributionFrame, bg='yellow', width=0.1)  # empty
        dis_frame3.pack(side='left', fill='both', expand=True)
        dis_frame4 = tk.Frame(distributionFrame, bg='red', width=0.1)  # empty
        dis_frame4.pack(side='left', fill='y', expand=0)

        outdddegree_image = Image.open('dis_images/out-ddd.png')  # empty
        outddegree_image = Image.open('dis_images/out-dd.png')  # empty

        outdegree_image = Image.open('dis_images/all-d.png')

        indegree_image = Image.open('dis_images/in-d.png')  # empty

        img_in = ImageTk.PhotoImage(indegree_image.resize((1, 1), Image.ANTIALIAS))  # empty

        img_out = ImageTk.PhotoImage(outdegree_image.resize((1000, 500), Image.ANTIALIAS))

        img_out_d = ImageTk.PhotoImage(outddegree_image.resize((1, 1), Image.ANTIALIAS))  # empty
        img_out_dd = ImageTk.PhotoImage(outdddegree_image.resize((1, 1), Image.ANTIALIAS))  # empty

        out_img_label_dd = tk.Label(dis_frame4, image=img_out_dd)  # empty
        out_img_label_d = tk.Label(dis_frame3, image=img_out_d)  # empty

        out_img_label = tk.Label(dis_frame1, image=img_out)

        in_img_label = tk.Label(dis_frame2, image=img_in)  # empty


        # out_img_label.image = img_out
        # in_img_label.image = img_in
        out_img_label_dd.pack()  # empty
        out_img_label_d.pack()  # empty

        out_img_label.pack()

        in_img_label.pack()  # empty

    """测试
    # # scrollbar
    # statsScroll = Scrollbar(factsFrame)
    # statsScroll.pack(side=RIGHT, fill=Y)
    # 
    # # table
    # columns = ("entity1", "relationship", "entity2")
    # headers = ("Entity", "Relationship", "Entity")
    # widthes = (200, 200, 200)
    # 
    # tv = ttk.Treeview(factsFrame, yscrollcommand=statsScroll.set, show="headings", columns=columns)
    # 
    # for (column, header, width) in zip(columns, headers, widthes):
    #     tv.column(column, width=width, anchor="w")
    #     tv.heading(column, text=header, anchor="w")
    # 
    # def insert_data():
    #     for i, person in enumerate(fact_string_list):
    #         tv.insert('', i, values=person)
    """

    update_from_file()
    build_fact_list()
    # insert_data()
    get_statistics(statsFrame)
    create_cate_view()
    create_base_tree_view()
    create_dis_image_view()
    # multi_graph_test.draw_distribution(multi_graph.G, distributionFrame)
    # tv.place(x=0, y=0, width=680, height=399)   #测试

    # tv.pack()

    # def get_data():  #测试
    #     item = tv.get_children()[0]  #测试
    #     print(tv.item(item, "values"))  #测试

    # button of statistics and visualization
    # statistics_window.protocol('WM_DELETE_WINDOW', lambda: [statistics_window.destroy(), enter()])
    statistics_page_button = Button(statistics_window, text="Statistics", background="#9e9796",
                                    activebackground="#d6cece", relief=SUNKEN, font=f3)
    statistics_page_button.place(x=0, y=810, width=170, height=90)

    visualization_page_button = Button(statistics_window, text="Visualisation", font=f3,
                                       command=lambda: [statistics_window.destroy(),
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
    ), sfwindow.destroy(),
        visualisation_window()])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
    saveButton.place(x=1020, y=600, width=160, height=33)

    uploadButton = tk.Button(sfwindow, text="Upload to Database",
                             command=lambda: [update_from_file(), build_fact_list(),
                                              db_conn.upload_data(dbname, new_relation, new_entity,
                                                                  new_train)])  # command=lambda: multi_graph.draw_graph(new_entity, new_relation, new_train)
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
    txt = Text()
    images = None

    # Select Database Bar
    selectedDatabases = [
        "kit301"
        # "Database 2",
        # "Database 3"
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
        global images
        images = None
        global subgraphs_rendered
        max_hops = 2
        max_entities = 2
        if ent_checked.get() == 1:
            print('box 1 checked')
            max_entities = num_entities.get()

        if hop_checked.get() == 1:
            print('box 2 checked')
            max_hops = hop_count.get()

        temp = entityBox.get().strip().split()
        temp_list = []
        for n in temp:
            temp_list.append(n)
        print(temp_list)
        # network.draw_subgraph(graphFrame, subgraphs_rendered, entityBox.get(), relationBox.get(), max_hops, max_entities, file_entity, file_relation, file_fact)

        # network1.first_func(entityBox.get(), relationBox.get(), max_hops, max_entities, file_entity, file_relation, file_fact)
        network1.first_func(temp_list, relationBox.get(), max_entities, file_entity, file_relation, file_fact,
                            graphFrame, subgraphs_rendered)
        subgraphs_rendered += 1
        # image_view()

    # frame for graph
    graphFrame = Frame(window, highlightbackground="black", highlightthickness=1, bg="#f7f3f2")
    graphFrame.place(x=200, y=120, width=1398, height=960)

    extraFrame = Frame(window, highlightbackground="black", highlightthickness=1, bg="#f7f3f2")
    extraFrame.place(x=200, y=120, width=0, height=0)

    def image_view():
        global txt, scroll_bar, images
        scroll_bar = Scrollbar(graphFrame)
        scroll_bar.pack(side=RIGHT, fill=Y)

        # txt = Text(graphFrame, width=200, height=300)
        txt = Text(graphFrame, width=200, height=220)
        txt.config(yscrollcommand=scroll_bar.set)  # 在Text组件中使用这个滚动条
        txt.pack()

        scroll_bar.config(command=txt.yview)  # 让这个滚动条发挥作用

        images = glob.glob('subgraph_images/*.png')
        images = [ImageTk.PhotoImage(Image.open(photo)) for photo in images]
        print(len(images))
        for i in range(len(images)):
            txt.image_create(END, image=images[i])
            txt.insert(tk.INSERT, 'the %dth image' % (i + 1))
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
    Checkbutton(subgraphFrame, text="No. of Entities", variable=ent_checked, font=f1, bg="#ded5d5").pack(fill=X,
                                                                                                         pady=15,
                                                                                                         padx=30)
    selectNumEntities = ttk.Combobox(subgraphFrame, textvariable=num_entities, values=subgraphOptions, width=1, font=f1)
    selectNumEntities.pack()

    # Select Hop Count, checkbutton and combobox
    hop_checked = IntVar()
    hop_count = IntVar()
    Checkbutton(subgraphFrame, text="Hop Count", variable=hop_checked, font=f1, bg="#ded5d5").pack(fill=X, pady=15,
                                                                                                   padx=30)
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

    # empty image view Button
    search_button = Button(subgraphFrame, text="Clear Images", command=lambda: [clear_images()], font=f1)
    search_button.pack(fill=X, pady=15, padx=30)

    # Select Files Button
    FilesButton = tk.Button(window, text="Select files", font=f1,
                            command=lambda: [window.destroy(), select_files_window()])  # command=select_files_window
    FilesButton.place(x=30, y=30, width=150, height=50)

    # Tab Page Buttons
    statistics_page_button = Button(window, text="Statistics", font=f3,
                                    command=lambda: [window.destroy(), statistics_window()])
    statistics_page_button.place(x=0, y=810, width=170, height=90)
    visualization_page_button = Button(window, text="Visualisation", font=f3, background="#9e9796",
                                       activebackground="#d6cece", relief=SUNKEN)
    visualization_page_button.place(x=0, y=710, width=170, height=90)
    window.mainloop()


visualisation_window()
