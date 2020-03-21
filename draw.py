import sys
import main
from PIL import Image,ImageDraw    

class Draw(main.Main):
    """ Creates an object to encasulate certain 
        fuction that utilise the PIL libray to 
        creates and minipualte image file """

    def __init__(self, name, rows, cols):
        super().__init__(name, rows, cols)
        self.height = rows*30
        self.width = cols*30
        self.img = Image.new(mode='L', size=(self. width,self.height), color=255)
        self.yStepSize = int(self.img.width/self.cols)
        self.yStepSize = int(self.img.height/self.rows)

    def drawGrid(self):
        # Draws a grid onto image file with set number of col/row
        draw = ImageDraw.Draw(self.img)
        yStart = 0
        yEnd = self.img.height
        borders = [[(0, self.img.height),(self.img.width, self.img.height)], [(self.img.width, 0),(self.img.width, self.img.height)]]

        for line in borders:
            draw.line(line, fill=None, width=5)

        for x in range(0, self.img.width, self.yStepSize):
            line = ((x, yStart),(x, yEnd))
            draw.line(line, fill=None, width=5)
        
        xStart = 0
        xEnd = self.img.width
        

        for y in range(0, self.img.height, self.yStepSize):
            line = ((xStart, y),(xEnd, y))
            draw.line(line, fill=None, width=5)
        
        del draw

        self.img.save(r'images\{}.png'.format(self.name))

    def lineToRemove(self, x, y, direction):
        # This removes walls in the 4 direction used for eraseing the generated path
        
        self.xStepSize = int(self.img.width/self.cols)
        self.yStepSize = int(self.img.height/self.rows)
        if direction == 'N':
            line = (x*self.yStepSize+3, y*self.yStepSize),((x+1)*self.yStepSize-3,y*self.yStepSize)
            return line
        elif direction == 'E':
            line = ((x+1)*self.yStepSize, y*self.yStepSize+3),((x+1)*self.yStepSize, (y+1)*self.yStepSize-3)
            return line
        elif direction == 'S':
            line = (x*self.yStepSize+3, (y+1)*self.yStepSize),((x+1)*self.yStepSize-3, (y+1)*self.yStepSize)
            return line
        elif direction == 'W':
            line = (x*self.yStepSize, y*self.yStepSize+3),(x*self.yStepSize, (y+1)*self.yStepSize-3)
            return line

    def drawLines(self, lines):
        self.img = Image.open(r'images\{}.png'.format(self.name))
        draw = ImageDraw.Draw(self.img)
        for line in lines:
            draw.line(line, fill=255, width=5)
        del draw    
        self.img.save(r'images\{}.png'.format(self.name))

    def connectCell(self, x1, y1, x2, y2):
        # This is used to draw completed path by connect the centre of 2 cells
        img = Image.open(r'images\{}.png'.format(self.name))
        draw = ImageDraw.Draw(img)
        self.yStepSize = int(self.img.width/self.cols)
        self.yStepSize = int(self.img.height/self.rows)
        line= (((x1+0.5)*self.yStepSize, (y1+0.5)*self.yStepSize),((x2+0.5)*self.yStepSize, (y2+0.5)*self.yStepSize))
        draw.line(line, fill=100, width=5)
        del draw
        img.save(r'images\{}.png'.format(self.name))



    
