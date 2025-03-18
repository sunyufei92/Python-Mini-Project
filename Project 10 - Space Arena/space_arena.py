"""
Space Arena Game
A 2D space shooting game where the player controls a spaceship to fight against enemies.
Features include:
- Player movement and shooting mechanics
- Different types of enemies (hunters, mines, surveillance)
- Power-up system
- Particle effects and explosions
- Radar system
- Camera following
- Sound effects and background music
"""

import turtle
import math
import random
import time
import os
import platform

# If on Windows, import winsound or, better yet, switch to Linux!
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print ("Winsound module not available.")
        
def play_sound(sound_file, time = 0):
    """
    Play sound effects based on the operating system
    Args:
        sound_file: Path to the sound file
        time: Time interval for repeating sound (0 for single play)
    """
    # Windows
    if platform.system() == 'Windows':
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    # Linux
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    # Mac
    else:
        os.system("afplay {}&".format(sound_file))

    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time * 1000))
        


SCREEN_WIDTH = 800  
SCREEN_HEIGHT = 600

wn = turtle.Screen()
wn.setup(width = SCREEN_WIDTH + 220, height = SCREEN_HEIGHT + 20)
wn.title("Space Arena! BY Jack Sun")
wn.bgcolor("black")

# Start the BGM
play_sound("bgm.wav", 120)

images = ["hunter.gif", "surveillance.gif", "mine.gif", "powerup.gif"]
for image in images:
    wn.register_shape(image)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

