from inverse import inver
from symmetric import symme
from get_graph_data import gi
from database import db

class Insert:
    def __init__(self):
        self.insert_json()

    def insert_json(self):
        graph = {
          "n_entity": gi.n_enti,
          "n_relation": gi.n_rela,
          "n_edge": gi.n_edg,
          "n_n": 0, "n_1": 0,
          "1_1": 0, "1_n": 0,
          "inverse": inver.n_inver,
          "symmetric": symme.n_sy,
          "in_degree": gi.in_d,
          "out_degree": gi.out_d
        }
        db.insert(graph)
        print(graph)
insert = Insert()
if __name__ == '__main__':
    print(insert.insert_json())