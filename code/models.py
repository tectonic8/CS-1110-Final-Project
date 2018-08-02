"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special class
forit.  Unless you need something special for your extra gameplay features, Ship
and Aliens could just be an instance of GImage that you move across the screen.
You only need a new class when you add extra features to an object. So
technically Bolt, which has a velocity, is really the only model that needs to
have its own class.

The collides methods in Ship and Boss require that I check if each of the points
of the new rotated Bolts (my extension) are in the image. To learn the math for
rotating points about a center, I looked at https://gamedev.stackexchange.com/qu
estions/86755/how-to-calculate-corner-positions-marks-of-a-rotated-tilted-rectan
gle
No code was copied, I just needed the formulas.

Hartek Sabharwal hs786
3 Dec 2017
"""
from consts import *
from game2d import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py. If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship
    just means changing the x attribute (which you can do directly), you want to
    prevent the player from moving the ship offscreen.  This is an ideal thing
    to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not
    require this.  You could put this method in Wave if you wanted to.  But the
    advantage of putting it here is that Ships and Aliens collide with different
    bolts.  Ships collide with Alien bolts, not Ship bolts.  And Aliens collide
    with Ship bolts, not Alien bolts. An easy way to keep this straight is for
    this class to have its own collision method.
    
    However, there is no need for any more attributes other than those inherited
    by GImage. You would only add attributes if you needed them for extra
    gameplay features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _velocity:  the number of pixels the ship moves per update
                    [int or float >= 0]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x coordinate of the middle of the ship image.
        """
        return self.x
    
    def setX(self,x):
        """
        Sets the x coordinate of the middle of the ship image.
        
        If x is lower than the left bound (SHIP_WIDTH//2) or greater than the
        right bound (GAME_WIDTH-SHIP_WIDTH//2), it sets it to those positions
        instead to prevent the ship from leaving the screen.
        
        Parameter x: the x coordinate to set the middle of the ship image to
        Precondition: x is any number (int or float)
        """
        position = max(SHIP_WIDTH//2, x)
        self.x = min(GAME_WIDTH-SHIP_WIDTH//2, position)
    
    def getVelocity(self):
        """
        Returns the _velocity attribute of the ship object. 
        """
        return self._velocity
    
    def setVelocity(self, velocity):
        """
        Sets the _velocity attribute of the ship object.
        
        If the velocity is a small number, it is rounded to zero to prevent
        weird float math making it constantly moving when it should come to a
        stop.
        
        Parameter velocity: the number of pixels the ship should move every
                            update.
        Precondition: velocity is a number (int or float)
        """
        if abs(velocity) < min(SHIP_DECELERATION, SHIP_ACCELERATION):
            self._velocity = 0
        else:
            self._velocity = velocity
            
    def getAngle(self):
        """
        Returns the angle attribute inherent in GObjects.
        """
        return self.angle
    
    def setAngle(self, angle):
        """
        Sets the angle attribute of the ship object.
        
        Parameter:  angle is the angle of rotation about the center, measured in
                    degrees counter-clockwise
        Precondition: angle is a number (int or float)
        """
        self.angle = angle
        
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Initializes the ship object and its velocity.
        
        The ship object is initialized using the GImage initializer with the
        default values for its width and height given in consts.py. The position
        is set to the middle, SHIP_BOTTOM away from the bottom of the screen.
        _velocity is set to 0.
        """
        super().__init__(x=GAME_WIDTH//2, y=SHIP_BOTTOM + SHIP_HEIGHT//2,
                         width=SHIP_WIDTH, height=SHIP_HEIGHT,
                         source = "ship.png")
        self._velocity = 0
        
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this
        alien
        
        Uses formulas learned from https://gamedev.stackexchange.com/questions/8
        6755/how-to-calculate-corner-positions-marks-of-a-rotated-tilted-rectang
        le
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        for n in [[0,0],[0,1],[1,0],[1,1]]: #This checks all 4 corners
            if bolt.getxVelocity() != 0: #does the math for a tilted bolt
                x = -BOLT_WIDTH/2+BOLT_WIDTH*n[0]
                y = -BOLT_HEIGHT/2+BOLT_HEIGHT*n[1]
                angle = math.atan(bolt.getyVelocity()/bolt.getxVelocity())
                rotatedX = (x*math.cos(angle) - y*math.sin(angle))+bolt.getX()
                rotatedY = (x*math.sin(angle) - y*math.cos(angle))+bolt.getY()
                if self.contains(tuple([rotatedX,
                                        rotatedY])) and bolt.getyVelocity()<0:
                    return True
            else:
                if self.contains(tuple([bolt.getX()-BOLT_WIDTH/2 + \
                                        BOLT_WIDTH*n[0], bolt.getY() - \
                                        BOLT_HEIGHT/2+BOLT_HEIGHT*n[1]])
                                 ) and bolt.getyVelocity()<0:
                    return True
        return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GSprite):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not
    require this.  You could put this method in Wave if you wanted to.  But the
    advantage of putting it here is that Ships and Aliens collide with different
    bolts.  Ships collide with Alien bolts, not Ship bolts.  And Aliens collide
    with Ship bolts, not Alien bolts. An easy way to keep this straight is for
    this class to have its own collision method.
    
    However, there is no need for any more attributes other than those inherited
    by GImage. You would only add attributes if you needed them for extra
    gameplay features (like giving each alien a score value). If you add
    attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _counter:  counts the number of times a call has been made to setFrame.
                    [int greater than or equal to 0]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x coordinate of the middle of the Alien sprite.
        """
        return self.x
    
    def setX(self,x):
        """
        Sets the x coordinate of the middle of the Alien sprite.
        
        Parameter x: the coordinate to set the middle of the sprite to.
        Precondition: x is a number (int or float)
                      (bounds are managed in wave.py)
        """
        self.x = x
        
    def getY(self):
        """
        Returns the y coordinate of the middle of the Alien sprite.
        """
        return self.y
    
    def setY(self,y):
        """
        Sets the y coordinate of the middle of the Alien sprite.
        
        Parameter y: the coordinate to set the middle of the sprite to.
        Precondition: y is a number (int or float)
                      (bounds are managed in wave.py)
        """
        self.y = min(GAME_HEIGHT-ALIEN_CEILING-ALIEN_HEIGHT//2, y)
    
    def getFrame(self):
        """
        Returns the frame attribute inherent in GSprite objects.
        """
        return self.frame
    
    def setFrame(self, frame):
        """
        Sets the frame attribute of the Alien sprite.
        
        If setting the frame to one of the explosion frames (2 to 5), the
        function actually only changes the frame every third function call. That
        is the purpose of the _counter attribute. It is a cheap way to slow down
        the animation rate of the explosions.
        
        Parameter frame: the frame to set the Alien to
        Precondition: frame is an int between 0 and 5 inclusive.
        """
        self._counter +=1 
        if frame > 1: 
            if (self._counter%EXPLOSION_SPEED == 0):
                self.frame = frame
        else:
            self.frame = frame
        
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, alienType):
        """
        Initializes the Alien as a GSprite object. _counter set to 0.
    
        Parameter x: The x coordinate to put the middle of the Alien at
        Precondition: x is a number (int or float)
        
        Parameter y The y coordinate to put the middle of the Alien at
        Precondition: y is a number (int or float)
        
        Parameter alienType: which of the 3 alien sprites to display
        Precondion: alienType is an int between 0 and 2 inclusive
        """
        super().__init__(x=x, y=y,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,
                         source=ALIEN_STRIP_IMAGES[alienType],format=(3,2))
        self._counter = 0
        
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this
        alien
        
        Uses formulas learned from https://gamedev.stackexchange.com/questions/8
        6755/how-to-calculate-corner-positions-marks-of-a-rotated-tilted-rectang
        le
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        for n in [[0,0],[0,1],[1,0],[1,1]]: #This checks all 4 corners
            if bolt.getxVelocity() != 0:
                x = -BOLT_WIDTH/2+BOLT_WIDTH*n[0]
                y = -BOLT_HEIGHT/2+BOLT_HEIGHT*n[1]
                angle = math.atan(bolt.getyVelocity()/bolt.getxVelocity())
                rotatedX = (x*math.cos(angle) - y*math.sin(angle))+bolt.getX()
                rotatedY = (x*math.sin(angle) - y*math.cos(angle))+bolt.getY()
                if self.contains(tuple([rotatedX,rotatedY])) and \
                                                bolt.getyVelocity()>0:
                    return True
            else:
                if self.contains(tuple([bolt.getX()-BOLT_WIDTH/2 + \
                                        BOLT_WIDTH*n[0], bolt.getY() - \
                                        BOLT_HEIGHT/2+BOLT_HEIGHT*n[1]])
                                 ) and bolt.getyVelocity()>0:
                    return True
        return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because
    we need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the
    starting velocity. This __init__ method will need to call the __init__ from
    GRectangle as a helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt
    by adding the velocity to the y-position.  However, the getter allows Wave
    to do this on its own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _xVelocity: The velocity in x direction (number of pixels to move right
                    each update) [float <= BOLT_SPEED]
        _yVelocity: The velocity in y direction (number of pixels to move up
                    each update) [float <=  BOLT_SPEED]

    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getxVelocity(self):
        """
        Returns the x component of the velocity of the bolt.
        """
        return self._xVelocity
    
    def getyVelocity(self):
        """
        Returns the y component of the velocity of the bolt.
        """
        return self._yVelocity
    
    def getY(self):
        """
        Returns the y coordinate of the middle of the bolt.
        """
        return self.y
    
    def getX(self):
        """
        Returns the x coordinate of the middle of the bolt.
        """
        return self.x
    
    def setY(self,y):
        """
        Sets the y coordinate of the middle of the bolt.
        
        Parameter y: The y coordinate to put the middle of the bolt at
        Precondition: y is a number (int or float)
        """
        self.y = y
        
    def setX(self,x):
        """
        Sets the x coordinate of the middle of the bolts.
        
        Parameter x: The x coordinate to put the middle of the bolt at
        Precondition: x is a number (int or float)
        """
        self.x = x
        
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y, xVelocity, yVelocity, rotation):
        """
        Initiates a bolt as a black GRectangle with set x and y velocity and
        rotation.
        
        Parameter xVelocity: number of pixels to move horizontally every update
        Precondition: xVelocity is a number (int or float)
        
        Parameter yVelocity: number of pixels to move vertically every update
        Precondition: yVelocity is a number (int or float)
        
        Parameter rotation: the angle of rotation of the bolt, measured in
                            degrees counterclockwise
        Precondition: angle is number (int or float)
        """
        super().__init__(x=x,y=y,width=BOLT_WIDTH,height=BOLT_HEIGHT,
                         fillcolor='black',linecolor="black", angle=rotation)
        self._xVelocity = xVelocity
        self._yVelocity = yVelocity
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class Boss(Alien):
    """
    A class representing the Boss alien.
    
    Extends the alien class. The only difference is the different dimensions
    of the boss image. No unique attributes.
    """ 
    def __init__(self, x, y):
        """
        Initializes the Boss using the GSprite initializer and the boss image
        dimensions.
        
        Parameter x: The x coordinate to put the middle of the Boss at
        Precondition: x is a number (int or float)
        
        Parameter y: The y coordinate to put the middle of the Alien at
        Precondition: y is a number (int or float)
        """
        super(Alien, self).__init__(x=x,y=y,width=BOSS_WIDTH,height=BOSS_HEIGHT,
                         source=ALIEN_STRIP_IMAGES[3])