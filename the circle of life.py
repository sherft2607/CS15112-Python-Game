from cmu_graphics import *
import math
import random

class InstructionScreen:
    def redrawAll(self, app):
        drawRect(0, 0, app.width, app.height, fill='lightyellow', border=None)
        drawLabel("Instructions", app.width / 2, 25, size=24, fill='black')  
        
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
            "Level 3 (Mouse Control):",
            "- Move the bird using the mouse cursor.",
            "- Collect all seeds to complete the level.",
            "- Avoid obstacles to maintain health.",
            "",
            "Good luck on your adventure!"
        ]

        yOffset = 60
        for instruction in instructions:
            drawLabel(instruction, app.width / 2, yOffset, align='center', size=10, fill='black') 
            yOffset += 12

class StartScreen:
    def __init__(self):
        self.spacePressed = False

    def draw(self):
        drawImage('background.jpg',0,0) #image taken from https://as1.ftcdn.net/v2/jpg/05/62/56/46/1000_F_562564643_OSsBfTgR7mLjKtY5TCHrwGA2auYkou2T.jpg
        
        drawRect(10, 10, 380, 380, fill=None, border='green', borderWidth=5)

        drawLabel("Welcome to", 200, 150, size=24, fill='black', font='Arial', align="center")
        drawLabel("The Circle of Life", 200, 200, size=48, fill='black', font='Arial', align='center' )
        drawLabel("developed by shandon herft", 200, 375, size=16, fill='black', font='Arial', align='center' )

        buttonRect = (100, 250, 200, 50)  
        drawRect(*buttonRect, fill='mediumseagreen', border='black', borderWidth=2)
        drawLabel("Press Space to Start", buttonRect[0] + buttonRect[2] // 2, buttonRect[1] + buttonRect[3] // 2, size=16, fill='black')


    def onKeyPress(self, app, key):
        if key == 'space':
            self.spacePressed = True

    def isSpacePressed(self):
        return self.spacePressed

class RestartButton:
    def __init__(self, app):
        self.app = app
        self.buttonRect = (60, 20, 50, 40)  

    def draw(self):
        drawRect(*self.buttonRect, fill='gray')
        drawLabel("Restart", self.buttonRect[0] + self.buttonRect[2] // 2, self.buttonRect[1] + self.buttonRect[3] // 2, size=8, fill='white')
        drawRect(10,20,100,40, border='black', fill=None)

    def isClicked(self, mouseX, mouseY):
        # Check if the mouse click is within the button boundaries
        x, y, width, height = self.buttonRect
        return x <= mouseX <= x + width and y <= mouseY <= y + height


app.restartButton = RestartButton(app)

class PauseButton:
    def __init__(self, app):
        self.app = app
        self.buttonRect = (10, 20, 50, 40) 

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
        self.buttonRect = (100, 250, 200, 50)  

    def draw(self):
        drawRect(0, 0, 400, 400, fill='lightgreen', border=None)
        drawLabel(f"Level {self.level}", 200, 175, size=70, fill='black')

        drawRect(*self.buttonRect, fill='blue', border='black')
        drawLabel("Start Level", self.buttonRect[0] + self.buttonRect[2] // 2, self.buttonRect[1] + self.buttonRect[3] // 2, size=24, fill='white')

    def isButtonClicked(self, mouseX, mouseY):
        # Check if the mouse click is within the button boundaries
        x, y, width, height = self.buttonRect
        return x <= mouseX <= x + width and y <= mouseY <= y + height

class Level2Screen:
    def __init__(self):
        self.buttonRect = (100, 250, 200, 50)  
        self.speed = 5  
        self.blockPositions = self.generateRandomBlockPositions()
    
    def generateRandomBlockPositions(self):
        # Generate random block positions for Level 2
        block_count = 9
        min_x, max_x = 50, 350
        min_y, max_y = 80, 280
        return [(random.randint(min_x, max_x), random.randint(min_y, max_y)) for _ in range(block_count)]


    def draw(self):
        drawRect(0, 0, 400, 400, fill='lightblue', border=None)
        drawLabel("Level 2", 200, 175, size=70, fill='black')

        drawRect(*self.buttonRect, fill='blue', border='black')
        drawLabel("Start Level", self.buttonRect[0] + self.buttonRect[2] // 2, self.buttonRect[1] + self.buttonRect[3] // 2, size=24, fill='white')

    def isButtonClicked(self, mouseX, mouseY):
        # Check if the mouse click is within the button boundaries
        x, y, width, height = self.buttonRect
        return x <= mouseX <= x + width and y <= mouseY <= y + height
    
    def update(self):
        # Gradually increase obstacle speed over time
        self.speed += 0.1

        # Randomize obstacle positions
        random.shuffle(self.blockPositions)


class Level3Screen:
    def __init__(self):
        self.buttonRect = (100, 250, 200, 50) 
        self.blockPositions = []

    def draw(self):
        drawRect(0, 0, 400, 400, fill='lightcoral', border=None)
        drawLabel("Level 3", 200, 175, size=70, fill='black')

        drawRect(*self.buttonRect, fill='purple', border='black')
        drawLabel("Start Level", self.buttonRect[0] + self.buttonRect[2] // 2, self.buttonRect[1] + self.buttonRect[3] // 2, size=24, fill='white')

    def isButtonClicked(self, mouseX, mouseY):
        # Check if the mouse click is within the button boundaries
        x, y, width, height = self.buttonRect
        return x <= mouseX <= x + width and y <= mouseY <= y + height


class PauseScreen:
    def __init__(self):
        pass

    def draw(self):
        drawRect(0, 0, 400, 400, fill='darkgray', border=None)
        drawLabel("Game Paused", 200, 200, size=48, fill='black', align='center')



class ContinueScreen:
    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill='lightblue', border=None)
        drawLabel("Level Completed!", app.width / 2, 150, size=36, fill='black', align='center')
        drawLabel("Press 'C' to Continue or 'Q' to Quit", app.width / 2, 250, size=24, fill='black', align='center')

class Level2ContinueScreen:
    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill='lightgreen', border=None)
        drawLabel("Level 2 Completed!", app.width / 2, 150, size=36, fill='black', align='center')
        drawLabel("Press 'C' to Continue or 'Q' to Quit", app.width / 2, 250, size=24, fill='black', align='center')

class GameOverScreen:
    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill='gold', border=None)
        drawLabel("Game Over!", app.width / 2, app.height / 2 - 20, size=36, fill='black', align='center')
        drawLabel("Press 'Q' to Quit", app.width / 2, app.height / 2 + 20, size=24, fill='black', align='center')


class Bird:
    def __init__(self, x, y, app):
        self.x = x
        self.y = y
        self.originalY = y
        self.radius = 20
        self.speed = 30
        self.jumpForce = 15  
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
        self.birdImage = 'bird.png'

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

        seeds_to_draw = []  

        for seedPosition in seedPositions:
            seedX, seedY = seedPosition
            if seedPosition not in self.collectedSeeds:
                if math.sqrt((seedX - self.x) ** 2 + (seedY - self.y) ** 2) <= self.radius + 10:
                    self.collectSeed(seedPosition)
                    seeds_to_draw.append(seedPosition)

        return seeds_to_draw  



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
        if self.app.currentLevel == 2:
            self.birdImage = 'bird2.png'#image taken from https://img.rankedboost.com/wp-content/plugins/pokemon-lets-go/assets/pixel-images/Pokemon-Lets-Go-Pidgeot.png
        elif self.app.currentLevel == 3:
            self.birdImage = 'bird3.png'#image taken from https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/8de88e59-7112-4450-891a-44efa6191fab/dcu89ym-f5e8c69e-8428-4a4e-97ed-377b28127030.png/v1/fit/w_440,h_400/mega_pidgeot__let_s_go_style__by_niconicoide_dcu89ym-375w-2x.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NDAwIiwicGF0aCI6IlwvZlwvOGRlODhlNTktNzExMi00NDUwLTg5MWEtNDRlZmE2MTkxZmFiXC9kY3U4OXltLWY1ZThjNjllLTg0MjgtNGE0ZS05N2VkLTM3N2IyODEyNzAzMC5wbmciLCJ3aWR0aCI6Ijw9NDQwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.nzJw1rSM__RRBVP7bpdzhz3N3_Hjs7Uqa2DqYEAlUg8

        drawImage(self.birdImage, self.x, self.y - 20) #image taken from https://art.pixilart.com/d69f8d494d01177.png

    def drawSeeds(self):
        seedPositions = []

        
        for block in self.app.blocks:
            seedPositions.append((block.x + block.width // 2, block.y - 20))

        for seedPosition in seedPositions:
            if seedPosition not in self.collectedSeeds:
                if self.app.currentLevel == 2:
                    drawImage('seed2.png', seedPosition[0], seedPosition[1], align='center') # im age from https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTcS9RswGU38CWRLOUwd-34kWw4eOQFumDJQBxY2acjIiUdgZgg
                elif self.app.currentLevel == 3:
                    drawImage('seed3.png', seedPosition[0], seedPosition[1], align='center') # image from https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTcS9RswGU38CWRLOUwd-34kWw4eOQFumDJQBxY2acjIiUdgZgg
                else:
                    drawImage('seed.png', seedPosition[0], seedPosition[1], align='center') # image from https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTcS9RswGU38CWRLOUwd-34kWw4eOQFumDJQBxY2acjIiUdgZgg

class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        drawImage('platform.png', self.x, self.y, opacity=80 ) # image from https://as2.ftcdn.net/v2/jpg/06/05/75/93/1000_F_605759340_A8flCzVnmwvHN123joG5IbOHIXDsrwKV.jpg
        

class Landscape:
    @staticmethod
    def drawClouds(scroll_speed=0):
        cloudColor = 'gainsboro'
        cloudPositions = [(50, 100), (200, 150), (350, 100)]  

        for x, y in cloudPositions:
            drawCircle(x, y - scroll_speed, 30, fill=cloudColor, border=None, opacity=40)
            drawCircle(x + 40, y - scroll_speed, 30, fill=cloudColor, border=None, opacity=40)
            drawCircle(x + 80, y - scroll_speed, 30, fill=cloudColor, border=None, opacity=40)
    

    @staticmethod
    def drawSky():
        drawRect(0, 0, 400, 400, fill='lightblue', border=None)

    @staticmethod
    def drawGround():
        drawLine(0, 320, 400, 320)
        drawImage('ground.jpg',0,320)

        
    @staticmethod
    def drawTrees():

        drawImage('tree.png',0, 120, opacity=80 ) # image taken from https://opengameart.org/sites/default/files/Tree_SpriteSheet_Outlined.png
        drawImage('tree.png',150, 150, opacity=80 ) # image taken from https://opengameart.org/sites/default/files/Tree_SpriteSheet_Outlined.png
        drawImage('tree.png',300, 120, opacity=80 ) # image taken from https://opengameart.org/sites/default/files/Tree_SpriteSheet_Outlined.png
    

    @staticmethod
    def drawSeedCounter(seedCounter, health):
        drawRect(300, 20, 80, 40, fill='white', border='black')
        drawLabel(f'Seeds: {seedCounter} Health: {health}', 340, 40, align='center', size=8, fill='black')
    

class Obstacle:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed  
    

    def move(self):
        # Accelerate the obstacle speed
        self.x += self.speed
        self.speed += 0.1
        if self.x >= 400 - self.radius:
            self.x = 400 - self.radius
            self.speed = -self.speed
        elif self.x <= self.radius:
            self.x = self.radius
            self.speed = -self.speed

    def draw(self):
        drawImage('enemy.png',self.x, self.y, align='center') # image taken from https://img.gamewith.net/article_tools/pokemon-lets-go/gacha/955_i.png

def onKeyPress(app, key):
    if app.gameOverScreenActive:
        if key == 'q':
            app.showContinueScreen = False
            app.startScreen = StartScreen()
            app.gameStarted = False
            app.levelScreen = None
            app.level2ContinueScreen = None  
            app.currentLevel = 1
            app.bird.resetPosition()
            app.bird.resetSeeds()
            app.bird.health = 3
            app.blocks = [Block(x, y, 50, 10) for x, y in blockPositions]  
            app.gameOverScreenActive = False
    if not app.gameStarted:
        if key == 'space':
            app.gameStarted = True
            app.startScreen = None  
            app.instructionScreen = InstructionScreen() 
            return
        elif key == 'c' and app.showContinueScreen:
            if app.currentLevel == 1:
                app.showContinueScreen = False
                app.levelScreen = Level2Screen()  
                app.gameStarted = True
            elif app.currentLevel == 2:
                app.showContinueScreen = False
                app.levelScreen = Level3Screen()  
                app.gameStarted = True
        elif key == 'q' and app.showContinueScreen:
            app.showContinueScreen = False
            app.startScreen = StartScreen()
            app.gameStarted = False
            app.levelScreen = None
            app.level2ContinueScreen = None  
            app.currentLevel = 1
            app.bird.resetPosition()
            app.bird.resetSeeds()
            app.bird.health = 3
            app.blocks = [Block(x, y, 50, 10) for x, y in blockPositions]  
    elif app.instructionScreen:
        app.instructionScreen = None
        app.levelScreen = LevelScreen(app.currentLevel)  
        app.gameStarted = True
    elif app.levelScreen:
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
        # Check if the level screen is Level2Screen before setting it to None
        if isinstance(app.levelScreen, Level2Screen):
            app.currentLevel = 2  # Set current level to 2

        elif isinstance(app.levelScreen, Level3Screen):
            app.currentLevel = 3  # Set current level to 3

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

def onMouseMove(app, mouseX, mouseY):
    # Update the mouseX and mouseY attributes in the app
    app.mouseX = mouseX
    app.mouseY = mouseY

def onKeyRelease(app, key):
    if key in {'up', 'down'}:
        app.bird.fall()

cooldownFrames = 0

def onStep(app):
    if not app.gameStarted:
        return

    if app.bird.paused:
        return
    
    if app.currentLevel == 3:
        # Check if all seeds are collected in Level 3
        if len(app.bird.collectedSeeds) == 9:
            # Transition to the game-over screen
            app.gameOverScreenActive = True
            return

    if app.levelScreen:
        # Check for level completion 
        if app.bird.y <= 0:
            app.currentLevel += 1
            if app.currentLevel == 2:
                app.levelScreen = Level2Screen()

            elif app.currentLevel <= 3:  
                app.levelScreen = LevelScreen(app.currentLevel)
            else:
                app.gameStarted = False
                app.levelScreen = None
                app.currentLevel = 1
                app.bird.resetPosition()
                app.bird.resetSeeds()
                app.bird.health = 3
            return

        # Update obstacle speed for Level 2
        if isinstance(app.levelScreen, Level2Screen):
            app.obstacle.speed = app.levelScreen.speed
            app.obstacle2 = Obstacle(100, 100, 30, app.levelScreen.speed)  

        if app.levelScreen and app.levelScreen.blockPositions and app.currentLevel != 3:
            # Create blocks based on the blockPositions
            app.blocks = [Block(x, y, 50, 10) for x, y in app.levelScreen.blockPositions]

            # Adjust the bird's jumpHeight for Level 2
            if isinstance(app.levelScreen, Level2Screen):
                app.bird.jumpHeight = 100  

    # Move both obstacles
    if hasattr(app, 'obstacle'):
        app.obstacle.move()
    if hasattr(app, 'obstacle2'):
        app.obstacle2.move()

    # Check for collision with obstacle
    if (
        (hasattr(app, 'obstacle') and
         app.bird.x - app.bird.radius < app.obstacle.x + app.obstacle.radius
         and app.bird.x + app.bird.radius > app.obstacle.x - app.obstacle.radius
         and app.bird.y - app.bird.radius < app.obstacle.y + app.obstacle.radius
         and app.bird.y + app.bird.radius > app.obstacle.y - app.obstacle.radius) or
        (hasattr(app, 'obstacle2') and
         app.bird.x - app.bird.radius < app.obstacle2.x + app.obstacle2.radius
         and app.bird.x + app.bird.radius > app.obstacle2.x - app.obstacle2.radius
         and app.bird.y - app.bird.radius < app.obstacle2.y + app.obstacle2.radius
         and app.bird.y + app.bird.radius > app.obstacle2.y - app.obstacle2.radius)
    ):
        if not app.bird.collisionDetected:
            app.bird.health -= 1
            app.bird.collisionDetected = True
            if app.bird.health == 0:
                print("Bird has died!")
                app.bird.resetPosition()
                app.bird.resetSeeds()
                app.bird.health = 3
    else:
        app.bird.collisionDetected = False

    # Check for collision with seeds
    seeds_to_draw = app.bird.checkSeedCollision()

    # Check if all seeds are collected and current level is not 3
    if len(app.bird.collectedSeeds) == 9 and app.currentLevel != 3:
        # Transition to the level end screen
        app.levelScreen = None
        app.gameStarted = False
        app.bird.resetPosition()
        app.bird.resetSeeds()
        app.bird.health = 3
        app.showContinueScreen = True

        if app.currentLevel == 2:
            app.level2ContinueScreen = Level2ContinueScreen()  # Display Level 2 Continue Screen

    # Check if the current level is 3
    if app.currentLevel == 3:
        # Move the bird based on the cursor position
        app.bird.x = app.mouseX
        app.bird.y = app.mouseY
        app.bird.checkBounds()





def redrawAll(app):
    if not app.gameStarted:
        if app.showContinueScreen:
            # Provide options for the player to continue or quit
            if app.currentLevel == 2:
                app.level2ContinueScreen.draw(app)  
            else:
                drawRect(0, 0, app.width, app.height, fill='lightblue', border=None)
                drawLabel("Level Completed!", app.width / 2, 150, size=48, fill='black', align='center')
                drawLabel("Press 'C' to Continue or 'Q' to Quit", app.width / 2, 250, size=24, fill='black', align='center')
        else:
            app.startScreen.draw()
    elif app.instructionScreen:
        app.instructionScreen.redrawAll(app)
    elif app.levelScreen:
        app.levelScreen.draw()
    elif app.bird.paused:
        app.pauseScreen.draw()
    elif app.gameOverScreenActive:
        app.gameOverScreen.draw(app)  # Draw the game-over screen
    else:
        Landscape.drawSky()
        Landscape.drawClouds()
        app.bird.draw()

        if hasattr(app, 'blocks') and app.currentLevel != 3:  
            for block in app.blocks:
                block.draw()

         # Draw both obstacles
        if hasattr(app, 'obstacle'):
            app.obstacle.draw()
        if hasattr(app, 'obstacle2'):
            app.obstacle2.draw()

        # Draw the seeds
        seeds_to_draw = app.bird.checkSeedCollision()
        for seedPosition in seeds_to_draw:
            seedX, seedY = seedPosition
            drawCircle(seedX, seedY, 10, fill='orange', border="black")

        # Draw the pause button
        app.pauseButton.draw()

        # Draw the pause button
        app.restartButton.draw()



if __name__ == "__main__":
    app.bird = Bird(50, 300, None)
    app.obstacle = Obstacle(200, 225, 30, 5)
    app.startScreen = StartScreen()
    app.pauseScreen = PauseScreen()
    app.pauseButton = PauseButton(app)
    app.gameStarted = False
    app.levelScreen = None
    app.instructionScreen = InstructionScreen()  
    app.currentLevel = 1  
    app.showContinueScreen = False
    app.continueScreen = ContinueScreen()
    app.level2ContinueScreen = Level2ContinueScreen()
    app.gameOverScreen = GameOverScreen()
    app.gameOverScreenActive = False

    # Add more blocks vertically
    blockPositions = [
        (100, 280), (250, 240), (380, 280),
        (100, 200), (250, 160), (380, 200),
        (100, 120), (250, 80), (380, 120)
    ]

    app.blocks = [Block(x, y, 50, 10) for x, y in blockPositions]

    app.bird.app = app
    


    runApp(width=400, height=400, onMousePress=onMousePress, onKeyDown=onKeyPress, onKeyUp=onKeyRelease, onStep=onStep, redrawAll=redrawAll)

