"""
Peppa Pig Drawing using Python Turtle Graphics

This project uses Python's Turtle graphics library to draw a simple representation of Peppa Pig,
a popular children's cartoon character. The drawing is broken down into several components 
such as the nose, head, ears, eyes, cheeks, and mouth, each defined in separate functions.

The project demonstrates:
- Basic usage of the Turtle graphics library.
- Drawing complex shapes using circles and arcs.
- Organizing code into functions for better readability and reusability.
- Setting up a drawing environment with customized pen size, speed, and color modes.

To run this project, ensure you have Python installed with the Turtle module available. 
When executed, the script will open a window where the drawing process can be observed in real-time.

This project is suitable for beginners who want to explore graphics programming in Python
or learn how to use the Turtle library effectively.

Version: 0.1
Author: Sun Yufei
Date: 2024-08-13
"""


from turtle import *

def draw_nose(x, y):
    """Draw the nose"""
    penup()
    goto(x, y)  # Move turtle to the specified coordinates
    pendown()
    setheading(-30)  # Set the direction of the turtle
    begin_fill()
    a = 0.4
    for i in range(120):
        if 0 <= i < 30 or 60 <= i < 90:
            a += 0.08  # Increase the step length
            left(3)  # Turn left by 3 degrees
            forward(a)  # Move forward by 'a' units
        else:
            a -= 0.08  # Decrease the step length
            left(3)
            forward(a)
    end_fill()

    # Draw the nostrils
    penup()
    setheading(90)
    forward(25)
    setheading(0)
    forward(10)
    pendown()
    pencolor(255, 155, 192)
    setheading(10)
    begin_fill()
    circle(5)
    color(160, 82, 45)  # Brown color for the nostril
    end_fill()

    penup()
    setheading(0)
    forward(20)
    pendown()
    pencolor(255, 155, 192)
    setheading(10)
    begin_fill()
    circle(5)
    color(160, 82, 45)  # Brown color for the nostril
    end_fill()


def draw_head(x, y):
    """Draw the head"""
    color((255, 155, 192), "pink")  # Set fill color to pink
    penup()
    goto(x, y)
    setheading(0)
    pendown()
    begin_fill()
    setheading(180)
    circle(300, -30)
    circle(100, -60)
    circle(80, -100)
    circle(150, -20)
    circle(60, -95)
    setheading(161)
    circle(-300, 15)
    
    # Draw a small part of the head with a loop
    penup()
    goto(-100, 100)
    pendown()
    setheading(-30)
    a = 0.4
    for i in range(60):
        if 0 <= i < 30 or 60 <= i < 90:
            a += 0.08
            left(3)
            forward(a)
        else:
            a -= 0.08
            left(3)
            forward(a)
    end_fill()


def draw_ears(x, y):
    """Draw the ears"""
    color((255, 155, 192), "pink")
    penup()
    goto(x, y)
    pendown()
    begin_fill()
    setheading(100)
    circle(-50, 50)
    circle(-10, 120)
    circle(-50, 54)
    end_fill()

    # Draw the second ear
    penup()
    setheading(90)
    forward(-12)
    setheading(0)
    forward(30)
    pendown()
    begin_fill()
    setheading(100)
    circle(-50, 50)
    circle(-10, 120)
    circle(-50, 56)
    end_fill()


def draw_eyes(x, y):
    """Draw the eyes"""
    color((255, 155, 192), "white")
    penup()
    setheading(90)
    forward(-20)
    setheading(0)
    forward(-95)
    pendown()
    begin_fill()
    circle(15)  # Draw the white part of the eye
    end_fill()

    # Draw the pupil
    color("black")
    penup()
    setheading(90)
    forward(12)
    setheading(0)
    forward(-3)
    pendown()
    begin_fill()
    circle(3)  # Draw the black pupil
    end_fill()

    # Draw the second eye
    color((255, 155, 192), "white")
    penup()
    setheading(90)
    forward(-25)
    setheading(0)
    forward(40)
    pendown()
    begin_fill()
    circle(15)
    end_fill()

    # Draw the second pupil
    color("black")
    penup()
    setheading(90)
    forward(12)
    setheading(0)
    forward(-3)
    pendown()
    begin_fill()
    circle(3)
    end_fill()


def draw_cheek(x, y):
    """Draw the cheek"""
    color((255, 155, 192))
    penup()
    goto(x, y)
    pendown()
    setheading(0)
    begin_fill()
    circle(30)
    end_fill()


def draw_mouth(x, y):
    """Draw the mouth"""
    color(239, 69, 19)
    penup()
    goto(x, y)
    pendown()
    setheading(-80)
    circle(30, 40)
    circle(40, 80)


def setup_environment():
    """Set up the environment"""
    pensize(4)  # Set the thickness of the pen
    hideturtle()  # Hide the turtle cursor
    colormode(255)  # Use 255 RGB color mode
    setup(840, 500)  # Set the window size
    speed(10)  # Set drawing speed


def main():
    """Main function"""
    setup_environment() 
    draw_nose(-100, 100)
    draw_head(-69, 167)
    draw_ears(0, 160)
    draw_eyes(0, 140)
    draw_cheek(80, 10)
    draw_mouth(-20, 30)
    done()  # Finish the drawing


if __name__ == '__main__':
    main()
