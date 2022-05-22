import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt
import numpy as np
# iris = sns.load_dataset('iris')
# setosa = iris.loc[iris.species == "setosa"].reset_index(drop=True)
# virginica = iris.loc[iris.species == "virginica"].reset_index(drop=True)
#
# ax = sns.kdeplot(iris.petal_width)
# a = [1 1 4 7 1 1 7 2 4 4 0 0 3 3 1 4]
a = [1, 2,3,4,5,6]
data = np.random.randn(10)
print(type(data))
print(data)
res = sns.kdeplot(a)

plt.show()