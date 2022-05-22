import networkx as nx

# 封装好的方法
G = nx.path_graph(4)  # 存一个图 or DiGraph, MultiGraph, MultiDiGraph, etc
H = G.subgraph([0, 1, 2])  # 需要根据输入的类型修改
list(H.edges)
[(0, 1), (1, 2)]

# Create a subgraph SG based on a (possibly multigraph) G（即选择具体哪条边的时候）
# SG = G.__class__()
# SG.add_nodes_from((n, G.nodes[n]) for n in largest_wcc)
# if SG.is_multigraph():
#     SG.add_edges_from((n, nbr, key, d)
#         for n, nbrs in G.adj.items() if n in largest_wcc
#         for nbr, keydict in nbrs.items() if nbr in largest_wcc
#         for key, d in keydict.items())
# else:
#     SG.add_edges_from((n, nbr, d)
#         for n, nbrs in G.adj.items() if n in largest_wcc
#         for nbr, d in nbrs.items() if nbr in largest_wcc)
# SG.graph.update(G.graph)
#
#
#
# if 111:  h=subgraph(1, 2)
# elif 222: h = subgraph(1, 3)

