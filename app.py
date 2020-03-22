import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

import SQLite
from gen import Generator, Cell
import solve

FONT = ("Verdana", 12)


def popUpMsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=FONT)
    label.pack(side="top", fill='x', pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()


def loadPhoto(path):
    root = tk.Toplevel()
    root.title('MAZE')
    root.geometry("600x600")
    root.configure(bg="black")
    img = Image.open(r"images\{}".format(path))
    resize = img.resize((600, 600), Image.ANTIALIAS)
    resize.save('temp.png')
    resized = ImageTk.PhotoImage(Image.open('temp.png'))
    img_label = tk.Label(root)
    img_label.image = resized
    img_label['image'] = img_label.image

    img_label.grid(column=1, row=0, rowspan=5)


class Run():

    def genMaze(self, size, alg, ID, name):
        size = int(size)
        maze = Generator(name, size, size)
        if alg == 'RB':
            time2gen = maze.reveseBacktracking()
        elif alg == 'BT':
            time2gen = maze.BinaryTree()
        else:
            return 'invalid input'
        maze.drawMaze()
        maze.saveMaze(time2gen)

    def solMaze(self, id, alg):
        maze = solve.Solve(id)
        if alg == 'BF':
            time2solve = maze.BFS()
        maze.drawPath()
        maze.saveMazeSolved(time2solve)

    def loadMaze(self, id):
        SQLite.readBLOBData(id)
        times = SQLite.getTimes(id)
        return times


global id
id = ''


class App(tk.Tk):

    def __init__(self, *args, **kargs):
        tk.Tk.__init__(self, *args, **kargs)
        self.title("BZB'S MAZES")

        container = ttk.Frame(self)
        s = ttk.Style(self)
        s.configure('TButton', foreground='black', background='white', fontsize=100)

        container.pack(side="top", fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (startPage, genMaze, solMaze, loadMaze):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(startPage)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class startPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("320x300")
        self.label = ttk.Label(self, text="My Amazing Mazes")
        self.B1 = ttk.Button(self, text='Generate a Maze', style='TButton',
                             command=lambda: controller.showFrame(genMaze))
        self.B2 = ttk.Button(self, text='Solve a Maze', command=lambda: controller.showFrame(solMaze))
        self.B3 = ttk.Button(self, text='Load a Maze', command=lambda: controller.showFrame(loadMaze))
        self.B4 = ttk.Button(self, text='Quit', command=lambda: controller.destroy())
        self.label.grid(column=0, row=0)
        self.B1.grid(column=0, row=1, padx=40, pady=10, sticky="ew", ipadx=50, ipady=10)
        self.B2.grid(column=0, row=2, padx=40, pady=10, sticky="ew", ipadx=50, ipady=10)
        self.B3.grid(column=0, row=3, padx=40, pady=10, sticky="ew", ipadx=50, ipady=10)
        self.B4.grid(column=0, row=4, padx=40, pady=10, sticky="ew", ipadx=50, ipady=10)


class genMaze(tk.Frame):

    def buttonPressGen(self):
        name = self.E1.get()
        ID = name
        size = self.E2.get()
        alg = self.E3.get()
        self.E1.delete(0, 'end')
        self.E2.delete(0, 'end')
        try:
            loadPhoto("thinking.gif")
            Run().genMaze(size, alg, ID, name)
            loadPhoto("giphy.gif")
        except MemoryError:
            popUpMsg('Sorry those numbers are too large, please enter a smaller number. Or use a different algorithm')
        except:
            popUpMsg(
                'Invaid input, please try again.\nSize has to be a intager.\nAlgorithms to choose from are:\nRB ('
                'revese Backtracking) or BT (binary Tree)')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.L1 = ttk.Label(self, text="Enter a name: ")
        self.L2 = ttk.Label(self, text="Enter a size: ")
        self.L3 = ttk.Label(self, text="Enter a algorithm: ")
        self.E1 = ttk.Entry(self, width=15)
        self.E2 = ttk.Entry(self, width=5)
        self.E3 = ttk.Entry(self, width=5)
        self.L1.grid(column=0, row=0, sticky="w")
        self.L2.grid(column=0, row=1, sticky="w")
        self.L3.grid(column=0, row=2, sticky="w")
        self.E1.grid(column=1, row=0, sticky="w")
        self.E2.grid(column=1, row=1, sticky="w")
        self.E3.grid(column=1, row=2, sticky="w")
        self.E3.insert(0, 'RB')
        B1 = ttk.Button(self, text='Enter', command=lambda: self.buttonPressGen())
        B2 = ttk.Button(self, text='Back', command=lambda: controller.showFrame(startPage))
        B1.grid(column=0, row=3, padx=40, pady=40)
        B2.grid(column=1, row=3, padx=40, pady=40)


class solMaze(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.L1 = ttk.Label(self, text="Enter an Algorithm: ")
        self.L2 = ttk.Label(self, text="Enter name of maze to solve: ")
        self.E1 = ttk.Entry(self, width=5)
        self.E2 = ttk.Entry(self, width=5)
        self.E1.insert(0, 'BF')
        self.E2.insert(0, id)
        self.B1 = ttk.Button(self, text='Solve', command=lambda: self.buttonPressSolve())
        self.B2 = ttk.Button(self, text='Back', command=lambda: controller.showFrame(startPage))
        self.L1.grid(column=0, row=0, padx=10, pady=10, sticky="e")
        self.L2.grid(column=0, row=1, padx=10, pady=10, sticky="e")
        self.E1.grid(column=1, row=0, padx=10, pady=10, sticky="w")
        self.E2.grid(column=1, row=1, padx=10, pady=10, sticky="w")
        self.B1.grid(column=0, row=2, padx=10, pady=50)
        self.B2.grid(column=1, row=2, padx=10, pady=50)

    def buttonPressSolve(self):
        loadPhoto("thinking.gif")
        alg = self.E1.get()
        name = self.E2.get()
        id = name
        try:
            Run().solMaze(id, alg)
            Run().loadMaze(id)
            loadPhoto('s{}.png'.format(name))
        except:
            popUpMsg("That maze doesn't exist. Please try a different ID.")



class loadMaze(tk.Frame):

    def buttonPressLoad(self, controller):
        name = self.E.get()
        try:
            time = Run().loadMaze(name)
            loadPhoto('{}.png'.format(name))
            try:
                loadPhoto('s{}.png'.format(name))
            except:
                pass
            popUpMsg('Time to Generate: {}\nTime to Solve: {}'.format(time[0], time[1]))
        except:
            popUpMsg("That maze doesn't exsited, please try a different ID.")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.L = ttk.Label(self, text="Enter name of maze: ")
        self.E = ttk.Entry(self, width=5)
        self.L.grid(column=0, row=0, padx=20, pady=50, sticky='e')
        self.E.grid(column=1, row=0, padx=10, pady=50, sticky="w")

        B1 = ttk.Button(self, text='Load Maze', command=lambda: self.buttonPressLoad(controller))
        B2 = ttk.Button(self, text='Back', command=lambda: controller.showFrame(startPage))
        B1.grid(column=0, row=1, padx=10, pady=50)
        B2.grid(column=1, row=1, padx=10, pady=50)



app = App()
app.mainloop()
