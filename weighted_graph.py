#打印带权重的无向图
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pymysql


# #打开文件
# f_entity = open('dataset/entity2id.txt', 'r')
# f_relation = open('dataset/relation2id.txt', 'r')
# f_train = open('dataset/train2id.txt', 'r')
#
# #读取全部内容
# #data = f.read()
# #print(data)   #end=''不打印换行空格，print(data, end='')
# # #操作文件
# all_entity = f_entity.readlines()
# all_relation = f_relation.readlines()
# all_train = f_train.readlines()
#
#
# new_entity, new_relation, new_train, feature_1, feature_2, weight = [], [], [], [], [], []
#
# def clear_dataset(dataset, new):
#     for i in dataset:
#         # print(i)
#         first = i.strip('\n')  # 去除\n
#         second = first.split()  # 去除空格
#         new.append(second)  # 连接数据
#
# clear_dataset(all_entity, new_entity)
# new_data = clear_dataset(all_relation, new_relation)
# clear_dataset(all_train, new_train)
#
# for train in new_train:
#     if len(train) != 1:
#         feature_1.append(train[0])
#         feature_2.append(train[1])
#         weight.append(train[2])
# #print(feature_1,feature_2,weight)
#
# #feature_1 = ['Boston', 'Boston', 'Chicago', 'ATX', 'NYC']
# #feature_2 = ['LA', 'SFO', 'LA', 'ATX', 'NJ']
# #score = ['1.00', '0.83', '0.34', '0.98', '0.89']
#
# df = pd.DataFrame({'f1': feature_1, 'f2': feature_2, 'score': weight})
# print(df)
#
# G = nx.from_pandas_edgelist(df=df, source='f1', target='f2', edge_attr='score')
# pos = nx.spring_layout(G, k=10)  # For better example looking
# nx.draw(G, pos, with_labels=True)
# labels = {e: G.edges[e]['score'] for e in G.edges}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
# plt.show()



#创建图变量
G = nx.MultiGraph()  #无向图

#打开文件
f_entity = open('subgraph_v1/entity2id.txt', 'r')
f_relation = open('subgraph_v1/relation2id.txt', 'r')
f_train = open('subgraph_v1/train2id.txt', 'r')

#读取全部内容
#data = f.read()
#print(data)   #end=''不打印换行空格，print(data, end='')
# #操作文件
all_entity = f_entity.readlines()
all_relation = f_relation.readlines()
all_train = f_train.readlines()


new_entity, new_relation, new_train, feature_1, feature_2, weight = [], [], [], [], [], []

def clear_dataset(dataset, new):
    for i in dataset:
        # print(i)
        first = i.strip('\n')  # 去除\n
        second = first.split()  # 去除空格
        new.append(second)  # 连接数据

clear_dataset(all_entity, new_entity)
new_data = clear_dataset(all_relation, new_relation)
clear_dataset(all_train, new_train)

for train in new_train:
    if len(train) != 1:
        feature_1.append(int(train[0]))
        feature_2.append(int(train[2]))
        weight.append(train[1])
#print(feature_1,feature_2,weight)

#print(new_relation)
#print(new_entity)
# for entity in new_entity:
#     if len(entity) != 1:
#         #print(data[1])
#         G.add_node(entity[1])


df = pd.DataFrame({'f1': feature_1, 'f2': feature_2, 'weight': weight})
#print(df)

G = nx.from_pandas_edgelist(df=df, source='f1', target='f2', edge_attr='weight')

# nodes = len(feature_1)
# print("长度是{}", nodes)
# #====================================================
#
# #====================================================
#
pos = nx.spring_layout(G, k=10)
nx.draw(G, pos, with_labels=True)

labels = {e: G.edges[e]['weight'] for e in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
#nx.draw(G, pos)

print (G.get_edge_data(10,12))
# for i in G.nodes:
#     print(i, G.edges(i))
# for train in new_train:
#     if len(train) != 1:
#         #G.add_edge(train[0], train[1])
#         G.add_weighted_edges_from(train[0], train[1], train[2])
#         #print(train[0], train[1], train[2])

print("图的边共有：{}".format(nx.number_of_edges(G)))    #打印图的边数
print("图的点共有：{}".format(nx.number_of_nodes(G)))    #打印图的节点数
print("图的子图共有：{}".format(nx.number_connected_components(G)))    #打印图的联通子图数量
#-------------------------------------------------------------------------
#添加节点
#G.add_nodes_from([1, 2, 3, 4, 5])
#添加边
#G.add_edges_from([(1,2), (1,3), (2,3), (2,4), (3,5), (4,5)])



#可视化
#nx.draw(G, node_size=500, with_labels=True)

#-------------------------------------------------------------------------

plt.show()


#链接数据库
# conn = pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='',
#     db='kit301',
#     charset='utf8'
# )
#
# #创建链接数据库的对象，类似于mysqli
# cursor = conn.cursor()
