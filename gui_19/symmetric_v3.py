relationWithHT = {}
symmetric = {}
# symmetricIndex = 0
strIndex = []
threshold = 0.95
total = {}
newDic = {}
symmetric_1 = []


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
        # print(newDic)
        for row in newDic:
            total[row] = 0
            symmetric[row] = []
            hashmap = {}
            for i in range(len(newDic[row])):
                hashmap[newDic[row][i]] = i
            for i in range(len(newDic[row])):
                item_reverse = newDic[row][i][::-1]
                if item_reverse in hashmap:
                    symmetric_1.append(item_reverse)
                    total[row] += 1
                    symmetric[row].append(item_reverse)


        # print(symmetric_1)
        # print('finish')
        # print(total)
        # print(symmetric)


        fSymmetric = open("symmetric_v1.txt", "w")

        # print(relationWithHT)
        # print(total)
        number = 0
        new_list = {}
        for i in range(len(total)):
            if total[strIndex[i]] != 0:
                rate = total[strIndex[i]] / len(relationWithHT[strIndex[i]])
                if rate >= threshold:
                    new_list[strIndex[i]] = symmetric[strIndex[i]]
                    number += 1
        fSymmetric.write("%d\n" % (number))

        for n in new_list:
            fSymmetric.write("%s\t%s\n" % (n, new_list[n]))


symme = Symmetric()
