import random
import networkx as nx
from read_data import DataLoader

def triplesToNxDiGraph(triples):
    # note that triples are with no inverse relations
    graph = nx.MultiDiGraph()
    nodes = list(set([h for (h, r, t) in triples] + [t for (h, r, t) in triples]))
    graph.add_nodes_from(nodes)

    for (h, r, t) in triples:
        graph.add_edges_from([(h, t)], relation=r)

    return graph

def triplesToNxGraph(triples):
    # note that triples are with no inverse relations
    graph = nx.Graph()
    nodes = list(set([h for (h,r,t) in triples] + [t for (h,r,t) in triples]))
    graph.add_nodes_from(nodes)
    edges = list(set([(h,t) for (h,r,t) in triples]))
    graph.add_edges_from(edges)

    return graph

def random_walk_induced_graph_sampling(complete_graph, nodes_to_sample):
    complete_graph = nx.convert_node_labels_to_integers(complete_graph, 0, 'default', True)
    # giving unique id to every node same as built-in function id
    for n, data in complete_graph.nodes(data=True):
        complete_graph.nodes[n]['id'] = n

    nr_nodes = len(complete_graph.nodes())
    upper_bound_nr_nodes_to_sample = nodes_to_sample
    index_of_first_random_node = random.randint(0, nr_nodes - 1)
    Sampled_nodes = set([complete_graph.nodes[index_of_first_random_node]['id']])

    iteration = 1
    growth_size = 2
    check_iters = 100
    nodes_before_t_iter = 0
    curr_node = index_of_first_random_node;
    print(f'==> curr_node: {curr_node}')
    while len(Sampled_nodes) != upper_bound_nr_nodes_to_sample:
        edges = [n for n in complete_graph.neighbors(curr_node)]
        index_of_edge = random.randint(0, len(edges) - 1)
        chosen_node = edges[index_of_edge]
        Sampled_nodes.add(complete_graph.nodes[chosen_node]['id'])
        curr_node = chosen_node
        iteration = iteration + 1

        if iteration % check_iters == 0:
            if ((len(Sampled_nodes) - nodes_before_t_iter) < growth_size):
                print(f'==> boost seaching, skip to No.{curr_node} node')
                curr_node = random.randint(0, nr_nodes - 1)
            nodes_before_t_iter = len(Sampled_nodes)

    return Sampled_nodes

if __name__ == '__main__':
    task_dir = './KG_Data/WN18RR'
    loader = DataLoader(task_dir, 1)

    n_ent, n_rel = loader.graph_size()

    train_data = loader.load_data('train')
    valid_data = loader.load_data('valid')
    test_data  = loader.load_data('test')

    all_triples = []
    homoGraph = triplesToNxGraph(all_triples)
    diGraph   = triplesToNxDiGraph(all_triples)
    sampled_nodes = random_walk_induced_graph_sampling(homoGraph, target_num_nodes=1)

    sampled_graph = diGraph.subgraph(sampled_nodes)