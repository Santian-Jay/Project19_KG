import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import *
import numpy as np

G = nx.MultiGraph()  #无向图

#添加节点
G.add_nodes_from([1, 2, 3, 4])
#添加边
G.add_edges_from([(1, 2), (1, 2), (1, 3), (1, 3), (2, 3), (2, 4)])

# #可视化
# nx.draw(G, node_size=500, with_labels=True)
#
# for i in G.nodes:
#     print(i, G.edges(i))
#
# print("图的边共有：{}".format(nx.number_of_edges(G)))    #打印图的边数
# print("图的点共有：{}".format(nx.number_of_nodes(G)))    #打印图的节点数
# print("图的子图共有：{}".format(nx.number_connected_components(G)))    #打印图的联通子图数量


pos = nx.random_layout(G)
#nx.draw_networkx_nodes(G, pos, node_color='r',  node_size=500, alpha=1)
nx.draw(G, pos, node_size=500, with_labels=True)

# 重复边的显示问题
ax = plt.gca()
for e in G.edges:
    ax.annotate("",
                xy=pos[e[0]], xycoords='data',
                xytext=pos[e[1]], textcoords='data',
                arrowprops=dict(arrowstyle="-", color="0.5",
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle="arc3, rad=rrr".replace('rrr', str(0.3*e[2])
                                                                        ),
                                ),
                )

print (G.get_edge_data(1,2))
plt.axis('off')
plt.show()


# #获取图的邻接矩阵
# As = nx.adjacency_matrix(G)
# print(As)
#
# #将邻接矩阵转化为二维数组形式的矩阵
# A = As.todense()
# print(A)
#
# #已知图的邻接矩阵，创建图
# # a_np = np.array([[0,1,1], [1,0,1], [1,1,0]])
# # g_np = nx.from_numpy_matrix(a_np)
# # nx.draw(g_np, node_size=500, with_labels=True)
#
#加权图
# g_wd = nx.Graph()
# g_wd.add_weighted_edges_from([(0,1,1.0), (1,2,7.5), (0,2,5)])
# a_wd = nx.adjacency_matrix(g_wd)
# #print(a_wd.todense())
# pos = nx.spring_layout(g_wd, 10)
# w = [g_wd[e[0]][e[1]]['weight'] for e in g_wd.edges()]
# #labels = {e: g_wd[e]['weight'] for e in g_wd.edges}
# nx.draw(g_wd, width=w, node_size=500, with_labels=True)
#nx.draw_networkx_edge_labels(g_wd, edge_labels=labels)
#
# #有向图
# g_d = nx.DiGraph()
# #添加节点
# g_d.add_nodes_from([1, 2, 3, 4])
# #添加边
# g_d.add_edges_from([(1,2), (1,3), (2,3), (3,4)])
# nx.draw(g_d, node_size=500, with_labels=True)

plt.show()