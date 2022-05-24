#coding: utf-8
#!/usr/bin/env python
"""
Draw a graph with matplotlib.
You must have matplotlib for this to work.
"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
#    Copyright (C) 2004-2008
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#raise的使用要求这一步必须运行
try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx

a = 251
b = 252
c = 253
d = 254
e = 255
f = 256
g = 257
h = 258

G1 = nx.MultiDiGraph()   #multiple directed graph

# G.add_nodes_from([1, 2, 3, 4, 5, 6])
#
# G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (3, 6), (5, 6)])

G1.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f'])

G1.add_edges_from([('a', 'b'), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'd'), ('c', 'e'), ('c', 'f'), ('e', 'f')])

pos = nx.random_layout(G1)

plt.subplot(a)
nx.draw(G1, pos, node_size=500, with_labels=True)
plt.subplot(b)
nx.draw(G1, pos, node_size=400, with_labels=True, node_color="r")
plt.subplot(c)
nx.draw(G1, pos, node_size=600, with_labels=True, node_color="g")
plt.subplot(d)
nx.draw(G1, pos, node_size=500, with_labels=True, node_color="b")


#用grid_2d_graph()生成一个16个节点的网格图
G=nx.grid_2d_graph(4,4)  #4x4 grid
pos=nx.spring_layout(G,iterations=100)
#開始画各个小图
plt.subplot(e)
nx.draw(G,pos,font_size=8)
plt.subplot(f)
nx.draw(G,pos,node_color='k',node_size=0,with_labels=False)
plt.subplot(g)
nx.draw(G,pos,node_color='g',node_size=250,with_labels=False,width=6)
#最后一幅子图转为有向图
plt.subplot(h)
H=G.to_directed()
nx.draw(H,pos,node_color='b',node_size=20,with_labels=False)
plt.savefig("four_grids.png")
plt.show()

# import numpy as np
#
# import matplotlib.pyplot as plt
#
#
#
# x = np.arange(0, 100)
#
# fig = plt.figure(figsize=(12,12), facecolor='blue')
#
# #划分子图
#
# fig,axes = plt.subplots(3,3)
#
# ax1 = axes[0, 0]
#
# ax2 = axes[0, 1]
#
# ax3 = axes[1, 0]
#
# ax4 = axes[1, 1]
#
#
#
# #作图1
#
# ax1.plot(x, x)
#
# #作图2
#
# ax2.plot(x, x)
#
# #作图3
#
# ax3.plot(x, x ** 2)
#
# ax3.grid(color='r', linestyle='--', linewidth=1, alpha=0.3)
#
# #作图4
#
# ax4.plot(x, 4*x)
#
# plt.show()
#
# plt.savefig('1.png')