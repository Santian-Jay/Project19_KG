import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from requests import options

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



#statisticsPageButton = Button(window, text="Statistics", command=beginsearch)
#statisticsPageButton.place(x=0, y=600, width=100, height=70)

#visualizationPageButton = Button(window, text="Visualisation", command=beginsearch)
#visualizationPageButton.place(x=0, y=700, width=100, height=70)

sub_window.mainloop()
