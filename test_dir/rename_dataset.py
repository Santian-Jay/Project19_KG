import os

root_dir = "../dataset/train"  #设置根路径
target_dir = "ants"          #目标文档
double_dir = ["ants", "bees"]
out_dir_double = ["ants_label", "bees_label"]

#写入两个文件夹
for n in range(2):
    img_path = os.listdir(os.path.join(root_dir, double_dir[n]))
    label = double_dir[n].split('_')[0]  #设置分隔符
    out_dir = out_dir_double[n]
    for i in img_path:
        file_name = i.split('.jpg')[0]   #设置分隔符
        with open(os.path.join(root_dir, out_dir_double[n], "{}.txt".format(file_name)), 'w') as f:   #创建txt文件
            f.write(label)

#写入一个文件夹
# img_path = os.listdir(os.path.join(root_dir, target_dir))
# label = target_dir.split('_')[0]
# out_dir = "ants_label"
# for i in img_path:
#     file_name = i.split('.jpg')[0]
#     with open(os.path.join(root_dir, out_dir, "{}.txt".format(file_name)), 'w') as f:
#         f.write(label)