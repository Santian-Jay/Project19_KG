import json


class MysqlDatabase:
    def __init__(self):
        self.graphs = json.loads(open('graph.json', mode='r', encoding='utf-8').read())
    def all_graph(self):
        return self.graphs

    def insert(self, graph):
        self.graphs.append(graph)

db = MysqlDatabase()

if __name__ == '__main__':
    print(db.all_graph())