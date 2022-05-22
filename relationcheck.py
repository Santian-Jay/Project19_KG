relationWithHT = {}
symmetric = {}
anti_symmetric = {}
inverse = {}
composition = {}
inverseIndex = 0
symmetricIndex = 0
strIndex = []

def checkRepeat(list1, list2):
    isIn = False
    for i in range(len(inverse)):
        if list1 == inverse[i] or list2 == inverse[i]:
            isIn = True
    return isIn

file = open("subgraph_v1/train2id.txt", "r")
entryNumber = (int)(file.readline())

for index in range(entryNumber):
    content = file.readline()
    head, tile, relation = content.strip().split()
    if relation not in relationWithHT:
        strIndex.append(str(relation))
        relationWithHT[relation] = []
    relationWithHT[relation].append((head, tile))


"""
inverse function, print pairs of triples that can be reversed
"""
"""
for i in range(len(relationWithHT)):
    for j in range(len(relationWithHT[strIndex[i]])):
        temp = relationWithHT[strIndex[i]][j]
        temp_1 = [temp[0], temp[1]]
        if i < len(relationWithHT) - 1:
            for l in range(len(relationWithHT) - 1):
                tempDic = relationWithHT[strIndex[l+1]]
                for k in range(len(tempDic)):
                    arr = [tempDic[k]]
                    tempArray = [tempDic[k][1], tempDic[k][0]]
                    new = [tempDic[k][0], tempDic[k][1]]
                    if temp_1 == tempArray:
                        list1 = [(temp_1, strIndex[i], new, strIndex[l+1])]
                        list2 = [(new, strIndex[l+1], temp_1, strIndex[i])]
                        if not checkRepeat(list1, list2):
                            inverse[inverseIndex] = []
                            inverse[inverseIndex].append((temp_1, strIndex[i], new, strIndex[l + 1]))
                            inverseIndex += 1
"""

# print(relationWithHT[strIndex[0][0]])
# print(relationWithHT[strIndex[1]][0][0])

# temparr = [relationWithHT[strIndex[1][1]], relationWithHT[strIndex[1][0]]]
# print(temparr)
# print(relationWithHT[strIndex[8]])
# print(strIndex)
# print(inverse)
#print(relationWithHT[1])4
# print(relationWithHT["0"][0])
# print(relationWithHT)
# print(symmetric)
# for i in range(len(relationWithHT)):
#     print(relationWithHT[strIndex[i]])
# for i in relationWithHT:
#     print(i)
# print("===============================")
# a = {"0": ["1", "2"]}
# b = {"0": ["2", "1"]}
# c = a["0"]
# d = b["0"]
# temp1 = [d[1], d[0]]
# print(type(c))
# print(type(temp1))
#
# if (c[0] == temp1[0] and c[1] == temp1[1]):
#     print("成功了")


# for i in range(len(relationWithHT)):
#     for j in range(len(relationWithHT[strIndex[i]])):
#         temp = relationWithHT[strIndex[i]][j]
#         temp_1 = [temp[0], temp[1]]
#         if i < len(relationWithHT) - 1:
#             for l in range(len(relationWithHT)):
#                 tempDic = relationWithHT[strIndex[i+1]]
#                 for k in range(len(tempDic)):
#                     arr = [tempDic[k]]
#                     tempArray = [tempDic[k][1], tempDic[k][0]]
#                     print(temp_1, tempArray)
#                     if temp_1 == tempArray:
#                         print("运行到这了吗3")
#                         inverse[inverseIndex] = []
#                         # inverse[inverseIndex].append(((temp, strIndex[i]), (tempDic[k], strIndex[i+1])))
#                         inverse[inverseIndex].append(((temp_1, strIndex[i]), arr, strIndex[i+1]))
#                         inverseIndex += 1


# list2 = [(['12', '4'], '5', ['4', '12'], '1')]
# for i in range(len(inverse)):
#     print(list2 == inverse[i])

