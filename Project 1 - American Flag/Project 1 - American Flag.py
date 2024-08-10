"""
This script uses Python's turtle module to draw the American flag. 
The flag consists of 13 horizontal stripes alternating red and white, 
with a blue rectangle (the Union) in the upper left corner containing 
50 white five-pointed stars arranged in a 9x11 grid pattern. 

The script is structured as follows:
1. A function to draw rectangles, used for the flag's stripes and the blue Union.
2. A function to draw five-pointed stars, used for placing the stars within the Union.
3. A main function that coordinates the drawing of the entire flag by calling the other two functions.

The turtle module is utilized to create graphics in a window, and the flag is drawn step by step. 
After running the script, a graphical window will open displaying the complete flag. 
The drawing speed is set to a relatively fast pace, but it can be adjusted if needed.
"""


import turtle

def draw_rectangle(x, y, width, height, color):
    """
    Draw a rectangle at a given position with specified width, height, and color.

    This function is responsible for drawing a filled rectangle with a specified size and color at a given position. 
    It is used to draw the stripes and the blue rectangle of the flag.

    Parameters:
    x (int): The x-coordinate of the top-left corner of the rectangle.
    y (int): The y-coordinate of the top-left corner of the rectangle.
    width (int): The width of the rectangle.
    height (int): The height of the rectangle.
    color (str): The fill color of the rectangle.
    """
    turtle.penup()  # Lift the pen to move without drawing
    turtle.goto(x, y)  # Move to the specified coordinates
    turtle.pendown()  # Lower the pen to start drawing
    turtle.pencolor(color)  # Set the pen color
    turtle.fillcolor(color)  # Set the fill color
    turtle.begin_fill()  # Begin filling the rectangle with color

    # Draw the rectangle using two pairs of forward and left turns
    for _ in range(2):
        turtle.forward(width)
        turtle.left(90)
        turtle.forward(height)
        turtle.left(90)

    turtle.end_fill()  # End the filling process

def draw_star(x, y, radius):
    """
    Draw a five-pointed star at a given position with a specified radius.

    This function draws a single five-pointed star at the specified location. 
    The star's size is determined by the radius parameter, which controls the length of the star's arms.

    Parameters:
    x (int): The x-coordinate of the center of the star.
    y (int): The y-coordinate of the center of the star.
    radius (int): The length of each star arm.
    """
    turtle.penup()  # Lift the pen to move without drawing
    turtle.goto(x, y)  # Move to the specified coordinates
    turtle.pendown()  # Lower the pen to start drawing
    turtle.setheading(-72)  # Set the initial heading to -72 degrees
    turtle.begin_fill()  # Begin filling the star with color

    # Draw the star using five forward and right turns
    for _ in range(5):
        turtle.forward(radius)
        turtle.right(144)  # Turn right by 144 degrees to form star points

    turtle.end_fill()  # End the filling process

def draw_american_flag():
    """
    Main function to draw the American flag using turtle graphics.

    The main function that coordinates drawing the American flag. 
    It first draws the 13 stripes, then adds the blue rectangle in the top-left corner, 
    and finally places the 50 stars in a staggered grid pattern within the blue rectangle.
    """
    turtle.speed(10)  # Set the turtle drawing speed
    turtle.penup()  # Lift the pen to move without drawing
    x, y = -270, 180  # Initial top-left corner position for the flag
    width, height = 540, 360  # Total width and height of the flag
    stripe_height = height / 13  # Height of each stripe (13 stripes in total)

    # Draw the 13 stripes (7 red and 6 white/light gray)
    for i in range(13):
        color = 'red' if i % 2 == 0 else 'light gray'  # Alternate between red and white
        draw_rectangle(x, y - i * stripe_height, width, stripe_height, color)

    # Define the dimensions and position of the blue rectangle (Union)
    blue_width, blue_height = width * 2 / 5, height * 7 / 13
    draw_rectangle(x, y - 6 * stripe_height, blue_width, blue_height, 'blue')

    # Star settings for the Union
    star_radius = 10  # Radius of each star
    star_rows = 9  # Number of rows of stars
    star_cols = 11  # Number of columns of stars
    offset_x = blue_width / star_cols  # Horizontal distance between stars
    offset_y = blue_height / star_rows  # Vertical distance between stars

    turtle.color('white')  # Set the star color to white
    # Draw the 50 stars (5 rows of 6 stars, 4 rows of 5 stars)
    for row in range(star_rows):
        for col in range(star_cols):
            # Draw stars only at alternating positions in a staggered grid
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                star_x = x + offset_x * (col + 0.3)  # Calculate the star's x position
                star_y = y - 6 * stripe_height - offset_y * (row - 8.9)  # Calculate the star's y position
                draw_star(star_x, star_y, star_radius)

    turtle.hideturtle()  # Hide the turtle after drawing is complete
    turtle.done()  # Finish the turtle graphics session

if __name__ == '__main__':
    draw_american_flag()
