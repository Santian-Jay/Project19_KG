import glob

import networkx as nx
from matplotlib import pyplot as plt
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Scrollbar, Text, Tk
from tkinter.constants import (HORIZONTAL, VERTICAL, RIGHT, LEFT, X, Y, BOTH, BOTTOM, YES, END)

# root = tk.Tk()
entity = r'./dataset/entity2id.txt'
relate = r'./dataset/relation2id.txt'
train = r'./dataset/train2id.txt'
max_entity = 15


def deepFirstGraphExtract(graph, sub_graph, relation, max_depth, max_entity_num):
    if max_entity_num <= 0:
        return sub_graph
    stack = []  # entity, depth
    for node in sub_graph.nodes:
        stack.append((node, 1))
    while stack:
        temp_tuple = stack.pop()
        temp_entity, temp_depth = temp_tuple[0], temp_tuple[1]
        if nx.number_of_nodes(sub_graph) >= max_entity_num:
            return sub_graph
        if temp_depth >= max_depth:
            continue
        print(temp_entity)
        for n, nbrs in graph.adj[temp_entity].items():
            for nbr, edict in nbrs.items():
                if edict['weight'] == relation and n not in sub_graph.nodes:
                    sub_graph.add_edge(temp_entity, n, weight=relation)
                    stack.append((n, temp_depth + 1))
    return sub_graph


def breadFirstGraphExtract(graph, sub_graph, relation, max_depth, max_entity_num):
    if max_entity_num <= 0:
        return sub_graph
    que = []  # entity, depth
    for node in sub_graph.nodes:
        que.append((node, 1))
    while que:
        temp_tuple = que.pop(0)
        temp_entity, temp_depth = temp_tuple[0], temp_tuple[1]
        if nx.number_of_nodes(sub_graph) >= max_entity_num:
            return sub_graph
        if temp_depth >= max_depth:
            continue
        for n, nbrs in graph.adj[temp_entity].items():
            for nbr, edict in nbrs.items():
                if edict['weight'] == relation and n not in sub_graph.nodes:
                    sub_graph.add_edge(temp_entity, n, weight=relation)
                    que.append((n, temp_depth + 1))
    return sub_graph


# Define function for reading txt file and skip first line, txt content split as tab
def get_data(file):
    res = []
    with open(file, 'r') as f:
        next(f)
        for line in f:
            l = line.split()
            l[0], l[1] = l[1], l[0]
            tl = tuple(l)
            res.append(tl)
    return res


# define function for replace node label
def replace_label(name):
    return dict(pts)[name]


def replace_relate(name):
    return dict(relates)[name]


# get the relationships
def get_relation(file):
    res = []
    with open(file, 'r') as f:
        next(f)
        for line in f:
            d = line.split()
            d[0] = replace_label(d[0])
            d[1] = replace_label(d[1])
            # d[2] = int(d[2])
            dt = tuple(d)
            res.append(dt)
    return res

pts = get_data(entity)
relates = get_data(relate)
weight = [w[2] for w in get_data(train)]

def draw_main(G):
    # Draw Graph
    node = [n[1] for n in pts]
    edge = get_relation(train)
    # create graph
    G.add_nodes_from(node)
    G.add_weighted_edges_from(edge)

    # modify the labels
    old_attrs = nx.get_edge_attributes(G, 'weight')
    attrs = {}
    for k, v in old_attrs.items():
        attrs[(k[0], k[1])] = v

    for key, value in attrs.items():
        attrs[key] = replace_relate(value)

    # layout setting
    pos = nx.circular_layout(G)
    # node
    # plt.figure(dpi=80, figsize=(24, 8))  # 不显示大图
    # nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#6495ED')  # 不显示大图
    # label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
    # nx.draw_networkx_labels(G, pos, font_size=9, bbox=label_options)  # 不显示大图
    # edge
    # nx.draw_networkx_edges(G, pos)  # 不显示大图
    print(attrs)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=attrs)  # 不显示大图
    # plt.axis('off')  # 不显示大图
    # plt.show()  #不显示大图


