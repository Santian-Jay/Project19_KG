relationWithHT = {}
symmetric = {}
anti_symmetric = {}
inverse = {}
composition = {}
inverseIndex = 0
symmetricIndex = 0
strIndex = []          # index in the dictionary

"""
Determine if new data is already included in the dataset
"""
def checkRepeat(list1, list2):
    isIn = False
    for i in range(len(inverse)):
        if list1 == inverse[i] or list2 == inverse[i]:
            isIn = True
    return isIn

file = open("../subgraph_v1/train2id.txt", "r")
entryNumber = (int)(file.readline())

"""
Classify the data in the dataset by relation
"""
for index in range(entryNumber):
    content = file.readline()
    head, tile, relation = content.strip().split()
    if relation not in relationWithHT:
        strIndex.append(str(relation))
        relationWithHT[relation] = []
    relationWithHT[relation].append((head, tile))




# ===================================Symmetric Start==========================================
"""
Symmetric relationship algorithm, print data that can be reversed in each relationship
"""

for i in range(len(relationWithHT)):
    temp = relationWithHT[strIndex[i]]      # 第一行
    temp_1 = [temp[0]]                      # 第一行第一组
    tempList_v = [temp_1[0][0], temp_1[0][1]] # 第一行第一组转换成list
    # print("最开始的对比的数据：", tempList)
    temp.remove(temp[0])    # 移除第一组
    while len(temp) != 0:
        for j in range(len(temp)):
            if len(temp) > 0:
                newArray = [temp[j][1], temp[j][0]]
                # print("对比的模型是：", newArray)
                if tempList_v == newArray:
                    symmetric[symmetricIndex] = []
                    symmetric[symmetricIndex].append((strIndex[i], tempList_v, strIndex[i], (temp[j][0], temp[j][1])))
                    symmetricIndex += 1
                    # print(newArray)
        tempList = [temp[0][0], temp[0][1]]
        # print("更新对比的数据：", tempList)
        temp.remove(temp[0])
# print("对称的的是：", symmetric)

for i in range(len(symmetric)):
    print(symmetric[i])


"""
inverse function, print pairs of triples that can be reversed
"""
for i in range(len(relationWithHT)):
    baseDic = relationWithHT[strIndex[i]]
    if i < len(relationWithHT) - 1:
        for j in range(len(baseDic)):
            tempList = [baseDic[j][0], baseDic[j][1]]
            round = i + 1
            while round < len(relationWithHT):
                targetDic = relationWithHT[strIndex[round]]
                for k in range(len(targetDic)):
                    arr = targetDic[k]
                    tempArray = [arr[1], arr[0]]
                    new = [arr[0], arr[1]]
                    if tempList == tempArray:
                        list1 = [tempList, strIndex[i], new, strIndex[round]]
                        list2 = [new, strIndex[round], tempList, strIndex[i]]
                        if not checkRepeat(list1, list2):
                            inverse[inverseIndex] = []
                            inverse[inverseIndex].append((tempList, strIndex[i], new, strIndex[round]))
                            inverseIndex += 1
                round += 1


for i in range(len(inverse)):
    print(inverse[i])


