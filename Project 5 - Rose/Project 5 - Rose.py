"""
This project implements a simple turtle graphics-based drawing of a rose using Python.
The project uses the turtle module to draw a single rose with red petals, a green stem, and leaves.
The drawing is accomplished by defining functions for drawing the rose and its stem and leaves, and
then calling these functions in sequence to assemble a complete rose.

The project demonstrates:
- Basic usage of the turtle graphics module in Python for drawing.
- Using functions to organize and structure the drawing process.
- Implementing repetitive shapes such as petals and leaves using loops and geometric drawing commands.
- Setting up turtle parameters such as pen size, color, and fill operations.
- Structuring the drawing into distinct parts: petals, stem, and leaves.

To run this project, simply execute the Python script. It requires Python and the turtle module, which is part of the standard library. 
When executed, the script opens a turtle graphics window and automatically draws the rose.

This project is a great learning opportunity for beginners who want to explore turtle graphics and practice organizing code with functions.

Version: 1.0
Author: Sun Yufei
Date: 2024-08-22
"""

import turtle
import time

# Set the turtle's speed (1 slowest, 10 fastest, 0 is instantaneous)
turtle.speed(5)

# Set initial position
turtle.penup()  # Lift the pen to move without drawing
turtle.left(90)  # Turn counterclockwise by 90 degrees
turtle.fd(200)  # Move forward by 200 units
turtle.pendown()  # Lower the pen to start drawing
turtle.right(90)  # Turn clockwise by 90 degrees

# Set the pen size
turtle.pensize(2)

# Drawing the flower center (stamen)
turtle.fillcolor("red")  # Set the fill color to red
turtle.begin_fill()  # Start filling
turtle.circle(10, 180)  # Draw a half circle with radius 10
turtle.circle(25, 110)  # Draw a portion of a circle with radius 25
turtle.left(50)
turtle.circle(60, 45)  # Draw a portion of a circle with radius 60
turtle.circle(20, 170)  # Draw a large portion of a circle with radius 20
turtle.right(24)
turtle.fd(30)  # Move forward by 30 units
turtle.left(10)
turtle.circle(30, 110)  # Draw a portion of a circle with radius 30
turtle.fd(20)  # Move forward by 20 units
turtle.left(40)
turtle.circle(90, 70)  # Draw a portion of a circle with radius 90
turtle.circle(30, 150)  # Draw a large portion of a circle with radius 30
turtle.right(30)
turtle.fd(15)  # Move forward by 15 units
turtle.circle(80, 90)  # Draw a portion of a circle with radius 80
turtle.left(15)
turtle.fd(45)  # Move forward by 45 units
turtle.right(165)
turtle.fd(20)  # Move forward by 20 units
turtle.left(155)
turtle.circle(150, 80)  # Draw a large portion of a circle with radius 150
turtle.left(50)
turtle.circle(150, 90)  # Draw a portion of a circle with radius 150
turtle.end_fill()  # End filling

# Drawing petal 1
turtle.left(150)
turtle.circle(-90, 70)  # Draw a portion of a circle with negative radius
turtle.left(20)
turtle.circle(75, 105)  # Draw a portion of a circle with radius 75
turtle.setheading(60)  # Set the heading to 60 degrees
turtle.circle(80, 98)  # Draw a portion of a circle with radius 80
turtle.circle(-90, 40)  # Draw a portion of a circle with negative radius 90

# Drawing petal 2
turtle.left(180)
turtle.circle(90, 40)  # Draw a portion of a circle with radius 90
turtle.circle(-80, 98)  # Draw a portion of a circle with negative radius 80
turtle.setheading(-83)  # Set the heading to -83 degrees

# Drawing leaf 1
turtle.fd(30)  # Move forward by 30 units
turtle.left(90)
turtle.fd(25)  # Move forward by 25 units
turtle.left(45)
turtle.fillcolor("green")  # Set fill color to green
turtle.begin_fill()  # Start filling
turtle.circle(-80, 90)  # Draw a portion of a circle with negative radius 80
turtle.right(90)
turtle.circle(-80, 90)  # Draw another portion with negative radius 80
turtle.end_fill()  # End filling

# Reposition for next leaf
turtle.right(135)
turtle.fd(60)
turtle.left(180)
turtle.fd(85)  # Move back to original position
turtle.left(90)
turtle.fd(80)

# Drawing leaf 2
turtle.right(90)
turtle.right(45)
turtle.fillcolor("green")  # Set fill color to green
turtle.begin_fill()  # Start filling
turtle.circle(80, 90)  # Draw a portion of a circle with radius 80
turtle.left(90)
turtle.circle(80, 90)  # Draw another portion of a circle with radius 80
turtle.end_fill()  # End filling

# Final adjustments
turtle.left(135)
turtle.fd(60)
turtle.left(180)
turtle.fd(60)
turtle.right(90)
turtle.circle(200, 50)  # Draw a large portion of a circle with radius 200 and angle 50

# Finish the drawing and prevent the window from closing immediately
turtle.done()
