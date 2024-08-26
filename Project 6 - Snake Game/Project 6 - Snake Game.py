"""
This project implements a classic Snake game using Python's Pygame module.
The game features a snake that the player controls using the arrow keys, and the goal is to eat as many apples as possible to increase the snake's length and score.
As the snake eats more apples, its speed increases, making the game progressively more difficult.
The snake dies if it runs into the window's borders or its own body.

The project demonstrates:
- Basic usage of the Pygame library for game development.
- Handling keyboard input for controlling game objects (the snake).
- Creating a simple game loop that processes input, updates the game state, and renders graphics.
- Using Pygame's drawing methods to create the snake, apples, and grid background.
- Implementing collision detection for the snake's interactions with walls and itself.
- Structuring the game code into different functions for improved readability and organization.

To run this project, simply execute the Python script. It requires Python and the Pygame module to be installed.
When executed, the script opens a window and begins the Snake game, where the player can start controlling the snake with the keyboard.

This project is a great learning opportunity for beginners interested in game development using Python and Pygame.

Version: 1.0
Author: Sun Yufei
Date: 2024-08-26
"""

import random
import pygame
import sys
from pygame.locals import *

# Game settings and constants
Snakespeed = 4  # Speed of the snake
Window_Width = 800  # Width of the game window
Window_Height = 500  # Height of the game window
Cell_Size = 20  # Size of each cell in the grid (snake and apple size)

# Ensuring that the window size is a multiple of the cell size.
assert Window_Width % Cell_Size == 0, "Window width must be a multiple of cell size."
assert Window_Height % Cell_Size == 0, "Window height must be a multiple of cell size."

# Calculating the number of cells in width and height.
Cell_W = int(Window_Width / Cell_Size)
Cell_H = int(Window_Height / Cell_Size)

# Defining colors for various elements in the game
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
DARKGreen = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
Red_DARK = (150, 0, 0)
BLUE = (0, 0, 255)
BLUE_DARK = (0, 0, 150)

# Background color for the game
BGCOLOR = Black

# Defining directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# Index for the head of the snake
HEAD = 0

# Main function to start the game
def main():
    global SnakespeedCLOCK, DISPLAYSURF, BASICFONT

    # Initialize pygame and create the main display window
    pygame.init()
    SnakespeedCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((Window_Width, Window_Height))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')  # Set window title

    # Show the start screen
    showStartScreen()

    # Main game loop that runs until the player quits
    while True:
        runGame()
        showGameOverScreen()

# Function that runs the game logic
def runGame():
    # Set a random start point for the snake
    startx = random.randint(5, Cell_W - 6)
    starty = random.randint(5, Cell_H - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]  # Snake starts with 3 segments
    direction = RIGHT  # Snake initially moves to the right

    # Start the apple in a random position
    apple = getRandomLocation()

    # Initialize score and speed
    score = 0  # Track the player's score
    Snakespeed = 5  # Initial speed of the snake

    # Main game loop
    while True:
        # Event handling loop (keyboard and quitting)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()  # Quit the game
            elif event.type == KEYDOWN:
                # Change direction based on key press, but avoid 180-degree turns
                if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()  # Quit if ESC is pressed

        # Check if the snake has hit the edge of the window or itself
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == Cell_W or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == Cell_H:
            return  # Game over when hitting the boundary
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # Game over if snake collides with itself

        # Check if the snake has eaten the apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # Don't remove the tail when the snake eats the apple
            apple = getRandomLocation()  # Generate a new apple location
            score += 1  # Increment score
            # Increase speed every 10 points
            if score % 10 == 0:
                Snakespeed += 1  # Increase the snake's speed level
        else:
            del wormCoords[-1]  # Remove the tail if no apple is eaten

        # Move the snake in the current direction
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)  # Insert the new head at the front of the snake

        # Redraw everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()  # Draw the grid
        drawWorm(wormCoords)  # Draw the snake
        drawApple(apple)  # Draw the apple
        drawScore(len(wormCoords) - 3)  # Display the score
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)  # Control the game's frame rate

# Display a message asking the player to press a key
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, White)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Window_Width - 200, Window_Height - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

# Check if any key has been pressed
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()  # Quit the game if the player closes the window
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()  # Quit if the player presses ESC
    return keyUpEvents[0].key

# Display the start screen before the game begins
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake!', True, White, DARKGreen)
    degrees1 = 0

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)  # Rotate the title for animation
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (Window_Width / 2, Window_Height / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        drawPressKeyMsg()  # Draw message prompting the user to press a key

        if checkForKeyPress():  # Wait for a keypress to start the game
            pygame.event.get()  # Clear event queue
            return
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)
        degrees1 += 3  # Rotate by 3 degrees each frame for animation

# Quit the game
def terminate():
    pygame.quit()
    sys.exit()

# Generate a random location for the apple
def getRandomLocation():
    return {'x': random.randint(0, Cell_W - 1), 'y': random.randint(0, Cell_H - 1)}

# Display the game over screen
def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render('Game', True, White)
    overSurf = gameOverFont.render('Over', True, White)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (Window_Width / 2, 10)
    overRect.midtop = (Window_Width / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()  # Prompt player to press a key to restart
    pygame.display.update()
    pygame.time.wait(500)  # Wait for a short duration
    checkForKeyPress()  # Clear out any keypresses in the event queue

    while True:
        if checkForKeyPress():  # Wait for a keypress to restart the game
            pygame.event.get()  # Clear event queue
            return

# Draw the player's score in the top right of the screen
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, White)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Window_Width - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

# Draw the snake on the screen
def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        wormSegmentRect = pygame.Rect(x, y, Cell_Size, Cell_Size)  # Draw the outer square for the worm's body
        pygame.draw.rect(DISPLAYSURF, DARKGreen, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)  # Draw the inner square
        pygame.draw.rect(DISPLAYSURF, Green, wormInnerSegmentRect)

# Draw the apple on the screen
def drawApple(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    appleRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(DISPLAYSURF, Red, appleRect)

# Draw the grid on the screen for visual effect
def drawGrid():
    for x in range(0, Window_Width, Cell_Size):  # Draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, Window_Height))
    for y in range(0, Window_Height, Cell_Size):  # Draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (Window_Width, y))

# Main execution
if __name__ == '__main__':
    try:
        main()  # Start the game
    except SystemExit:
        pass  # Exit the program gracefully
