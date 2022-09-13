import os

input_path = 'D:\PyCharm\pythonProject\pythonProject_v5/KG_Data'

dir_list = []
file_list = []

for root, dirs, files in os.walk(input_path):
    dir_list = dirs
    file_list = files
    break

print('dirs list: ', dir_list, len(dir_list))
print('files list: ', file_list, len(file_list))
#
# print(os.getcwd())
#
# print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath('.'))
print(os.path.abspath('..'))