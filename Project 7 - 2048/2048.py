import turtle
import random

# Initialize game window using turtle graphics
wn = turtle.Screen()
wn.title("2048 by @TokyoEdTech")
wn.bgcolor("black")
wn.setup(width=450, height=400)
wn.tracer(0)  # Turn off screen updates for better performance

# Initialize game score
score = 0

# Initialize the game grid (4x4) with zeros
grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# Track which cells have been merged in the current move
grid_merged = [
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False]
]

# Set up the drawing pen for the game grid
pen = turtle.Turtle()
pen.speed(0)  # Fastest drawing speed
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.turtlesize(stretch_wid=2, stretch_len=2, outline=2)
pen.goto(0, 260)

def draw_grid():
    """
    Draw the game grid and numbers.
    - Each cell is colored based on its value
    - Numbers are displayed in blue
    - Empty cells (value 0) are displayed as blank
    """
    # Define colors for different number values
    colors = {
        0: "white",
        2: "yellow",
        4: "orange",
        8: "pink",
        16: "red",
        32: "light green",
        64: "green",
        128: "violet",
        256: "purple",
        512: "gold",
        1024: "silver",
        2048: "black"
    }

    # Draw each cell in the grid
    grid_y = 0
    y = 120
    for row in grid:
        grid_x = 0
        x = -120
        y -= 45
        for column in row:
            x += 45
            pen.goto(x, y)
            
            value = grid[grid_y][grid_x]
            color = colors[value]

            # Draw the cell background
            pen.color(color)
            pen.stamp()

            # Draw the number
            pen.color("blue")
            number = str(column) if column != 0 else ""
            pen.sety(pen.ycor() - 10)
            pen.write(number, align="center", font=("Courier", 14, "bold"))
            pen.sety(pen.ycor() + 10)

            grid_x += 1
        grid_y += 1

def add_random():
    """
    Add a new number (2 or 4) to a random empty cell.
    This happens after each move.
    """
    added = False
    while not added:
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        value = random.choice([2, 4])

        if grid[y][x] == 0:
            grid[y][x] = value
            added = True

def check_game_over():
    """
    Check if the game is over.
    Game ends when:
    1. Grid is full (no zeros)
    2. No valid moves remain (no adjacent matching numbers)
    """
    # Check for empty cells
    is_full = all(all(cell != 0 for cell in row) for row in grid)
    
    # Check for possible moves
    can_move = False
    for y in range(4):
        for x in range(4):
            # Check for empty cells
            if grid[y][x] == 0:
                can_move = True
                break
            # Check horizontal matches
            if x < 3 and grid[y][x] == grid[y][x + 1]:
                can_move = True
                break
            # Check vertical matches
            if y < 3 and grid[y][x] == grid[y + 1][x]:
                can_move = True
                break
        if can_move:
            break

    # If no moves possible, end the game
    if not can_move:
        # Draw semi-transparent background
        pen.goto(-200, -200)
        pen.color("gray")
        pen.fillcolor("black")
        pen.begin_fill()
        for _ in range(4):
            pen.forward(400)
            pen.left(90)
        pen.end_fill()
        
        # Show game over message
        pen.goto(0, 0)
        pen.color("red")
        pen.write("游戏结束!", align="center", font=("Arial", 36, "bold"))
        
        # Show final score
        pen.goto(0, -50)
        pen.color("white")
        pen.write(f"最终得分: {score}", align="center", font=("Arial", 24, "normal"))
        
        # Update screen and disable controls
        wn.update()
        wn.onkeypress(None, "Left")
        wn.onkeypress(None, "Right")
        wn.onkeypress(None, "Up")
        wn.onkeypress(None, "Down")
        return True
    return False

def reset_grid_merged():
    """
    Reset the merged status of all cells.
    Called after each move to prepare for the next move.
    """
    global grid_merged
    grid_merged = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False]
    ]

