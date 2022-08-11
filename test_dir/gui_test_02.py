# Print the graph and save it in .png format
# This method produces temporary files
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk

# G = nx.Graph()
# epoch = 1
#
# # add nodes
# G.add_nodes_from([1, 2, 3, 4])
# # add edges
# G.add_edges_from([(1,2), (1,3), (2,3), (2,4)])
#
# # draw graph
# nx.draw(G, node_size=500, with_labels=True)
#
# save_path = '../subgraph_v1/image/pic-{}.png'.format(epoch+1)
# #plt.savefig('./image/pic-{}.png'.format(epoch+1))
# plt.savefig(save_path)
#
# plt.close()


root = tk.Tk()   # Create tk main window
root.title("tkinter show networkx")

frame1 = tk.Frame(root)   # frame1 Can be regarded as the first page of the book
frame1.pack()             # show first page

img = tk.PhotoImage(file='../subgraph_v1/image/pic-2.png')
# img = tk.PhotoImage(file=save_path)
label_img = tk.Label(frame1, image=img, pady=30, padx=30, bd=0)
label_img.pack(side=tk.LEFT, anchor=tk.N)

tk.Label(frame1, text='anything', height=25, font=24, padx=30, pady=30, anchor=tk.S).pack(side=tk.LEFT)

root.mainloop()