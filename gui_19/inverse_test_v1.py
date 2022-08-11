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
        print('e')
        print(relationWithHT)

        for i in range(len(relationWithHT)):
            baseDic = relationWithHT[strIndex[i]]
            print('temp head is: ', strIndex[i])
            if i < len(relationWithHT) - 1:
                for j in range(len(baseDic)):
                    tempList = (baseDic[j][1], baseDic[j][0])
                    round = i + 1
                    # print('temp list is: ', tempList)
                    while round < len(relationWithHT):
                        # print('round is:', round)
                        targetDic = relationWithHT[strIndex[round]]
                        # print(targetDic)
                        if tempList in targetDic:
                            # if len(inverse) != 0:
                            #     for l in range(len(inverse)):
                            #         if [(strIndex[i], strIndex[round])] != inverse[l]:
                            #             inverse[inverseIndex] = []
                            #             inverse[inverseIndex].append((strIndex[i], strIndex[round]))
                            # else:
                            #     inverse[inverseIndex] = []
                            #     inverse[inverseIndex].append((strIndex[i], strIndex[round]))
                            inverse[inverseIndex] = []
                            inverse[inverseIndex].append((strIndex[i], strIndex[round]))
                            total[strIndex[i]] += 1
                            total[strIndex[round]] += 1
                            inverseIndex += 1
                        round += 1
                        # for k in range(len(targetDic)):
                        #     print('k is:', k)
                        #     arr = targetDic[k]
                        #     tempArray = [arr[1], arr[0]]
                        #     new = [arr[0], arr[1]]
                        #     if tempList == tempArray:
                        #         list1 = [tempList, strIndex[i], new, strIndex[round]]
                        #         list2 = [new, strIndex[round], tempList, strIndex[i]]
                        #         if not checkRepeat(list1, list2):
                        #             # inverse[inverseIndex].append((tempList, strIndex[i], new, strIndex[round]))
                        #             if len(inverse) != 0:
                        #                 for l in range(len(inverse)):
                        #                     if [(strIndex[i], strIndex[round])] != inverse[l]:
                        #                         inverse[inverseIndex] = []
                        #                         inverse[inverseIndex].append((strIndex[i], strIndex[round]))
                        #             else:
                        #                 inverse[inverseIndex] = []
                        #                 inverse[inverseIndex].append((strIndex[i], strIndex[round]))
                        #             total[strIndex[i]] += 1
                        #             total[strIndex[round]] += 1
                        #             inverseIndex += 1
                        # round += 1
        # for i in range(len(relationWithHT)):
        #     print('f')
        #     baseDic = relationWithHT[strIndex[i]]
        #     if i < len(relationWithHT) - 1:
        #         for j in range(len(baseDic)):
        #             print(j)
        #             tempList = [baseDic[j][0], baseDic[j][1]]
        #             round = i + 1
        #             while round < len(relationWithHT):
        #                 print('round is:', round)
        #                 targetDic = relationWithHT[strIndex[round]]
        #                 for k in range(len(targetDic)):
        #                     print('k is:', k)
        #                     arr = targetDic[k]
        #                     tempArray = [arr[1], arr[0]]
        #                     new = [arr[0], arr[1]]
        #                     if tempList == tempArray:
        #                         list1 = [tempList, strIndex[i], new, strIndex[round]]
        #                         list2 = [new, strIndex[round], tempList, strIndex[i]]
        #                         if not checkRepeat(list1, list2):
        #                             # inverse[inverseIndex].append((tempList, strIndex[i], new, strIndex[round]))
        #                             if len(inverse) != 0:
        #                                 for l in range(len(inverse)):
        #                                     if [(strIndex[i], strIndex[round])] != inverse[l]:
        #                                         inverse[inverseIndex] = []
        #                                         inverse[inverseIndex].append((strIndex[i], strIndex[round]))
        #                             else:
        #                                 inverse[inverseIndex] = []
        #                                 inverse[inverseIndex].append((strIndex[i], strIndex[round]))
        #                             total[strIndex[i]] += 1
        #                             total[strIndex[round]] += 1
        #                             inverseIndex += 1
        #                 round += 1

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
