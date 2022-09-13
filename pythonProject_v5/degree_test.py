entity = {}
degree = {}


class Degree:
    def __init__(self):
        self.create_degree()
        self.count_degree()
        self.in_ave, self.out_ave = self.count_ave_degree()

        print(self.in_ave, self.out_ave)

    def get_result(self):
        return self.in_ave, self.out_ave

    def create_degree(self):  # 可以改为接受两个参数，一个entity，一个trian
        file = open("dataset/entity2id.txt", 'r', encoding='UTF-8')
        n_entity = int(file.readline())
        for index in range(n_entity):
            content = file.readline()
            name, code = content.strip().split()
            degree[code] = []
            degree[code].append(0)
            degree[code].append(0)
        # print(degree)

    def count_degree(self):
        file2 = open("dataset/train2id.txt", 'r', encoding='UTF-8')
        n_train = int(file2.readline())
        for i in range(n_train):
            context = file2.readline()
            head, tail, relation = context.strip().split()
            if head in degree:
                degree[head][0] += 1  # out degree
            if tail in degree:
                degree[tail][1] += 1  # in degree
        # print(degree)

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
    print(deg.get_result())

# file = open("dataset/entity2id.txt", 'r')
# file2 = open("dataset/train2id.txt", 'r')
#
# n_entity = int(file.readline())
# n_train = int(file2.readline())
# print(n_entity)
# for index in range(n_entity):
#     content = file.readline()
#     name, code = content.strip().split()
#     print(name, code)
#     # if code not in degree:
#     degree[code] = []
#     degree[code].append(0)
#     degree[code].append(0)
#
# print(degree)
