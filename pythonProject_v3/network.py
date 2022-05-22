#!/usr/bin/env python
# coding: utf-8

# In[4]:
import tkinter

import networkx as nx

# In[5]:
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def deepFirstGraphExtract(graph, entity, relation, max_depth, max_entity_num):
  sub_graph = nx.MultiDiGraph()
  if max_entity_num <= 0:
    return sub_graph
  stack = []
  stack.append((entity, 1)) # entity, depth
  sub_graph.add_node(entity)
  while stack:
    temp_tuple = stack.pop()
    temp_entity, temp_depth = temp_tuple[0], temp_tuple[1]
    if nx.number_of_nodes(sub_graph) >= max_entity_num:
      return sub_graph
    if temp_depth >= max_depth:
      continue
    for n, nbrs in graph.adj[temp_entity].items():
      for nbr, edict in nbrs.items():
        if edict['weight'] == relation:
          sub_graph.add_edge(temp_entity, n, weight=relation)
          stack.append((nbr, temp_depth+1))
  return sub_graph


# In[22]:


def breadFirstGraphExtract(graph, entity, relation, max_depth, max_entity_num):
    sub_graph = nx.MultiDiGraph()
    if max_entity_num <= 0:
        return sub_graph
    que = []
    que.append((entity, 1))  # entity, depth
    sub_graph.add_node(entity)
    while que:
        temp_tuple = que.pop(0)
        temp_entity, temp_depth = temp_tuple[0], temp_tuple[1]
        if nx.number_of_nodes(sub_graph) >= max_entity_num:
            return sub_graph
        if temp_depth >= max_depth:
            continue
        for n, nbrs in graph.adj[temp_entity].items():
            for nbr, edict in nbrs.items():
                if edict['weight'] == relation:
                    sub_graph.add_edge(temp_entity, n, weight=relation)
                    que.append((nbr, temp_depth+1))
    return sub_graph


# In[11]:

def draw_subgraph(frame, subgraphs_rendered, search_entity, search_relation, max_depth, max_entities, f_entity, f_relation, f_fact):
    # coding:utf-8
    from matplotlib import pyplot as plt

    # Define function for reading txt file and skip first line, txt content split as tab
    def get_data(file):
        res = []
        with open(file, 'r', encoding='UTF-8') as f:
            next(f)
            for line in f:
                l = line.split()
                l[0], l[1] = l[1], l[0]
                tl = tuple(l)
                res.append(tl)
        return res

    # path of txt files
    entity = f_entity #r'dataset/entity2id.txt'
    relate = f_relation #r'dataset/relation2id.txt'
    train = f_fact #r'dataset/train2id.txt'

    # txt to Dataframe
    pts = get_data(entity)
    relates = get_data(relate)
    weight = [w[2] for w in get_data(train)]

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

    # Draw Graph
    node = [n[1] for n in pts]
    edge = get_relation(train)
    # create graph
    G = nx.MultiDiGraph()
    G.add_nodes_from(node)
    G.add_weighted_edges_from(edge)

    # modify the labels
    attrs = nx.get_edge_attributes(G, 'weight')
    # rs == relationship
    for key, value in attrs.items():
        attrs[key] = {"rs": replace_relate(value)}

    print(max_depth)
    print(max_entities)

    # ***************************** CALL SUBGRAPH EXTRACTION ****************************************
    sub = breadFirstGraphExtract(G, search_entity, search_relation, max_depth, max_entities)

    old_attrs = nx.get_edge_attributes(sub, 'weight')
    attrs = {}
    for k,v in old_attrs.items():
      attrs[(k[0],k[1])] = v
    print(attrs)
    # rs == relationship
    for key, value in attrs.items():
        attrs[key] = replace_relate(value)
    pos = nx.circular_layout(sub)
    # node
    plt.figure(dpi=80,figsize=(16,8))
    f = plt.figure(figsize=(5, 5), dpi=80)
    nx.draw_networkx_nodes(sub, pos, node_size=400, node_color='#6495ED')
    label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
    nx.draw_networkx_labels(sub, pos, font_size=9, bbox=label_options)
    # edge
    nx.draw_networkx_edges(sub, pos)
    nx.draw_networkx_edge_labels(sub, pos, edge_labels=attrs)
    plt.axis('off')
    # plt.show()

    print(subgraphs_rendered)
    sg_row = int(subgraphs_rendered / 2)
    sg_col = int(subgraphs_rendered % 2)
    print(f'row: {sg_row}')
    print(f'col: {sg_col}')
    frame2 = tkinter.Frame(frame)
    frame2.columnconfigure(0, weight=1)
    frame2.columnconfigure(1, weight=1)
    canvas = FigureCanvasTkAgg(f, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().grid(row=sg_row, column=sg_col, sticky=tkinter.EW)  # .pack(side=tkinter.TOP)  # , fill=tkinter.BOTH, expand=1
    frame2.grid(row=sg_row, column=sg_col, sticky=tkinter.EW)