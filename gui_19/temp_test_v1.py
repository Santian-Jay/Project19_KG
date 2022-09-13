# a = {9: [1, 90, 9], 3: [10, 36, 22], 8:[11,22,33], 1:[14, 15], 10:[37, 38]}
# # length = 0
# # for item in a:
# #     length = length + len(a[item])
# # print(length)
# deleted = [9, 3]
# for n in deleted:
#     if 9 in a[n]:
#         del a[n]
#
# print(a)

# import random
# position = []
# for i in range(10):
#     x = random.randint(100, 1300)
#     y = random.randint(60, 1100)
#     if (x, y) not in position:
#         position.append((x, y))
#
# print(position)
from tkinter import *
name = 'relation' + str(1)
a = {name: 123}
n = 'relation' + str(1)
n = Button(text='test')
print(type(n))
print(a)
