f = open("dataset/train2id.txt", "r")

total = f.readline()
print('first row is: %s' % total)
second = f.readlines()
print('second row is: %s' % second)