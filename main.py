class Main:

    """ This class is used by gen, solve and draw as a parent class"""
    def __init__(self, name, rows, cols):
        self.name = name
        self.id = name
        self.rows = rows
        self.cols = cols