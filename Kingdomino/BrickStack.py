
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
        
    def get4(self):
        bricks4 = []
        for i in range(0, 4):
            bricks4.append(self.pull())
        bricks4 = sorted(bricks4,key = itemgetter('value'))
        return bricks4
    
    #fixa print crowns
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

    def draw(self,brick,player,surface,rect):
        posX = rect[0]
        posY = rect[1]
        width = rect[2]
        hight = rect[3]
        if player == 0:
            color = (0,0,0)
        else:
            color = player.color
        rect1 = (rect[0],rect[1],rect[2],rect[3])
        rect2 = (rect[0]+rect[2],rect[1],rect[2],rect[3])
        pygame.draw.rect(surface,allColors[brick['bioms'][0]],rect1)
        pygame.draw.rect(surface,color,rect1,3)
        pygame.draw.rect(surface,allColors[brick['bioms'][1]],rect2)
        pygame.draw.rect(surface,color,rect2,3)
        return

    def drawColor(self,player,brick,surface,rect):
        posX = rect[0]
        posY = rect[1]
        width = rect[2]
        hight = rect[3]
        rect1 = (rect[0],rect[1],rect[2],rect[3])
        rect2 = (rect[0]+rect[2],rect[1],rect[2],rect[3])
        pygame.draw.rect(surface,allColors[brick['bioms'][0]],rect1)
        pygame.draw.rect(surface,player.color,rect1,4)
        pygame.draw.rect(surface,allColors[brick['bioms'][1]],rect2)
        pygame.draw.rect(surface,player.color,rect2,4)
        return  
    
    def draw4(self,brick4,surface,pos,brickSize):
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
                self.drawColor(player,brick,surface,(posX,posY,brickSize,brickSize))
            else:
                self.draw(brick,chosen[i],surface,(posX,posY,brickSize,brickSize))
            posY = posY + brickSize + brickSize/10
            i = i+1
        return
    
    def drawPlayerBricks(self,playerQueue,surface,pos,brickSize):
        posX = pos[0]
        posY = pos[1]
        for player in playerQueue:
            self.drawColor(player,player.chosenBrick,surface,(posX,posY,brickSize,brickSize))
            posY = posY + brickSize + brickSize/10
        return