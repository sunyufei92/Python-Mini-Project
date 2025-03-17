# Main game file for Frogger implementation using Python Turtle graphics
# This is a classic arcade game where the player controls a frog trying to cross a busy road and a dangerous river
# The goal is to get the frog safely to one of the home positions at the top of the screen

import turtle  # For graphics
import math    # For collision detection calculations
import time    # For timing and animation
import random  # For random turtle diving intervals

# Initialize the game window
wn = turtle.Screen()
wn.cv._rootwindow.resizable(False, False)  # Prevent window resizing for consistent gameplay
wn.title("Frogger")
wn.setup(600, 800)  # Set window dimensions (width: 600px, height: 800px)
wn.bgcolor("green")  # Set background color
wn.bgpic("background.gif")  # Set background image for the game
wn.tracer(0)  # Turn off automatic updates for better performance (manual update in game loop)

# Register all game sprites/images
# These images must be in the same directory as the script
shapes = ["frog.gif", "car_left.gif", "car_right.gif", "log_full.gif", "turtle_left.gif", "turtle_right.gif", "turtle_right_half.gif", 
    "turtle_left_half.gif", "turtle_submerged.gif", "home.gif", "frog_home.gif", "frog_small.gif"]
    
for shape in shapes:
    wn.register_shape(shape)  # Register each image as a valid turtle shape

# Create pen for drawing
# This pen is used for rendering game objects and UI elements
pen = turtle.Turtle()
pen.speed(0)  # Fastest drawing speed
pen.hideturtle()  # Hide the turtle cursor
pen.penup()  # Don't draw lines when moving

# Base Sprite class for all game objects
# Provides common functionality for position, dimensions, and collision detection
class Sprite():
    def __init__(self, x, y, width, height, image):
        self.x = x          # X coordinate
        self.y = y          # Y coordinate
        self.width = width  # Sprite width for collision detection
        self.height = height # Sprite height for collision detection
        self.image = image  # Visual representation

    # Draw the sprite on screen using the pen object
    def render(self, pen):
        pen.goto(self.x, self.y)  # Move pen to sprite position
        pen.shape(self.image)     # Set the sprite's image
        pen.stamp()               # Stamp the image at current position
        
    def update(self):
        pass  # Base update method, overridden by child classes
        
    # Check for collision with other sprites using AABB method
    # AABB (Axis-Aligned Bounding Box) is a simple and efficient collision detection method
    def is_collision(self, other):
        # Calculate collision on both axes
        # Multiply by 2 to create a proper bounding box
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

# Player class representing the frog
# Handles player movement, lives, scoring, and timer
class Player(Sprite):
    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = 0         # Horizontal movement speed (used when on logs/turtles)
        self.collision = False  # Flag for tracking collision with safe objects (logs/turtles)
        self.frogs_home = 0    # Counter for successfully delivered frogs
        self.max_time = 60     # Time limit per level in seconds
        self.time_remaining = 60  # Current remaining time
        self.start_time = time.time()  # Level start time
        self.lives = 3         # Number of lives player has
        
    # Movement methods - each move is 50 pixels (grid-based movement)
    def up(self):
        self.y += 50    # Move up one grid space

    def down(self):
        self.y -= 50    # Move down one grid space

    def right(self):
        self.x += 50    # Move right one grid space

    def left(self):
        self.x -= 50    # Move left one grid space
        
    def update(self):
        self.x += self.dx  # Update position based on platform movement
        
        # Keep player within screen bounds
        # If player goes too far left/right, reset to starting position
        if self.x < -300 or self.x > 300:
            self.x = 0
            self.y = -300
            
        # Prevent player from moving below bottom of screen
        if self.y < -325:
            self.y = -325
        
        # Update remaining time and check for timeout
        self.time_remaining = self.max_time - round(time.time() - self.start_time)
        
        # Handle time out - player loses a life and returns home
        if self.time_remaining <= 0:
            player.lives -= 1
            self.go_home()
            
    # Reset player position and timer
    # Called when player dies or reaches home
    def go_home(self):
        self.dx = 0
        self.x = 0
        self.y = -325
        self.max_time = 60
        self.time_remaining = 60
        self.start_time = time.time()
        
