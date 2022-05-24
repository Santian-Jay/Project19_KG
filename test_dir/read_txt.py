# open file
f = open('../subgraph_v1/entity2id.txt', 'r')

# 读取全部内容
# data = f.read()
# print(data)   #end=''不打印换行空格，print(data, end='')


f = open('../subgraph_v1/entity2id.txt', 'r')  # open file

all_data = f.readlines()  # read data line by line

new = []  # save data to list
for i in all_data:
    first = i.strip('\n')
    second = first.split()
    new.append(second)

f.close()  # close file
