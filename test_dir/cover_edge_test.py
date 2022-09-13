import networkx as nx
import matplotlib.pyplot as plt
# G = nx.DiGraph()
# G.add_nodes_from([0,1])
# pos = nx.circular_layout(G)
# nx.draw_networkx_nodes(G, pos,  node_color = 'r', node_size = 100, alpha = 1)
# nx.draw_networkx_edges(G, pos,connectionstyle='arc3, rad = 0.1', edgelist = [(0,1)], width = 2, alpha = 0.5, edge_color='b')
# nx.draw_networkx_edges(G, pos,connectionstyle='arc3, rad = 0.1', edgelist= [(1,0)], width = 1, alpha = 1)
# plt.axis('off')
# plt.show()

G=nx.MultiGraph ([(1,2),(1,2),(1,2),(3,1),(3,2)])
pos = nx.random_layout(G)
nx.draw_networkx_nodes(G, pos, node_color = 'r', node_size = 100, alpha = 1)
ax = plt.gca()
for e in G.edges:
    ax.annotate("",
                xy=pos[e[0]], xycoords='data',
                xytext=pos[e[1]], textcoords='data',
                arrowprops=dict(arrowstyle="->", color="0.5",
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*e[2])
                                ),
                                ),
                )
plt.axis('off')
plt.show()

# G = nx.DiGraph()
# G.add_nodes_from([0,1])
# pos = nx.circular_layout(G)
# nx.draw_networkx_nodes(G, pos, node_color = 'r', node_size = 100, alpha = 1)
# nx.draw_networkx_edges(G, pos, edgelist = [(0,1)], width = 2, alpha = 0.5, edge_color='b')
# nx.draw_networkx_edges(G, pos, edgelist= [(1,0)], width = 1, alpha = 1)
# plt.axis('off')
# plt.show()