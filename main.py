import torch
import networkx
import pyodbc
import numpy
import torchvision
from torch.utils.data import Dataset

print("----------------------")
print(torch.__version__)
print(torchvision.__version__)
print("----------------------")
print(torch.version.cuda)
print(torch.backends.cudnn.version())
print('GPU', torch.cuda.is_available())
print('=====================')
print(networkx.__version__)
print(pyodbc.version)
print(numpy.__version__)


# x=torch.rand(5,3)
# print(x)