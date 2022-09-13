
def nn_categorization(new_train):
	lef = {}
	rig = {}
	rellef = {}
	relrig = {}

	# triple = new_train

	temp = open('dataset/temp_text.txt', 'w', encoding='UTF-8')
	temp.write(new_train[0][0]+"\n")
	for data in new_train:
		if len(data) != 1:
			temp.write(data[0] + '\t' + data[1] + '\t' + data[2] + '\n')
	temp.close()
	# triple = open("subgraph_v1/train2id.txt", "r")
	# valid = open("dataset/valid2id.txt", "r")
	# test = open("dataset/test2id.txt", "r")
	triple = open("dataset/YAGO3-10/train2id.txt", "r", encoding='UTF-8')
	tot = (int)(triple.readline())

	print(tot)
	for i in range(tot):
		content = triple.readline()
		h,t,r = content.strip().split()
		if not (h,r) in lef:
			lef[(h,r)] = []
		if not (r,t) in rig:
			rig[(r,t)] = []
		lef[(h,r)].append(t)
		rig[(r,t)].append(h)
		if not r in rellef:
			rellef[r] = {}
		if not r in relrig:
			relrig[r] = {}
		rellef[r][h] = 1
		relrig[r][t] = 1
	#
	# tot = (int)(valid.readline())
	# for i in range(tot):
	# 	content = valid.readline()
	# 	h,t,r = content.strip().split()
	# 	if not (h,r) in lef:
	# 		lef[(h,r)] = []
	# 	if not (r,t) in rig:
	# 		rig[(r,t)] = []
	# 	lef[(h,r)].append(t)
	# 	rig[(r,t)].append(h)
	# 	if not r in rellef:
	# 		rellef[r] = {}
	# 	if not r in relrig:
	# 		relrig[r] = {}
	# 	rellef[r][h] = 1
	# 	relrig[r][t] = 1
	#
	# tot = (int)(test.readline())
	# for i in range(tot):
	# 	content = test.readline()
	# 	h,t,r = content.strip().split()
	# 	if not (h,r) in lef:
	# 		lef[(h,r)] = []
	# 	if not (r,t) in rig:
	# 		rig[(r,t)] = []
	# 	lef[(h,r)].append(t)
	# 	rig[(r,t)].append(h)
	# 	if not r in rellef:
	# 		rellef[r] = {}
	# 	if not r in relrig:
	# 		relrig[r] = {}
	# 	rellef[r][h] = 1
	# 	relrig[r][t] = 1
	#
	# test.close()

	# valid.close()
	# triple.close()

	# f = open("type_constrain.txt", "w")
	# f.write("%d\n"%(len(rellef)))
	# for i in rellef:
	# 	f.write("%s\t%d"%(i,len(rellef[i])))
	# 	for j in rellef[i]:
	# 		f.write("\t%s"%(j))
	# 	f.write("\n")
	# 	f.write("%s\t%d"%(i,len(relrig[i])))
	# 	for j in relrig[i]:
	# 		f.write("\t%s"%(j))
	# 	f.write("\n")
	# f.close()

	rellef = {}
	totlef = {}
	relrig = {}
	totrig = {}
	# lef: (h, r)
	# rig: (r, t)

	for i in lef:
		if not i[1] in rellef:    # i 是dictionary lef的index（('10', '0'): ['3']）。index 是 ('10', '0'),len(lef[i]) = 1
			rellef[i[1]] = 0
			totlef[i[1]] = 0
		rellef[i[1]] += len(lef[i])
		totlef[i[1]] += 1.0
	print(rellef)
	print(totlef)

	for i in rig:
		if not i[0] in relrig:
			relrig[i[0]] = 0
			totrig[i[0]] = 0
		relrig[i[0]] += len(rig[i])
		totrig[i[0]] += 1.0

	s11=0
	s1n=0
	sn1=0
	snn=0
	f = open("dataset/YAGO3-10/train2id.txt", "r", encoding='UTF-8')
	tot = (int)(f.readline())
	for i in range(tot):
		content = f.readline()
		h,t,r = content.strip().split()
		rign = rellef[r] / totlef[r]
		lefn = relrig[r] / totrig[r]
		if (rign < 1.5 and lefn < 1.5):
			s11+=1
		if (rign >= 1.5 and lefn < 1.5):
			s1n+=1
		if (rign < 1.5 and lefn >= 1.5):
			sn1+=1
		if (rign >= 1.5 and lefn >= 1.5):
			snn+=1
	f.close()

	# used code
	f = open("dataset/YAGO3-10/train2id.txt", "r", encoding='UTF-8')
	f11 = open("dataset/1-1.txt", "w", encoding='UTF-8')
	f1n = open("dataset/1-n.txt", "w", encoding='UTF-8')
	fn1 = open("dataset/n-1.txt", "w", encoding='UTF-8')
	fnn = open("dataset/n-n.txt", "w", encoding='UTF-8')
	fall = open("dataset/test2id_all.txt", "w", encoding='UTF-8')
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
			f11.write(r+"\n")
			fall.write("0"+"\t"+content)
		if (rign >= 1.5 and lefn < 1.5):
			f1n.write(r+"\n")
			fall.write("1"+"\t"+content)
		if (rign < 1.5 and lefn >= 1.5):
			fn1.write(r+"\n")
			fall.write("2"+"\t"+content)
		if (rign >= 1.5 and lefn >= 1.5):
			fnn.write(r+"\n")
			fall.write("3"+"\t"+content)
	fall.close()
	f.close()
	f11.close()
	f1n.close()
	fn1.close()
	fnn.close()
	return s11, s1n, sn1, snn
