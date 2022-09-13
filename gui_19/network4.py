from subgraph import *
import networkx as nx
import os
from matplotlib import pyplot as plt
import numpy as np
from subgraph.subgraph import get_neighbor_nodes


def subgraph_extraction_labeling_pro(ind, A_list, h=1, enclosing_sub_graph=False, max_nodes_per_hop=None, max_node_label_value=None):
    # extract the h-hop enclosing subgraphs around link 'ind'
    A_incidence = incidence_matrix(A_list)
    A_incidence += A_incidence.T

    roots_nei = [get_neighbor_nodes(set([ind[0]]), A_incidence, h, max_nodes_per_hop) for i in range(len(ind))]

    subgraph_nei_nodes_int = roots_nei[0]
    subgraph_nei_nodes_un = roots_nei[0]

    for i in range(1, len(ind)):
        subgraph_nei_nodes_int &= roots_nei[i]
        subgraph_nei_nodes_un |= roots_nei[i]


    # Extract subgraph | Roots being in the front is essential for labelling and the model to work properly.
    if enclosing_sub_graph:
        subgraph_nodes = list(ind) + list(subgraph_nei_nodes_int)
    else:
        subgraph_nodes = list(ind) + list(subgraph_nei_nodes_un)

    return subgraph_nodes


def incidence_matrix_weight1(adj_list):
    '''
    adj_list: List of sparse adjacency matrices
    '''

    rows, cols, dats = [], [], []
    dim = adj_list[0].shape
    for adj in adj_list:
        adjcoo = adj.tocoo()
        rows += adjcoo.row.tolist()
        cols += adjcoo.col.tolist()
        dats += adjcoo.data.tolist()
    row = np.array(rows)
    col = np.array(cols)
    data = np.array(dats)
    temp_m =  ssp.csc_matrix((data, (row, col)), shape=dim)
    adjcoo = temp_m.tocoo()
    rows = adjcoo.row.tolist()
    cols = adjcoo.col.tolist()
    row = np.array(rows)
    col = np.array(cols)
    data = np.ones(row.shape)
    return ssp.csc_matrix((data, (row, col)), shape=dim)

def preprocess_func(task_dir, centers, hop=3):

    loader = DataLoader(task_dir, 1)
    n_ent, n_rel = loader.graph_size()
    train_data = loader.load_data('train')
    valid_data = loader.load_data('valid')
    test_data = loader.load_data('test')
    adj_list = []
    triplets = []
    adj_weight_list = []
    for i in range(len(train_data[0])):
        triplets.append([train_data[0][i], train_data[1][i], train_data[2][i]])
    triplets = np.array(triplets)
    for i in range(n_rel):
        idx = np.argwhere(triplets[:, 2] == i)
        adj_list.append(csc_matrix((np.ones(len(idx), dtype=np.uint8),
                                    (triplets[:, 0][idx].squeeze(1), triplets[:, 1][idx].squeeze(1))),
                                    shape=(n_ent, n_ent)))
    for i in range(n_rel):
        idx = np.argwhere(triplets[:, 2] == i)
        adj_weight_list.append(csc_matrix((np.full(len(idx),fill_value=i, dtype=np.uint8),
                                    (triplets[:, 0][idx].squeeze(1), triplets[:, 1][idx].squeeze(1))),
                                    shape=(n_ent, n_ent)))


    nodes = subgraph_extraction_labeling_pro(centers, adj_list, hop, True, None)

    adj = incidence_matrix_weight1(adj_list)
    adj = adj[nodes, :][:, nodes]
    adj_weight_list = [m[nodes, :][:, nodes] for m in adj_weight_list]

    return nodes, adj, adj_weight_list


def get_relation_id(adj_list, node1, node2):
    for i in range(len(adj_list)):
        if adj_list[i][node1,node2] > 0 or adj_list[i][node2,node1]:
            return i
    return 0

def get_muticenter(graph, adj_weight_list, centers, max_graph_num):
    centers_graphs = []
    routes = [[]]
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            new_routes = []
            for route in routes:
                if nx.has_path(graph, centers[i], centers[j]):
                    for k, path in enumerate(nx.shortest_simple_paths(graph, centers[i], centers[j])):
                        if k >= max_graph_num:
                            break
                        new_routes.append(route + path)

                if nx.has_path(graph, centers[j], centers[i]):
                    for k, path in enumerate(nx.shortest_simple_paths(graph, centers[j], centers[i])):
                        if k >= max_graph_num:
                            break
                        new_routes.append(route + path)
            routes = new_routes
    for i, route in enumerate(routes):
        if i >= max_graph_num:
            break
        sub_graph = nx.MultiDiGraph()
        for i in range(len(route)-1):
            sub_graph.add_edge(route[i], route[i+1], weight=get_relation_id(adj_weight_list, route[i], route[i+1]))
        centers_graphs.append(sub_graph)
    return centers_graphs

