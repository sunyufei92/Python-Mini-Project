"""
This project implements a basic console-based (or window-based) Tetris game using Python. 
Tetris is a tile-matching puzzle game where players manipulate falling blocks, called Tetrominoes, which are composed of four square blocks. 
The goal is to create complete horizontal lines of blocks without any gaps. 
When a line is completed, it disappears, and the blocks above drop down to fill the space. 
The game continues until the blocks stack up to the top of the playing field, resulting in a game over.

The project demonstrates:

-Fundamental Python usage for game development.
-Implementing game mechanics like gravity, collision detection, and line clearing.
-Handling user input for controlling Tetrominoes (rotation and movement).
-Using a grid-based system for the game board and organizing Tetromino shapes.
-Structuring the game loop for continuous gameplay, including increasing speed as the game progresses.
-Creating a graphical interface using libraries such as Tkinter or Pygame.

To run this project, simply execute the Python script. It requires Python and the appropriate library (e.g., Tkinter or Pygame). 
The game will open in a window, and players can control the Tetrominoes using the arrow keys to move and rotate them as they fall.

This project is a great learning opportunity for beginners and intermediate Python programmers who want to practice their skills in game logic, user interaction, and GUI programming.

Version: 1.0
Author: Sun Yufei
Date: 2024-08-19
"""

from tkinter import *
import random
import time
import tkinter.messagebox
 
# The height of the Tetris game grid
HEIGHT = 34
 
# The width of the Tetris game grid
WIDTH = 20
 
# Constants representing the state of the blocks
ACTIVE = 1
PASSIVE = 0
TRUE = 1
FALSE = 0

