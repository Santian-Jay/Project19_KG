import itertools

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
new = []
nodeNumber = 8
routeDic = {}
allRoutes = []
sign, residue = [], []
numberOfEdges = 0
count = 0
searchList = [0, 1, 4, 3, 5]
all_shortest_path = {}
tempList = []
used_routes = []
all_sub = []
temp1 = []
big_dic = {}
relatesDic = {}
entityDic = {}
neighborNode = {}

# entity = r'./dataset/YAGO3-10/entity2id.txt'
# relate = r'./dataset/YAGO3-10/relation2id.txt'
entity = r'./dataset/entity2id.txt'
relate = r'./dataset/relation2id.txt'

def get_relate(file):
    with open(file, 'r', encoding='UTF-8') as f:
        next(f)
        for line in f:
            name, index = line.strip().split()
            relatesDic[int(index)] = name


def get_entity(file):
    with open(file, 'r', encoding='UTF-8') as f:
        next(f)
        for line in f:
            name, index = line.strip().split()
            entityDic[int(index)] = name


get_relate(relate)
get_entity(entity)

def create_path(graph, list1):
    temp = []

    for i in range(len(list1) - 1):
        graph.add_node(entityDic[list1[i]])
        #nx.draw_networkx_nodes(graph, node_color='r')
        if i < len(list1) - 1:
            if (list1[i], list1[i+1]) in big_dic:
                temp.append((list1[i], list1[i+1]))
            else:
                temp.append((list1[i+1], list1[i]))
    # pos = nx.circular_layout(graph)
    # nx.draw_networkx_nodes(graph, pos, node_color='r')
    for item in list1:
        addCount = 0
        for item2 in big_dic:
            if item in item2:
                if item2 not in temp:
                    if addCount < 4:
                        temp.append(item2)
                        addCount += 1
                    else:
                        break
    return temp



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
file = open("dataset/train2id.txt", "r", encoding='UTF-8')

entryNumber = (int)(file.readline())
G = nx.path_graph(1)
for index in range(entryNumber):
    content = file.readline()
    head, tile, relation = content.strip().split()
    big_dic[(int(head), int(tile))] = int(relation)
    # big_dic[(head, tile)].append(relation)
    nx.add_path(G, [int(head), int(tile)])
    addEdge(int(head), int(tile))


def printRoute(stackList):
    global nodeNumber
    nodeNumber += 1
    G.node(str(nodeNumber), stackList[0])
    for node in stackList[1:]:
        nodeNumber += 1
        G.node(str(nodeNumber), node)
        G.edge(str(nodeNumber - 1), str(nodeNumber))


# def findAllRoutes(start, end):
#     global total, new, stack, count
#     stack.append(start)
#     if total >= 1:
#         if start == end:
#             print('找到路径： ', stack)
#             # new = []
#             for i in stack:
#                 new.append(i)
#             allRoutes.append(new)
#             stack.pop()
#             # total -= 1
#         else:
#             for nextPoint in edgeLinks[start]:
#                 if nextPoint not in stack: findAllRoutes(nextPoint, end)
#             stack.pop()

def findAR(start, end):
     global graph, sign
     stack1 = []
     Sign()
     stack1.append(start)
     while len(stack1) != 0:
         top = stack1[-1]
         le = len(graph[top])
         for i in graph[top]:
             dst = graph[top].index(i)
             if sign[top][dst] == 0 and i not in stack1:
                 stack1.append(i)
                 sign[top][dst] = 1
                 break

         if end in stack1:
            print('stack1 is:  ', stack1)
            stack1.pop()
            continue
         last = stack1[-1]
         if last == top:
             sign[top] = [0] * le
             stack1.pop()


def Sign():
    global sign, residue
    for i in  range(0,entryNumber):
        le = len(residue[i])
        sign[i] = [0] * le


# all_pairs = list(itertools.combinations(searchList, 2))
# print(all_pairs)
# for item in all_pairs:
#     all_shortest_path[(item)] = []
#     print('计算图中节点%d到节点%d的所有最短路径: %s' % (item[0], item[1], [p for p in nx.all_shortest_paths(G, source=item[0], target=item[1])]))
#     for q in nx.all_shortest_paths(G, source=item[0], target=item[1]):
#         # allRoutes.append(q)
#         all_shortest_path[(item)].append(q)


# print(allRoutes)
# print(all_shortest_path[(0, 4)])
# for p in nx.all_shortest_paths(G, source=0, target=4):
#     allRoutes.append(p)
#     create_path(p)
# print(temp1)
# print(allRoutes)
# print(len(all_shortest_path[(0, 4)]))

# print('计算图中节点%d到节点%d的所有最短路径: %s' % (0, 4, [p for p in nx.all_shortest_paths(G, source=0, target=4)]))
a = {}
# print('all_simple_edge_paths')
# # for path in sorted(nx.all_simple_edge_paths(G, 0, 4)):
# for path in nx.all_simple_edge_paths(G, 0, 4):
#     print(path)
#     a.append(path)



# print('all_simple_paths')
# print('all_simple_paths')
# for path in nx.all_simple_paths(G, 0, 4):
#     print(path)

print('shortest_simple_paths')
if nx.has_path(G, 3, 5):
    for path in nx.shortest_simple_paths(G, 3, 5):
        print(path)
        if path[1] not in a:
            if len(a) < 5:
                a[path[1]] = []
                a[path[1]].append(path)
            else:
                break
    length = 0
    for item in a:
        length = length + len(a[item])
    if length < 5 and len(a) < 5:
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

