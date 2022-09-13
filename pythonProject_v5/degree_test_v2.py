import nnrelation
import json
from symmetric import symme
from inverse import inver
from entity_feature import efeature
entity = {}
degree = {}
n_relation = {}


class Degree:
    def __init__(self):
        self.n_entity = self.create_degree()
        self.n_edge, self.n_relation, self.n_11, self.n_1n, self.n_n1, self.n_nn = self.count_degree()
        self.in_ave, self.out_ave = self.count_ave_degree()
        self.n_relation_head, self.n_relation_tail = efeature.get_count()
        # data list
        data_list = [self.n_entity, self.n_edge, self.in_ave, self.out_ave, self.n_relation, self.n_11, self.n_1n, self.n_n1, self.n_nn,
                     symme.n_sy, inver.n_inver, self.n_relation_head, self.n_relation_tail]
        print('f')
        # insert data to json
        with open('data.json', 'r+') as f:
            json_data = json.load(f)
            for i in range(len(data_list)):
                json_data[i]['value'] = data_list[i]
            f.seek(0)
            f.write(json.dumps(json_data))
            f.truncate()

        print(self.in_ave, self.out_ave, self.n_entity, self.n_relation, self.n_edge)

    def get_result(self):
        return self.in_ave, self.out_ave, self.n_entity, self.n_relation, self.n_edge, self.n_11, self.n_1n, self.n_n1, self.n_nn

    def create_degree(self):  # 可以改为接受两个参数，一个entity，一个triad
        file = open("dataset/entity2id.txt", 'r', encoding='UTF-8')

        n_entity = int(file.readline())

        for index in range(n_entity):
            content = file.readline()
            name, code = content.strip().split()
            degree[code] = []
            degree[code].append(0)
            degree[code].append(0)
        return n_entity

    def count_degree(self):
        file2 = open("dataset/train2id.txt", 'r', encoding='UTF-8')
        n_train = int(file2.readline())
        new_train = []
        for i in range(n_train):
            context = file2.readline()
            head, tail, relation = context.strip().split()
            new_train.append((head, tail, relation))
            if head in degree:
                degree[head][0] += 1  # out degree
            if tail in degree:
                degree[tail][1] += 1  # in degree
            if relation not in n_relation:
                n_relation[relation] = []
        n_11, n_1n, n_n1, n_nn = nnrelation.nn_categorization(new_train)
        return n_train, len(n_relation), n_11, n_1n, n_n1, n_nn

    def count_ave_degree(self):
        total_in_ave = 0
        total_out_ave = 0
        for j in degree:
            total_in_ave += degree[j][0]
            total_out_ave += degree[j][1]
        in_ave = total_in_ave / len(degree)
        out_ave = total_out_ave / len(degree)
        # print(in_ave, out_ave)
        return in_ave, out_ave


deg = Degree()

if __name__ == '__main__':
    print('degree class')
