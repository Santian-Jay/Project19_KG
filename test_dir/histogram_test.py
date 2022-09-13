# from tkinter import *
# import tkinter.messagebox
# import urllib.request
# import turtle
#
#
# def main():
#     counts = analyzeFile(url.get())
#     drawHistogram(counts)
#
# def analyzeFile(url):
#     try:
#         infile = urllib.request.urlopen(url)
#         s = str(infile.read().decode()) # Read the content as string from the URL
#
#         counts = countLetters(s.lower())
#
#         infile.close() # Close file
#     except ValueError:
#         tkinter.messagebox.showwarning("Analyze URL",
#             "URL " + url + " does not exist")
#
#     return counts
#
# def countLetters(s):
#     counts = 26 * [0] # Create and initialize counts
#     for ch in s:
#         if ch.isalpha():
#             counts[ord(ch) - ord('a')] += 1
#     return counts
#
# def drawHistogram(list):
#
#     WIDTH = 400
#     HEIGHT = 300
#
#     raw_turtle.penup()
#     raw_turtle.goto(-WIDTH / 2, -HEIGHT / 2)
#     raw_turtle.pendown()
#     raw_turtle.forward(WIDTH)
#
#     widthOfBar = WIDTH / len(list)
#
#     for i in range(len(list)):
#         height = list[i] * HEIGHT / max(list)
#         drawABar(-WIDTH / 2 + i * widthOfBar,
#             -HEIGHT / 2, widthOfBar, height, letter_number=i)
#
#     raw_turtle.hideturtle()
#
# def drawABar(i, j, widthOfBar, height, letter_number):
#     alf='abcdefghijklmnopqrstuvwxyz'
#     raw_turtle.penup()
#     raw_turtle.goto(i+2, j-20)
#
#     #sign letter on histogram
#     raw_turtle.write(alf[letter_number])
#     raw_turtle.goto(i, j)
#
#     raw_turtle.setheading(90)
#     raw_turtle.pendown()
#
#
#     raw_turtle.forward(height)
#     raw_turtle.right(90)
#     raw_turtle.forward(widthOfBar)
#     raw_turtle.right(90)
#     raw_turtle.forward(height)
#
# window = Tk()
# window.title("Occurrence of Letters in a Histogram from URL")
#
# frame1 = Frame(window)
# frame1.pack()
#
# scrollbar = Scrollbar(frame1)
# scrollbar.pack(side = RIGHT, fill = Y)
#
# canvas = tkinter.Canvas(frame1, width=450, height=450)
# raw_turtle = turtle.RawTurtle(canvas)
#
# scrollbar.config(command = canvas.yview)
# canvas.config( yscrollcommand=scrollbar.set)
# canvas.pack()
#
# frame2 = Frame(window)
# frame2.pack()
#
# Label(frame2, text = "Enter a URL: ").pack(side = LEFT)
# url = StringVar()
# Entry(frame2, width = 50, textvariable = url).pack(side = LEFT)
# Button(frame2, text = "Show Result", command = main).pack(side = LEFT)
#
# window.mainloop()


# #柱形图
# import pandas
# import numpy
# import matplotlib
# from matplotlib import pyplot as plt
# #导入数据
# data_columns=pandas.read_csv('D://Python projects//reference data//6.4//data.csv')
# #定义中文格式
# font={'family':'MicroSoft Yahei',
#       'weight':'bold',
#       'size':12}
# matplotlib.rc('font',**font)
# #使用手机品牌作为分组列，月消费作为统计列
# result_columns=data_columns.groupby(
#         by=['手机品牌'],
#         as_index=False)['月消费（元）'
#                       ].agg({'月总消费':numpy.sum
#                               })
# #生成一个间隔为1的序列
# index=numpy.arange(result_columns.月总消费.size)
# #绘制纵向柱形图
# plt.bar(index,result_columns['月总消费'])
# #%matplotlib qt
# plt.show()
# #配置颜色
# maincolor=(42/256,87/256,141/256,1)
# plt.bar(index,
#         result_columns['月总消费'])
# plt.show()
# #配置X轴标签
# plt.bar(index,
#         result_columns['月总消费'])
# plt.xticks(index,result_columns.手机品牌)
# plt.show()
# #对数据进行降序排序后展示
# result_asd=result_columns.sort_values(
#         by='月总消费',
#         ascending=False)
# plt.bar(index,
#         result_asd.月总消费,
#         color=maincolor)
# plt.xticks(index,result_asd.手机品牌)
# plt.show()


