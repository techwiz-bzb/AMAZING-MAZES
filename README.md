# AMAZING-MAZES
My first program, that works properly.

To ensure the program will run. You will have to install the following python librarie.

- Python Imaging Library (Fork) - URL - https://pypi.org/project/Pillow/

Then run the app.py file. 

Using the GUI you will be able to need to generate a maze, this maze will be stored in a SQL database along with its time to generate.

Generation algorithm: "RB" and "BT". (without quotes)

Currently the RB (Revese Backtracking) can only make mazes up to 50x50. Above that you will need to use a BT (binary tree algorithm). You can generate and store a large number of different mazes but each one must have a unique name.

Going back to the main menu, you can then either solve or load a maze from the database.

Solving will draw a path from the top left corner to bottom right corner, this will also save the solved maze to the database meaning to program can be safely closed and no data lost. I have only implented one solving fuction.

Loading will just load a maze unsolved and if its been solved, then will load the solved maze aswell. Also it creates a popup of times to generate and solve. And also leave a .png file in the images folder of all mazes loaded.

Hope you enjoy,
Billy.