graphList = []
# for i in range(5):
#     sub_graph = nx.MultiDiGraph()
#     graphList.append(sub_graph)

for p in a:
    sub_graph = nx.MultiDiGraph()
    graphList.append(sub_graph)
    if len(a[p]) > 1:
        for item in a[p]:
            all_sub.append(create_path(sub_graph, item))
    else:
        all_sub.append(create_path(sub_graph, a[p][0]))



print('neighbor: ', neighborNode)
# for p in a:
#     if len(a[p]) > 1:
#         for item in a[p]:
#             all_sub.append(create_path(item))
#     else:
#         # print('current path is: ', a[path])
#         # temp2 = create_path(a[p][0])
#         all_sub.append(create_path(a[p][0]))
#         # print(create_path(a[p][0]))


    # print(path)
# for i in all_shortest_path:
#     print(i[0])
# for p in allRoutes:
#     if ()
print(len(a))
print(a)
print('all path')
print(all_sub)
# print(big_dic)





def draw_sub(sub, index):
    old_attrs = nx.get_edge_attributes(sub, 'weight')
    attrs = {}
    for k, v in old_attrs.items():
         attrs[(k[0], k[1])] = v
    # rs == relationship
    # for key, value in attrs.items():
    #     attrs[key] = replace_relate(value)
    pos = nx.circular_layout(sub)
    # node
    plt.figure(dpi=160, figsize=(12, 8))
    nx.draw_networkx_nodes(sub, pos, node_size=400, node_color='#6495ED')
    label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
    nx.draw_networkx_labels(sub, pos, font_size=10, bbox=label_options)
    # edge
    nx.draw_networkx_edges(sub, pos)

    nx.draw_networkx_edge_labels(sub, pos, edge_labels=attrs)
    plt.axis('off')
    save_path = 'subgraph_images/picture-{}.png'.format(index + 1)
    plt.savefig(save_path)



for g in range(len(all_sub)):
    for i in all_sub[g]:
        reverse = tuple(reversed(i))
        if i not in big_dic:
            r = big_dic[reverse]
            graphList[g].add_edge(entityDic[reverse[0]], entityDic[reverse[1]], weight=relatesDic[r])
        else:
            r = big_dic[i]
            graphList[g].add_edge(entityDic[i[0]], entityDic[i[1]], weight=relatesDic[r])
            # graphList[g].add_edge(i[0], i[1], weight=relatesDic[r])
    draw_sub(graphList[g], g)



# plt.show()
# for i in range(len(searchList)):
#     start = searchList[i]
#     for j in range(len(searchList)):
#         end = searchList[j]
#         if start != end:
#             print('计算图中节点%d到节点%d的所有最短路径: %s' % (start, end, [p for p in nx.all_shortest_paths(G, source=start, target=end)]))

# for item in searchList:
#     for left in searchList:
#         if item != left:
#             print('计算图中节点0到节点4的所有最短路径: ', [p for p in nx.all_shortest_paths(G, source=item, target=left)])

# G.add_path(1, 2)
# G.add_path(2, 3)
# G.add_path(4, 5)
# print(G.has_path(G, 0, 2))
# print('0节点到4节点最短路径: ', nx.shortest_path(G, source=0, target=4))
# p1 = nx.shortest_path(G, source=5)
# print('0节点到所有节点最短路径: ', p1)
# print('计算图中节点0到节点4的所有最短路径: ', [p for p in nx.all_shortest_paths(G, source=0, target=4)])
# for q in nx.all_shortest_paths(G, source=0, target=4):
#     allRoutes.append(q)
# pos = nx.circular_layout(G)
# nx.draw(G, with_labels=True)
# findAllRoutes(0, 4)
# print(nx.has_path(G, 0, 4))
# print(allRoutes)
# print('total numberOfEdges', numberOfEdges)
# print('number_of_edges', nx.number_of_edges(G))
# print('number_of_nodes', nx.number_of_nodes(G))
# print('all routes list', allRoutes)
# print('edgelinks ', edgeLinks)
# As_1 = nx.adjacency_matrix(G, weight=None)
# A_1 = As_1.todense()
# print(A_1)
# result = np.sum(A_1, axis=1)
# result_1 = np.sum(A_1, axis=0)
# print(result)
# print(result_1)
# print(in_degree)
# print(out_degree)

# all_path = open("path.txt", "w")
# all_path.write("%s" % "aaa")

# plt.show()

# print(G.path.bidirectional_dijkstra(G, 1, 2))
# shortest_path(G, 1, 3)
# for index in range(entryNumber):
#     content = file.readline()
#     head, tile, relation = content.strip().split()
#     G.add_edge(int(head), int(tile))

# G.has_path(G, 84050, 70790)

# for item in big_dic:
#     # if 12 in item:
#     print(item)

# temp2 = []
# for item in [3, 9, 6, 5]:
#     addCount = 0
#     print('current number is: ', item)
#     for item2 in big_dic:
#         if item in item2:
#             # if item2 not in temp2 and addCount < 5:
#             if item2 not in temp2:
#                 print('current item2 is: ', item2)
#                 if addCount < 4:
#                     temp2.append(item2)
#                     addCount += 1
#                 else:
#                     # addCount = 0
#                     print('current temp2 is: ', temp2)
#                     break
# print(temp2)