# ===================================Symmetric Start==========================================
"""
Symmetric relationship algorithm, print data that can be reversed in each relationship
"""
"""
for i in range(len(relationWithHT)):
    temp = relationWithHT[strIndex[i]]      # 第一行
    temp_1 = [temp[0]]                      # 第一行第一组
    tempList = [temp_1[0][0], temp_1[0][1]] # 第一行第一组转换成list
    # print("最开始的对比的数据：", tempList)
    temp.remove(temp[0])    # 移除第一组
    while len(temp) != 0:
        for j in range(len(temp)):
            if len(temp) > 0:
                newArray = [temp[j][1], temp[j][0]]
                # print("对比的模型是：", newArray)
                if tempList == newArray:
                    symmetric[symmetricIndex] = []
                    symmetric[symmetricIndex].append((strIndex[i], tempList, strIndex[i], (temp[j][0], temp[j][1])))
                    symmetricIndex += 1
                    # print(newArray)
        tempList = [temp[0][0], temp[0][1]]
        # print("更新对比的数据：", tempList)
        temp.remove(temp[0])
# print("对称的的是：", symmetric)
"""


        # if len(temp) > 0:
        #     tempList = [temp[0][0], temp[0][1]]
        #     print("运行得到这里了", tempList)
    # if len(temp) != 0:
    #     temp.remove(temp[0])
            # temp.remove(temp[0])
        # temp.remove(temp_1)
        # for k in range(len(temp) - 1):
        #     if k != 1:
        #         temp.remove(temp[k])
        #         print(temp)
                # print("运行到这了吗")
                # removedTemp = temp[k]
                # removedTempList = [removedTemp[0], removedTemp[1]]
                # list1 = [(temp_1, strIndex[i], removedTempList, strIndex[i])]
                # list2 = [(removedTempList, strIndex[i], temp_1, strIndex[i])]
                # symmetric[symmetricIndex] = []
                # symmetric[symmetricIndex].append((temp_1, strIndex[i], removedTempList, strIndex[i]))
                # symmetricIndex += 1


        # for k in range(len(relationWithHT[strIndex[i]]) - i):
        # for k in range(len(relationWithHT[strIndex[i]]) - i):
        #     if k < (len(relationWithHT[strIndex[i]]) - 1) and k != 1:
        #         new = relationWithHT[strIndex[i]][k + 1]
        #         newTemp = [new[0], new[1]]
        #         inverseTemp = [new[1], new[0]]
        #         list1 = [(temp_1, strIndex[i], newTemp, strIndex[i])]
        #         list2 = [(newTemp, strIndex[i], temp_1, strIndex[i])]
        #         print("=============")
        #         print(temp_1)
        #         print(inverseTemp)
        #         print("=============")
        #         if temp_1 == inverseTemp:
        #             if not checkRepeat(list1, list2):
        #                 symmetric[symmetricIndex] = []
        #                 symmetric[symmetricIndex].append((temp_1, strIndex[i], newTemp, strIndex[i]))
        #                 symmetricIndex += 1

            # if i < len(relationWithHT) - 1:
            #     for k in range(len(relationWithHT[strIndex[i]]) - 1):
            #         newArray = []
        # x = temp[0]
        # y = temp[1]
        # if x == y:
        #     symmetric[symmetricIndex] = []
        #     symmetric[symmetricIndex].append((temp, strIndex[i]))
        #     symmetricIndex += 1
        # temp_1 = [temp[0], temp[1]]
        # if i < len(relationWithHT) - 1:
        #     for l in range(len(relationWithHT) - 1):
        #         tempDic = relationWithHT[strIndex[l+1]]
        #         for k in range(len(tempDic)):
        #             arr = [tempDic[k]]
        #             tempArray = [tempDic[k][0], tempDic[k][1]]
        #             # new = [tempDic[k][0], tempDic[k][1]]
        #             # print(type(new))
        #             # print(temp_1, tempArray)
        #             if temp_1 == tempArray:
        #                 list1 = [(temp_1, strIndex[i], tempArray, strIndex[l+1])]
        #                 list2 = [(tempArray, strIndex[l+1], temp_1, strIndex[i])]

                        # inverse[inverseIndex].append((temp_1, strIndex[i], new, strIndex[l + 1]))
                        # inverseIndex += 1

                        # inverse[inverseIndex].append((temp_1, strIndex[i], new, strIndex[l + 1]))
                        # inverseIndex += 1
                        # for m in range(len(inverse)):
                        # if not checkRepeat(list1, list2):
                        #     symmetric[symmetricIndex] = []
                        #     symmetric[symmetricIndex].append((temp_1, strIndex[i], tempArray, strIndex[l + 1]))
                        #     symmetricIndex += 1

# for i in range(len(inverse)):
#      print(inverse[i])

# for i in range(len(symmetric)):
#     print(symmetric[i])

# a = {0:[('12', '3'), ('9', '3'), ('9', '7'), ('6', '3'), ('6', '7'),('11', '14')]}
# a = {0:('12', '3'), 1:('9', '3'), 2:('9', '7'), 3:('6', '3'),4: ('6', '7'),5: ('11', '14')}
# print(type(a))
# b = a[0][0]
# print(type(a[0]))
# print(b)
# print(a[0].remove(b))
# a = a
# print(a)
# c = a[0][0]
# a[0].remove(c)
# print(a)
# c = a[0][0]
# a[0].remove(c)
# a = a
# print(a)
# print(a)
# for i in range(len(a[0])):
#     b = a[0][0]
#     a[0].remove(b)
#     a = a
#     if len(a[0]) != 0:
#         print(a)

# =================================打印列表======================================
# for i in range(len(relationWithHT)):
#     temp = relationWithHT[strIndex[i]]      # 第一行
#     temp_1 = [temp[0]]                      # 第一行第一组
#     tempList = [temp_1[0][0], temp_1[0][1]] # 第一行第一组转换成list
#     temp.remove(temp[0])                    # 移除第一组
#     for j in range(len(temp)):
#         if len(temp) != 0:
#             print(temp)
#             temp.remove(temp[0])
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

#print(inverse)