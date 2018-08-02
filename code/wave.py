"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the
Alien Invaders game.  Instances of Wave represent a single wave.  Whenever you
move to new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen.  These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue.  If you do not know, ask on Piazza and we will answer.

I wrote the parametric equation that models the boss movement (function
__bossController) after looking at some graphs on http://jwilson.coe.uga.edu/EMA
T6680Fa05/Parveen/Assignment%2010/parametric_equations.htm
No code was copied, and the idea was my own.

I wrote the code for making sure that the bolt comes out of the new rotated
tip of the ship (__boltController) after learning the math for rotating points
about a center from https://gamedev.stackexchange.com/questions/86755/how-to-cal
culate-corner-positions-marks-of-a-rotated-tilted-rectangle
No code was copied, I just needed the formulas.

Hartek Sabharwal hs786
3 Dec 2017
"""
from game2d import *
from consts import *
from models import *
import random
import math

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary. It
    also marches the aliens back and forth across the screen until they are all
    destroyed or they reach the defense line (at which point the player loses).
    When the wave is complete, you should create a NEW instance of Wave (in
    Invaders) if you want to make a new wave of aliens.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This class
    will be similar tothat one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave
                 [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen
                 [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in class Invaders. It is okay if you do, but you
    MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter
    for any attribute that you need to access in Invaders.  Only add the getters
    and setters that you need for Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may
    want to keep track of the score.  You also might want some label objects to
    display the score and number of lives. If you make changes, please list the
    changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _alienDirection:    the direction the aliens are traveling in
                    [int 1 if moving right, int -1 if moving left]
        _stepsUntilFire:    the number of steps until the aliens fire
                    [random integer between 1 and BOLT_RATE]
        _waveState:         the current state of the game represented as a value
                            from consts.py
                    [one of IN_PROGRESS, WAVE_WON, WAVE_LOST]
        _exploded:          1d list of aliens that were killed by a bolt and are
                            now going through the 4 explosion animation frames.
                            Removed after the animation.
                    [list of Alien or None]
        _boss:              the boss alien that appears at the end of the wave
                    [Boss type object or None]
        _bossLives:         the number of lives the boss alien has
                    [int between 0 and BOSS_LIVES inclusive]
        _cumulativeTime:    the amount of time since the boss first appeared,
                            divided by BOSS_SPEED
                    [float >= 0]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Returns the number of lives the ship has left.
        """
        return self._lives
    
    def getShipStatus(self):
        """
        Returns whether the player ship is still alive.
        
        True if self._ship if _ship is Ship, False if self._ship is None (which
        occurs when it is hit by a bolt)
        """
        return not (self._ship is None)
    
    def getWaveState(self):
        """
        Returns the attribute _waveState
        """
        return self._waveState
    
    def setShip(self, ship):
        """
        Sets the player ship _ship.
        
        Parameter ship: the player ship to control
        Precondition: ship is a Ship object
        """
        self._ship = ship
        
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the wave with default values for all the attributes.
        
        Also it makes a function call to create the grid of Aliens.
        """
        self._aliens=[]
        self._exploded = []
        self._boss = None
        self.__makeAliens()
        self._ship = Ship()
        self._dline = GPath(points=[START_DEFENSE_LINE,DEFENSE_LINE,
                                    END_DEFENSE_LINE, DEFENSE_LINE],linewidth=1,
                            linecolor="black")
        self._alienDirection = 1
        self._bolts = []
        self._stepsUntilFire = random.randint(1,BOLT_RATE)
        self._lives = SHIP_LIVES
        self._bossLives = BOSS_LIVES
        self._waveState = IN_PROGRESS
        self._time = 0
        self._cumulativeTime = 0
        
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, keyList, dt):
        """
        Animates a single frame of the wave.
        
        It moves the ship according to player inputs (call to __shipHandler),
        marches the aliens across the screen (call to __alienShiftController).
        fires laser bolt from either the ship or an alien (call to
        __boltController), moves any laser bolts across the screen (call to
        __boltController), and resolves any collisions with a laser bolt (call
        to __collisionHanlder). Also animates the explosion sequences and the
        boss.
        
        Parameter keyList: an array holding whether the left key, right key, and
                           space bar is pressed.
        Precondition: keyList is a boolean list of length 3
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        userDirection = 1*keyList[0]-1*keyList[1] 
        if not (self._ship is None):
            self.__shipHandler(userDirection)
        self.__alienShiftController(dt)
        self.__collisionHandler()
        if self.__checkCompletion():
            self._boss = Boss(GAME_WIDTH/2, GAME_HEIGHT+DEFENSE_LINE/2)
        self.__explosionHandler()
        self.__boltController(keyList[2])
        self.__bossController(dt)


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws all the game objects to view.
        
        Draws every alien still alive in _aliens, the ship if it exists, the
        defense line, the boss if the player has gotten to that stage, and the
        bolts in _bolts.
        
        Parameter view: the game view, used in drawing 
        Precondition: instance of GView
        """
        for row in self._aliens:
            for alien in row:
                if not (alien is None):
                    alien.draw(view)
        for alien in self._exploded:
            alien.draw(view)
        if not (self._ship is None):
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)
        if not self._boss is None:
            self._boss.draw(view)
            
    # HELPER METHODS FOR COLLISION DETECTION
    def __makeAliens(self):
        """
        Populates _aliens with the initial grid of aliens.
        
        Makes _aliens a 2d list of ALIEN_ROWS rows and ALIENS_IN_ROW columns of
        Alien objects, with the appropriate starting coordinates and 
        ALIEN_H_SEP separation between each horizontally and ALIEN_V_SEP
        separation betwen each vertically. Also sets the alien types so that
        two rows of each type are made, starting from the bottom to the top.
        """
        self._aliens = []
        for row in range(ALIEN_ROWS):
            self._aliens.append([])
            for column in range(ALIENS_IN_ROW):
                #(int(row/2)%3) figures out alien image from row number.
                self._aliens[row].append(Alien((ALIEN_H_SEP*(column+1) \
                                                + ALIEN_WIDTH*(column+0.5)),
                    (GAME_HEIGHT-ALIEN_CEILING-ALIEN_HEIGHT//2 \
                     -(ALIEN_ROWS-row-1)*(ALIEN_HEIGHT+ALIEN_V_SEP)),
                    (int(row/2)%3)))
                
    def __alienShiftController(self, dt):
        """
        Manages how the aliens shift across the screen.
        
        It finds the leftmost and rightmost Aliens still on the screen and
        passes their location to __handleAlienWalk for it to decide the
        movement. Also, it finds the bottommost Alien and if it is below the
        defense line, it sets the _waveState to WAVE_LOST. Also, it only makes
        the aliens shift when _time >= ALIEN_SPEED, and only lets them fire
        bolts when they shift.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time += dt
        if self._time >= ALIEN_SPEED and self._boss is None:
            leftEdge = GAME_WIDTH
            rightEdge = GAME_LEFT_EDGE
            for row in range(ALIEN_ROWS):
                leftestAlien = None
                rightestAlien = None
                for col in range(ALIENS_IN_ROW):
                    if not self._aliens[row][ALIENS_IN_ROW-1-col] is None:
                        leftestAlien = self._aliens[row][ALIENS_IN_ROW-1-col]
                    if not self._aliens[row][col] is None:
                        rightestAlien = self._aliens[row][col]
                if not leftestAlien is None:
                    leftEdge = min(leftEdge, leftestAlien.getX()-ALIEN_WIDTH//2)
                if not rightestAlien is None:
                    rightEdge=max(rightEdge,rightestAlien.getX()+ALIEN_WIDTH//2) 
            self.__handleAlienWalk(rightEdge, leftEdge)     
            bottommostAlien = None
            for row in range(ALIEN_ROWS):
                for col in range(ALIENS_IN_ROW):
                    if not self._aliens[ALIEN_ROWS-row-1][col] is None:
                        bottommostAlien = self._aliens[ALIEN_ROWS-row-1][col]
            if not bottommostAlien is None and bottommostAlien.getY() \
                                            -ALIEN_HEIGHT/2 < DEFENSE_LINE:
                self._waveState = WAVE_LOST
            self.__alienBoltFire()
            self._time = 0
    
    def __handleAlienWalk(self, rightEdge, leftEdge):
        """
        Decides how to move aliens across the screen.
        
        If the aliens exceed the left or right bounds of the game screen, it
        shifts the aliens down, reverses their direction, and moves them back to
        the bound. Otherwise,it just moves all of them in the current direction.
        
        Parameter rightEdge: the x coordinate of the right edge of the
                             rightmost Alien on the screen.
        Precondition: ridgeEdge is an int or float between ALIEN_WIDTH/2 and
                      GAME_WIDTH
        
        Parameter leftEdge: the x coordinate of the left edge of the
                             leftmost Alien on the screen.
        Precondition: leftEdge is an int or float between 0 and
                      GAME_WIDTH-ALIEN_WIDTH/2
        """
        if rightEdge > (GAME_WIDTH - ALIEN_H_SEP):
                self._alienDirection = -1
                self.__alienShifter(-(rightEdge-(GAME_WIDTH-ALIEN_H_SEP)),
                                    ALIEN_V_SEP)
        elif leftEdge < ALIEN_H_SEP:
            self._alienDirection = 1
            self.__alienShifter(ALIEN_H_SEP - leftEdge, ALIEN_V_SEP)
        else:
            self.__alienShifter(ALIEN_H_WALK*self._alienDirection,0)
                
    def __alienShifter(self,x,y):
        """
        Moves the aliens across the screen and updates the sprite frame.
        
        Parameter x: the horizontal pixel distance to move all the alienns
        Precondition: x is an int or float
        
        Parameter y: the vertical pixel to move all the aliens down (negated)
        Precondition: y is an int or float
        """
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.setX(alien.getX() + x)
                    alien.setY(alien.getY() - y)
                    alien.setFrame((alien.getFrame()+1)%2)
                    
    def __boltController(self, fire):
        """
        Controls when the player fires bolts and deletion of bolts.
        
        Lets the player create a bolt when the spacebar is pressed and there
        isn't already a player bolt on the screen. The function does the math
        so that the bolt travels in the same angle as the player's ship and
        calculates x and y components of velocity so that it moves BOLT_SPEED
        only in its direction. The function also deletes alien bolts that go
        below the game screen, player bolts that go above the game screen or
        past the left and right bounds since my extension of bolts allows that.
        
        The function does the math so that the bolt comes out of the new rotated
        tip of the ship. I learned this math from https://gamedev.stackexchange.
        com/questions/86755/how-to-calculate-corner-positions-marks-of-a-rotated
        -tilted-rectangle
        No code was copied, I just needed the formulas.

        
        Parameter fire: whether the player has pressed/is pressing spacebar
        Precondition: fire is True if spacebar is pressed, False otherwise.
        """
        playerBolt = False
        n = 0
        while n < len(self._bolts):
            if self._bolts[n].getyVelocity()>0:
                playerBolt = True
            self._bolts[n].setY(self._bolts[n].getY() \
                                + self._bolts[n].getyVelocity())
            self._bolts[n].setX(self._bolts[n].getX() \
                                + self._bolts[n].getxVelocity())
            if ((self._bolts[n].getY() - BOLT_HEIGHT/2) > GAME_HEIGHT
                ) or ((self._bolts[n].getY() + BOLT_HEIGHT/2) < 0
                ) or ((self._bolts[n].getX()+BOLT_HEIGHT//2)<0
                ) or ((self._bolts[n].getX()-BOLT_HEIGHT//2)>GAME_WIDTH):
                del self._bolts[n]
                n -= 1
            n += 1
        if fire and (not playerBolt) and (not self._ship is None):
            #Math for rotated coordinates
            angle = math.pi*(self._ship.getAngle())/180
            self._bolts.append(Bolt(-1*(SHIP_HEIGHT//2+BOLT_HEIGHT//2) \
                                    *math.sin(angle)+self._ship.getX(),
                                    (SHIP_HEIGHT//2+BOLT_HEIGHT//2) \
                                    *math.cos(angle)+SHIP_BOTTOM+SHIP_HEIGHT//2,
                                    -BOLT_SPEED*math.cos(math.pi*(
                                        90-self._ship.getAngle())/180),
                                    BOLT_SPEED*math.sin(math.pi*(90-abs(
                                        self._ship.getAngle()))/180),
                                    self._ship.getAngle()))
            
    def __alienBoltFire(self):
        """
        Makes the aliens fire bolts.
        
        Only lets the aliens fire if _stepsUntilFire steps have been made. Then
        it finds all the columns that still have aliens in them. Then it
        randomly chooses one of these columns. Then it finds the bottommost
        Alien in that column and fires a bolt from its location.
        _stepsUntilFire is reset to a new random between 1 and BOLT_RATE.
        """
        self._stepsUntilFire -= 1
        if self._stepsUntilFire == 0:
            nonemptyColumns = []
            for col in range(ALIENS_IN_ROW):
                nonempty = False
                for row in range(ALIEN_ROWS):
                    if not(self._aliens[row][col] is None):
                        nonempty = True
                if nonempty:
                    nonemptyColumns += [col]
            if len(nonemptyColumns) == 0:
                return
            randomColumn = random.choice(nonemptyColumns)
            for row in range(ALIEN_ROWS):
                if (not self._aliens[ALIEN_ROWS-row-1][randomColumn] is None):
                    bottomAlien = self._aliens[ALIEN_ROWS-row-1][randomColumn]
                
            self._bolts.append(Bolt(bottomAlien.getX(),bottomAlien.getY() \
                                    -ALIEN_HEIGHT/2-BOLT_HEIGHT/2,0,
                                    -BOLT_SPEED,0))
            self._stepsUntilFire = random.randint(1,BOLT_RATE)
            
    def __collisionHandler(self):
        """
        Handles collisions of bolts with aliens, player ship, and the Boss.
        
        Checks whether each of the bolts in _bolts has collided with an alien,
        the ship, or the boss. If there is a collision, that bolt is deleted.
        If the collision is with the player or the boss, they lose one of their
        lives. If ship has no lives left, _waveState  is set to WAVE_LOST. If
        the boss has no lives left, _waveState is set to WAVE_WON. Also, only
        bolts made by the player can hurt aliens or the boss, and the vice-
        versa.
        """
        self.__collisionAlienHandler()
        n = 0
        while n < len(self._bolts):
            if (not self._ship is None) and self._ship.collides(self._bolts[n]):
                self._ship = None
                self._lives -= 1
                self._bolts = []
                if self._lives <= 0:
                    self._waveState = WAVE_LOST
            n += 1
        n = 0
        while n < len(self._bolts):
            if (not self._boss is None) and self._boss.collides(self._bolts[n]):
                self._bossLives -= 1
                del self._bolts[n]
                n -= 1
                if self._bossLives <= 0:
                    self._waveState = WAVE_WON
            n += 1
            
    def __collisionAlienHandler(self):
        """
        Handles collisions between player bolts and the aliens, incl. explosions
        
        For each alien in _aliens and each bolts in _bolts, checks that the bolt
        was fired from the player and that it collided with the alien. If so,
        the Alien is set to None, and an exploded Alien animation is added to
        _exploded. The bolt is deleted from the screen.
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                    n = 0
                    while n < len(self._bolts):
                        if (not self._aliens[row][col] is None) and \
                                self._aliens[row][col].collides(self._bolts[n]):
                            self._exploded.append(Alien(
                                self._aliens[row][col].getX(),
                                self._aliens[row][col].getY(),(int(row/2)%3)))
                            self._exploded[-1].setFrame(2)
                            self._aliens[row][col] = None
                            del self._bolts[n]
                            n -= 1
                        n += 1
                        
    def __checkCompletion(self):
        """
        Returns whether the player has defeated every element.
        
        If there are any Aliens in _aliens, it returns False. If everything is
        None, it is True. Does not include the Boss.
        """
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    return False
        return True
        
    def __explosionHandler(self):
        """
        Handles the explosion animation of aliens.
        
        For every exploded alien in _exploded (they are separated because
        exploded aliens shouldn't walk or be able to fire bolts), it updates the
        frame. If the animation sequence is finished, it is deleted. Slowing
        down the animation sequence is done in models.py.
        """
        n = 0
        while n < len(self._exploded):
            currentFrame = self._exploded[n].getFrame()
            if currentFrame < 5:
                self._exploded[n].setFrame(currentFrame+1)
            else:
                del self._exploded[n]
                n -= 1
            n += 1
                
    def __shipHandler(self, userDirection):
        """
        Handles the movement of the ship according to my extension.
        
        The ships moves according to velocity and acceleration instead of a
        constant speed. Pressing the left or right arrow keys adds positive or
        negative velocity. Pressing both means 0 acceleration. There is also a
        constant deceleration SHIP_DECELERATION which moves the absolute value
        of the velocity to 0 to make natural, inertial movement. If the ship
        hits the left or right bounds of the game screen, its velocity is reset
        to 0. Finally, the function also rotates the angle of the ship to agree
        with its velocity, making it look like it's turning.
        
        Parameter userDirection: the direction user input tells the ship to move
        Precondition: userDirection is -1 if to the left, 1 if to the right, or
                      0 if no change.
        """
        if self._ship.getVelocity() > 0:
            decelerationFactor = SHIP_DECELERATION
        elif self._ship.getVelocity() < 0:
            decelerationFactor = -SHIP_DECELERATION
        else:
            decelerationFactor = 0
        self._ship.setVelocity(self._ship.getVelocity() + userDirection*\
                               SHIP_ACCELERATION-decelerationFactor)
        self._ship.setX(self._ship.getX()+self._ship.getVelocity())
        if self._ship.getX()>=GAME_WIDTH-SHIP_WIDTH//2 or \
                                self._ship.getX()<=SHIP_WIDTH//2:
            self._ship.setVelocity(0)
        self._ship.setAngle(self._ship.getVelocity()*-ANGLE_MULTIPLIER)
        
    def __bossController(self, dt):
        """
        Handles movement and bolt firing of the boss.
        
        The boss doesn't move in steps. It moves according to a parametric
        equation to make it look like it's moving somewhat unpredictably and so
        that it moves widely across the screen. _cumulativeTime is used as the
        parameter.
        
        The boss fires bolts when every interval of BOSS_FIRE_RATE. It fires
        volleys of between 1 and 9 bolts. The function does the math so that the
        bolts are equally spaced, rotated the proper angle, and traveling at the
        right x- and y-components of velocity so that BOLT_SPEED is preserved,
        and the math works for any number of bolts.
        
        I wrote this parametric equation after looking at some graphs on
        http://jwilson.coe.uga.edu/EMAT6680Fa05/Parveen/Assignment%2010/parametr
        ic_equations.htm
        No code was copied, and the idea was my own.
        """
        if not self._boss is None:
            self._cumulativeTime += dt/BOSS_SPEED_FACTOR
            #parametric equation for x
            self._boss.setX(GAME_WIDTH/2 + P_X*math.cos(
                P_ALPHA*self._cumulativeTime))
            #parametric equation for y
            self._boss.setY((GAME_HEIGHT+DEFENSE_LINE)/2 + P_Y*math.sin(
                P_BETA*self._cumulativeTime))
            if self._time > BOSS_FIRE_RATE:
                boltsFired = random.randrange(1,9)
                for x in range(boltsFired):
                    angle = math.pi*((x+1)/(boltsFired+1))
                    self._bolts.append(Bolt(self._boss.getX(),
                                            self._boss.getY()-ALIEN_HEIGHT/2,
                                            BOLT_SPEED*math.cos(angle),
                                            -BOLT_SPEED*math.sin(angle),
                                            (DEGREES/2)*(boltsFired-1)/\
                                            (boltsFired+1)-(DEGREES/(
                                                boltsFired+1)*x)))
                self._time = 0
        
        