# Car class for vehicle obstacles
# Cars move horizontally and kill the frog on collision
class Car(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx  # Horizontal movement speed (negative for left, positive for right)
        
    def update(self):
        self.x += self.dx  # Update car position
        
        # Wrap around screen edges to create infinite stream of cars
        if self.x < -400:
            self.x = 400
        if self.x > 400:
            self.x = -400

# Log class for floating platforms
# Logs move horizontally and carry the frog safely across water
class Log(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx  # Horizontal movement speed
        
    def update(self):
        self.x += self.dx  # Update log position
        
        # Wrap around screen edges to create infinite stream of logs
        if self.x < -400:
            self.x = 400
        if self.x > 400:
            self.x = -400

# Turtle class for floating/sinking platforms
# Turtles move horizontally and periodically submerge, making them temporary platforms
class Turtle(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx
        self.state = "full"  # States: full (above water), half (partially submerged), submerged
        # Random timing for state changes to make game more unpredictable
        self.full_time = random.randint(8, 12)      # Time to stay fully visible
        self.half_time = random.randint(4, 6)       # Time for transition states
        self.submerged_time = random.randint(4, 6)  # Time to stay underwater
        self.start_time = time.time()  # Track time for state changes
        
    def update(self):
        self.x += self.dx  # Update turtle position
        
        # Wrap around screen edges
        if self.x < -400:
            self.x = 400
        if self.x > 400:
            self.x = -400
            
        # Update turtle image based on state and movement direction
        if self.state == "full":
            if self.dx > 0:
                self.image = "turtle_right.gif"
            else:
                self.image = "turtle_left.gif"
        elif self.state == "half_up" or self.state == "half_down":
            if self.dx > 0:
                self.image = "turtle_right_half.gif"
            else:
                self.image = "turtle_left_half.gif"
        elif self.state == "submerged":
            self.image = "turtle_submerged.gif"

        # Handle state transitions based on timing
        # Creates a cycle: full -> half_down -> submerged -> half_up -> full
        if self.state == "full" and time.time() - self.start_time > self.full_time:
            self.state = "half_down"
            self.start_time = time.time()
        elif self.state == "half_down" and time.time() - self.start_time > self.half_time:
            self.state = "submerged"
            self.start_time = time.time()
        elif self.state == "submerged" and time.time() - self.start_time > self.submerged_time:
            self.state = "half_up"
            self.start_time = time.time()
        elif self.state == "half_up" and time.time() - self.start_time > self.half_time:
            self.state = "full"
            self.start_time = time.time()            

# Home class for goal positions
# These are the safe spots at the top where frogs need to reach
class Home(Sprite):
    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = 0  # Homes don't move

# Timer class for visual countdown
# Displays a shrinking line representing remaining time
class Timer():
    def __init__(self, max_time):
        self.x = 200        # X position of timer
        self.y = -375       # Y position of timer
        self.max_time = max_time  # Maximum time allowed
        self.width = 200    # Width of timer bar
        
    def render(self, time, pen):
        pen.color("green")   # Timer color
        pen.pensize(5)       # Timer line thickness
        pen.penup()
        pen.goto(self.x, self.y)
        pen.pendown()
        percent = time/self.max_time  # Calculate remaining time percentage
        dx = percent * self.width     # Calculate timer width
        pen.goto(self.x-dx, self.y)   # Draw timer bar
        pen.penup()

# Initialize game objects
player = Player(0, -325, 40, 40, "frog.gif")  # Create player at bottom center
timer = Timer(60)  # Create 60-second timer

# Define level layout with cars, logs, and turtles
# Each row has specific objects with different movement patterns
level_1 = [
    # First row of cars (moving left)
    Car(0, -275, 121, 40, "car_left.gif", -0.1),
    Car(221, -275, 121, 40, "car_left.gif", -0.1),
    
    # Second row of cars (moving right)
    Car(0, -225, 121, 40, "car_right.gif", 0.1),
    Car(221, -225, 121, 40, "car_right.gif", 0.1),
    
    # Third row of cars (moving left)
    Car(0, -175, 121, 40, "car_left.gif", -0.1),
    Car(221, -175, 121, 40, "car_left.gif", -0.1),
    
    # Fourth row of cars (moving right)
    Car(0, -125, 121, 40, "car_right.gif", 0.1),
    Car(221, -125, 121, 40, "car_right.gif", 0.1),
    
    # Fifth row of cars (moving left)
    Car(0, -75, 121, 40, "car_left.gif", -0.1),
    Car(221, -75, 121, 40, "car_left.gif", -0.1),
    
    # First row of logs (moving right)
    Log(0, 25, 161, 40, "log_full.gif", 0.2),
    Log(261, 25, 161, 40, "log_full.gif", 0.2),
    
    # Second row of logs (moving left)
    Log(0, 75, 161, 40, "log_full.gif", -0.2),
    Log(261, 75, 161, 40, "log_full.gif", -0.2),
    
    # First row of turtles (moving right)
    Turtle(0, 125, 155, 40, "turtle_right.gif", 0.15),
    Turtle(255, 125, 155, 40, "turtle_right.gif", 0.15),
    
    # Second row of turtles (moving left)
    Turtle(0, 175, 155, 40, "turtle_left.gif", -0.15),
    Turtle(255, 175, 155, 40, "turtle_left.gif", -0.15),
    
    # Third row of logs (moving right)
    Log(0, 225, 161, 40, "log_full.gif", 0.2),
    Log(261, 225, 161, 40, "log_full.gif", 0.2)
    ]

# Define home positions at the top of the screen
homes = [
    Home(0, 275, 50, 50, "home.gif"),      # Center home
    Home(-100, 275, 50, 50, "home.gif"),   # Left of center
    Home(-200, 275, 50, 50, "home.gif"),   # Far left
    Home(100, 275, 50, 50, "home.gif"),    # Right of center
    Home(200, 275, 50, 50, "home.gif")     # Far right
    ]

# Combine all sprites into one list for easier updating and rendering
sprites = level_1 + homes
sprites.append(player)

# Set up keyboard controls
wn.listen()  # Start listening for keyboard input
wn.onkeypress(player.up, "Up")       # Up arrow moves frog up
wn.onkeypress(player.down, "Down")   # Down arrow moves frog down
wn.onkeypress(player.right, "Right") # Right arrow moves frog right
wn.onkeypress(player.left, "Left")   # Left arrow moves frog left

# Main game loop
while True:    
    # Update and render all sprites
    for sprite in sprites:
        sprite.render(pen)  # Draw each sprite
        sprite.update()     # Update sprite position/state
        
    # Update timer display
    timer.render(player.time_remaining, pen)
    
    # Display remaining lives as small frogs
    pen.goto(-290, -375)  # Position for lives display
    pen.shape("frog_small.gif")
    for life in range(player.lives):
        pen.goto(-280 + (life * 30), -375)  # Space lives evenly
        pen.stamp()
    
    # Check for collisions with game objects
    player.dx = 0  # Reset horizontal movement
    player.collision = False  # Reset collision flag
    for sprite in sprites:
        if player.is_collision(sprite):
            if isinstance(sprite, Car):  # Collision with car - lose life
                player.lives -= 1
                player.go_home()
                break
            elif isinstance(sprite, Log):  # Move with log
                player.dx = sprite.dx  # Match log's speed
                player.collision = True
                break
            elif isinstance(sprite, Turtle) and sprite.state != "submerged":  # Move with visible turtle
                player.dx = sprite.dx  # Match turtle's speed
                player.collision = True
                break
            elif isinstance(sprite, Home):  # Reached a home position
                player.go_home()
                sprite.image = "frog.gif"  # Show frog in home
                player.frogs_home += 1
                break
                
    # Check if player is in water without support (log or turtle)
    if player.y > 0 and player.collision != True:
        player.lives -= 1
        player.go_home()

    # Check if all homes are filled (level complete)
    if player.frogs_home == 5:
        player.go_home()
        player.frogs_home = 0  # Reset counter
        for home in homes:
            home.image = "home.gif"  # Reset home images
        
    # Handle game over (no lives remaining)
    if player.lives == 0:
        player.go_home()
        player.frogs_home = 0  # Reset score
        for home in homes:
            home.image = "home.gif"  # Reset home images
        player.lives = 3  # Reset lives
    
    # Update screen
    wn.update()  # Refresh display

    # Clear drawing for next frame
    pen.clear()
