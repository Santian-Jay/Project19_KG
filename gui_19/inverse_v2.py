relationWithHT = {}
inverse = {}
# inverseIndex = 0
strIndex = []
threshold = 0.95
total = {}


def checkRepeat(list1, list2):
    isIn = False
    for i in range(len(inverse)):
        if list1 == inverse[i] or list2 == inverse[i]:
            isIn = True
    return isIn


class Inverse:

    def __init__(self):
        # super().__init__()
        print('a')
        self.inverse_func()
        self.data = open("inverse_v1.txt", 'r', encoding='UTF-8')
        self.n_inver = self.data.readline().split()
        # print(self.n_inver)

    def get_data(self):
        return self.n_inver

    def inverse_func(self):
        print('b')
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

        #print(relationWithHT)

        relation_map = {}

        hash_table = {}
        index = 0
        for key, row in enumerate(relationWithHT):
            for item in relationWithHT[row]:
                new_tuple = (key, item[0], item[1])
                hash_table[new_tuple] = index
                index += 1
        for item in hash_table:
            for i in range(len(relationWithHT)):
                if (i, item[2], item[1]) in hash_table and i != item[0]:
                    print("%d and %d has inverse" % (item[0], i))
                    print((item[1], item[2]))
                    if (strIndex[item[0]], strIndex[i]) in relation_map:
                        relation_map[(strIndex[item[0]], strIndex[i])].append((item[1], item[2]))
                    else:
                        if (strIndex[i], strIndex[item[0]]) not in relation_map:
                            relation_map[(strIndex[item[0]], strIndex[i])] = []
                            relation_map[(strIndex[item[0]], strIndex[i])].append((item[1], item[2]))


        # for key, row in enumerate(relationWithHT): # look entireii
        #     hashmap = {}
        #     for i in range(len(relationWithHT[row])): # look each row
        #         #print(relationWithHT[row][i])
        #         item_reverse = relationWithHT[row][i][::-1]
        #         for o_index, o_row in enumerate(relationWithHT):
        #             if key != o_index:
        #                 for o_i in range(len(relationWithHT[o_row])):
        #                     hashmap[relationWithHT[o_row][o_i]] = o_i
        #                 for o_i in range(len(relationWithHT[o_row])):
        #                     if item_reverse in hashmap:
        #                         print("%d and %d has inverse" % (key, o_index))
        #                         print(item_reverse)
        #
        #                         if (strIndex[key], strIndex[o_index]) in relation_map:
        #                             relation_map[(strIndex[key], strIndex[o_index])].append(item_reverse)
        #                         else:
        #                             if (strIndex[o_index], strIndex[key]) not in relation_map:
        #                                 relation_map[(strIndex[key], strIndex[o_index])] = []
        #                                 relation_map[(strIndex[key], strIndex[o_index])].append(item_reverse)
        #                         hashmap.clear()
        #                         break
        #                 hashmap.clear()

        print(relation_map)
        print(inverse)
        print('total is: ', total)

        fInverse = open("inverse_v1.txt", "w")
        fInverse.write("%d\n" % (len(inverse)))

        for n in range(len(inverse)):
            h = inverse[n][0][0]
            t = inverse[n][0][1]
            hRate = total[h] / len(relationWithHT[h])
            tRate = total[t] / len(relationWithHT[t])
            print(hRate, tRate)
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

# print(inverse)
# # for i in range(len(inverse)):
# #     print(inverse)
#     # print(i, inverse[i])
# print(strIndex)
# print(total)
# for i in range(len(total)):
#     print(total[strIndex[i]])
