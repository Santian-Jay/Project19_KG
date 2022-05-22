import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# import GUI_19



def sub_window():
    sub_window = tk.Tk()
    sub_window.title("Knowledge Graph Visualization Tool")
    sub_window.geometry("1920x1080")

    # Upload files
    def create_sub_Window():
        sfwindow = tk.Toplevel(sub_window)
        sfwindow.title("Select Files")
        sfwindow.geometry("1000x500")
        entityFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        entityFrame.grid(row=0, column=0, padx=(150, 80), pady=100)
        entityButton = tk.Button(entityFrame, text="Entity", command=lambda: filedialog.askopenfile(mode='r'))
        entityButton.place(x=28, y=240, width=120, height=25)
        relationFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        relationFrame.grid(row=0, column=1, padx=0, pady=100)
        relationButton = tk.Button(relationFrame, text="Relation", command=lambda: filedialog.askopenfile(mode='r'))
        relationButton.place(x=28, y=240, width=120, height=25)
        factFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        factFrame.grid(row=0, column=2, padx=80, pady=100)
        factButton = tk.Button(factFrame, text="Fact", command=lambda: filedialog.askopenfile(mode='r'))
        factButton.place(x=28, y=240, width=120, height=25)
        cancelButton = tk.Button(sfwindow, text="cancel")
        cancelButton.place(x=600, y=450, width=120, height=25)
        saveButton = tk.Button(sfwindow, text="Save")
        saveButton.place(x=770, y=450, width=120, height=25)

    FilesButton = tk.Button(sub_window, text="Select files", command=create_sub_Window)
    FilesButton.place(x=100, y=30, width=120, height=35)

    # DatabaseBar
    selectedDatabases = [
        "Database 1",
        "Database 2",
        "Database 3"
    ]
    selectDatabase = ttk.Combobox(sub_window, values=selectedDatabases, width=30)
    selectDatabase.place(x=285, y=30, width=280, height=35)
    # selectDatabase.pack(padx=135, pady=15, side=LEFT)
    selectDatabase.set("Select your database")

    # search bar_1
    searchBox = Entry(sub_window, width=100)
    searchBox.place(x=570, y=30, width=250, height=35)
    # searchBox.pack(padx=5, pady=15, side=LEFT)
    searchBox.insert(0, "Entity")

    # search bar_2
    searchBox = Entry(sub_window, width=100)
    searchBox.place(x=830, y=30, width=250, height=35)
    # searchBox.pack(padx=5, pady=15, side=LEFT)
    searchBox.insert(0, "Relation")

    def beginsearch():
        result = "result"

    search_button = Button(sub_window, text="Batch search", command=beginsearch)
    search_button.place(x=1100, y=30, width=100, height=35)
    # searchButton.pack(padx=5, pady=15, side=LEFT)

    # frame for table
    statsFrame = Frame(sub_window, highlightbackground="black", highlightthickness=2)
    statsFrame.place(x=250, y=150, width=900, height=600)

    # scrollbar
    statsScroll = Scrollbar(statsFrame)
    statsScroll.pack(side=RIGHT, fill=Y)

    # table
    columns = ("entity1", "relationship", "entity2")
    headers = ("Entity", "Relationship", "Entity")
    widthes = (200, 150, 200)
    tv = ttk.Treeview(statsFrame, yscrollcommand=statsScroll.set, show="headings", columns=columns)

    for (column, header, width) in zip(columns, headers, widthes):
        tv.column(column, width=width, anchor="w")
        tv.heading(column, text=header, anchor="w")

    def inser_data():
        """List"""
        facts = [
            ('Dog', 'Intimidates', 'Cat'),
            ('Cat', 'Attacks', 'Dog'),
            ('Giraffe', 'Carries', 'Monkey'),
            ('Elephant', 'Carries', 'Birds'),
            ('Monkey', 'Fights', 'Monkey'),
            ('Dog', 'Intimidates', 'Cat'),
            ('Cat', 'Attacks', 'Dog'),
            ('Giraffe', 'Carries', 'Monkey'),
            ('Elephant', 'Carries', 'Birds'),
            ('Monkey', 'Fights', 'Monkey'),
            ('Dog', 'Intimidates', 'Cat'),
            ('Cat', 'Attacks', 'Dog'),
            ('Giraffe', 'Carries', 'Monkey'),
            ('Elephant', 'Carries', 'Birds'),
            ('Monkey', 'Fights', 'Monkey'),
        ]
        for i, person in enumerate(facts):
            tv.insert('', i, values=person)

    inser_data()

    # tv.place(x=300, y=200, width=600, height=500)
    tv.pack()

    sub_window.protocol('WM_DELETE_WINDOW', lambda: [sub_window.destroy(), enter()])
    # statisticsPageButton = Button(window, text="Statistics", command=beginsearch)
    # statisticsPageButton.place(x=0, y=600, width=100, height=70)

    # visualizationPageButton = Button(window, text="Visualisation", command=beginsearch)
    # visualizationPageButton.place(x=0, y=700, width=100, height=70)

    sub_window.mainloop()

# ====================================main window==============================================

