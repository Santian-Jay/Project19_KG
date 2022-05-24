lef = {}
rig = {}
rellef = {}
relrig = {}

# triple = open("dataset/train2id.txt", "r")
valid = open("../dataset/valid2id.txt", "r")
# test = open("test2id.txt", "r")

tot = (int(valid.readline()))
print(type(tot))
for i in range(tot):
    content = valid.readline()
    h, t, r = content.strip().split()   # 12, 9, 8
    if not (h, r) in lef:               # if 12,8 not in lef
        lef[(h, r)] = []                # lef[(12, 8)] = []
    if not (r, t) in rig:               # if 8,9 not in rig
        rig[(r, t)] = []                # right[(8, 9)] = []
    lef[(h, r)].append(t)               # lef[(12, 8)].append(9)   => lef(12, 8): [9]
    rig[(r, t)].append(h)               # rig[(8, 9)].append(12)   => rig(8, 9): [12]
    if r not in rellef:                 # if 8 not in rellef
        rellef[r] = {}                  # rellef[8] = {}
    if r not in relrig:                 # if 8 not in relrig
        relrig[r] = {}                  # relrig[8] = {}
    rellef[r][h] = 1                    # rellef[8][12] = 1  => rellef[8][12, 1]
    relrig[r][t] = 1                    # relrig[8][9] = 1   => relrig[8][9, 1]
print(lef)
print(rig)
print("------------------------------------------------")
print(rellef)     # 关系（r）是0，7,8,5，6,4,1,2,3的h
print(relrig)     # 关系（r）是0，7,8,5,6,4,1,2,3的t


f = open("type_constrain.txt", "w")
f.write("%d\n"%(len(rellef)))
for i in rellef:    # 'i' is 'relation', key in the dict
    print("i is:", i)
    f.write("%s\t%d"%(i,len(rellef[i])))
    print('组合 is: ', rellef[i])
    for j in rellef[i]:    # 'j' is 'head', key in the dict
        print('j is: ', j)
        f.write("\t%s"%(j))
    f.write("\n")
    f.write("%s\t%d"%(i,len(relrig[i])))
    print('组合 2 is: ', relrig[i])
    for j in relrig[i]:
        print('k is: ', j)
        f.write("\t%s"%(j))
    f.write("\n")
f.close()