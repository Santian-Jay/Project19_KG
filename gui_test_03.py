# This method reads the image through the cache and does not generate temporary files
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
import io
from PIL import Image
from PIL import ImageTk

root = tk.Tk()   # Create tk main window
root.title("tkinter show networkx")

G = nx.Graph()  # Undirected graph
epoch = 1

# add nodes
G.add_nodes_from([1, 2, 3, 4, 5])
# addd edges
G.add_edges_from([(1,2), (1,3), (2,3), (2,4), (3,5), (4,5)])

# draw graph
nx.draw(G, node_size=500, with_labels=True)

# buffer variable
buffer = io.BytesIO()
plt.savefig(buffer, format='PNG')
img0 = Image.open(io.BytesIO(buffer.getvalue()))
print(type(img0))
img1 = img0.resize((500, 500))
buffer.close()
#img1.show()
#print(type(img1))

#
# canvas = Canvas(root, bg='green', height=800, width=1000)          # can also put pictures on canvas
# canvas.pack()
#
# im2 = ImageTk.PhotoImage(img1)
# canvas.create_image(1, 1, anchor=NW, image=im2)
#
# root.mainloop()

##save_path = './image/pic-{}.png'.format(epoch+1)
#plt.savefig('./image/pic-{}.png'.format(epoch+1))
#plt.savefig(save_path)
#plt.pause(1)
#plt.close()
#plt.show()

frame1 = tk.Frame(root)
frame1.pack()

# img = tk.PhotoImage(file='image/Figure_1.png')  #The first method, read the image from the path
# print(type(img))
# img = tk.PhotoImage(file=)

img = ImageTk.PhotoImage(img1)  # The second method, read the image from the cache

label_img = tk.Label(frame1, image=img, pady=30, padx=30, bd=0)
label_img.pack(side=tk.LEFT, anchor=tk.N)

tk.Label(frame1, text='anything', height=25, font=24, padx=30, pady=30, anchor=tk.S).pack(side=tk.LEFT)

root.mainloop()