def up():
    """
    Move all tiles upward and merge matching numbers.
    Returns True if any tiles moved or merged.
    """
    moved = False
    for _ in range(4):
        for y in range(1, 4):
            for x in range(4):
                # Move to empty space
                if grid[y-1][x] == 0:
                    grid[y-1][x] = grid[y][x]
                    grid[y][x] = 0
                    moved = True
                    continue
                
                # Merge matching numbers
                if grid[y-1][x] == grid[y][x] and not grid_merged[y-1][x]:
                    grid[y-1][x] *= 2
                    grid_merged[y-1][x] = True
                    grid[y][x] = 0
                    moved = True
                    continue
    
    # If movement occurred, update game state
    if moved:
        reset_grid_merged()
        add_random()
        draw_grid()
        if check_game_over():
            wn.update()

def down():
    """
    Move all tiles downward and merge matching numbers.
    Returns True if any tiles moved or merged.
    """
    moved = False
    for _ in range(4):
        for y in range(2, -1, -1):
            for x in range(4):
                # Move to empty space
                if grid[y+1][x] == 0:
                    grid[y+1][x] = grid[y][x]
                    grid[y][x] = 0
                    moved = True
                    continue
                
                # Merge matching numbers
                if grid[y+1][x] == grid[y][x] and not grid_merged[y+1][x]:
                    grid[y+1][x] *= 2
                    grid_merged[y+1][x] = True
                    grid[y][x] = 0
                    moved = True
                    continue
    
    # If movement occurred, update game state
    if moved:
        reset_grid_merged()
        add_random()
        draw_grid()
        if check_game_over():
            wn.update()

def left():
    """
    Move all tiles left and merge matching numbers.
    Returns True if any tiles moved or merged.
    """
    moved = False
    for y in range(4):
        # First pass: move all numbers left
        for x in range(1, 4):
            if grid[y][x] != 0:
                current_x = x
                while current_x > 0 and grid[y][current_x - 1] == 0:
                    grid[y][current_x - 1] = grid[y][current_x]
                    grid[y][current_x] = 0
                    current_x -= 1
                    moved = True
        
        # Second pass: merge matching numbers
        for x in range(1, 4):
            if grid[y][x] != 0 and grid[y][x] == grid[y][x - 1] and not grid_merged[y][x - 1]:
                grid[y][x - 1] *= 2
                grid_merged[y][x - 1] = True
                grid[y][x] = 0
                moved = True
                # Move remaining numbers left
                current_x = x + 1
                while current_x < 4 and grid[y][current_x] != 0:
                    grid[y][current_x - 1] = grid[y][current_x]
                    grid[y][current_x] = 0
                    current_x += 1

    # If movement occurred, update game state
    if moved:
        reset_grid_merged()
        add_random()
        draw_grid()
        if check_game_over():
            wn.update()

def right():
    """
    Move all tiles right and merge matching numbers.
    Returns True if any tiles moved or merged.
    """
    moved = False
    for y in range(4):
        # First pass: move all numbers right
        for x in range(2, -1, -1):
            if grid[y][x] != 0:
                current_x = x
                while current_x < 3 and grid[y][current_x + 1] == 0:
                    grid[y][current_x + 1] = grid[y][current_x]
                    grid[y][current_x] = 0
                    current_x += 1
                    moved = True
        
        # Second pass: merge matching numbers
        for x in range(2, -1, -1):
            if grid[y][x] != 0 and grid[y][x] == grid[y][x + 1] and not grid_merged[y][x + 1]:
                grid[y][x + 1] *= 2
                grid_merged[y][x + 1] = True
                grid[y][x] = 0
                moved = True
                # Move remaining numbers right
                current_x = x - 1
                while current_x >= 0 and grid[y][current_x] != 0:
                    grid[y][current_x + 1] = grid[y][current_x]
                    grid[y][current_x] = 0
                    current_x -= 1

    # If movement occurred, update game state
    if moved:
        reset_grid_merged()
        add_random()
        draw_grid()
        if check_game_over():
            wn.update()

# Initialize game
draw_grid()
add_random()  # Add first random number

# Set up keyboard controls
wn.listen()
wn.onkeypress(left, "Left")
wn.onkeypress(right, "Right")
wn.onkeypress(up, "Up")
wn.onkeypress(down, "Down")

# Start game loop
wn.mainloop()