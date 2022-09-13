import itertools
from itertools import product, chain
A = ['a', 'b', 'c']
B = ['A', 'B', 'C']
C = [1, 2, 3]
D = [4, 5, 6]

# for i in a:
#     e = []
#     for j in b:
#         for k in c:
#             e.append((i,j,k))
#         d.append(e)
# print(d)
# for row in product(zip(a, b), zip(c, d)):
#     print(list(chain(*row)))
# from itertools import combinations
# for a, b in zip(a, b):
#     print ([c for c in combinations([a,b]+c+d, 4)])
e = [(a, b, c, d) for a in A for b in B for c in C for d in D]
print(e)
import itertools
# from itertools import pairwise
# F = [1,2,3,4,5,6]
# f = list(pairwise(F))
#
# print(f)
