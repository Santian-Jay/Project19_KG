relationWithHT = {}
symmetric = {}
# symmetricIndex = 0
strIndex = []
threshold = 0.95
total = {}
newDic = {}


class Symmetric:
    def __init__(self):
        self.symmertric_func()
        self.data = open("symmetric_v1.txt", 'r', encoding='UTF-8')
        self.n_sy = self.data.readline()
        if self.n_sy == "" : self.n_sy = 0
        print(self.n_sy)

    def get_data(self):
        return self.n_sy

    def symmertric_func(self):
        symmetricIndex = 0
        file = open("dataset/train2id.txt", "r", encoding='UTF-8')
        entryNumber = (int)(file.readline())

        """
        Classify the data in the dataset by relation
        """
        for index in range(entryNumber):
            content = file.readline()
            head, tile, relation = content.strip().split()
            if relation not in relationWithHT:
                total[relation] = 0
                strIndex.append(str(relation))
                relationWithHT[relation] = []
                newDic[relation] = []
            relationWithHT[relation].append((int(head), int(tile)))
            newDic[relation].append((int(head), int(tile)))

        """
        Symmetric relationship algorithm, print data that can be reversed in each relationship
        """
        print(relationWithHT)
        # for i in range(len(newDic)):
        for i in range(len(newDic)):
            # print(newDic)
            temp = newDic[strIndex[i]]  # first row
            temp_1 = [temp[0]]  # first group of first row
            tempList = (temp_1[0][1], temp_1[0][0])  # first group of first row change to list
            print("The first comparison data：", tempList)
            temp.remove(temp[0])  # remove first group
            print(temp)
            while len(temp) != 0:
                print('temp length is', len(temp))
                if tempList in temp:
                    total[strIndex[i]] += 2
                    symmetric[symmetricIndex] = []
                    # symmetric[symmetricIndex].append((strIndex[i], tempList, strIndex[i], (temp[j][0], temp[j][1])))
                    symmetric[symmetricIndex].append((strIndex[i], tempList))
                    symmetricIndex += 1
                    temp.remove(tempList)
                # for j in range(len(temp)):
                #     print('j is :', j)
                #     if len(temp) > 0:
                #         newArray = [temp[j][1], temp[j][0]]
                #         # print("The model for comparison is：", newArray)
                #         if tempList == newArray:
                #             total[strIndex[i]] += 2
                #             symmetric[symmetricIndex] = []
                #             symmetric[symmetricIndex].append(
                #                 (strIndex[i], tempList, strIndex[i], (temp[j][0], temp[j][1])))
                #             symmetricIndex += 1
                            # print(newArray)
                tempList = [temp[0][1], temp[0][0]]
                # print("update comparative data：", tempList)
                temp.remove(temp[0])

        print(symmetric)

        # for i in range(len(newDic)):
        #     # print(newDic)
        #     temp = newDic[strIndex[i]]  # first row
        #     temp_1 = [temp[0]]  # first group of first row
        #     tempList = [temp_1[0][0], temp_1[0][1]]  # first group of first row change to list
        #     # print("The first comparison data：", tempList)
        #     temp.remove(temp[0])  # remove first group
        #     while len(temp) != 0:
        #         print('temp length is', len(temp))
        #         for j in range(len(temp)):
        #             print('j is :', j)
        #             if len(temp) > 0:
        #                 newArray = [temp[j][1], temp[j][0]]
        #                 # print("The model for comparison is：", newArray)
        #                 if tempList == newArray:
        #                     total[strIndex[i]] += 2
        #                     symmetric[symmetricIndex] = []
        #                     symmetric[symmetricIndex].append(
        #                         (strIndex[i], tempList, strIndex[i], (temp[j][0], temp[j][1])))
        #                     symmetricIndex += 1
        #                     # print(newArray)
        #         tempList = [temp[0][0], temp[0][1]]
        #         # print("update comparative data：", tempList)
        #         temp.remove(temp[0])

        # for i in range(len(symmetric)):
        #     print('test:' + symmetric[i])

        fSymmetric = open("symmetric_v1.txt", "w")

        # print(relationWithHT)
        # print(total)
        number = 0
        new_list = {}
        for i in range(len(total)):
            if total[strIndex[i]] != 0:
                rate = total[strIndex[i]] / len(relationWithHT[strIndex[i]])
                if rate >= threshold:
                    new_list[strIndex[i]] = []
                    for data in range(len(symmetric[strIndex[i]])):
                        new_list[strIndex[i]].append(symmetric[strIndex[i]][data])
                    print("relation %s can be symmetric" % (strIndex[i]))
                    number += 1
        fSymmetric.write("%d\n" % (number))

        for n in new_list:
            fSymmetric.write("%s\t%s\n" % (n, new_list[n]))


symme = Symmetric()
