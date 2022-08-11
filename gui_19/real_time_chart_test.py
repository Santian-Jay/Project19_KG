import warnings
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", "GUI is implemented")

x = np.arange(0, 10)
y = np.random.randint(10, 30, 10)
for i in range(20):
    #
    plt.cla()
    plt.barh(x, y)
    plt.title(str(i))
    plt.yticks(x, list(map(lambda i: '%d月'%i, x)), fontproperties='simhei')

    plt.pause(0.5)
    y = y+np.random.randint(0, 5, 10)

plt.show()

# from pyecharts.charts import Bar
#
# # v1 版本开始支持链式调用
# bar = (
#     Bar()
#         .add_xaxis(['衬衫', '毛衣', '裤子'])
#         .add_yaxis('商家A', [10, 20, 30])
#         .add_yaxis('商家B', [30, 20, 10])
# )
#
# # render 会生成本地 html 文件，默认当前目录，且文件名称为 render.html
# # 同样也可以传入参数，例如：bar.render('mycharts.html')
# bar.render()