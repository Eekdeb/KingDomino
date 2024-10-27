
import json
import random
import pygame
from operator import itemgetter

background_colour = (117, 115, 89) 
startBrickColor = (255,255,255)
wheatColor = (212, 204, 59)
forestColor = (25, 115, 49)
waterColor = (45, 116, 179)
fieldColor = (36, 201, 80)
desertColor = (144, 150, 123)
mineColor = (64, 69, 49)

allColors =  [background_colour,startBrickColor,wheatColor,forestColor,waterColor,fieldColor,desertColor,mineColor]

class BrickStack:
    
    def __init__(self):
        f = open("C:\\Users\\Eek\\OneDrive\\Dokument\\Codes\\Python\\Kingdomino\\Bricks.json")
        data = json.load(f)
        self.bricks = data["bricks"]
    
    def __str__(self):
        string =  str(self.bricks['bioms'][0]) + " "
        string += self.crownToStars(self.bricks['crowns'][0])
        string += str(self.bricks['bioms'][1])
        string += self.crownToStars(self.bricks['crowns'][1])
        return string
    
    def print4(self,brick4):
        string = ""
        for i in range(0, 4):
            string += str(i+1) + ": ["
            string +=  str(brick4[i]['bioms'][0])
            string += self.crownToStars(brick4[i]['crowns'][0])
            string += str(brick4[i]['bioms'][1])
            string += self.crownToStars(brick4[i]['crowns'][1])
            string += "]\n"
        print(string)
    
    def crownToStars(self,crown):
        if(crown == 0):
            return "   "
        if(crown == 1):
            return "*  "
        if(crown == 2):
            return "** "
        if(crown == 3):
            return "***"
    
    def pull(self):
        return self.bricks.pop(0)
    
    def shuffle(self):
        random.shuffle(self.bricks)
        
    #takes the top 4 bricks in the stack and returns them
    def get4(self):
        bricks4 = []
        for i in range(0, 4):
            bricks4.append(self.pull())
        bricks4 = sorted(bricks4,key = itemgetter('value'))
        return bricks4
    

    #draw a brick on the board
    def draw(self, brick, player, surface, rect):
        posX, posY, width, height = rect
        
        # Determine color based on player state
        color = (0, 0, 0) if player == 0 else player.color

        # Define the main rectangles for the brick biomes
        rect_biome1 = pygame.Rect(posX, posY, width, height)
        rect_biome2 = pygame.Rect(posX + width, posY, width, height)
        # Define the main rectangles for the crowns
        rect_crown1 = pygame.Rect(posX+width/10, posY+height/10, width/8, height/8)
        rect_crown2 = pygame.Rect(posX + width+width/10, posY+height/10, width/8, height/8)
        offsett = width/7

        # Draw the biomes with borders
        pygame.draw.rect(surface, allColors[brick['bioms'][0]], rect_biome1)   # First biome
        pygame.draw.rect(surface, color, rect_biome1, 3)                       # Border for first biome
        for crown in range(brick['crowns'][0]):
            pygame.draw.rect(surface, (0,0,0), rect_crown1)
            rect_crown1.left += offsett

        pygame.draw.rect(surface, allColors[brick['bioms'][1]], rect_biome2)   # Second biome
        pygame.draw.rect(surface, color, rect_biome2, 3)       
                        # Border for second biome 
        for crown in range(brick['crowns'][1]):
            pygame.draw.rect(surface, (0,0,0), rect_crown2)
            rect_crown2.left += offsett

    #takes 4 bricks on the borad
    def take4(self,brick4,surface,pos,brickSize):
        posX = pos[0]
        posY = pos[1]
        for brick in brick4:
            self.draw(brick,0,surface,(posX,posY,brickSize,brickSize))
            posY = posY + brickSize + brickSize/10
        return
    
    """
    Inputs
    player: current player chosing
    chosen: Lists wich bricks are chosen for who
    brick4: the 4 bricks that you choos from
    selected the index of the brick selected
    surface: the window to draw on
    pos: where in the window to draw
    brickSize: the size the brick is gona be drawn in
    """
    def draw4Choose(self,player,chosen,brick4,selected,surface,pos,brickSize):
        i = 0
        posX = pos[0]
        posY = pos[1]
        for brick in brick4:
            if(i == selected):
                self.draw(brick,player,surface,(posX,posY,brickSize,brickSize))
            else:
                self.draw(brick,chosen[i],surface,(posX,posY,brickSize,brickSize))
            posY = posY + brickSize + brickSize/10
            i = i+1
        return
    
    def drawPlayerBricks(self,playerQueue,surface,pos,brickSize):
        posX = pos[0]
        posY = pos[1]
        for player in playerQueue:
            self.draw(player.chosenBrick,player,surface,(posX,posY,brickSize,brickSize))
            posY = posY + brickSize + brickSize/10
        return