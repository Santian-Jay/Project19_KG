import pymysql
import networkx as nx
import matplotlib.pyplot as plt


G = nx.MultiGraph()  # multiple graph

# open file
f_entity = open('subgraph_v1/entity2id.txt', 'r')
f_relation = open('subgraph_v1/relation2id.txt', 'r')
f_train = open('subgraph_v1/train2id.txt', 'r')
f_test = open('dataset/test2id.txt', 'r')

# read all data
# data = f.read()
# #process data
all_entity = f_entity.readlines()
all_relation = f_relation.readlines()
all_train = f_train.readlines()
all_test = f_test.readlines()


new_entity, new_relation, new_train, feature_1, feature_2, weight, new_test = [], [], [], [], [], [], []

def clear_dataset(dataset, new):
    for i in dataset:
        # print(i)
        first = i.strip('\n')  # delete \n
        second = first.split()  # delete space
        new.append(second)  # add data into list

clear_dataset(all_entity, new_entity)
new_data = clear_dataset(all_relation, new_relation)
clear_dataset(all_train, new_train)
clear_dataset(all_test, new_test)


for train in new_train:
    if len(train) != 1:
        feature_1.append(train[0])
        feature_2.append(train[1])
        weight.append(train[2])
#print(feature_1,feature_2,weight)

# for test in new_test:
#     if len(test) != 1:
#         feature_1.append(test[0])
#         feature_2.append(test[1])
#         weight.append(test[2])

#print(new_relation)
#print(new_entity)
for entity in new_entity:
    if len(entity) != 1:
        #print(data[1])
        G.add_node(entity[1])

for train in new_train:
    if len(train) != 1:
        G.add_edge(train[0], train[1])
        #print(train[0], train[1], train[2])
nx.draw(G, node_size=500, with_labels=True)

print("graph has：{} edges".format(nx.number_of_edges(G)))    # print number of edge
print("graph has：{} nodes".format(nx.number_of_nodes(G)))    # print number of node
print("graph has：{} subgraph".format(nx.number_connected_components(G)))    # print number of connected subgraph

print(G.get_edge_data(10,12))


plt.show()


# connected database
conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='kit301',  # database used
    charset='utf8'
)

# Create an object linked to a database, similar to mysqli
cursor = conn.cursor()
