import networkx as nx
import sys
sys.setrecursionlimit(400000)
import matplotlib.pyplot as plt
import numpy as np
from graphviz import Digraph

total = 10
edgeLinks = dict()
in_degree = dict()
out_degree = dict()
stack = []
nodeNumber = 8
routeDic = {}
allRoutes = []
sign, residue = [], []
numberOfEdges = 0
subGraph = {}

def addEdge(a, b):
    global numberOfEdges
    numberOfEdges += 1
    # global edgeLinks
    if a not in edgeLinks: edgeLinks[a] = set()
    if b not in edgeLinks: edgeLinks[b] = set()
    if a not in in_degree: in_degree[a] = 0
    if b not in in_degree: in_degree[b] = 0
    if a not in out_degree: out_degree[a] = 0
    if b not in out_degree: out_degree[b] = 0
    edgeLinks[a].add(b)
    edgeLinks[b].add(a)
    in_degree[b] += 1
    out_degree[a] += 1
# file = open("dataset/YAGO3-10/train2id.txt", "r", encoding='UTF-8')

# entryNumber = (int)(file.readline())
G = nx.path_graph(1)

# for index in range(entryNumber):
#     content = file.readline()
#     head, tile, relation = content.strip().split()
#     nx.add_path(G, [int(head), int(tile)])
#     addEdge(int(head), int(tile))


def printRoute(stackList):
    global nodeNumber
    nodeNumber += 1
    G.node(str(nodeNumber), stackList[0])
    for node in stackList[1:]:
        nodeNumber += 1
        G.node(str(nodeNumber), node)
        G.edge(str(nodeNumber - 1), str(nodeNumber))


def findAllRoutes(start, end):
    global total
    stack.append(start)
    # print('current stack is: ', stack)
    if total >= 1:
        if start == end:
            print('找到路径： ', stack)
            stack.pop()
            total -= 1
        else:
            for nextPoint in edgeLinks[start]:
                if nextPoint not in stack: findAllRoutes(nextPoint, end)
            stack.pop()

# def findAR(start, end):
#      global graph, sign
#      stack1 = []
#      Sign()
#      stack1.append(start)
#      while len(stack1) != 0:
#          top = stack1[-1]
#          le = len(graph[top])
#          for i in graph[top]:
#              dst = graph[top].index(i)
#              if sign[top][dst] == 0 and i not in stack1:
#                  stack1.append(i)
#                  sign[top][dst] = 1
#                  break
#
#          if end in stack1:
#             print('stack1 is:  ', stack1)
#             stack1.pop()
#             continue
#          last = stack1[-1]
#          if last == top:
#              sign[top] = [0] * le
#              stack1.pop()


# def Sign():
#     global sign, residue
#     for i in  range(0,entryNumber):
#         le = len(residue[i])
#         sign[i] = [0] * le
G.add_edge(1, 2)
G.add_edge(1, 5)
G.add_edge(1, 6)
G.add_edge(1, 7)
G.add_edge(1, 17)
G.add_edge(2, 3)
G.add_edge(2, 8)
G.add_edge(2, 9)
G.add_edge(2, 10)
G.add_edge(3, 4)
G.add_edge(3, 11)
G.add_edge(3, 12)
G.add_edge(3, 13)
G.add_edge(4, 14)
G.add_edge(4, 15)
G.add_edge(4, 16)
G.add_edge(4, 17)
G.add_edge(4, 6)
G.add_edge(4, 18)
G.add_edge(18, 3)
G.add_edge(19, 2)
G.add_edge(19, 1)
G.add_edge(3, 1)
# G.add_edge(11, 5)
# G.add_edge(12, 5)
# G.add_edge(13, 5)
# G.add_edge(4, 1)
print('计算图中节点1到节点4的所有最短路径: ', [p for p in nx.all_shortest_paths(G, source=4, target=1)])
print('计算图中节点2到节点4的所有最短路径: ', [p for p in nx.all_shortest_paths(G, source=4, target=2)])
# print('0节点到4节点最短路径: ', nx.shortest_path(G, source=0, target=4))
# p1 = nx.shortest_path(G, source=5)
# print('0节点到所有节点最短路径: ', p1)
# print('计算图中节点0到节点4的所有最短路径: ', [p for p in nx.all_shortest_paths(G, source=0, target=4)])
# for q in nx.all_shortest_paths(G, source=0, target=4):
#     allRoutes.append(q)
pos = nx.circular_layout(G)
nx.draw(G, with_labels=True)
# findAllRoutes(0, 4)
print(nx.has_path(G, 0, 4))
# print(nx.all_simple_edge_paths(G, 1, 4))
# for path in sorted(nx.all_simple_edge_paths(G, 1, 4)):
# for path in nx.all_simple_edge_paths(G, 1, 4):
    # print(path)

# print('all_simple_edge_paths')
# # for path in sorted(nx.all_simple_edge_paths(G, 0, 4)):
# for path in nx.all_simple_edge_paths(G, 1, 4):
#     print(path)
#
# # print('all_simple_paths')
# print('all_simple_paths')
# for path in nx.all_simple_paths(G, 1, 4):
#     print(path)

a = {}
print('shortest_simple_paths')
for path in nx.shortest_simple_paths(G, 3, 5):
    print(path)
    if path[1] not in a:
        if len(a) < 5:
            a[path[1]] = []
            a[path[1]].append(path)
        else:
            break
length = 0
for path in nx.shortest_simple_paths(G, 3, 5):
    if len(a) < 5:
        for i in a:
            if path != a[i][0]:
                if i == path[1]:
                    if length < 5:
                        a[path[1]].append(path)
                    for item in a:
                        length = length + len(a[item])
                    break

print(len(a))
print(a)


# print(len(a[2]))
# print(allRoutes)
# print('total numberOfEdges', numberOfEdges)
# print('number_of_edges', nx.number_of_edges(G))
# print('number_of_nodes', nx.number_of_nodes(G))
# print('all routes list', allRoutes)
# print('edgelinks ', edgeLinks)
# print(in_degree)
# print(out_degree)

plt.show()

