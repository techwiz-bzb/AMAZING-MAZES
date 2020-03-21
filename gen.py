from PIL import Image,ImageDraw
import pickle, sys, random, numpy, main, time, os
from SQLite import insertBLOB
from draw import Draw

sys.setrecursionlimit(9999)
class Cell:
    """ Creates a object for each cell in a grid.
        Walls, which walls still stand True = Wall
        visited, Used to find if cell has been vistited """

    def __init__(self, x, y):
        self.walls = {'N': True, 'E':True, 'S':True, 'W':True}
        self.x = x
        self.y = y
        self.visited = False

    def getCoor(self):
        # Returns coordinate of instance of cell
        return(self.x, self.y)

    def getWalls(self):
        # Returns all the False walls
        for wall in self.walls:
            if not self.walls[wall]:
                return wall
    
    def getVisited(self):
        # Returns a boolean for if cell has been visited
        return(self.visited)

    def removeCellWalls(self, dirction):
        # Removes a wall in a certain direction for a instace of the cell
        self.walls[dirction] = False



class Generator(main.Main):
    """ Creates an object that encapsulates all the data
    needed to store a maze, and instantiate a cell and stores 
    2 array them """

    def __init__(self, name, rows, cols):
        super().__init__(name, rows, cols)
        self.grid = []
        self.path = []
        self.g = Draw(self.name, self.cols, self.rows) # Draws a grid
        # Makes a 2d array and assines each element a cell
        for x in range(self.cols):
            self.grid.append([])
            for y in range(self.rows):
                self.grid[x].append(Cell(x,y))

    def printGrid(self):
        # Prints a crude text maze and basic infomation about the cell
        for row in self.grid:
            for i in row:
                print(i.getCoor())
                print(i.getWalls())
                print(i.getVisited())
    
    def returnAdjCells(self, x, y): 
        # Returns all adjacent cell along with the direction to travel, direction came from
        adjList = []
        if y > 0:
            adjList.append([self.grid[x][y-1], 'N', 'S'])
        if x < len(self.grid[0])-1:
            adjList.append([self.grid[x+1][y], 'E', 'W'])
        if y < len(self.grid[0])-1:
            adjList.append([self.grid[x][y+1], 'S', 'N'])
        if x > 0:
            adjList.append([self.grid[x-1][y], 'W', 'E'])
        return adjList

    def allCellsVisted(self):
        #Retruns if vistited for every cell in grid
        for row in self.grid:
            for cell in row:
                if not cell.getVisited():
                    return False
        return True

    def drawMaze(self):
        # Draws the path that has been created by algorithm
        grid = self.g
        grid.drawGrid()
        lines = []
        for row in self.grid:
            for cell in row:
                x, y = cell.getCoor()
                for key, val in cell.walls.items():
                    if val == True:
                        pass
                    else:
                        lines.append(grid.lineToRemove(x, y, key))
        
        grid.drawLines(lines)

    
    def reveseBacktracking(self, x=0, y=0, prev_cells=[], p=[],):
        start_time = time.time()
        uvn=[]
        print(x, y)
        ogCell = self.grid[x][y]
        ogCell.visited = True
        if len(p)==0:
            p.append(ogCell)
        for i in self.returnAdjCells(x, y):
            if not i[0].visited:
                uvn.append(i)
        for i in uvn:
            if i[0].visited:
                uvn.remove(i)

        if len(uvn) > 0:
            prev_cells.append(ogCell)
            nCell = random.choice(uvn)
            ogCell.removeCellWalls(nCell[1])
            nCell[0].removeCellWalls(nCell[2])
            p.append(nCell[0])
            x, y = nCell[0].getCoor()
            self.reveseBacktracking(x, y, prev_cells, p)

        elif len(prev_cells) > 0:
            x, y = prev_cells[-1].getCoor()
            prev_cells.pop()
            self.reveseBacktracking(x, y, prev_cells, p)
        
        self.path = p
        end_time = time.time()
        return(end_time-start_time)


    def BinaryTree(self):
        start_time = time.time()
        directions = ['S', 'E']
        p_cell = self.grid[0][0]
        for row in self.grid:
            for cell in row:
                x, y = cell.getCoor()
                if x == len(row)-1:
                    direction = 'S'
                elif y == len(row)-1:
                    direction = 'E'
                else:
                    direction = random.choice(directions)
              
                cell.removeCellWalls(direction)
            
        
        return time.time() - start_time
        
    def saveMaze(self, time2gen):
        pickle_out = open("{}.pickle".format(self.name), "wb")
        pickle.dump(self, pickle_out)
        pickle_out.close()
        self.id = self.name
        insertBLOB(self.id, self.name, r'images\{}.png'.format(self.name), r'{}.pickle'.format(self.name), time2gen)



