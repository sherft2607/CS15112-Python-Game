from cmu_graphics import *
import math
import random

class InstructionScreen:
    def redrawAll(self, app):
        drawRect(0, 0, app.width, app.height, fill='lightyellow', border=None)
        drawLabel("Instructions", app.width / 2, 15, size=14, fill='black')  # Adjusted y-coordinate and font size
        
        instructions = [
            "Objective: Navigate the bird, collect seeds, and avoid obstacles.",
            "Movement:",
            "- Up arrow: Jump",
            "- Down arrow: Move down",
            "- Left arrow: Move left",
            "- Right arrow: Move right",
            "Collecting Seeds:",
            "- Move the bird over seeds to collect them.",
            "- Seed counter is displayed at the top right.",
            "Obstacles:",
            "- Red obstacles move horizontally and reduce health on collision.",
            "- Avoid collisions to maintain health.",
            "Pause/Resume:",
            "- Press 'p' to pause or resume the game.",
            "Level Completion:",
            "- Reach the top of the screen to complete the level.",
            "- Each level increases in difficulty.",
            "Game Over/Restart:",
            "- Restart level if health reaches zero.",
            "- Press Space on Start Screen to restart the game.",
            "",
            "Good luck on your adventure!"
        ]

        y_offset = 40
        for instruction in instructions:
            drawLabel(instruction, app.width / 2, y_offset, align='center', size=12, fill='black')  # Adjusted y-coordinate and font size
            y_offset += 15

class StartScreen:
    def __init__(self):
        self.spacePressed = False

    def draw(self):
        drawRect(0, 0, 400, 400, fill='lightblue', border=None)
        drawLabel("Press Space to Start", 200, 200, size=20, fill='black')

    def onKeyPress(self, app, key):
        if key == 'space':
            self.spacePressed = True

    def isSpacePressed(self):
        return self.spacePressed