# import matplotlib as mpl
# import matplotlib.pyplot as plt
#
# mpl.rcParams["font.sans-serif"]=["SimHei"]
# #指定字体为SimHei，用于显示中文，如果Ariel,中文会乱码
# mpl.rcParams["axes.unicode_minus"]=False
#
# x = [1,2]
# y = [30,11]
# #数据
# # labels=["A","B","C","D","E","F","G","H"]
# labels=["A","B"]
# #定义柱子的标签
# plt.bar(x,y,align="center",color="rgb",tick_label=labels,width=0.2)
# #绘制纵向柱状图,hatch定义柱图的斜纹填充，省略该参数表示默认不填充。
#
# #bar柱图函数还有以下参数：
# #颜色：color,可以取具体颜色如red(简写为r),也可以用rgb让每条柱子采用不同颜色。
# #描边：edgecolor（ec）：边缘颜色；linestyle（ls）：边缘样式；linewidth（lw）：边缘粗细
# #填充：hatch，取值：/,|,-,+,x,o,O,.,*
# #位置标志：tick_label
#
# plt.xlabel(u"样品编号")
# plt.ylabel(u"库伦效率/%")
#
# plt.show()


# import matplotlib.pyplot as plt;plt.rcdefaults()
# from numpy.random import rand
# from numpy import arange
# import numpy as np
#
# def libra_execution_time():
#     data = np.genfromtxt('C:\\programming\\Python27\\libra_graphs\\File\\histogram.csv',delimiter=',')
#
#     hash_diff,key_diff,binary_diff = 0,0,0
#
#     hash_time_lst,key_time_lst,binary_time_lst = [],[],[]
#
#     for row in data:
#         if not np.isnan(row[7]):
#             hash_diff = row[7]-hash_diff
#     hash_time_lst.append(hash_diff)
#
#     for row in data:
#         if not np.isnan(row[8]):
#             key_diff = row[8]-key_diff
#     key_time_lst.append(key_diff)
#
#     for row in data:
#         if not np.isnan(row[9]):
#             binary_diff = row[9]-binary_diff
#     binary_time_lst.append(binary_diff)
#
#     # print "#Hash Partitioner ->" ,hash_time_lst,len(hash_time_lst)
#     # print "#Key Field Partitioenr ->", key_time_lst,len(key_time_lst)
#     # print "#Binary Partitioner ->",binary_time_lst,len(binary_time_lst)
#
#
#     #x_lst = (hash_time_lst + key_time_lst + binary_time_lst)
#     #print x_lst
#     job_time = {"Hash Time":hash_time_lst,"Key_Time":key_time_lst,"Binary Time":binary_time_lst}
#     # print job_time
#     # print job_time.keys(),job_time.values()
#
#     y_pos = np.arange(len(job_time.values()))
#     # print "Y position",y_pos
#     val = np.array(job_time.values())
#     # print val
#
#
#     plt.barh(y_pos,val ,align='center',height = 0.5 ,color=('r','y','g'))
#     plt.yticks(y_pos,job_time.keys())
#
#     plt.xlabel('Time(seconds)')
#     plt.ylabel('Performance ->')
#     plt.title('Job Execution LIBRA')
#
#     plt.show()
#
# libra_execution_time()
import matplotlib.pyplot as plt
# x = [3]
# y = [10]
x = [1,2,3,4,5,6,7,8]
y = [30,11,42,53,81,98,72,25]
fig,ax = plt.subplots(1,1)
ax.bar(x, y, width=0.4)
ax.set_xlim(0, 10)
plt.show()