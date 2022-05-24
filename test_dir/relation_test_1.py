lef = {}
rig = {}
rellef = {}
relrig = {}

triple = open("../subgraph_v1/train2id.txt", "r")
# valid = open("dataset/valid2id.txt", "r")
# test = open("test2id.txt", "r")

tot = (int(triple.readline()))
print(type(tot))
for i in range(tot):
    content = triple.readline()
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


# f = open("type_constrain.txt", "w")
# f.write("%d\n"%(len(rellef)))
# for i in rellef:    # 'i' is 'relation', key in the dict
#     print("i is:", i)
#     f.write("%s\t%d"%(i,len(rellef[i])))
#     for j in rellef[i]:    # 'j' is 'head', key in the dict
#         print('j is: ', j)
#         f.write("\t%s"%(j))
#     f.write("\n")
    # f.write("%s\t%d"%(i,len(relrig[i])))
    # for j in relrig[i]:
    #     f.write("\t%s"%(j))
    # f.write("\n")
print('------------------------------------------------')

rellef = {}
totlef = {}
relrig = {}
totrig = {}

for i in lef:
    #print('i is: ', i)
    if not i[1] in rellef:
        #print('i[1] is: ', i[1])
        rellef[i[1]] = 0
        totlef[i[1]] = 0
    rellef[i[1]] += len(lef[i])
    totlef[i[1]] += 1.0
print('rellef is: ', rellef)   # head and relation
print('totlef is: ', totlef)   # how many in each relation, do not include repeated one
print('------------------------------------------------')

for i in rig:
    if not i[0] in relrig:
        relrig[i[0]] = 0
        totrig[i[0]] = 0
    relrig[i[0]] += len(rig[i])
    totrig[i[0]] += 1.0
print('riglef is: ', relrig)   # relation and tail
print('totrig is: ', totrig)   # how many in each relation, do not include repeated one
#f.close()

s11=0
s1n=0
sn1=0
snn=0

f = open("../dataset/test2id.txt", "r")
f11 = open("1-1.txt", "w")
f1n = open("1-n.txt", "w")
fn1 = open("n-1.txt", "w")
fnn = open("n-n.txt", "w")
fall = open("test2id_all.txt", "w")
tot = (int)(f.readline())
fall.write("%d\n"%(tot))
f11.write("%d\n"%(s11))
f1n.write("%d\n"%(s1n))
fn1.write("%d\n"%(sn1))
fnn.write("%d\n"%(snn))
for i in range(tot):
	content = f.readline()
	h,t,r = content.strip().split()
	rign = rellef[r] / totlef[r]
	lefn = relrig[r] / totrig[r]
	if (rign < 1.5 and lefn < 1.5):
		f11.write(content)
		fall.write("0"+"\t"+content)
	if (rign >= 1.5 and lefn < 1.5):
		f1n.write(content)
		fall.write("1"+"\t"+content)
	if (rign < 1.5 and lefn >= 1.5):
		fn1.write(content)
		fall.write("2"+"\t"+content)
	if (rign >= 1.5 and lefn >= 1.5):
		fnn.write(content)
		fall.write("3"+"\t"+content)
fall.close()
f.close()
f11.close()
f1n.close()
fn1.close()
fnn.close()