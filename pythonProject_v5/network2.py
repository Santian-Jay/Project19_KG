#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
# from matplotlib import pyplot as plt
# In[52]:


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


# In[53]:


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


# # path of txt files
# entity = r'./dataset/entity2id.txt'
# relate = r'./dataset/relation2id.txt'
# train = r'./dataset/train2id.txt'
#
# # txt to Dataframe
# pts = get_data(entity)
# relates = get_data(relate)
# weight = [w[2] for w in get_data(train)]





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


# # Draw Graph
# node = [n[1] for n in pts]
# edge = get_relation(train)
# # create graph
# G = nx.MultiDiGraph()
# # G = nx.DiGraph()
# G.add_nodes_from(node)
# G.add_weighted_edges_from(edge)
#
# # modify the labels
# old_attrs = nx.get_edge_attributes(G, 'weight')
# attrs = {}
# for k, v in old_attrs.items():
#     attrs[(k[0], k[1])] = v
# # rs == relationship
# for key, value in attrs.items():
#     attrs[key] = {"rs": replace_relate(value)}


# nx.set_edge_attributes(G, edge_labels)
# labels = nx.get_edge_attributes(G, 'relation')
# layout setting
# pos = nx.circular_layout(G)
# node
# plt.figure(dpi=300,figsize=(24,8))
# nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#6495ED')
# label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
# nx.draw_networkx_labels(G, pos, font_size=9, bbox=label_options)
# # edge
# nx.draw_networkx_edges(G, pos)
# # nx.draw_networkx_edges(G, pos, width=weight)
# # nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10)
# print(attrs)
# nx.draw_networkx_edge_labels(G, pos, edge_labels=attrs)
# plt.axis('off')
# plt.show()


# In[28]:


def draw_sub(sub):

    def replace_relate(name):
        return dict(relates)[name]

    old_attrs = nx.get_edge_attributes(sub, 'weight')
    attrs = {}
    for k, v in old_attrs.items():
        attrs[(k[0], k[1])] = v
    # rs == relationship
    for key, value in attrs.items():
        attrs[key] = replace_relate(value)
    pos = nx.circular_layout(sub)
    # node
    plt.figure(dpi=100, figsize=(12, 8))
    nx.draw_networkx_nodes(sub, pos, node_size=400, node_color='#6495ED')
    label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
    nx.draw_networkx_labels(sub, pos, font_size=9, bbox=label_options)
    # edge
    nx.draw_networkx_edges(sub, pos)
    nx.draw_networkx_edge_labels(sub, pos, edge_labels=attrs)
    plt.axis('off')
    # plt.show()


# In[22]:


def get_muticenter(G, graph, centers, max_graph_num):
    centers_graphs = []
    routes = [[]]
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            new_routes = []
            for route in routes:
                if nx.has_path(graph, centers[i], centers[j]):
                    for path in nx.all_simple_edge_paths(G, centers[i], centers[j]):
                        new_routes.append(route + path)
                if nx.has_path(graph, centers[j], centers[i]):
                    for path in nx.all_simple_edge_paths(G, centers[j], centers[i]):
                        new_routes.append(route + path)
            routes = new_routes
    for i, route in enumerate(routes):
        if i >= max_graph_num:
            break
        sub_graph = nx.MultiDiGraph()
        for edge in route:
            sub_graph.add_edge(edge[0], edge[1], edge[2], weight=graph.edges[tuple(edge)]['weight'])
        centers_graphs.append(sub_graph)
    return centers_graphs


def first_function(frame, subgraphs_rendered, search_entity, search_relation, max_depth, max_entities, f_entity, f_relation, f_fact):
    entity = r'./dataset/entity2id.txt'
    relate = r'./dataset/relation2id.txt'
    train = r'./dataset/train2id.txt'

    # txt to Dataframe
    pts = get_data(entity)
    relates = get_data(relate)
    weight = [w[2] for w in get_data(train)]

    # define function for replace node label
    def replace_label(name):
        return dict(pts)[name]

    def replace_relate(name):
        return dict(relates)[name]

    node = [n[1] for n in pts]
    edge = get_relation(train)
    G = nx.MultiDiGraph()
    G.add_nodes_from(node)
    G.add_weighted_edges_from(edge)

    # modify the labels
    old_attrs = nx.get_edge_attributes(G, 'weight')
    attrs = {}
    for k, v in old_attrs.items():
        attrs[(k[0], k[1])] = v
    # rs == relationship
    for key, value in attrs.items():
        attrs[key] = {"rs": replace_relate(value)}

    max_num = 2  # 最多的子图数
    centers = get_muticenter(G, ['Tove', 'SweynForkbeard', 'Harthacnut'], max_num)  # 3个中心节点
    for i in range(len(centers)):
        res = breadFirstGraphExtract(G, centers[i], '8', 5, 5)  # 这里可以改成deapfirst， 5是最大深度，15是最大节点数
        draw_sub(centers[i])
        draw_sub(res)