# Block shapes and their rotations (defined as coordinates)
style = [
    [[(0, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (0, 2)], [(0, 1), (1, 1), (2, 1), (2, 2)],
     [(1, 0), (2, 0), (1, 1), (1, 2)]],  # J shape
    [[(1, 0), (1, 1), (1, 2), (2, 1)], [(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (0, 1)],
     [(0, 1), (1, 1), (2, 1), (1, 2)]],  # T shape
    [[(0, 1), (1, 1), (2, 1), (2, 0)], [(0, 0), (1, 0), (1, 1), (1, 2)], [(0, 1), (1, 1), (2, 1), (0, 2)],
     [(1, 0), (1, 1), (1, 2), (2, 2)]],  # Reverse L shape
    [[(0, 0), (0, 1), (1, 1), (1, 2)], [(2, 1), (1, 1), (1, 2), (0, 2)], [(0, 0), (0, 1), (1, 1), (1, 2)],
     [(2, 1), (1, 1), (1, 2), (0, 2)]],  # Z shape
    [[(1, 0), (1, 1), (0, 1), (0, 2)], [(0, 1), (1, 1), (1, 2), (2, 2)], [(1, 0), (1, 1), (0, 1), (0, 2)],
     [(0, 1), (1, 1), (1, 2), (2, 2)]],  # Reverse Z shape
    [[(0, 0), (0, 1), (1, 1), (1, 0)], [(0, 0), (0, 1), (1, 1), (1, 0)], [(0, 0), (0, 1), (1, 1), (1, 0)],
     [(0, 0), (0, 1), (1, 1), (1, 0)]],  # Square shape
    [[(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)], [(1, 0), (1, 1), (1, 2), (1, 3)],
     [(0, 1), (1, 1), (2, 1), (3, 1)]]  # I shape (long bar)
]
 
root = Tk()
root.title('Tetris')

# The main application class inheriting from Frame
class App(Frame):
    def __init__(self, master):
        Frame.__init__(self)
        
        # Bind keys for movement and control
        master.bind('<Up>', self.Up)        # Rotate block
        master.bind('<Left>', self.Left)    # Move block left
        master.bind('<Right>', self.Right)  # Move block right
        master.bind('<Down>', self.Down)    # Move block down
        master.bind('<space>', self.Space)  # Drop block to the bottom
        master.bind('<Control-Shift-Key-F12>', self.Play)  # Show info
        master.bind('<Key-P>', self.Pause)  # Pause the game
        master.bind('<Key-S>', self.StartByS)  # Start the game
        
        # Define RGB color values for various game elements
        self.backg = "#%02x%02x%02x" % (120, 150, 30)  # Background color
        self.frontg = "#%02x%02x%02x" % (40, 120, 150)  # Color for next shape
        self.nextg = "#%02x%02x%02x" % (150, 100, 100)  # Background for next block preview
        self.flashg = "#%02x%02x%02x" % (210, 130, 100)  # Flash color when line is cleared
        
        # Create labels to display lines cleared, score, and time spent
        self.LineDisplay = Label(master, text='Lines: ', bg='black', fg='red')
        self.Line = Label(master, text='0', bg='black', fg='red')
        self.ScoreDisplay = Label(master, text='Score: ', bg='black', fg='red')
        self.Score = Label(master, text='0', bg='black', fg='red')
        self.SpendTimeDisplay = Label(master, text='Time: ', bg='black', fg='red')
        self.SpendTime = Label(master, text='0.0', bg='black', fg='red')
        
        # Layout the labels on the screen
        self.LineDisplay.grid(row=HEIGHT - 2, column=WIDTH, columnspan=2)
        self.Line.grid(row=HEIGHT - 2, column=WIDTH + 2, columnspan=3)
        self.ScoreDisplay.grid(row=HEIGHT - 1, column=WIDTH, columnspan=2)
        self.Score.grid(row=HEIGHT - 1, column=WIDTH + 2, columnspan=3)
        self.SpendTimeDisplay.grid(row=HEIGHT - 4, column=WIDTH, columnspan=2)
        self.SpendTime.grid(row=HEIGHT - 4, column=WIDTH + 2, columnspan=3)
 
        # Initialize time, lines, and score
        self.TotalTime = 0.0
        self.TotalLine = 0
        self.TotalScore = 0
        
        # Game state variables
        self.isgameover = FALSE  # Flag for game over
        self.isPause = FALSE     # Flag for pause
        self.isStart = FALSE     # Flag for start
        self.NextList = []       # Preview area for next block
        self.NextRowList = []    # Row of blocks in the preview area
 
        self.px = 0  # X-coordinate of the block reference point
        self.py = 0  # Y-coordinate of the block reference point
 
        # Render the preview area for the next block
        r = 0
        c = 0
        for k in range(4 * 4):  # Loop through 4x4 preview area
            LN = Label(master, text='    ', bg=str(self.nextg), fg='white', relief=FLAT, bd=3)
            LN.grid(row=r, column=WIDTH + c, sticky=N + E + S + W)
            self.NextRowList.append(LN)
            c = c + 1
            if c >= 4:  # Move to next row after 4 columns
                r = r + 1
                c = 0
                self.NextList.append(self.NextRowList)
                self.NextRowList = []
 
        # Render the main game grid
        self.BlockList = []      # Matrix representing the state of each block
        self.BlockRowList = []   # Row of blocks in the grid
        self.LabelList = []      # Matrix of labels representing blocks
        self.LabelRowList = []   # Row of labels
        row = 0
        col = 0
        for i in range(HEIGHT * WIDTH):  # Loop through the grid
            L = Label(master, text='    ', bg=str(self.backg), fg='white', relief=FLAT, bd=4)
            L.grid(row=row, column=col, sticky=N + E + S + W)
            L.row = row
            L.col = col
            L.isactive = PASSIVE  # Set block as passive (inactive)
            self.BlockRowList.append(0)  # Initialize each grid block to 0
            self.LabelRowList.append(L)
            col = col + 1
            if col >= WIDTH:  # Move to the next row after the column reaches WIDTH
                row = row + 1
                col = 0
                self.BlockList.append(self.BlockRowList)
                self.LabelList.append(self.LabelRowList)
                self.BlockRowList = []
                self.LabelRowList = []
 
        # Create or load the file for saving scores
        fw = open('text.txt', 'a')
        fw.close()
        hasHead = FALSE
        f = open('text.txt', 'r')
        if f.read(5) == 'score':
            hasHead = TRUE
        f.close()
        self.file = open('text.txt', 'a')
        if hasHead == FALSE:
            self.file.write('score    line    time    scorePtime    linePtime    scorePline    date/n')
            self.file.flush()
 
        # Set the initial speed of the game (delay time in milliseconds)
        self.time = 1000
        self.OnTimer()  # Start the game timer
 
    def __del__(self):
        # Destructor to close the file
        pass
 
    # Toggle pause state
    def Pause(self, event):
        self.isPause = 1 - self.isPause  # Toggle between 0 and 1
 
    # Handle block rotation (Up key)
    def Up(self, event):
        BL = self.BlockList  # Block matrix
        LL = self.LabelList  # Label matrix
 
        Moveable = TRUE  # Flag indicating whether the block can be rotated
 
        # Get the current and next style of the block
        nowStyle = style[self.xnow][(self.ynow)]
        newStyle = style[self.xnow][(self.ynow + 1) % 4]  # Calculate next rotation
        self.ynow = (self.ynow + 1) % 4  # Update rotation index
 
        print("nowStyle:" + str(nowStyle) + "=====>>newStyle:" + str(newStyle))
 
        # Calculate the coordinates for the rotated block
        SourceList = []
        DestList = []
 
        for i in range(4):  # Loop through each block in the shape
            SourceList.append([nowStyle[i][0] + self.px, nowStyle[i][1] + self.py])
            x = newStyle[i][0] + self.px
            y = newStyle[i][1] + self.py
            DestList.append([x, y])
 
            if x < 0 or x >= HEIGHT or y < 0 or y >= WIDTH:  # Check for boundaries
                Moveable = FALSE
 
        if Moveable == TRUE:  # If the block can be rotated, update the grid
            for i in range(len(SourceList)):
                self.Empty(SourceList[i][0], SourceList[i][1])
            for i in range(len(DestList)):
                self.Fill(DestList[i][0], DestList[i][1])
 
    # Move the block left (Left key)
    def Left(self, event):
        BL = self.BlockList
        LL = self.LabelList
        Moveable = TRUE
        for i in range(HEIGHT):  # Loop through grid to check if block can move left
            for j in range(WIDTH):
                if LL[i][j].isactive == ACTIVE and j - 1 < 0: Moveable = FALSE  # Check boundaries
                if LL[i][j].isactive == ACTIVE and j - 1 >= 0 and BL[i][j - 1] == 1 and LL[i][
                    j - 1].isactive == PASSIVE: Moveable = FALSE  # Check if there's a block in the way
        if Moveable == TRUE:  # If the block can move left, update the grid
            self.py -= 1
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if j - 1 >= 0 and LL[i][j].isactive == ACTIVE and BL[i][j - 1] == 0:
                        self.Fill(i, j - 1)
                        self.Empty(i, j)
 
    # Move the block right (Right key)
    def Right(self, event):
        BL = self.BlockList
        LL = self.LabelList
        Moveable = TRUE
        for i in range(HEIGHT):  # Loop through grid to check if block can move right
            for j in range(WIDTH):
                if LL[i][j].isactive == ACTIVE and j + 1 >= WIDTH: Moveable = FALSE  # Check boundaries
                if LL[i][j].isactive == ACTIVE and j + 1 < WIDTH and BL[i][j + 1] == 1 and LL[i][
                    j + 1].isactive == PASSIVE: Moveable = FALSE  # Check if there's a block in the way
        if Moveable == TRUE:  # If the block can move right, update the grid
            self.py += 1
            for i in range(HEIGHT - 1, -1, -1):
                for j in range(WIDTH - 1, -1, -1):
                    if j + 1 < WIDTH and LL[i][j].isactive == ACTIVE and BL[i][j + 1] == 0:
                        self.Fill(i, j + 1)
                        self.Empty(i, j)
 
    # Move the block down (Down key)
    def Down(self, event):
        BL = self.BlockList
        LL = self.LabelList
        Moveable = TRUE
        for i in range(HEIGHT):  # Loop through grid to check if block can move down
            for j in range(WIDTH):
                if LL[i][j].isactive == ACTIVE and i + 1 >= HEIGHT: Moveable = FALSE  # Check bottom boundary
                if LL[i][j].isactive == ACTIVE and i + 1 < HEIGHT and BL[i + 1][j] == 1 and LL[i + 1][
                    j].isactive == PASSIVE: Moveable = FALSE  # Check if there's a block below
        if Moveable == TRUE and self.isStart:  # If the block can move down, update the grid
            self.px += 1
            for i in range(HEIGHT - 1, -1, -1):
                for j in range(WIDTH - 1, -1, -1):
                    if i + 1 < HEIGHT and LL[i][j].isactive == ACTIVE and BL[i + 1][j] == 0:
                        self.Fill(i + 1, j)
                        self.Empty(i, j)
        if Moveable == FALSE:  # If the block can't move down, it becomes passive
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    LL[i][j].isactive = PASSIVE
            self.JudgeLineFill()  # Check if any lines are filled
            self.Start()  # Start a new block
            if self.isgameover == TRUE:
                showinfo('T_T', 'The game is over!')
                self.Distroy()
                return FALSE
            for i in range(4):
                for j in range(4):
                    self.NextEmpty(i, j)
            self.Rnd()
        return Moveable
 
    # Drop the block to the bottom (Space key)
    def Space(self, event):
        while 1:
            if self.Down(0) == FALSE: break
 
    # Game timer to control the speed of block falling
    def OnTimer(self):
        if self.isStart == TRUE and self.isPause == FALSE:
            self.TotalTime = self.TotalTime + float(self.time) / 1000
            self.SpendTime.config(text=str(self.TotalTime))
 
        if self.isPause == FALSE:
            self.Down(0)
        
        # Increase falling speed as score increases
        if self.TotalScore >= 1000: self.time = 900
        if self.TotalScore >= 2000: self.time = 750
        if self.TotalScore >= 3000: self.time = 600
        if self.TotalScore >= 4000: self.time = 400
        
        self.after(self.time, self.OnTimer)  # Recursively call OnTimer to update the timer
 
    # Check and remove filled lines
    def JudgeLineFill(self):
        BL = self.BlockList
        LL = self.LabelList
        count = 0
        LineList = [1] * WIDTH  # A list representing a fully filled line
        # Display a flash effect when a line is filled
        for i in range(HEIGHT):
            if BL[i] == LineList:
                count = count + 1
                for k in range(WIDTH):
                    LL[i][k].config(bg=str(self.flashg))
                    LL[i][k].update()
        if count != 0: self.after(100)
        
        # Remove the filled line and update the grid
        for i in range(HEIGHT):
            if BL[i] == LineList:
                for j in range(i, 0, -1):
                    for k in range(WIDTH):
                        BL[j][k] = BL[j - 1][k]
                        LL[j][k]['relief'] = LL[j - 1][k].cget('relief')
                        LL[j][k]['bg'] = LL[j - 1][k].cget('bg')
                for l in range(WIDTH):
                    BL[0][l] = 0
                    LL[0][l].config(relief=FLAT, bg=str(self.backg))
        
        # Update score based on the number of lines cleared
        self.TotalLine = self.TotalLine + count
        if count == 1: self.TotalScore = self.TotalScore + 1 * WIDTH
        if count == 2: self.TotalScore = self.TotalScore + 3 * WIDTH
        if count == 3: self.TotalScore = self.TotalScore + 6 * WIDTH
        if count == 4: self.TotalScore = self.TotalScore + 10 * WIDTH
        self.Line.config(text=str(self.TotalLine))
        self.Score.config(text=str(self.TotalScore))
 
    # Fill a block on the grid
    def Fill(self, i, j):
        if j < 0: return
        if self.BlockList[i][j] == 1: self.isgameover = TRUE
        self.BlockList[i][j] = 1
        self.LabelList[i][j].isactive = ACTIVE
        self.LabelList[i][j].config(relief=RAISED, bg=str(self.frontg))
 
    # Empty a block on the grid
    def Empty(self, i, j):
        self.BlockList[i][j] = 0
        self.LabelList[i][j].isactive = PASSIVE
        self.LabelList[i][j].config(relief=FLAT, bg=str(self.backg))
 
    # Show info about the game
    def Play(self, event):
        showinfo('Made in China', '^_^')
 
    # Fill a block in the next block preview area
    def NextFill(self, i, j):
        self.NextList[i][j].config(relief=RAISED, bg=str(self.frontg))
 
    # Empty a block in the next block preview area
    def NextEmpty(self, i, j):
        self.NextList[i][j].config(relief=FLAT, bg=str(self.nextg))
 
    # Destroy the current game state and reset the game
    def Distroy(self):
        # Save the score to file
        if self.TotalScore != 0:
            savestr = '%-9u%-8u%-8.2f%-14.2f%-13.2f%-14.2f%s/n' % (
                self.TotalScore, self.TotalLine, self.TotalTime,
                self.TotalScore / self.TotalTime,
                self.TotalLine / self.TotalTime,
                float(self.TotalScore) / self.TotalLine,
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            self.file.seek(0, 2)
            self.file.write(savestr)
            self.file.flush()
 
        # Reset all blocks and stats
        for i in range(HEIGHT):
            for j in range(WIDTH):
                self.Empty(i, j)
        self.TotalLine = 0
        self.TotalScore = 0
        self.TotalTime = 0.0
        self.Line.config(text=str(self.TotalLine))
        self.Score.config(text=str(self.TotalScore))
        self.SpendTime.config(text=str(self.TotalTime))
        self.isgameover = FALSE
        self.isStart = FALSE
        self.time = 1000
        for i in range(4):
            for j in range(4):
                self.NextEmpty(i, j)
 
    # Start a new block
    def Start(self):
        nextStyle = style[self.x][self.y]  # Get the style of the next block
        self.xnow = self.x
        self.ynow = self.y  # Record the block's position
        self.py = random.randint(0, 6)
        print("Assigned random py value:" + str(self.py))
        self.px = 0
        for ii in range(4):
            self.Fill(int(nextStyle[ii][0]), int(nextStyle[ii][1]) + self.py)
        self.isStart = TRUE  # Game has started
 
    # Select a random block for the next piece
    def Rnd(self):
        self.x = random.randint(0, 6)
        self.y = random.randint(0, 3)
        nextStyle = style[self.x][self.y]  # Get the style of the next block
        for ii in range(4):
            self.NextFill(int(nextStyle[ii][0]), int(nextStyle[ii][1]))
 
    # Select the first block at the start of the game
    def RndFirst(self):
        self.x = random.randint(0, 6)  # Select a random block style
        self.y = random.randint(0, 3)
 
    # Show the leaderboard
    def Show(self):
        self.file.seek(0)
        strHeadLine = self.file.readline()
        dictLine = {}
        strTotalLine = ''
        for OneLine in self.file.readlines():
            temp = int(OneLine[:5])
            dictLine[temp] = OneLine
 
        list = sorted(dictLine.items(), key=lambda d: d[0])
        ii = 0
        for onerecord in reversed(list):
            ii = ii + 1
            if ii < 11:
                strTotalLine += onerecord[1]
        showinfo('Ranking', strHeadLine + strTotalLine)
 
    # Start the game by pressing 'S'
    def StartByS(self, event):
        self.RndFirst()
        self.Start()
        self.Rnd()
 
 
def Start():
    app.RndFirst()
    app.Start()
    app.Rnd()
 
 
def End():
    app.Distroy()
 
 
def Set():
    print("Settings function is not complete yet...")
 
 
def Show():
    app.Show()
 
 
# Main menu setup
mainmenu = Menu(root)
root['menu'] = mainmenu
 
# Game menu
gamemenu = Menu(mainmenu)
mainmenu.add_cascade(label='Game', menu=gamemenu)
gamemenu.add_command(label='Start', command=Start)
gamemenu.add_command(label='End', command=End)
gamemenu.add_separator()
gamemenu.add_command(label='Exit', command=root.quit)
 
# Settings menu
setmenu = Menu(mainmenu)
mainmenu.add_cascade(label='Settings', menu=setmenu)
setmenu.add_command(label='Settings', command=Set)
 
# Show menu
showmenu = Menu(mainmenu)
mainmenu.add_cascade(label='Leaderboard', menu=showmenu)
showmenu.add_command(label='Show', command=Show)
 
# Instantiate the App class and start the game
app = App(root)

# Enter the Tkinter main loop to run the game
root.mainloop()
