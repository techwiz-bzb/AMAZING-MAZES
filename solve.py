from draw import Draw
import pickle, random, heapq, os, SQLite, time
from SQLite import readBLOBData, insertBLOBsolved
from gen import Generator, Cell


class Solve():
    """ Loads a maze object from SQL database, then solves loaded maze
        then saves the solution back to database """

    def __init__(self, id):
        self.id = id
        self.name = readBLOBData(id)
        self.maze = pickle.load(open('{}.pickle'.format(self.name), 'rb'))
        self.path = []
        self.end = self.maze.grid[self.maze.cols-1][self.maze.rows-1]
        self.start = self.maze.grid[0][0]
        self.grid = self.maze.g
        for row in self.maze.grid:
            for cell in row:
                cell.visited = False


    def adjacent(self, cell1):
        # Returns a list cells adjacent that are also not visited
        coor = cell1.getCoor()
        ways = []
        for row in self.maze.grid:
            for cell in row:
                if cell.getCoor() == coor:
                    for k, v in cell.walls.items():
                        if v == False:
                            ways.append(k)
        adj = []
        x, y = coor
        temp = self.maze.returnAdjCells(x, y)
        for obj in temp:
            if obj[1] in ways: 
                adj.append(obj[0])

        return(adj)

        

    def BFS(self):
        #Performs a breadth-first-search though the maze the backtracks to give you a final path
        start_time = time.time()
        node_q = []
        visited = []
        travel_path = []
        end = self.end
        start = self.start
        node_q.append(start)
        visited.append(start)
        travel_path.append(start)
        printstament = []
        printstament.append(start)
        while len(node_q) > 0:
            v = node_q.pop(0)
            v.visited = True
            adj = self.adjacent(v)
            for cell in adj:
                printstament.append(cell)
            if v == end:
                while travel_path[-1] != end:
                    travel_path.pop()
                travel_path.reverse()
                p_item = travel_path[0]
                for i in range(1, len(travel_path)):
                    n_item = travel_path[i]
                    if not(p_item in self.path):
                        self.path.append(p_item) 
                    if n_item in self.adjacent(p_item):
                        p_item = n_item
                self.path.append(start)
                #return(travel_path)
            for next in adj:
                if not(next in visited):
                    node_q.append(next)
                    visited.append(next)
                    travel_path.append(next)
        if len(self.path) < 3:
            self.path = printstament
        end_time = time.time()
        return(end_time-start_time)
                
    def drawPath(self):
        # Draws the solved path onto the image
        first = self.path.pop()
        while len(self.path)> 1:
            second = self.path.pop()
            x1, y1 = first.getCoor()
            x2, y2 = second.getCoor()
            self.grid.connectCell(x1, y1, x2, y2)
            first = second
        second = self.path[0]
        x1, y1 = first.getCoor()
        x2, y2 = second.getCoor()
        self.grid.connectCell(x1, y1, x2, y2)


    def saveMazeSolved(self, time2solve):
        pickle_out = open("{}.pickle".format(self.name), "wb")
        pickle.dump(self, pickle_out)
        pickle_out.close()
        insertBLOBsolved('images/{}.png'.format(self.name), "{}.pickle".format(self.name), self.id, time2solve) 
        os.remove("{}.pickle".format(self.name))
""" 
solve = Solve('test2')
solve.BFS()
for i in solve.path:
    print(i.getCoor())
solve.drawPath()
 """