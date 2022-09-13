# import json
#
# fjson = 'json_insert_test.json'
# with open(fjson, 'r') as f:
#     content = json.load(f)
# print(len(content))
# a = 'TransE'
# path = 'path/' + a + '/data.json'
# print(path)
# print(type(content))
# xis = {"xis": [22, 10, 11, 10]}
# content.update(xis)
#
# with open(fjson, 'w') as f_new:
#     json.dump(content, f_new)

# y = [{'id': 0, 'name': []},
#      {'id': 5, 'name': 'Hank'},
#      {'id': 8, 'name': 'Fred'},
#      {'id': 30, 'name': 'Jill'}]


# new_value = {'id': 43, 'name': 'Ja'}
#
# for index, value in enumerate(content):
#     # Assuming y is in increasing order.
#     insert = False
#     print('current index: ', index, value)
#     if index <= len(content) - 1:
#         if value['id'] > new_value['id']:
#             content.insert(index, new_value)
#             insert = True
#             # print('current index: ', index, value)
#             break
#     if index == len(content) - 1 and insert is False:
#         content.insert(index + 1, new_value)
#         break
# with open(fjson, 'w') as f_new:
#     json.dump(content, f_new)
# print(content)

# import time
# import datetime
#
# now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
# print(now_time)
import torch
print(torch.cuda.is_available())