relationWithHT = {}
inverse = {}
# inverseIndex = 0
strIndex = []
threshold = 0.95
total = {}
tempH = 0
tempT = 0


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
        file = open("dataset/YAGO3-10/train2id.txt", "r", encoding='UTF-8')
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
        # print('e')
        # print(relationWithHT)
        # print(relationWithHT[strIndex[1]])
        # a = (10, 3)
        # print(a in relationWithHT[strIndex[1]])

        for i in range(len(relationWithHT)):
            baseDic = relationWithHT[strIndex[i]]
            if i < len(relationWithHT) - 1:
                for j in range(len(baseDic)):
                    tempList = (baseDic[j][1], baseDic[j][0])
                    round = i + 1
                    print('temp list is: ', tempList)
                    while round < len(relationWithHT):
                        print('round is:', round)
                        targetDic = relationWithHT[strIndex[round]]
                        # print(targetDic)
                        if tempList in targetDic:
                            tempH = int(strIndex[i])
                            tempT = int(strIndex[round])
                            inverse[inverseIndex] = []
                            inverse[inverseIndex].append((int(strIndex[i]), int(strIndex[round])))
                            total[strIndex[i]] += 1
                            total[strIndex[round]] += 1
                            if tempH != int(strIndex[i]) and tempT != int(strIndex[round]):
                                inverseIndex += 1
                        round += 1
        print('inverse is', inverse)
        print('total is: ', total)

        fInverse = open("inverse_v1.txt", "w")
        fInverse.write("%d\n" % (len(inverse)))

        for n in range(len(inverse)):
            h = inverse[n][0][0]
            t = inverse[n][0][1]
            # print(h,t)
            # print(total[str(h)])
            # print(len(relationWithHT[str(h)]))
            hRate = total[str(h)] / len(relationWithHT[str(h)])
            tRate = total[str(t)] / len(relationWithHT[str(t)])
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
