#!/usr/bin/env python
# coding: utf-8

# In[4]:


import networkx as nx


# In[5]:


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
  que.append((entity, 1)) # entity, depth
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


# coding:utf-8
from matplotlib import pyplot as plt


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


# path of txt files
entity = r'dataset/entity2id.txt'
relate = r'dataset/relation2id.txt'
train = r'dataset/train2id.txt'

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
# G = nx.DiGraph()
G.add_nodes_from(node)
G.add_weighted_edges_from(edge)

# modify the labels
attrs = nx.get_edge_attributes(G, 'weight')
# rs == relationship
for key, value in attrs.items():
    attrs[key] = {"rs": replace_relate(value)}

# nx.set_edge_attributes(G, edge_labels)
# labels = nx.get_edge_attributes(G, 'relation')
# layout setting
pos = nx.circular_layout(G)
# node
plt.figure(dpi=100,figsize=(24,8))
nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#6495ED')
label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
nx.draw_networkx_labels(G, pos, font_size=9, bbox=label_options)
# edge
nx.draw_networkx_edges(G, pos)
# nx.draw_networkx_edges(G, pos, width=weight)
# nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10)
print(attrs)
# nx.draw_networkx_edge_labels(G, pos, edge_labels=attrs)
plt.axis('off')
plt.show()


# In[23]:


sub = breadFirstGraphExtract(G, 'Harthacnut', '0', 2, 2)


# In[30]:


old_attrs = nx.get_edge_attributes(sub, 'weight')
attrs = {}
for k,v in old_attrs.items():
  attrs[(k[0],k[1])] = v
print(attrs)
# rs == relationship
for key, value in attrs.items():
    attrs[key] = {"rs": replace_relate(value)}
pos = nx.circular_layout(sub)
# node
plt.figure(dpi=100,figsize=(24,8))
nx.draw_networkx_nodes(sub, pos, node_size=400, node_color='#6495ED')
label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
nx.draw_networkx_labels(sub, pos, font_size=9, bbox=label_options)
# edge
nx.draw_networkx_edges(sub, pos)
# nx.draw_networkx_edges(G, pos, width=weight)
# nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10)
nx.draw_networkx_edge_labels(sub, pos, edge_labels=attrs)
plt.axis('off')
plt.show()


# In[ ]:




