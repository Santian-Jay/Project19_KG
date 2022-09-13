import networkx as nx
import sys
sys.setrecursionlimit(400000)
import matplotlib.pyplot as plt
import numpy as np
from graphviz import Digraph

def subgraph_extra(p1, p2, p3, entity_list, max_n):
    print('eneity: ', p1)
    print('relation: ', p2)
    print('train: ', p3)
# def subgraph_extra(path, entity_list):
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


# def subgraph_extra(entity_file, relation_file, train_file):

    # entity = r'./dataset/entity2id.txt'
    # relate = r'./dataset/relation2id.txt'
    # file = open("dataset/train2id.txt", "r", encoding='UTF-8')
    start = int(entity_list[0])
    end = int(entity_list[1])

    # entity_path = path + '/entity2id.txt'
    # relation_path = path + '/relation2id.txt'
    # train_path = path + '/train2id.txt'


    entity_path = p1
    relation_path = p2
    train_path = p3

    entity = open(entity_path, "r", encoding='UTF-8')
    relate = open(relation_path, "r", encoding='UTF-8')
    file = open(train_path, "r", encoding='UTF-8')

    # entity = r'./dataset/entity2id.txt'
    # relate = r'./dataset/relation2id.txt'

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


    get_relate(relation_path)
    get_entity(entity_path)


    def create_path(graph, list1):
        n_nodes = len(list1)
        temp = []
        for i in range(len(list1) - 1):
            graph.add_node(entityDic[list1[i]])
            if i < len(list1) - 1:
                if (list1[i], list1[i + 1]) in big_dic:
                    temp.append((list1[i], list1[i + 1]))
                else:
                    temp.append((list1[i + 1], list1[i]))
        # for item in list1:
        #     addCount = 0
        #     for item2 in big_dic:
        #         if item in item2:
        #             # if len(big_dic[item2]) == 1:
        #             if item2 not in temp:
        #                 if addCount < 4:
        #                     temp.append(item2)
        #                     addCount += 1
        #                 else:
        #                     break
        for i in range(max_n - n_nodes):
            if len(list1) < max_n:
                for item in list1:
                    if len(list1) < max_n:
                        for item2 in big_dic:
                            if item in item2:
                                if item2 not in temp:
                                    temp.append(item2)
                                    for number in item2:
                                        if number not in list1:
                                            list1.append(number)
                                    break
                    else:
                        break
            else:
                break
        return temp


    def addEdge(a, b):
        # global numberOfEdges
        # numberOfEdges += 1
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


    entryNumber = (int)(file.readline())
    G = nx.path_graph(1)
    for index in range(entryNumber):
        content = file.readline()
        head, tile, relation = content.strip().split()
        if (int(head), int(tile)) not in big_dic:
            big_dic[(int(head), int(tile))] = [int(relation)]
        else:
            big_dic[(int(head), int(tile))].append(int(relation))
        nx.add_path(G, [int(head), int(tile)])
        addEdge(int(head), int(tile))
    print(len(big_dic))
    print(big_dic)
    a = {}  # save path list, index is neighbors of start entity

    print('shortest_simple_paths')
    if nx.has_path(G, start, end):
        for path in nx.shortest_simple_paths(G, start, end):
            print(path)
            if len(path) < 5:
                if path[1] not in a:
                    if len(a) < 5:
                        a[path[1]] = []
                        a[path[1]].append(path)
                    else:
                        break
            else:
                break
        length = 0
        for item in a:
            length = length + len(a[item])
        if length < 5 and len(a) < 5:
            # length = 0
            for path in nx.shortest_simple_paths(G, start, end):
                # print(path)
                if length < 5:
                    for i in a:
                        if path != a[i][0]:
                            if i == path[1]:
                                if length < 5:
                                    a[path[1]].append(path)
                                length = 0
                                for item in a:
                                    length = length + len(a[item])
                                break
                else:
                    break
    print('a', a)
    graphList = []

    # expand every path as a graph
    for p in a:
        if len(a[p]) > 1:
            for item in a[p]:
                sub_graph = nx.MultiDiGraph()
                graphList.append(sub_graph)
                all_sub.append(create_path(sub_graph, item))
        else:
            sub_graph = nx.MultiDiGraph()
            graphList.append(sub_graph)
            all_sub.append(create_path(sub_graph, a[p][0]))



    #
    #
    #
    # # print('neighbor: ', neighborNode)
    # # print(len(a))
    # print(a)
    # # print('all path')
    # # print(all_sub)
    # print('big_dic: ', big_dic)
    # print('big_dic length: ', len(big_dic))
    #
    #
    #
    #
    #
    def draw_sub(sub, index):
        old_attrs = nx.get_edge_attributes(sub, 'weight')
        attrs = {}
        temp_dic = {}
        for k, v in old_attrs.items():
            if (k[0], k[1]) not in attrs:
                attrs[(k[0], k[1])] = v
            else:
                attrs[(k[0], k[1])] = attrs[(k[0], k[1])] + ' / ' + v
                # temp_dic[(k[0], k[1])] = 0
                temp_dic[k] = 0
        pos = nx.circular_layout(sub)

        # pos = nx.spring_layout(sub, k=10)
        # node
        plt.figure(dpi=120, figsize=(12, 8))
        nx.draw_networkx_nodes(sub, pos, node_size=400, node_color='#6495ED')
        label_options = {"ec": "k", "fc": "white", "alpha": 0.3}
        nx.draw_networkx_labels(sub, pos, font_size=10, bbox=label_options)

        ax = plt.gca()
        # for e in sub.edges:
        for e in temp_dic:
            print('e: ', e)
            # if e not in temp_dic:
            #     temp_dic[e] = 0
            ax.annotate("",
                        xy=pos[e[0]], xycoords='data',
                        xytext=pos[e[1]], textcoords='data',
                        arrowprops=dict(arrowstyle="<-", color="0.5",
                                        shrinkA=5, shrinkB=5,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3, rad=rrr".replace('rrr', str(0.5 * e[2])
                                                                                ),
                                        ),
                        )
        # edge
        nx.draw_networkx_edges(sub, pos)
        nx.draw_networkx_edge_labels(sub, pos, edge_labels=attrs)

        # print duplicate edges

        plt.axis('off')
        plt.tight_layout()
        save_path = 'subgraph_images/picture-{}.png'.format(index + 1)
        plt.savefig(save_path)


    for g in range(len(all_sub)):
        for i in all_sub[g]:
            reverse = tuple(reversed(i))
            if i not in big_dic:
                # r = big_dic[reverse]
                # graphList[g].add_edge(entityDic[reverse[0]], entityDic[reverse[1]], weight=relatesDic[r])
                if len(big_dic[i]) == 1:
                    r = big_dic[i][0]
                    graphList[g].add_edge(entityDic[i[0]], entityDic[i[1]], weight=relatesDic[r])
                else:
                    for relation in big_dic[i]:
                        graphList[g].add_edge(entityDic[i[0]], entityDic[i[1]], weight=relatesDic[relation])
            else:
                if len(big_dic[i]) == 1:
                    r = big_dic[i][0]
                    graphList[g].add_edge(entityDic[i[0]], entityDic[i[1]], weight=relatesDic[r])
                else:
                    for relation in big_dic[i]:
                        graphList[g].add_edge(entityDic[i[0]], entityDic[i[1]], weight=relatesDic[relation])
        draw_sub(graphList[g], g)

# subgraph_extra('D:\PyCharm\pythonProject\pythonProject_v5\dataset', 0, 4)