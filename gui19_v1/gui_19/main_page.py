import tkinter as tk
from views import *


class Main:
    def __init__(self, master: tk.Tk):
        self.root = master
        self.root.title('Knowledge Graph Visualization Tool')
        self.root.geometry('1920x1080')
        self.createPage()

    def createPage(self):
        # tk.Button(root, text='Select Files').place(x=50, y=0, width=200, height=50)
        self.VisualPage = VisualFrame(self.root)  # 创建不同Frame
        self.StatisticPage = StatisticFrame(self.root)
        self.TrainPage = TrainFrame(self.root)

        self.VisualPage.pack(fill='both', expand=True)  # 默认显示可视化界面

        menubar = tk.Menu(self.root)

        menubar.add_command(label='Visualization', command=self.visualData)

        menubar.add_command(label='Statistic', command=self.statisticData)

        menubar.add_command(label='Train', command=self.trainData)

        self.root['menu'] = menubar  # 设置菜单栏

    def visualData(self):
        self.StatisticPage.pack_forget()
        self.TrainPage.pack_forget()

        self.VisualPage.pack(fill='both', expand=True)

    def statisticData(self):
        self.VisualPage.pack_forget()
        self.TrainPage.pack_forget()

        self.StatisticPage.pack(fill='both', expand=True)

    def trainData(self):
        self.VisualPage.pack_forget()
        self.StatisticPage.pack_forget()

        self.TrainPage.pack(fill='both', expand=True)


if __name__ == '__main__':
    root = tk.Tk()
    Main(root)
    root.mainloop()