def breadFirstGraphExtract(graph, sub_graph, adj_weight_list, relation, max_depth, max_entity_num):
    if max_entity_num <= 0:
        return sub_graph
    que = []  # entity, depth
    for node in sub_graph.nodes:
        que.append((node, 1))
    while que:
        temp_tuple = que.pop(0)
        temp_entity, temp_depth = temp_tuple[0], temp_tuple[1]
        if nx.number_of_nodes(sub_graph) >= max_entity_num:
            return sub_graph
        if temp_depth >= max_depth:
            continue
        for n in graph.adj[temp_entity].keys():
            rel_ = get_relation_id(adj_weight_list, temp_entity, n)
            if rel_ in relation:
                sub_graph.add_edge(temp_entity, n, weight=rel_)
                que.append((n, temp_depth+1))
            if nx.number_of_nodes(sub_graph) >= max_entity_num:
                return sub_graph
    return sub_graph
def deepFirstGraphExtract(graph, sub_graph, adj_weight_list, relation, max_depth, max_entity_num):
    if max_entity_num <= 0:
        return sub_graph
    stack = []  # entity, depth
    for node in sub_graph.nodes:
        stack.append((node, 1))
    while stack:
        temp_tuple = stack.pop()
        temp_entity, temp_depth = temp_tuple[0], temp_tuple[1]
        if nx.number_of_nodes(sub_graph) >= max_entity_num:
            return sub_graph
        if temp_depth >= max_depth:
            continue
        for n in graph.adj[temp_entity].keys():
            rel_ = get_relation_id(adj_weight_list, temp_entity, n)
            if rel_ in relation:
                sub_graph.add_edge(temp_entity, n, weight=rel_)
                stack.append((n, temp_depth+1))
            if nx.number_of_nodes(sub_graph) >= max_entity_num:
                return sub_graph
    return sub_graph

def get_id2relation(file, encoding='utf-8'):
    id2relation = {}
    with open(file, 'r', encoding=encoding) as f:
        next(f)
        for i, line in enumerate(f):
            d=line.split()
            id2relation[int(d[1])] = d[0]
    return id2relation

def get_id2entity(file, encoding='utf-8'):
    id2entity = {}
    with open(file, 'r', encoding=encoding) as f:
        next(f)
        for i, line in enumerate(f):
            d=line.split()
            id2entity[int(d[1])] = d[0]
    return id2entity

def draw_graph(graph, id2entity, id2relation, index):
    old_edge_labels = nx.get_edge_attributes(graph, 'weight')

    edge_labels = {}
    for k, v in old_edge_labels.items():
        edge_labels[(k[0], k[1])] = id2relation[int(v)]

    node_labels = {}
    for n in graph.nodes():
        node_labels[n] = id2entity[n]
    pos = nx.circular_layout(graph)
    # node
    plt.figure(dpi=100, figsize=(12, 8))
    nx.draw_networkx_nodes(graph, pos, node_size=400, node_color='#6495ED')
    label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
    nx.draw_networkx_labels(graph, pos, font_size=9, bbox=label_options, labels=node_labels)
    # edge
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.axis('off')
    save_path = f"subgraph_images/pic-{index+1}.png"
    plt.savefig(save_path)

if __name__ == '__main__':
    task_dir = './dataset/YAGO3-10'
    centers = ['Nitin_Saxena', 'Peace_Prize_of_the_German_Book_Trade','Hong_Kong_Rangers_FC']
    relations = [
        'isConnectedTo', 'isKnownFor', 'graduatedFrom', 'hasChild', 
        'actedIn', 'exports', 'isLocatedIn', 'wroteMusicFor', 'hasCurrency', 
        'playsFor', 'directed', 'owns', 'isPoliticianOf', 'diedIn', 'hasGender', 
        'edited', 'isInterestedIn', 'created', 'livesIn', 'dealsWith', 
        'hasOfficialLanguage', 'isMarriedTo', 'hasMusicalRole'
        ]
    hop = 3

    id2relation = get_id2relation(os.path.join(task_dir,'relation2id.txt'))
    relation2id = dict([(v,k) for k,v in id2relation.items()])
    id2entity = get_id2entity(os.path.join(task_dir,'entity2id.txt'))
    entity2id = dict([(v,k) for k,v in id2entity.items()])

    centers_id = [entity2id[c] for c in centers]
    relations_id = [relation2id[r] for r in relations]

    sub_nodes, adj, adj_weight_list = preprocess_func(task_dir, centers_id, hop)

    nodes2sub_nodes = dict([(sub_nodes[i], i) for i in range(len(sub_nodes))])
    id2entity_sub = dict([(i, id2entity[sub_nodes[i]]) for i in range(len(sub_nodes))])
    entity2id_sub = dict([(v,k) for k,v in id2entity_sub.items()])
    print(f"sub nodes number: {len(sub_nodes)}")
    graph = nx.from_scipy_sparse_matrix(adj)
    centers_graphs = get_muticenter(graph, adj_weight_list, [nodes2sub_nodes[node] for node in centers_id], 2)
    for i in range(len(centers_graphs)):
        sub_graph = breadFirstGraphExtract(graph, centers_graphs[i], adj_weight_list, relations_id, 3, 10)
        draw_graph(sub_graph, id2entity_sub, id2relation, i)