def draw_sub(sub, index):
    old_attrs = nx.get_edge_attributes(sub, 'weight')
    attrs = {}
    for k, v in old_attrs.items():
        attrs[(k[0], k[1])] = v
    # rs == relationship
    for key, value in attrs.items():
        attrs[key] = replace_relate(value)
    pos = nx.circular_layout(sub)
    # node
    plt.figure(dpi=80, figsize=(12, 8))
    nx.draw_networkx_nodes(sub, pos, node_size=400, node_color='#6495ED')
    label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
    nx.draw_networkx_labels(sub, pos, font_size=8, bbox=label_options)
    # edge
    nx.draw_networkx_edges(sub, pos)

    nx.draw_networkx_edge_labels(sub, pos, edge_labels=attrs)
    plt.axis('off')
    save_path = 'subgraph_images/pic-{}.png'.format(index + 1)
    plt.savefig(save_path)
    # plt.close()
    # plt.axis('off')

    # plt.show()


def get_muticenter(graph, centers, max_graph_num, relation, max_entities):
    centers_graphs = []
    routes = [[]]
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            new_routes = []
            for route in routes:
                if nx.has_path(graph, centers[i], centers[j]):
                    for path in nx.all_simple_edge_paths(graph, centers[i], centers[j]):
                        new_routes.append(route + path)
                if nx.has_path(graph, centers[j], centers[i]):
                    for path in nx.all_simple_edge_paths(graph, centers[j], centers[i]):
                        new_routes.append(route + path)
            routes = new_routes
    for k, route in enumerate(routes):
        if k >= max_graph_num:
            break
        sub_graph = nx.MultiDiGraph()
        for edge in route:
            sub_graph.add_edge(edge[0], edge[1], edge[2], weight=graph.edges[tuple(edge)]['weight'])
        centers_graphs.append(sub_graph)
    # return centers_graphs

    for i in range(len(centers_graphs)):
        res = breadFirstGraphExtract(graph, centers_graphs[i], relation, 5, max_entities)  # 这里可以改成deapfirst， 5是最大深度，15是最大节点数
        draw_sub(centers_graphs[i], i)
        # draw_sub(res)


# if __name__ == '__main__':
def first_func(entities, relation, n_entities, f_entity, f_relation, f_train):
    global entity, relate, train, max_entity
    entity = f_entity
    relate = f_relation
    train = f_train
    max_entity = n_entities

    G = nx.MultiDiGraph()
    draw_main(G)

    max_num = 5  # 最多的子图数
    get_muticenter(G, entities, max_num, relation, max_entity)
    # get_muticenter(G, ['Tove', 'SweynForkbeard', 'Harthacnut'], max_num)
    # centers = get_muticenter(G, ['Tove', 'SweynForkbeard', 'Harthacnut'], max_num)  # 3个中心节点
    # centers = get_muticenter(G, ['Gyrid', 'Tove'], max_num)  # 3个中心节点
    # print(len(centers))
    # for i in range(len(centers)):
    #     res = breadFirstGraphExtract(G, centers[i], '8', 5, 15)  # 这里可以改成deapfirst， 5是最大深度，15是最大节点数
    #     draw_sub(centers[i], i)
    #     draw_sub(res)

    # root.title('subgraph')
    # root.geometry('1920x1080')
    #
    # # 创建一个滚动条
    # scroll_bar = Scrollbar(root)
    # scroll_bar.pack(side=RIGHT, fill=Y)
    #
    # txt = Text(root, width=200, height=300)
    # txt.config(yscrollcommand=scroll_bar.set)  # 在Text组件中使用这个滚动条
    # txt.pack()
    #
    # frame1 = tk.Frame(root, bg='green')
    # frame1.pack(fill='both')
    #
    # scroll_bar.config(command=txt.yview)  # 让这个滚动条发挥作用
    #
    # images = glob.glob('image/*.png')
    # images = [ImageTk.PhotoImage(Image.open(photo)) for photo in images]
    # current_photo_n = 0
    #
    # for i in range(len(images)):
    #     # tk.Label(root, image=images[i], width=400, height=600).pack(fill='both')
    #     txt.image_create(END, image=images[i])
    #
    # # img = tk.PhotoImage(file='image/pic-1.png')
    # # img = Image.open('image/pic-1.png')
    # # img = img.resize((600, 600), Image.ANTIALIAS)
    # # my_img = ImageTk.PhotoImage(img)
    # # label_image = tk.Label(frame1, image=my_img, pady=10, padx=10, bd=0)
    # # label_image.image = img
    # # label_image.pack()
    #
    # root.mainloop()