class CharacterPen:
    """
    A class for rendering text characters in the game
    Handles drawing of numbers and letters using turtle graphics
    """
    def __init__(self, color = "white", scale = 1.0):
        """
        Initialize the character pen
        Args:
            color: Color of the text
            scale: Scale factor for text size
        """
        self.color = color
        self.scale = scale

        # Define character shapes using coordinates
        self.characters = {}
        # Numbers 0-9
        self.characters["1"] = ((-5, 10),(0, 10),(0, -10),(-5, -10), (5, -10))
        self.characters["2"] = ((-5, 10),(5, 10),(5, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["3"] = ((-5, 10),(5, 10),(5, 0), (0, 0), (5, 0), (5,-10), (-5, -10))
        self.characters["4"] = ((-5, 10), (-5, 0), (5, 0), (2,0), (2, 5), (2, -10))
        self.characters["5"] = ((5, 10), (-5, 10), (-5, 0), (5,0), (5,-10), (-5, -10))
        self.characters["6"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (-5, 0))
        self.characters["7"] = ((-5, 10), (5, 10), (0, -10))
        self.characters["8"] = ((-5, 0), (5, 0), (5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0))
        self.characters["9"] = ((5, -10), (5, 10), (-5, 10), (-5, 0), (5, 0))
        self.characters["0"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))

        # Letters A-Z
        self.characters["A"] = ((-5, -10), (-5, 10), (5, 10), (5, -10), (5, 0), (-5, 0))
        self.characters["B"] = ((-5, -10), (-5, 10), (3, 10), (3, 0), (-5, 0), (5,0), (5, -10), (-5, -10))
        self.characters["C"] = ((5, 10), (-5, 10), (-5, -10), (5, -10))
        self.characters["D"] = ((-5, 10), (-5, -10), (5, -8), (5, 8), (-5, 10))
        self.characters["E"] = ((5, 10), (-5, 10), (-5, 0), (0, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["F"] = ((5, 10), (-5, 10), (-5, 0), (5, 0), (-5, 0), (-5, -10))
        self.characters["G"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (0, 0))
        self.characters["H"] = ((-5, 10), (-5, -10), (-5, 0), (5, 0), (5, 10), (5, -10))
        self.characters["I"] = ((-5, 10), (5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters["J"] = ((5, 10), (5, -10), (-5, -10), (-5, 0))   
        self.characters["K"] = ((-5, 10), (-5, -10), (-5, 0), (5, 10), (-5, 0), (5, -10))
        self.characters["L"] = ((-5, 10), (-5, -10), (5, -10))
        self.characters["M"] = ((-5, -10), (-3, 10), (0, 0), (3, 10), (5, -10))
        self.characters["N"] = ((-5, -10), (-5, 10), (5, -10), (5, 10))
        self.characters["O"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))
        self.characters["P"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0))
        self.characters["Q"] = ((5, -10), (-5, -10), (-5, 10), (5, 10), (5, -10), (2, -7), (6, -11))
        self.characters["R"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0), (5, -10))
        self.characters["S"] = ((5, 8), (5, 10), (-5, 10), (-5, 0), (5, 0), (5, -10), (-5, -10), (-5, -8))
        self.characters["T"] = ((-5, 10), (5, 10), (0, 10), (0, -10)) 
        self.characters["V"] = ((-5, 10), (0, -10), (5, 10)) 
        self.characters["U"] = ((-5, 10), (-5, -10), (5, -10), (5, 10)) 
        self.characters["W"] = ((-5, 10), (-3, -10), (0, 0), (3, -10), (5, 10))   
        self.characters["X"] = ((-5, 10), (5, -10), (0, 0), (-5, -10), (5, 10))   
        self.characters["Y"] = ((-5, 10), (0, 0), (5, 10), (0,0), (0, -10))   
        self.characters["Z"] = ((-5, 10), (5, 10), (-5, -10), (5, -10))   
        
        # Special characters
        self.characters["-"] = ((-3, 0), (3, 0)) 
         
    def draw_string(self, pen, str, x, y):
        """
        Draw a string of characters at specified coordinates
        Args:
            pen: Turtle pen object
            str: String to draw
            x: X coordinate
            y: Y coordinate
        """
        pen.width(2)
        pen.color(self.color)
        
        # Center text
        x -= 15 * self.scale * ((len(str) - 1) / 2)
        
        for character in str:
            self.draw_character(pen, character, x, y)
            x += 15 * self.scale

    def draw_character(self, pen, character, x, y):
        """
        Draw a single character at specified coordinates
        Args:
            pen: Turtle pen object
            character: Character to draw
            x: X coordinate
            y: Y coordinate
        """
        scale = self.scale
        
        # Handle lowercase letters
        if character in "abcdefghijklmnopqrstuvwxyz":
            scale *= 0.8
            y -= 10 * (1 - scale)

        # Convert to uppercase for lookup
        character = character.upper()
            
        if character in self.characters:
            pen.penup()
            xy = self.characters[character][0]
            pen.goto(x + xy[0] * scale, y + xy[1] * scale)
            pen.pendown()
            for i in range(1, len(self.characters[character])):
                xy = self.characters[character][i]
                pen.goto(x + xy[0] * scale, y + xy[1] * scale)
            pen.penup()

# Splash screen
character_pen = CharacterPen("red", 3.0)
character_pen.draw_string(pen, "SPACE ARENA", 0, 160)

character_pen.scale = 1.0
character_pen.draw_string(pen, "BY Jack Sun", 0, 100)

pen.color("white")
pen.shape("triangle")

pen.goto(-150, 20)
pen.stamp()

character_pen.scale = 1.0
character_pen.draw_string(pen, "Player", -150, -20)

pen.shape("hunter.gif")
pen.goto(0, 20)
pen.stamp()
character_pen.draw_string(pen, "Enemy", 0, -20)

pen.shape("powerup.gif")
pen.goto(150, 20)
pen.stamp()
character_pen.draw_string(pen, "Powerup", 150, -20)

character_pen.draw_string(pen, "Up Arrow", -100, -60)
character_pen.draw_string(pen, "Accelerate", 100, -60)

character_pen.draw_string(pen, "Left Arrow", -100, -100)
character_pen.draw_string(pen, "Rotate Left", 100, -100)

character_pen.draw_string(pen, "Right Arrow", -100, -140)
character_pen.draw_string(pen, "Rotate Right", 100, -140)

character_pen.draw_string(pen, "Space", -100, -180)
character_pen.draw_string(pen, "Fire", 100, -180)


character_pen.scale = 1.0
character_pen.draw_string(pen, "PRESS S TO START", 0, -240)



wn.tracer(0)
wn.update()

class Game():
    """
    Main game class that handles game state and rendering
    Manages game loop, scoring, and level progression
    """
    def __init__(self, width, height):
        """
        Initialize the game
        Args:
            width: Game world width
            height: Game world height
        """
        self.width = width
        self.height = height
        self.frame = 0
        self.level = 1
        self.state = "splash"  # Game states: splash, playing, paused
        
    def start_game(self):
        """Start the game from splash screen"""
        self.state = "playing"
        
    def toggle_pause(self):
        """Toggle between playing and paused states"""
        if self.state == "paused":
            self.state = "playing"
        else:
            self.state = "paused"
        
    def render_info(self, pen, score, active_enemies):
        """
        Render game information panel
        Args:
            pen: Turtle pen object
            score: Current game score
            active_enemies: Number of active enemies
        """
        # Draw info panel background
        pen.color("#222255")
        pen.penup()
        pen.goto(400, 0)
        pen.shape("square")
        pen.setheading(90)
        pen.shapesize(stretch_wid=10, stretch_len=32, outline=None)
        pen.stamp()
        
        # Draw separator line
        pen.color("white")
        pen.width(3)
        pen.goto(300, 400)
        pen.pendown()
        pen.goto(300, -400)
        
        # Draw game stats
        pen.penup() 
        pen.color("white")
        pen.goto(400, 250)
        pen.goto(400, 230)
        character_pen.scale = 1.0
        character_pen.draw_string(pen, "SPACE ARENA".format(score), 400, 270)
        character_pen.draw_string(pen, "Score {}".format(score), 400, 240)
        character_pen.draw_string(pen, "Enemies {}".format(active_enemies), 400, 210)
        character_pen.draw_string(pen, "Lives {}".format(player.lives), 400, 180)
        character_pen.draw_string(pen, "Level {}".format(game.level), 400, 150)
        
    def render_border(self, pen, x_offset, y_offset, screen_width, screen_height):
        """
        Render game world border
        Args:
            pen: Turtle pen object
            x_offset: Camera X offset
            y_offset: Camera Y offset
            screen_width: Screen width
            screen_height: Screen height
        """
        pen.color("white")
        pen.width(3)
        pen.penup()
        left = -self.width/2.0 - x_offset
        right = self.width/2.0 - x_offset
        top = self.height/2.0 - y_offset
        bottom = -self.height/2.0 - y_offset
        
        # Draw border rectangle
        pen.goto(left, top)
        pen.pendown()
        pen.goto(right, top)
        pen.goto(right, bottom)
        pen.goto(left, bottom)
        pen.goto(left, top)
        pen.penup()

class Sprite():
    """
    Base class for all game objects
    Handles basic physics, collision detection, and rendering
    """
    
    @staticmethod
    def is_collision(sprite1, sprite2, threshold):
        """
        Check if two sprites are colliding
        Args:
            sprite1: First sprite
            sprite2: Second sprite
            threshold: Collision distance threshold
        Returns:
            bool: True if sprites are colliding
        """
        d = math.sqrt((sprite1.x-sprite2.x)**2 + (sprite1.y-sprite2.y)**2)
        if d < threshold:
            return True
        else:
            return False
    
    @staticmethod
    def is_on_screen(sprite, screen_width, screen_height, x_offset, y_offset):
        """
        Check if sprite is visible on screen
        Args:
            sprite: Sprite to check
            screen_width: Screen width
            screen_height: Screen height
            x_offset: Camera X offset
            y_offset: Camera Y offset
        Returns:
            bool: True if sprite is on screen
        """
        if sprite.x - x_offset < screen_width / 2 and sprite.x - x_offset > -screen_width / 2\
            and sprite.y - y_offset < screen_height /2 and sprite.y - y_offset > - screen_height / 2:    
            return True
        else:
            return False
            
    def __init__(self, x, y, shape="square", color = "white"):
        """
        Initialize a sprite
        Args:
            x: Initial X position
            y: Initial Y position
            shape: Sprite shape
            color: Sprite color
        """
        self.shape = shape
        self.color = color
        self.width = 20.0
        self.height = 20.0
        self.heading = 0.0  # Rotation angle
        self.dx = 0.0      # X velocity
        self.dy = 0.0      # Y velocity
        self.da = 0.0      # Angular velocity
        self.thrust = 0.0  # Thrust force
        self.max_d = 2.0   # Maximum speed
        self.x = x         # X position
        self.y = y         # Y position
        self.state = "active"  # Sprite state: active, inactive, ready
        
    def bounce(self, other):
        """
        Handle elastic collision with another sprite
        Args:
            other: Other sprite to bounce off
        """
        temp_dx = self.dx
        temp_dy = self.dy
        
        self.dx = other.dx
        self.dy = other.dy
        
        other.dx = temp_dx
        other.dy = temp_dy 

    def update(self):        
        """
        Update sprite physics
        Handles movement, rotation, and boundary checking
        """
        self.heading += self.da
        self.heading %= 360.0
        
        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust
        
        self.x += self.dx
        self.y += self.dy
        
        self.border_check()
            
    def border_check(self):
        """
        Keep sprite within game world boundaries
        Handles bouncing off walls
        """
        if self.x > game.width / 2.0 - 10.0:
            self.x = game.width / 2.0 - 10.0
            self.dx *= -1.0
        elif self.x < -game.width / 2.0 + 10.0:
            self.x = -game.width / 2.0 + 10.0
            self.dx *= -1.0
            
        if self.y > game.height / 2.0 - 10.0:
            self.y = game.height / 2.0 - 10.0
            self.dy *= -1.0
        elif self.y < -game.height / 2.0 + 10.0:
            self.y = -game.height / 2.0 + 10.0
            self.dy *= -1.0       
        
    def render(self, pen, x_offset = 0, y_offset = 0):
        """
        Render the sprite on screen
        Args:
            pen: Turtle pen object
            x_offset: Camera X offset
            y_offset: Camera Y offset
        """
        # Check if active
        if self.state == "active":
            # Check if it is on the screen
            screen_x = self.x - x_offset
            screen_y = self.y - y_offset
            
            if(screen_x > -game.width/2.0 and screen_x < game.width/2.0 and screen_y > -game.height/2.0 and screen_y < game.width/2.0):
                pen.goto(self.x - x_offset, self.y - y_offset)
                pen.shape(self.shape)
                pen.color(self.color)
                pen.shapesize(stretch_wid=1, stretch_len=1, outline=None)
                pen.setheading(self.heading)
                pen.stamp()
        
class Player(Sprite):
    """
    Player-controlled spaceship class
    Handles player movement, shooting, and health
    """
    def __init__(self):
        """
        Initialize the player spaceship
        Sets up initial stats and abilities
        """
        Sprite.__init__(self, 0.0, 0.0, "triangle")
        self.da = 0.0
        self.heading = 90.0
        self.score = 0
        self.max_health = 40
        self.health = self.max_health
        self.sensor_range = 500  # Range for detecting enemies
        self.thrust = 0.0
        self.acceleration = 0.2
        self.lives = 3
        
    def rotate_left(self):
        """Rotate the ship counterclockwise"""
        self.da = 10.0
        
    def rotate_right(self):
        """Rotate the ship clockwise"""
        self.da = -10.0
        
    def stop_rotation(self):
        """Stop ship rotation"""
        self.da = 0.0
        
    def accelerate(self):
        """
        Apply thrust to the ship
        Creates exhaust particles and plays sound
        """
        play_sound("thruster.wav")
        self.thrust += self.acceleration
        
        # Create exhaust particles
        dx = math.cos(math.radians(self.heading + 180)) * 5 
        dy = math.sin(math.radians(self.heading + 180)) * 5
        
        exhaust.explode(self.x - 100, self.y, dx, dy)
        
    def decelerate(self):
        """Stop applying thrust"""
        self.thrust = 0.0
        
    def fire(self):
        """
        Fire missiles from the ship
        Creates three spread missiles and plays sound
        """
        play_sound("missile_fire.wav")
        
        directions = [0, 5, -5]  # Spread angles for missiles
        
        for missile in missiles:
            if missile.state == "ready":
                # Set missile initial position and velocity
                missile.x = player.x
                missile.y = player.y
                missile.heading = player.heading + directions[0]
                missile.dx = math.cos(math.radians(missile.heading)) * missile.thrust
                missile.dy = math.sin(math.radians(missile.heading)) * missile.thrust
                missile.dx += player.dx
                missile.dy += player.dy
                missile.state = "active"
                
                # Apply recoil to player
                self.dx -= missile.dx * 0.01
                self.dy -= missile.dy * 0.01
                
                directions.pop(0)
                
                if len(directions) == 0:
                    break
                
    def reset(self):
        """
        Reset player to initial state
        Called after losing a life
        """
        self.x = 0.0
        self.y = 0.0
        self.dx = 0.0
        self.dy = 0.0
        self.da = 0.0
        self.heading = 90.0
        self.health = self.max_health
        
    def render(self, pen, x_offset = 0, y_offset = 0):
        """
        Render the player ship and health bar
        Args:
            pen: Turtle pen object
            x_offset: Camera X offset
            y_offset: Camera Y offset
        """
        # Draw ship
        pen.shapesize(stretch_wid=0.5, stretch_len=1, outline=None) 
        pen.goto(self.x - x_offset, self.y - y_offset)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.setheading(self.heading)
        pen.stamp()
        
        # Draw health bar
        pen.goto(self.x - x_offset - 10.0, self.y - y_offset + 20.0)
        pen.width(3.0)
        pen.pendown()
        pen.setheading(0.0)
        try:
            # Color health bar based on health percentage
            if self.health/self.max_health < 0.3:
                pen.color("red")
            elif self.health/self.max_health < 0.7:
                pen.color("yellow")
            else:
                pen.color("green")
            # Draw filled portion
            pen.fd(20.0 * (self.health/self.max_health))
            # Draw empty portion
            pen.color("grey")
            pen.fd(20.0 * ((self.max_health-self.health)/self.max_health))
        except:
            pass
            
        pen.penup()

class Enemy(Sprite):
    """
    Enemy spaceship class
    Handles different types of enemies with unique behaviors
    """
    def __init__(self, x, y, shape = "square", color = "red"):
        """
        Initialize an enemy
        Args:
            x: Initial X position
            y: Initial Y position
            shape: Enemy shape
            color: Enemy color
        """
        Sprite.__init__(self, x, y, shape, color)
        self.max_health = random.randint(10, 30)
        self.health = self.max_health
        # Randomly select enemy type
        self.type = random.choice(["hunter", "mine", "surveillance"])
        self.max_dx = 3.0
        self.max_dy = 3.0
        self.sensor_range = random.randint(40, 60)
        
        # Configure enemy based on type
        if self.type == "hunter":
            self.color = "red"
            self.shape = "hunter.gif"
            self.sensor_range = random.randint(100, 200)
            
        elif self.type == "mine":
            self.color = "orange"
            self.shape = "mine.gif"
            self.sensor_range = random.randint(100, 200)

        elif self.type == "surveillance":
            self.color = "pink"
            self.shape = "surveillance.gif"
            self.sensor_range = random.randint(200, 400)

    def update(self):
        """
        Update enemy behavior based on type
        Handles movement, health, and type-specific actions
        """
        # Check if enemy is destroyed
        if self.health <= 0:
            self.state = "inactive"
                    
        self.heading += self.da
        self.heading %= 360.0
        
        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust
        
        self.x += self.dx
        self.y += self.dy
        
        # Type-specific behavior
        if self.type == "hunter":
            # Chase player when in range
            if Sprite.is_collision(player, self, self.sensor_range):
                if self.x < player.x:
                    self.dx += 0.05
                else: 
                    self.dx -= 0.05

                if self.y < player.y:
                    self.dy += 0.05
                else: 
                    self.dy -= 0.05
            
        elif self.type == "mine":
            # Stay stationary until player approaches
            self.dx = 0.0
            self.dy = 0.0
            
            if Sprite.is_collision(player, self, self.sensor_range):
                self.type = "hunter"
                self.color = "red"
            
        elif self.type == "surveillance":
            # Move away from player when in range
            if Sprite.is_collision(player, self, self.sensor_range):
                if self.x > player.x:
                    self.dx += 0.03
                else: 
                    self.dx -= 0.03

                if self.y > player.y:
                    self.dy += 0.03
                else: 
                    self.dy -= 0.03
        
        # Limit maximum velocity
        if self.dx > self.max_dx:
            self.dx = self.max_dx
        elif self.dx < -self.max_dx:
            self.dx = -self.max_dx
            
        if self.dy > self.max_dy:
            self.dy = self.max_dy
        elif self.dy < -self.max_dy:
            self.dy = -self.max_dy
        
        self.border_check()

    def render(self, pen, x_offset, y_offset):
        """
        Render the enemy and its health bar
        Args:
            pen: Turtle pen object
            x_offset: Camera X offset
            y_offset: Camera Y offset
        """
        if self.state == "active":
            # Draw enemy
            pen.shapesize(stretch_wid=1, stretch_len=1, outline=None) 
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.setheading(self.heading)
            pen.stamp()
            
            # Draw health bar
            pen.goto(self.x - x_offset - 10.0, self.y - y_offset + 20.0)
            pen.width(2)
            pen.pendown()
            pen.setheading(0.0)
            try:
                # Color health bar based on health percentage
                if self.health/self.max_health < 0.3:
                    pen.color("red")
                elif self.health/self.max_health < 0.7:
                    pen.color("yellow")
                else:
                    pen.color("green")
                # Draw filled portion
                pen.fd(20.0 * (self.health/self.max_health))
                # Draw empty portion
                pen.color("grey")
                pen.fd(20.0 * ((self.max_health-self.health)/self.max_health))
            except:
                pass
                
            pen.penup()

class Missile(Sprite):
    """
    Missile projectile class
    Handles missile movement and damage
    """
    def __init__(self, x, y, shape = "triangle", color = "yellow"):
        """
        Initialize a missile
        Args:
            x: Initial X position
            y: Initial Y position
            shape: Missile shape
            color: Missile color
        """
        Sprite.__init__(self, x, y, shape, color)
        self.state = "ready"  # ready, active
        self.thrust = 5.0     # Missile speed
        self.max_fuel = 200.0 # Maximum travel distance
        self.fuel = 200.0     # Current fuel remaining
        self.damage = 5.0     # Damage dealt to enemies

    def update(self):        
        self.heading += self.da
        self.heading %= 360.0
        
        self.x += self.dx
        self.y += self.dy
        
        self.border_check()
        
        self.fuel -= self.thrust
        if self.fuel < 0:
            self.state = "ready"
            self.fuel = self.max_fuel

            
    def reset(self):
        self.state = "ready"
        self.fuel = self.max_fuel

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None) 
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.setheading(self.heading)
            pen.stamp()

class Star(Sprite):
    """
    Background star class
    Creates parallax scrolling effect
    """
    def __init__(self, x, y, shape = "circle", color = "yellow"):
        """
        Initialize a star
        Args:
            x: Initial X position
            y: Initial Y position
            shape: Star shape
            color: Star color
        """
        Sprite.__init__(self, x, y, shape, color)
        self.distance = random.randint(2, 6)  # Star depth for parallax
        self.color = random.choice(["white", "yellow", "orange", "red"])
        self.width = 0.5 / self.distance  # Star size based on distance

    def render(self, pen, x_offset = 0, y_offset = 0):
        if self.state == "active":
            pen.shapesize(stretch_wid=0.5/self.distance, stretch_len=0.5/self.distance, outline=None) 
            pen.goto(self.x - x_offset/self.distance, self.y - y_offset/self.distance)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.setheading(self.heading)
            pen.stamp()

class Powerup(Sprite):
    """
    Power-up item class
    Provides missile upgrades when collected
    """
    def __init__(self, x, y, shape = "circle", color = "blue"):
        """
        Initialize a power-up
        Args:
            x: Initial X position
            y: Initial Y position
            shape: Power-up shape
            color: Power-up color
        """
        Sprite.__init__(self, x, y, shape, color)
        self.dx = random.randint(-30, 30) / 10.0  # Random X velocity
        self.dy = random.randint(-30, 30) / 10.0  # Random Y velocity
        self.shape = "powerup.gif"

class Particle(Sprite):
    """
    Particle effect class
    Used for explosions and exhaust effects
    """
    def __init__(self, x, y, shape = "triangle", color = "red"):
        """
        Initialize a particle
        Args:
            x: Initial X position
            y: Initial Y position
            shape: Particle shape
            color: Particle color
        """
        Sprite.__init__(self, x, y, shape, color)
        self.dx = random.randint(-6, 6)  # Random X velocity
        self.dy = random.randint(-6, 6)  # Random Y velocity
        self.frame = random.randint(10, 20)  # Particle lifetime
        self.color = random.choice(["red", "orange", "yellow"])
        self.shape = "triangle"
        self.state = "inactive"
        
    def render(self, pen, x_offset = 0, y_offset = 0):
        self.frame -= 1
        self.dx *= 0.85
        self.dy *= 0.85
        if self.frame <= 0:
            self.frame = random.randint(10, 20)
            self.state = "inactive"
        pen.shapesize(stretch_wid=0.05, stretch_len=0.05, outline=None) 
        pen.goto(self.x - x_offset, self.y - y_offset)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()       

class Explosion():
    """
    Explosion effect manager
    Creates and manages particle effects for explosions
    """
    def __init__(self, number_of_particles):
        """
        Initialize explosion system
        Args:
            number_of_particles: Number of particles in explosion
        """
        self.particles = []
        for _ in range(number_of_particles):
            self.particles.append(Particle(0,0))
            
    def explode(self, x, y, dx_offset = 0, dy_offset = 0):
        """
        Create explosion effect at specified position
        Args:
            x: X position of explosion
            y: Y position of explosion
            dx_offset: X velocity offset
            dy_offset: Y velocity offset
        """
        play_sound("explosion.wav")
        for particle in self.particles:
            if particle.state == "inactive":
                particle.x = x
                particle.y = y
                particle.dx = random.randint(-12, 12)
                particle.dy = random.randint(-12, 12)
                particle.dx += dx_offset * 2
                particle.dy += dy_offset * 2
                particle.state = "active"
                
    def render(self, pen, x_offset = 0, y_offset = 0):
        for particle in self.particles:
            if particle.state == "active":
                particle.update()
                particle.render(pen, x_offset, y_offset) 
                
class Exhaust():
    """
    Exhaust effect manager
    Creates and manages particle effects for ship exhaust
    """
    def __init__(self, number_of_particles):
        """
        Initialize exhaust system
        Args:
            number_of_particles: Number of particles in exhaust
        """
        self.particles = []
        for _ in range(number_of_particles):
            self.particles.append(Particle(0,0))
            
    def explode(self, x, y, dx_offset = 0, dy_offset = 0):
        """
        Create exhaust effect at specified position
        Args:
            x: X position of exhaust
            y: Y position of exhaust
            dx_offset: X velocity offset
            dy_offset: Y velocity offset
        """
        for particle in self.particles:
            if particle.state == "inactive":
                particle.color = random.choice(["red", "yellow"])
                particle.x = x
                particle.y = y
                particle.dx = random.randint(-1, 1)
                particle.dy = random.randint(-1, 1)
                particle.dx += dx_offset * 2
                particle.dy += dy_offset * 2
                particle.state = "active"
                
    def render(self, pen, x_offset = 0, y_offset = 0):
        for particle in self.particles:
            if particle.state == "active":
                particle.update()
                pen.width(2)
                particle.render(pen, x_offset, y_offset) 

class Radar():
    """
    Radar display system
    Shows nearby objects relative to player position
    """
    def __init__(self, x, y, width, height):
        """
        Initialize radar display
        Args:
            x: X position of radar
            y: Y position of radar
            width: Radar width
            height: Radar height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def render(self, pen, sprites):
        """
        Render radar and detected objects
        Args:
            pen: Turtle pen object
            sprites: List of sprites to display on radar
        """
        # Draw radar border         
        character_pen.draw_string(pen, "Radar", self.x, self.y + 130)
        
        pen.color("white")
        pen.penup()

        # Draw sprite radar images
        for sprite in sprites:
            if sprite.state == "active" and Sprite.is_collision(player, sprite, player.sensor_range):
                # Calculate relative position on radar
                radar_x = self.x + (sprite.x - player.x) * (self.width / game.width)
                radar_y = self.y + (sprite.y - player.y) * (self.height / game.height)
                pen.goto(radar_x, radar_y)
                pen.color(sprite.color)
                pen.shape(sprite.shape)
                pen.setheading(sprite.heading)
                
                # Adjust size based on sprite type
                if isinstance(sprite, Player):
                    pen.shapesize(stretch_wid=0.1, stretch_len=0.2, outline=None) 
                elif isinstance(sprite, Missile):
                    pen.shapesize(stretch_wid=0.05, stretch_len=0.5, outline=None)
                elif isinstance(sprite, Enemy):
                    pen.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None)
                elif isinstance(sprite, Powerup):
                    pen.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None)
                    
                pen.stamp()
                
        # Draw radar circle
        pen.setheading(90)
        pen.goto(self.x + 100, self.y)
        pen.pendown()
        pen.circle(100)
        pen.penup()

class Camera():
    """
    Camera system class
    Handles view following and camera movement
    """
    def __init__(self, x, y):
        """
        Initialize camera
        Args:
            x: Initial X position
            y: Initial Y position
        """
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.heading = 90
        self.visible = False
        
    def toggle_visibility(self):
        """Toggle camera visibility"""
        self.visible = not self.visible
                    
    def update(self, player):
        """
        Update camera position to follow player
        Args:
            player: Player object to follow
        """
        # Calculate angle to player
        dy = player.y - self.y
        dx = player.x - self.x
        if dx != 0:
            self.heading = math.degrees(math.atan2(dy,dx))
        else:
            self.heading = 90
        
        # Calculate distance and movement
        distance = math.sqrt(((self.x-player.x)**2) + ((self.y-player.y)**2))
        self.dx = math.cos(math.radians(self.heading)) * distance / 8
        self.dy = math.sin(math.radians(self.heading)) * distance / 8
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
    def render(self, pen):
        """
        Render camera indicator if visible
        Args:
            pen: Turtle pen object
        """
        if self.visible:
            pen.shapesize(stretch_wid=0.3, stretch_len=0.3, outline=None) 
            pen.goto(self.x - player.x - 100, self.y - player.y)
            pen.shape("triangle")
            pen.color("red")
            pen.setheading(self.heading)
            pen.stamp()

# Set up the game
game = Game(1600, 1200)  # Create game world with dimensions 1600x1200

# Create radar display
radar = Radar(400, -200, 200, 200)  # Position radar at (400, -200) with size 200x200

# Create the player
player = Player()

# Create the camera
camera = Camera(player.x, player.y)  # Initialize camera at player position

# Create missile pool
missiles = []
for _ in range(30):  # Create 30 reusable missiles
    missiles.append(Missile(0.0, 0.0))

# Create enemies
enemies = []
for _ in range(25):  # Create 25 enemies
    enemies.append(Enemy(0.0, 0.0))
    
# Initialize enemy positions and velocities
for enemy in enemies:
    x = random.randint(-game.width/2.0, game.width/2.0)
    y = random.randint(-game.height/2.0, game.height/2.0)
    dx = random.randint(0, 10) / 20.0
    dy = random.randint(0, 10) / 20.0
    enemy.x = x
    enemy.y = y
    enemy.dx = dx
    enemy.dy = dy

# Create background stars
stars = []    
for _ in range(20):  # Create 20 background stars
    x = random.randint(int(-game.width/4.0), int(game.width/4.0))
    y = random.randint(int(-game.height/4.0), int(game.height/4.0))
    stars.append(Star(x, y))

# Create power-ups
powerups = []
for _ in range(5):  # Create 5 power-ups
    x = random.randint(-game.width/2.0, game.width/2.0)
    y = random.randint(-game.height/2.0, game.height/2.0)
    powerups.append(Powerup(x, y))

# Create special effects
explosion = Explosion(30)  # Explosion effect with 30 particles
exhaust = Exhaust(20)     # Exhaust effect with 20 particles

# Create sprite lists for rendering
sprites = []          # Main sprite list
background_sprites = []  # Background sprite list

# Add sprites to appropriate lists
for star in stars:
    background_sprites.append(star)
    
for powerup in powerups:
    sprites.append(powerup)

for missile in missiles:
    sprites.append(missile)

for enemy in enemies:
    sprites.append(enemy)

sprites.append(player)

# Keyboard bindings
wn.listen()

# Player movement controls
wn.onkeypress(player.rotate_left, "Left")     # Rotate left with left arrow
wn.onkeyrelease(player.stop_rotation, "Left")

wn.onkeypress(player.rotate_right, "Right")   # Rotate right with right arrow
wn.onkeyrelease(player.stop_rotation, "Right")

wn.onkeypress(player.accelerate, "Up")        # Accelerate with up arrow
wn.onkeyrelease(player.decelerate, "Up")

wn.onkeypress(player.fire, "space")           # Fire missiles with spacebar

# Game settings controls
wn.onkeypress(camera.toggle_visibility, "c")  # Toggle camera with C key
wn.onkeypress(camera.toggle_visibility, "C")

wn.onkeypress(game.start_game, "s")          # Start game with S key
wn.onkeypress(game.start_game, "S")

wn.onkeypress(game.toggle_pause, "p")        # Pause game with P key
wn.onkeypress(game.toggle_pause, "P")

def timer(game=game):
    """
    FPS counter update function
    Prints current frame rate every second
    """
    os.system("clear")
    print("FPS: {}".format(game.frame))
    game.frame = 0
    turtle.ontimer(timer, 1000)

# Start FPS counter
turtle.ontimer(timer, 1000)

# Main game loop
while True:
    # Handle splash screen
    if game.state == "splash":
        wn.update()
        continue
        
    # Main game update
    if game.state == "playing":
        game.frame += 1
        
        # Update and render effects
        explosion.render(pen, camera.x, camera.y)
        exhaust.render(pen, camera.x, camera.y)
        
        # Update and render background
        for sprite in background_sprites:
            sprite.update()
            if Sprite.is_on_screen(sprite, SCREEN_WIDTH, SCREEN_HEIGHT, player.x, player.y):
                sprite.render(pen, camera.x+100, camera.y)
        
        # Update and render game sprites
        for sprite in sprites:
            if sprite.state == "active":
                sprite.update()
                if Sprite.is_on_screen(sprite, SCREEN_WIDTH, SCREEN_HEIGHT, player.x, player.y):
                    sprite.render(pen, camera.x+100, camera.y)
        
        # Count active enemies
        active_enemies = 0
            
        # Check for collisions
        for sprite in sprites:
            # Check if sprite is active
            if sprite.state == "active":
                # Handle enemy collisions
                if isinstance(sprite, Enemy):
                    active_enemies += 1
                    
                    # Player collides with enemy
                    if Sprite.is_collision(player, sprite, 18.0):
                        # Create explosion effect
                        center_x = (player.x + sprite.x) / 2.0
                        center_y = (player.y + sprite.y) / 2.0
                        explosion.explode(center_x-100, center_y) 
                        
                        # Handle collision physics and damage                           
                        player.bounce(sprite)
                        
                        # Check for player death
                        if player.health <= 0:
                            player.reset()
                            player.lives -= 1
                            if player.lives == 0:
                                print("GAME OVER")
                        else:
                            # Apply damage to both player and enemy
                            if sprite.health > 0:
                                player.health -= random.randint(int(sprite.health / 2.0), int(sprite.health))
                            if player.health > 0:
                                sprite.health -= random.randint(int(player.health / 2.0), int(player.health))
                            if sprite.health <= 0:
                                sprite.state = "inactive"

                    # Missile collides with enemy
                    for missile in missiles:
                        if missile.state == "active":
                            if Sprite.is_collision(missile, sprite, 13.0):
                                # Apply damage and knockback
                                sprite.health -= missile.damage
                                sprite.dx += missile.dx / 3.0
                                sprite.dy += missile.dy / 3.0
                                if sprite.health <= 0:
                                    sprite.state = "inactive"
                                    player.score += 10
                                
                                # Create explosion effect
                                explosion.explode(missile.x-100, missile.y, -missile.dx, -missile.dy) 
                                missile.reset()

                # Handle power-up collisions
                if isinstance(sprite, Powerup):
                    # Missile hits power-up
                    for missile in missiles:
                        if missile.state == "active":
                            if Sprite.is_collision(missile, sprite, 13):
                                play_sound("explosion.wav")
                                sprite.state = "inactive"
                                player.score -= 50
                                
                                explosion.explode(missile.x-100, missile.y, -missile.dx, -missile.dy)
                                missile.reset()
                            
                    # Player collects power-up
                    if Sprite.is_collision(player, sprite, 18):
                        play_sound("powerup.wav")
                        sprite.state = "inactive"
                        
                        # Add new missile and upgrade all missiles
                        missiles.append(Missile(0, 0))
                        missiles[-1].max_fuel = missiles[0].max_fuel
                        missiles[-1].thrust = missiles[0].thrust
                        sprites.append(missiles[-1])
                        for missile in missiles:
                            missile.max_fuel *= 1.1   # Increase fuel capacity by 10%
                            missile.thrust *= 1.05    # Increase speed by 5%
                            missile.damage *= 1.1     # Increase damage by 10%
        
        # Render game elements
        game.render_border(pen, camera.x+100, camera.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        game.render_info(pen, player.score, active_enemies)
        radar.render(pen, sprites)
        
        # Update and render camera
        camera.update(player)
        camera.render(pen)
        
        # Update screen
        wn.update()
        pen.clear()

# wn.mainloop()  # Not needed with custom game loop