def enter():
    window = tk.Tk()
    window.title("Knowledge Graph Visualization Tool")
    window.geometry("1920x1080")

    # Upload files
    def create_Window():
        sfwindow = tk.Toplevel(window)
        sfwindow.title("Select Files")
        sfwindow.geometry("1000x500")
        entityFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        entityFrame.grid(row=0, column=0, padx=(150, 80), pady=100)
        entityButton = tk.Button(entityFrame, text="Entity", command=lambda: filedialog.askopenfile(mode='r'))
        entityButton.place(x=28, y=240, width=120, height=25)
        relationFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        relationFrame.grid(row=0, column=1, padx=0, pady=100)
        relationButton = tk.Button(relationFrame, text="Relation", command=lambda: filedialog.askopenfile(mode='r'))
        relationButton.place(x=28, y=240, width=120, height=25)
        factFrame = Frame(sfwindow, width=180, height=300, highlightbackground="black", highlightthickness=2)
        factFrame.grid(row=0, column=2, padx=80, pady=100)
        factButton = tk.Button(factFrame, text="Fact", command=lambda: filedialog.askopenfile(mode='r'))
        factButton.place(x=28, y=240, width=120, height=25)
        cancelButton = tk.Button(sfwindow, text="cancel")
        cancelButton.place(x=600, y=450, width=120, height=25)
        saveButton = tk.Button(sfwindow, text="Save")
        saveButton.place(x=770, y=450, width=120, height=25)

    FilesButton = tk.Button(window, text="Select files", command=create_Window)
    FilesButton.place(x=100, y=30, width=120, height=35)

    # DatabaseBar
    selectedDatabases = [
        "Database 1",
        "Database 2",
        "Database 3"
    ]
    selectDatabase = ttk.Combobox(window, values=selectedDatabases, width=30)
    selectDatabase.place(x=285, y=30, width=280, height=35)
    # selectDatabase.pack(padx=135, pady=15, side=LEFT)
    selectDatabase.set("Select your database")

    # search bar
    searchBox = Entry(window, width=100)
    searchBox.place(x=670, y=30, width=400, height=25)
    # searchBox.pack(padx=5, pady=15, side=LEFT)
    searchBox.insert(0, "batch search")

    # search bar_1
    searchBox = Entry(window, width=100)
    searchBox.place(x=570, y=30, width=250, height=35)
    # searchBox.pack(padx=5, pady=15, side=LEFT)
    searchBox.insert(0, "Entity")

    # search bar_2
    searchBox = Entry(window, width=100)
    searchBox.place(x=830, y=30, width=250, height=35)
    # searchBox.pack(padx=5, pady=15, side=LEFT)
    searchBox.insert(0, "Relation")

    def beginsearch():
        result = "result"

    search_button = Button(window, text="Batch search", command=beginsearch)
    search_button.place(x=1100, y=30, width=100, height=35)
    # searchButton.pack(padx=5, pady=15, side=LEFT)

    # frame for rangeBox
    statsFrame = Frame(window, highlightbackground="black", highlightthickness=1)
    statsFrame.place(x=1100, y=530, width=180, height=150)

    var = tk.StringVar()
    label = tk.Label(statsFrame, background="grey", width=20, text="Range")
    label.pack()

    # def print_list():
    # label.config(text="Range" + var.get())

    RangeButton1 = tk.Radiobutton(statsFrame, text="No. of Entities", variable=var, value="Entities")
    RangeButton1.pack(fill=X, pady=3)
    RangeButton2 = tk.Radiobutton(statsFrame, text="Hop Count", variable=var, value="Count")
    RangeButton2.pack(fill=X, pady=3)
    RangeButton3 = tk.Radiobutton(statsFrame, text="No. of Subgraphs", variable=var, value="Entities")
    RangeButton3.pack(fill=X, pady=3)

    # frame for subGraphs
    # subgraphFrame = Frame(window, highlightbackground="black", highlightthickness=1)
    # subgraphFrame.place(x=1100, y=630, width=180, height=140)

    # label2 = tk.Label(subgraphFrame, background="grey", width=20, text="SubGraphs")
    # label2.pack()

    # var1 = tk.IntVar()
    # var2 = tk.IntVar()
    # var3 = tk.IntVar()

    # subGraph1 = tk.Checkbutton(subgraphFrame, text='search 1', variable=var1, onvalue=1, offvalue=0, )
    # subGraph2 = tk.Checkbutton(subgraphFrame, text='search 2', variable=var2, onvalue=1, offvalue=0, )
    # subGraph3 = tk.Checkbutton(subgraphFrame, text='search 3', variable=var3, onvalue=1, offvalue=0, )
    # subGraph1.pack(fill=X, pady=3)
    # subGraph2.pack(fill=X, pady=3)
    # subGraph3.pack(fill=X, pady=3)

    # statisticsPageButton = Button(window, text="Statistics", command=lambda: [window.destroy, GUI_19.create_sub_Window()])
    statisticsPageButton = Button(window, text="Statistics", command=lambda: [window.destroy(), sub_window()])
    statisticsPageButton.place(x=0, y=600, width=100, height=70)

    visualizationPageButton = Button(window, text="Visualisation", command=beginsearch)
    visualizationPageButton.place(x=0, y=700, width=100, height=70)

    window.mainloop()

enter()