class RestartButton:
    def __init__(self, app):
        self.app = app
        self.buttonRect = (60, 20, 50, 40)  # (x, y, width, height)

    def draw(self):
        drawRect(*self.buttonRect, fill='gray')
        drawLabel("Restart", self.buttonRect[0] + self.buttonRect[2] // 2, self.buttonRect[1] + self.buttonRect[3] // 2, size=8, fill='white')
        drawRect(10,20,100,40, border='black', fill=None)

    def isClicked(self, mouseX, mouseY):
        # Check if the mouse click is within the button boundaries
        x, y, width, height = self.buttonRect
        return x <= mouseX <= x + width and y <= mouseY <= y + height


# Add the RestartButton instance to the app
app.restartButton = RestartButton(app)

class PauseButton:
    def __init__(self, app):
        self.app = app
        self.buttonRect = (10, 20, 50, 40)  # (x, y, width, height)

    def draw(self):
        drawRect(*self.buttonRect, fill='gray')
        drawLabel("Pause", self.buttonRect[0] + self.buttonRect[2] // 2, self.buttonRect[1] + self.buttonRect[3] // 2, size=8, fill='white')
        drawLine(60,20,60,60)
        

    def isClicked(self, mouseX, mouseY):
        # Check if the mouse click is within the button boundaries
        x, y, width, height = self.buttonRect
        return x <= mouseX <= x + width and y <= mouseY <= y + height

class LevelScreen:
    def __init__(self, level):
        self.level = level
        self.blockPositions = []
        self.buttonRect = (150, 250, 100, 50)  # (x, y, width, height)

    def draw(self):
        drawRect(0, 0, 400, 400, fill='lightgreen', border=None)
        drawLabel(f"Level {self.level}", 200, 200, size=20, fill='black')

        # Draw the button
        drawRect(*self.buttonRect, fill='blue', border='black')
        drawLabel("Start Level", self.buttonRect[0] + self.buttonRect[2] // 2, self.buttonRect[1] + self.buttonRect[3] // 2, size=12, fill='white')

    def isButtonClicked(self, mouseX, mouseY):
        # Check if the mouse click is within the button boundaries
        x, y, width, height = self.buttonRect
        return x <= mouseX <= x + width and y <= mouseY <= y + height

class Level2Screen:
    def __init__(self):
        self.buttonRect = (150, 250, 100, 50)  # (x, y, width, height)
        self.speed = 10  # Adjust the speed value for Level 2
        self.blockPositions = [
            (100, 280), (250, 240), (380, 280),
            (100, 120), (250, 80), (380, 120)
        ]

    def draw(self):
        drawRect(0, 0, 400, 400, fill='lightblue', border=None)
        drawLabel("Level 2", 200, 200, size=20, fill='black')

        # Draw the start screen elements without scrolling
        drawRect(*self.buttonRect, fill='blue', border='black')
        drawLabel("Start Level", self.buttonRect[0] + self.buttonRect[2] // 2, self.buttonRect[1] + self.buttonRect[3] // 2, size=12, fill='white')

    def isButtonClicked(self, mouseX, mouseY):
        # Check if the mouse click is within the button boundaries
        x, y, width, height = self.buttonRect
        return x <= mouseX <= x + width and y <= mouseY <= y + height




class PauseScreen:
    def __init__(self):
        pass

    def draw(self):
        drawRect(0, 0, 400, 400, fill='darkgray', border=None)
        drawLabel("Game Paused", 200, 200, size=20, fill='white')

class LevelEndScreen:
    def draw(self):
        drawRect(0, 0, 400, 400, fill='purple', border=None)
        drawLabel("Level Completed!", 200, 150, size=20, fill='white')
        drawLabel("Press Space to Continue", 200, 200, size=15, fill='white')

class Bird:
    def __init__(self, x, y, app):
        self.x = x
        self.y = y
        self.originalY = y
        self.radius = 20
        self.speed = 30
        self.jumpForce = 15  # New variable for jump force
        self.jumpDuration = 10  # Adjust the jump duration
        self.jumpFrames = 0  # Variable to keep track of frames during jump
        self.jumpHeight = 15  # Default jump height
        self.originalJumpHeight = 15  # Original jump height
        self.seedCounter = 0
        self.health = 3
        self.collectedSeeds = []
        self.onBlock = False 
        self.collisionDetected = False
        self.paused = False
        self.app = app

    def draw(self):
        Landscape.drawSky()
        Landscape.drawClouds()
        Landscape.drawTrees()
        Landscape.drawGround()
        self.drawBird()
        self.drawSeeds()
        Landscape.drawSeedCounter(self.seedCounter, self.health)

    def jump(self):
        if not self.checkBlockCollision() and not self.paused:
            if self.jumpFrames < self.jumpDuration:
                self.y -= self.jumpHeight
                self.jumpFrames += 1
            else:
                self.jumpFrames = 0

    def fall(self):
        if not self.onBlock and not self.paused:
            newY = self.y + self.speed
            self.y = min(newY, 300)
        else:
            self.onBlock = False  
    

    def moveDown(self, moveHeight=50):
        if self.y + moveHeight < 300 and not self.paused:
            self.y += moveHeight

    def moveLeft(self):
        if not self.paused:
            self.x -= self.speed
            self.checkBounds()
            self.checkSeedCollision()
            self.checkObstacleCollision()

    def moveRight(self):
        if not self.paused:
            self.x += self.speed
            self.checkBounds()
            self.checkSeedCollision()
            self.checkObstacleCollision()

    def checkBounds(self):
        if self.x - self.radius < 0:
            self.x = self.radius
        elif self.x + self.radius > 400:
            self.x = 400 - self.radius

    def resetPosition(self):
        self.x = 50
        self.y = self.originalY
        self.seedCounter = 0
        self.collectedSeeds = []  
    
    def resetSeeds(self):
        seedPositions = [(100, 310), (250, 310), (380, 310)]
        self.collectedSeeds = []

    def collectSeed(self, seedPosition):
        if seedPosition not in self.collectedSeeds:
            self.seedCounter += 1
            self.collectedSeeds.append(seedPosition)

    def checkSeedCollision(self):
        seedPositions = []

        # Adjust seed positions to be on top of blocks
        for block in self.app.blocks:
            seedPositions.append((block.x + block.width // 2, block.y - 20))

        seeds_to_draw = []  # Keep track of seeds to draw

        for seedPosition in seedPositions:
            seedX, seedY = seedPosition
            if seedPosition not in self.collectedSeeds:
                if math.sqrt((seedX - self.x) ** 2 + (seedY - self.y) ** 2) <= self.radius + 10:
                    self.collectSeed(seedPosition)
                    seeds_to_draw.append(seedPosition)

        return seeds_to_draw  # Return seeds to draw



    def checkBlockCollision(self):
        for block in self.app.blocks:
            if (
                self.x - self.radius < block.x + block.width
                and self.x + self.radius > block.x
                and self.y + self.radius > block.y
                and self.y - self.radius < block.y + block.height
            ):
                if self.y < block.y - self.radius or not self.onBlock:
                    self.onBlock = True
                    self.y = block.y - self.radius
                    return True
        self.onBlock = False
        return False

    def checkObstacleCollision(self):
        if not self.collisionDetected:
            if (
                self.x - self.radius < self.app.obstacle.x + self.app.obstacle.radius
                and self.x + self.radius > self.app.obstacle.x - self.app.obstacle.radius
                and self.y - self.radius < self.app.obstacle.y + self.app.obstacle.radius
                and self.y + self.radius > self.app.obstacle.y - self.app.obstacle.radius
            ):
                self.health -= 1
                self.collisionDetected = True
                if self.health <= 0:
                    self.resetPosition()
                    self.resetSeeds()
                    self.health = 3
        else:
            self.collisionDetected = False

    def drawBird(self):
        drawCircle(self.x, self.y, 20, fill='yellow', border='black')

    def drawSeeds(self):
        seedPositions = []

        # Adjust seed positions to be on top of blocks
        for block in self.app.blocks:
            seedPositions.append((block.x + block.width // 2, block.y - 20))

        for seedPosition in seedPositions:
            if seedPosition not in self.collectedSeeds:
                drawCircle(seedPosition[0], seedPosition[1], 10, fill='orange', border="black")

class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill='antiqueWhite', border='black')

class Landscape:
    @staticmethod
    def drawClouds(scroll_speed=0):
        cloudColor = 'gainsboro'
        cloudPositions = [(50, 100), (200, 150), (350, 100)]  # Set fixed cloud positions

        for x, y in cloudPositions:
            drawCircle(x, y - scroll_speed, 30, fill=cloudColor, border=None, opacity=40)
            drawCircle(x + 40, y - scroll_speed, 30, fill=cloudColor, border=None, opacity=40)
            drawCircle(x + 80, y - scroll_speed, 30, fill=cloudColor, border=None, opacity=40)
    

    @staticmethod
    def drawSky():
        drawRect(0, 0, 400, 400, fill='lightblue', border=None)

    @staticmethod
    def drawGround(scroll_speed=0):
        drawRect(0, 320 - scroll_speed, 400, 100, fill='green')
        drawLine(0, 320 - scroll_speed, 400, 320 - scroll_speed)

        x1, y1, x2, y2 = 20, 320 - scroll_speed, 0, 400 - scroll_speed
        while x1 <= 400:
            drawLine(x1, y1, x2, y2, fill='black', opacity=30)
            x1 += 20
            x2 += 20

    @staticmethod
    def drawTrees(scroll_speed=0):
        treeColor = 'lightgreen'

        drawRect(40, 250 - scroll_speed, 20, 100, fill='brown', border="black")
        drawRect(185, 250 - scroll_speed, 20, 100, fill='brown', border="black")
        drawRect(335, 250 - scroll_speed, 20, 100, fill='brown', border="black")

        drawRegularPolygon(50, 250 - scroll_speed, 50, 3, fill=treeColor, border="black")
        drawRegularPolygon(195, 250 - scroll_speed, 50, 3, fill=treeColor, border="black")
        drawRegularPolygon(345, 250 - scroll_speed, 50, 3, fill=treeColor, border="black")

    @staticmethod
    def drawSeedCounter(seedCounter, health):
        drawRect(300, 20, 80, 40, fill='white', border='black')
        drawLabel(f'Seeds: {seedCounter} Health: {health}', 340, 40, align='center', size=8, fill='black')
        

class Obstacle:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 1  # Adjust the speed value to reduce the obstacle's movement speed

    def move(self):
        self.x += self.speed
        if self.x >= 400 - self.radius:
            self.x = 400 - self.radius
            self.speed = -self.speed
        elif self.x <= self.radius:
            self.x = self.radius
            self.speed = -self.speed

    def draw(self):
        drawCircle(self.x, self.y, self.radius, fill='red', border='black')
        

def onKeyPress(app, key):
    if not app.gameStarted:
        if key == 'space':
            app.gameStarted = True
            app.startScreen = None  # Dismiss the start screen
            app.instructionScreen = InstructionScreen()  # Display the instruction screen
            return
        elif key == 'c' and app.showContinueScreen:
            # Transition to Level 2 when 'C' is pressed after completing a level
            app.showContinueScreen = False
            app.levelScreen = Level2Screen()
            app.gameStarted = True

            # Update the jump height and obstacle speed for Level 2
            app.bird.jumpHeight = 100
            app.obstacle.speed = app.levelScreen.speed

        elif key == 'q' and app.showContinueScreen:
            # Restart the game and bring the player back to the Start Screen when 'Q' is pressed
            app.showContinueScreen = False
            app.startScreen = StartScreen()
            app.gameStarted = False
            app.levelScreen = None
            app.currentLevel = 1
            app.bird.resetPosition()
            app.bird.resetSeeds()
            app.bird.health = 3
    elif app.instructionScreen:
        # Proceed to the game when any key is pressed on the instruction screen
        app.instructionScreen = None
    elif app.levelScreen:
        # Proceed to the next level or game when any key is pressed on the level screen
        app.levelScreen = None
        app.gameStarted = True
    elif app.bird.paused:
        if key == 'p':
            app.bird.paused = not app.bird.paused
    else:
        if key == 'up':
            app.bird.jump()
        elif key == 'down':
            app.bird.moveDown()
        elif key == 'left':
            app.bird.moveLeft()
        elif key == 'right':
            app.bird.moveRight()
        elif key == 'p':
            app.bird.paused = not app.bird.paused



def onMousePress(app, mouseX, mouseY):
    if app.startScreen and app.startScreen.isSpacePressed():
        # Start the game when Space is pressed on the Start Screen
        app.startScreen = None
        app.gameStarted = True

    elif app.levelScreen and app.levelScreen.isButtonClicked(mouseX, mouseY):
        # Start the selected level when the button is clicked on the Level Screen
        app.levelScreen = None
        app.gameStarted = True

    elif app.pauseButton.isClicked(mouseX, mouseY):
        # Go to the pause screen when the pause button is clicked
        app.bird.paused = True

    elif app.restartButton.isClicked(mouseX, mouseY):
        # Restart the level when the restart button is clicked
        app.bird.resetPosition()
        app.bird.resetSeeds()
        app.bird.health = 3
        app.levelScreen = None
        app.gameStarted = True
   
def onKeyRelease(app, key):
    if key in {'up', 'down'}:
        app.bird.fall()

cooldownFrames = 0

def onStep(app):
    if not app.gameStarted:
        return

    if app.bird.paused:
        return

    if app.levelScreen:
        # Check for level completion (you can customize this based on your game logic)
        if app.bird.y <= 0:
            app.currentLevel += 1
            if app.currentLevel == 2:
                app.levelScreen = Level2Screen()
            elif app.currentLevel <= 3:  # Assuming there are 3 levels
                app.levelScreen = LevelScreen(app.currentLevel)
            else:
                app.gameStarted = False
                app.levelScreen = None
                app.currentLevel = 1
                app.bird.resetPosition()
                app.bird.resetSeeds()
                app.bird.health = 3
            return

    app.obstacle.move()

    # Check if app.levelScreen is not None before accessing its properties
    if app.levelScreen and app.levelScreen.blockPositions:
        # Create blocks based on the blockPositions
        app.blocks = [Block(x, y, 50, 10) for x, y in app.levelScreen.blockPositions]

    # Check for collision with obstacle
    if (
        app.bird.x - app.bird.radius < app.obstacle.x + app.obstacle.radius
        and app.bird.x + app.bird.radius > app.obstacle.x - app.obstacle.radius
        and app.bird.y - app.bird.radius < app.obstacle.y + app.obstacle.radius
        and app.bird.y + app.bird.radius > app.obstacle.y - app.obstacle.radius
    ):
        if not app.bird.collisionDetected:
            app.bird.health -= 1
            app.bird.collisionDetected = True
            if app.bird.health == 0:
                # Perform actions when the bird dies
                print("Bird has died!")
                # You can add more actions here, such as resetting the game or showing a game-over screen.
                app.bird.resetPosition()
                app.bird.resetSeeds()
                app.bird.health = 3
    else:
        app.bird.collisionDetected = False

    # Check for collision with seeds
    seeds_to_draw = app.bird.checkSeedCollision()

    # Check if all seeds are collected
    if len(app.bird.collectedSeeds) == 9:
        # Transition to the level end screen
        app.levelScreen = None
        app.gameStarted = False
        app.bird.resetPosition()
        app.bird.resetSeeds()
        app.bird.health = 3
        app.showContinueScreen = True


def redrawAll(app):
    if not app.gameStarted:
        if app.showContinueScreen:
            # Display continue screen after completing a level
            # Provide options for the player to continue or quit
            drawRect(0, 0, app.width, app.height, fill='lightblue', border=None)
            drawLabel("Level Completed!", app.width / 2, 150, size=20, fill='white')
            drawLabel("Press 'C' to Continue or 'Q' to Quit", app.width / 2, 200, size=15, fill='white')
        else:
            app.startScreen.draw()
    elif app.instructionScreen:
        app.instructionScreen.redrawAll(app)
    elif app.levelScreen:
        app.levelScreen.draw()
    elif app.bird.paused:
        app.pauseScreen.draw()
    else:
        # Existing code for drawing game elements
        Landscape.drawSky()
        Landscape.drawClouds()
        app.bird.draw()
        app.obstacle.draw()
        for block in app.blocks:
            block.draw()

        # Draw the seeds
        seeds_to_draw = app.bird.checkSeedCollision()
        for seedPosition in seeds_to_draw:
            seedX, seedY = seedPosition
            drawCircle(seedX, seedY, 10, fill='orange', border="black")

        # Draw the pause button
        app.pauseButton.draw()

        # Draw the restart button
        app.restartButton.draw()



if __name__ == "__main__":
    app.bird = Bird(50, 300, None)
    app.obstacle = Obstacle(200, 225, 30, 5)
    app.startScreen = StartScreen()
    app.pauseScreen = PauseScreen()
    app.pauseButton = PauseButton(app)
    app.gameStarted = False
    app.levelScreen = None
    app.instructionScreen = InstructionScreen()  # Added instruction screen instance
    app.currentLevel = 1  # Start at level 1
    app.showContinueScreen = False

    # Add more blocks vertically
    blockPositions = [
        (100, 280), (250, 240), (380, 280),
        (100, 200), (250, 160), (380, 200),
        (100, 120), (250, 80), (380, 120)
    ]

    app.blocks = [Block(x, y, 50, 10) for x, y in blockPositions]

    app.bird.app = app
    


    runApp(width=400, height=400, onMousePress=onMousePress, onKeyDown=onKeyPress, onKeyUp=onKeyRelease, onStep=onStep, redrawAll=redrawAll)

