# Import required libraries
import turtle  # For creating graphics and game objects
import time    # For controlling game speed and delays

# Set up the game window
wn = turtle.Screen()
wn.title("Flappy Bird by @TokyoEdTech")
wn.bgcolor("blue")  # Set background color
wn.bgpic("background.gif")  # Set background image
wn.setup(width=500, height=800)  # Set window size
wn.tracer(0)  # Turn off automatic screen updates for smoother animation

# Register game shapes
wn.register_shape("bird.gif")  # Load bird sprite

# Create score display
pen = turtle.Turtle()
pen.speed(0)  # Set to fastest speed
pen.hideturtle()  # Hide the turtle cursor
pen.penup()
pen.color("white")
pen.goto(0, 250)  # Position score at top of screen
pen.write("0", move=False, align="left", font=("Arial", 32, "normal"))

# Create player (bird)
player = turtle.Turtle()
player.speed(0)  # Set to fastest speed
player.penup()
player.color("yellow")
player.shape("bird.gif")  # Use bird sprite
player.goto(-200, 0)  # Starting position
player.dx = 0  # Horizontal velocity
player.dy = 1  # Initial vertical velocity

# Create first pipe pair (top and bottom)
pipe1_top = turtle.Turtle()
pipe1_top.speed(0)
pipe1_top.penup()
pipe1_top.color("green")
pipe1_top.shape("square")
pipe1_top.shapesize(stretch_wid=18, stretch_len=3, outline=None)  # Make pipe wider and longer
pipe1_top.goto(300, 250)  # Starting position
pipe1_top.dx = -2  # Move left
pipe1_top.dy = 0
pipe1_top.value = 1  # Score value for passing this pipe

pipe1_bottom = turtle.Turtle()
pipe1_bottom.speed(0)
pipe1_bottom.penup()
pipe1_bottom.color("green")
pipe1_bottom.shape("square")
pipe1_bottom.shapesize(stretch_wid=18, stretch_len=3, outline=None)
pipe1_bottom.goto(300, -250)  # Starting position
pipe1_bottom.dx = -2  # Move left
pipe1_bottom.dy = 0

# Create second pipe pair with different heights
pipe2_top = turtle.Turtle()
pipe2_top.speed(0)
pipe2_top.penup()
pipe2_top.color("green")
pipe2_top.shape("square")
pipe2_top.shapesize(stretch_wid=18, stretch_len=3, outline=None)
pipe2_top.goto(600, 280)  # Different height for variety
pipe2_top.dx = -2
pipe2_top.dy = 0
pipe2_top.value = 1

pipe2_bottom = turtle.Turtle()
pipe2_bottom.speed(0)
pipe2_bottom.penup()
pipe2_bottom.color("green")
pipe2_bottom.shape("square")
pipe2_bottom.shapesize(stretch_wid=18, stretch_len=3, outline=None)
pipe2_bottom.goto(600, -220)  # Different height for variety
pipe2_bottom.dx = -2
pipe2_bottom.dy = 0

# Create third pipe pair with different heights
pipe3_top = turtle.Turtle()
pipe3_top.speed(0)
pipe3_top.penup()
pipe3_top.color("green")
pipe3_top.shape("square")
pipe3_top.shapesize(stretch_wid=18, stretch_len=3, outline=None)
pipe3_top.goto(900, 320)  # Different height for variety
pipe3_top.dx = -2
pipe3_top.dy = 0
pipe3_top.value = 1

pipe3_bottom = turtle.Turtle()
pipe3_bottom.speed(0)
pipe3_bottom.penup()
pipe3_bottom.color("green")
pipe3_bottom.shape("square")
pipe3_bottom.shapesize(stretch_wid=18, stretch_len=3, outline=None)
pipe3_bottom.goto(900, -180)  # Different height for variety
pipe3_bottom.dx = -2
pipe3_bottom.dy = 0

# Set gravity constant (negative value for downward acceleration)
gravity = -0.3

# Define function to make bird jump
def go_up():
    player.dy += 8  # Add upward velocity
    
    if player.dy > 8:  # Cap maximum upward velocity
        player.dy = 8

# Set up keyboard controls
wn.listen()  # Listen for keyboard input
wn.onkeypress(go_up, "space")  # Bind space key to jump function

# Initialize game variables
player.score = 0  # Start score at 0

# Create list of pipe pairs for easier management
pipes = [(pipe1_top, pipe1_bottom), (pipe2_top, pipe2_bottom), (pipe3_top, pipe3_bottom)]

# Main Game Loop
while True:
    # Pause for smooth animation (20ms delay)
    time.sleep(0.02)
    # Update the screen
    wn.update()
    
    # Apply gravity to bird (constant downward acceleration)
    player.dy += gravity
    
    # Move bird vertically based on current velocity
    y = player.ycor()
    y += player.dy
    player.sety(y)
    
    # Check for bottom border collision (prevent bird from going below screen)
    if player.ycor() < -390:
        player.dy = 0
        player.sety(-390)

    # Handle pipe movement and collisions
    for pipe_pair in pipes:
        pipe_top = pipe_pair[0]
        pipe_bottom = pipe_pair[1]
        
        # Move pipes horizontally (constant speed to the left)
        x = pipe_top.xcor()
        x += pipe_top.dx
        pipe_top.setx(x) 
        
        x = pipe_bottom.xcor()
        x += pipe_bottom.dx
        pipe_bottom.setx(x)
        
        # Reset pipes when they go off screen (recycle pipes for continuous gameplay)
        if pipe_top.xcor() < -350:
            pipe_top.setx(600)  # Move back to right side
            pipe_bottom.setx(600)
            pipe_top.value = 1  # Reset score value for this pipe

        # Check for collisions between bird and pipes
        # Check horizontal overlap
        if (player.xcor() + 10 > pipe_top.xcor() - 30) and (player.xcor() - 10 < pipe_top.xcor() + 30):
            # Check vertical overlap with either pipe
            if (player.ycor() + 10 > pipe_top.ycor() - 180) or (player.ycor() - 10 < pipe_bottom.ycor() + 180):
                # Game over sequence
                pen.clear()
                pen.write("Game Over", move=False, align="center", font=("Arial", 16, "normal"))
                wn.update()
                time.sleep(3)  # Show game over message for 3 seconds
                # Reset game state
                player.score = 0
                pipe_top.setx(450)  # Reset pipe positions
                pipe_bottom.setx(450)
                player.goto(-200, 0)  # Reset bird position
                player.dy = 0  # Reset bird velocity
                pen.clear()
                pen.write("0", move=False, align="center", font=("Arial", 16, "normal"))
                
        # Update score when passing through pipes
        # Check if bird has passed the pipe (pipe is behind bird)
        if pipe_top.xcor() + 30 < player.xcor() - 10:
            player.score += pipe_top.value  # Add score
            pipe_top.value = 0  # Prevent multiple scoring
            pen.clear()
            pen.write(player.score, move=False, align="center", font=("Arial", 32, "normal"))

# Keep the window open
wn.mainloop()
