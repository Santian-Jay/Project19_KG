import tkinter as tk
from views import *


class Main:
    def __init__(self, master: tk.Tk):
        self.root = master
        self.root.title('Knowledge Graph Visualization Tool')
        self.root.geometry('1920x1080')
        self.createPage()

    def createPage(self):
        self.VisualPage = VisualFrame(self.root)  # 创建不同Frame
        self.StatisticPage = StatisticFrame(self.root)

        self.VisualPage.pack(fill='both', expand=True)  # 默认显示可视化界面

        menubar = tk.Menu(self.root)

        menubar.add_command(label='Visualization', command=self.visualData)

        menubar.add_command(label='Statistic', command=self.statisticData)

        self.root['menu'] = menubar  # 设置菜单栏

    def visualData(self):
        self.VisualPage.pack(fill='both', expand=True)

        self.StatisticPage.pack_forget()

    def statisticData(self):
        self.VisualPage.pack_forget()

        self.StatisticPage.pack(fill='both', expand=True)


if __name__ == '__main__':
    root = tk.Tk()
    Main(root)
    root.mainloop()
