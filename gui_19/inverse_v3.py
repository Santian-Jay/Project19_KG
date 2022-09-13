relationWithHT = {}
inverse = {}
strIndex = []
threshold = 0.95
total = {}


# def checkRepeat(list1, list2):
#     isIn = False
#     for i in range(len(inverse)):
#         if list1 == inverse[i] or list2 == inverse[i]:
#             isIn = True
#     return isIn


class Inverse:
    def __init__(self):
        # super().__init__()
        self.inverse_func()
        self.data = open("inverse_v1.txt", 'r', encoding='UTF-8')
        self.n_inver = self.data.readline().split()
        # print(self.n_inver)

    def get_data(self):
        return self.n_inver

    def inverse_func(self):
        file = open("dataset/train2id.txt", "r", encoding='UTF-8')
        entryNumber = (int)(file.readline())
        inverseIndex = 0
        for index in range(entryNumber):
            content = file.readline()
            head, tile, relation = content.strip().split()
            if relation not in relationWithHT:
                strIndex.append(str(relation))
                total[relation] = 0
                relationWithHT[relation] = []
            relationWithHT[relation].append((int(head), int(tile)))

        relation_map = {}

        hash_table = {}
        inverseIndex = []
        index = 0

        for key, row in enumerate(relationWithHT):
            for item in relationWithHT[row]:
                new_tuple = (key, item[0], item[1])
                hash_table[new_tuple] = index
                index += 1
        for item in hash_table:
            for i in range(len(relationWithHT)):
                if (i, item[2], item[1]) in hash_table and i != item[0]:
                    if (strIndex[item[0]], strIndex[i]) in relation_map:
                        relation_map[(strIndex[item[0]], strIndex[i])].append((item[1], item[2]))
                        total[strIndex[i]] += 1
                        total[strIndex[item[0]]] += 1
                        if (strIndex[item[0]], strIndex[i]) not in inverseIndex:
                            inverseIndex.append((strIndex[item[0]], strIndex[i]))
                    else:
                        if (strIndex[i], strIndex[item[0]]) not in relation_map:
                            relation_map[(strIndex[item[0]], strIndex[i])] = []
                            relation_map[(strIndex[item[0]], strIndex[i])].append((item[1], item[2]))
                            total[strIndex[i]] += 1
                            total[strIndex[item[0]]] += 1
                            if (strIndex[item[0]], strIndex[i]) not in inverseIndex:
                                inverseIndex.append((strIndex[item[0]], strIndex[i]))

        # print(relation_map)
        # print(inverse)
        # print('total is: ', total)
        # print(inverseIndex)

        fInverse = open("inverse_v1.txt", "w")
        fInverse.write("%d\n" % (len(relation_map)))

        for n in range(len(relation_map)):
            h = inverseIndex[n][0]
            t = inverseIndex[n][1]
            hRate = total[h] / len(relationWithHT[h])
            tRate = total[t] / len(relationWithHT[t])
            # print(hRate, tRate)
            fInverse.write("%s\t%s\n" % (h, t))
            if hRate >= threshold and tRate >= threshold:
                print("relation {} and {} can be inverse".format(h, t))


inver = Inverse()

"""
Determine if new data is already included in the dataset
"""

"""
Classify the data in the dataset by relation
"""


