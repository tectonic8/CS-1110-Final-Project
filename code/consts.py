"""
Constants for Alien Invaders

This module global constants for the game Alien Invaders. These constants need
to be used in the model, the view, and the controller. As these are spread
across multiple modules, we separate the constants into their own module. This
allows all modules to access them.

Hartek Sabharwal hs786
3 Dec 2017
"""
import cornell
import sys

### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display 
GAME_WIDTH  = 800
#: the height of the game display
GAME_HEIGHT = 700


### SHIP CONSTANTS ###

# the width of the ship
SHIP_WIDTH    = 44
# the height of the ship
SHIP_HEIGHT   = 44
# the distance of the (bottom of the) ship from the bottom of the screen
SHIP_BOTTOM   = 32
# The number of pixels to move the ship per update
SHIP_MOVEMENT = 5
# The number of lives a ship has
SHIP_LIVES    = 3

# The y-coordinate of the defensive line the ship is protecting
DEFENSE_LINE = 100


### ALIEN CONSTANTS ###

# the width of an alien
ALIEN_WIDTH   = 33
# the height of an alien
ALIEN_HEIGHT  = 33
# the horizontal separation between aliens
ALIEN_H_SEP   = 16
# the vertical separation between aliens
ALIEN_V_SEP   = 16
# the number of horizontal pixels to move an alien
ALIEN_H_WALK  = ALIEN_WIDTH // 4
# the number of vertical pixels to move an alien
ALIEN_V_WALK  = ALIEN_HEIGHT // 2
# The distance of the top alien from the top of the window
ALIEN_CEILING = 100
# the number of rows of aliens, in range 1..10
ALIEN_ROWS     = 5
# the number of aliens per row
ALIENS_IN_ROW  = 12
# the image files for the aliens (bottom to top)
ALIEN_IMAGES   = ('alien1.png','alien2.png','alien3.png')
# the number of seconds (0 < float <= 1) between alien steps
ALIEN_SPEED = 1.0


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 4
# the height of a laser bolt
BOLT_HEIGHT = 16
# the number of pixels to move the bolt per update
BOLT_SPEED  = 6
# the number of ALIEN STEPS (not frames) between bolts
BOLT_RATE   = 5


### GAME CONSTANTS ###

# state before the game has started
STATE_INACTIVE = 0 
# state when we are initializing a new wave
STATE_NEWWAVE  = 1 
# state when the wave is activated and in play
STATE_ACTIVE   = 2 
# state when we are paused between lives
STATE_PAUSED   = 3
# state when we restoring a destroyed ship
STATE_CONTINUE = 4
#: state when the game is complete (won or lost)
STATE_COMPLETE = 5


### USE COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF ALIENS IN A ROW"""
"""
sys.argv is a list of the command line arguments when you run Python. These
arguments are everything after the word python. So if you start the game typing

    python invaders 3 4 0.5
    
Python puts ['breakout.py', '3', '4', '0.5'] into sys.argv. Below, we take
advantage of this fact to change the constants ALIEN_ROWS, ALIENS_IN_ROW,
and ALIEN_SPEED.
"""
try:
    rows = int(sys.argv[1])
    if rows >= 1 and rows <= 10:
        ALIEN_ROWS = rows
except:
    pass # Use original value

try:
    perrow = int(sys.argv[2])
    if perrow >= 1 and perrow <= 15:
        ALIENS_IN_ROW = perrow
except:
    pass # Use original value

try:
    speed = float(sys.argv[3])
    if speed > 0 and speed <= 3:
        ALIEN_SPEED = speed
except:
    pass # Use original value

### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY ###
#beginning x-coordinate of defense line
START_DEFENSE_LINE=0
#ending x-coordinate of defense line
END_DEFENSE_LINE = 800
#x-coordinate of the left edge of the game screen
GAME_LEFT_EDGE = 0
#state of the wave when the player still lives left and hasn't lost
IN_PROGRESS = 0 
#state of the wave when all the aliens are killed
WAVE_WON  = 1 
#state of the wave when all lives are lost or an alien dips below the defense
#line
WAVE_LOST  = 2
#Message font size for "Game Over" and "You Win" and "Press 'c' to continue"
FONT_SIZE = 30
#filenames of film strips of each type of alien and also the boss image
ALIEN_STRIP_IMAGES  = ('alien-strip1.png','alien-strip2.png','alien-strip3.png',
                       'boss.png')
#Slows down the frame rate of the alien explosion animation by a factor of this
EXPLOSION_SPEED = 3
#Absolute value of speed change of ship every update for which player holds down
#right or left arrow key
SHIP_ACCELERATION = 0.15
#Absolute value of speed decrease of ship every update(allows inertial slow-down)
SHIP_DECELERATION = 0.075
#The angle rotation of the ship is this multiple of its horizontal velocity
ANGLE_MULTIPLIER = 6
#The number of lives of the boss at the end of the wave
BOSS_LIVES = 3
#A value of the parametric equation that controls the boss's movement
P_ALPHA = 7
#A value of the parametric equation that controls the boss's movement
P_BETA = 6
#A multiplier for how much horizontal space the boss moves through on the screen
P_X = 250
#A multiplier for how much vertical space the boss moves through on the screen
P_Y = 150
#A multiplier for how fast the boss moves. There is honestly no easy translation
#between this number and pixels. Higher numbers make it slower.
BOSS_SPEED_FACTOR = 4
#The interval of time between the boss's volleys.
BOSS_FIRE_RATE = 2
#The height of the boss image in pixels
BOSS_HEIGHT = 75
#The width of the boss image in pixels
BOSS_WIDTH = 75
#Half the number of degrees in a circle
DEGREES = 180