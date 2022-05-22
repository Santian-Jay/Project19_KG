from torch.utils.tensorboard import SummaryWriter
from PIL import Image
import numpy as np
import tkinter

writer = SummaryWriter("logs")
image_path = "dataset/train/ants/0013035.jpg"
img_PIL = Image.open(image_path)
image_array = np.array(img_PIL)
print(type(image_array))
print(image_array.shape)

writer.add_image("test", image_array, 2, dataformats='HWC')

#writer.add_image()
for i in range(100):
    writer.add_scalar("y=x", i, i)
writer.close()


#运行，在terminal中输入 tensorboard --logdir=logs