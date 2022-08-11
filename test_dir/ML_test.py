import torch
# torch.LongTensor(1)
a = [1,8,4,4,5,6]
b = []
# for v in a:
#     b.append(torch.LongTensor(v))
b = [torch.LongTensor(vec) for vec in a]
print(b)