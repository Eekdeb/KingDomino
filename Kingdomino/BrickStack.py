
import json
from pathlib import Path
import random
import pygame
from operator import itemgetter
import config

class BrickStack:
    
    def __init__(self):
        base_path = Path(__file__).parent
        json_file_path = base_path / "Bricks.json"
        try:
            with open(json_file_path) as f:
                data = json.load(f)
                self.bricks = data["bricks"]
        except FileNotFoundError:
            raise RuntimeError("Bricks.json file not found.")
        except json.JSONDecodeError:
            raise RuntimeError("Error decoding JSON from Bricks.json.")
    
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
        if not self.bricks:
            raise RuntimeError("No more bricks in the stack.")
        return self.bricks.pop(0)
    
    def shuffle(self):
        random.shuffle(self.bricks)
        
    #takes the top 4 bricks in the stack and returns them
    def get4(self):
        bricks4 = [self.pull() for _ in range(4)]
        bricks4 = sorted(bricks4,key = itemgetter('value'))  
        return bricks4
    
    #draw a brick on the board
    def draw(self, brick, player, surface, rect):
        posX, posY, width, height = rect
        color = (0, 0, 0) if player == 0 else player.color
        
        # Define the main rectangles for the brick biomes
        rect_biome1 = pygame.Rect(posX, posY, width, height)
        rect_biome2 = pygame.Rect(posX + width, posY, width, height)
        # Define the main rectangles for the crowns
        rect_crown1 = pygame.Rect(posX+width/10, posY+height/10, width/8, height/8)
        rect_crown2 = pygame.Rect(posX + width+width/10, posY+height/10, width/8, height/8)
        offset = width/7

        # Draw the biomes with borders
        pygame.draw.rect(surface, config.allColors[brick['bioms'][0]], rect_biome1)
        pygame.draw.rect(surface, color, rect_biome1, 3)
        for crown in range(brick['crowns'][0]):
            pygame.draw.rect(surface, (0,0,0), rect_crown1)
            rect_crown1.left += offset

        pygame.draw.rect(surface, config.allColors[brick['bioms'][1]], rect_biome2)
        pygame.draw.rect(surface, color, rect_biome2, 3)       
        for crown in range(brick['crowns'][1]):
            pygame.draw.rect(surface, (0,0,0), rect_crown2)
            rect_crown2.left += offset

    #takes 4 bricks on the borad
    def take4(self,brick4,surface,pos,brickSize):
        posX,posY = pos
        for brick in brick4:
            self.draw(brick,0,surface,(posX,posY,brickSize,brickSize))
            posY = posY + brickSize + brickSize/10    
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
    def draw4_choose(self,player,chosen,brick4,selected,surface,pos,brick_size):
        i = 0
        posX = pos[0]
        posY = pos[1]
        for brick in brick4:
            if(i == selected):
                self.draw(brick,player,surface,(posX,posY,brick_size,brick_size))
            else:
                self.draw(brick,chosen[i],surface,(posX,posY,brick_size,brick_size))
            posY = posY + brick_size + brick_size/10
            i = i+1
    
    def draw_player_bricks(self,player_queue,surface,pos,brick_size):
        posX,posY = pos
        for player in player_queue:
            self.draw(player.chosenBrick,player,surface,(posX,posY,brick_size,brick_size))
            posY = posY + brick_size + brick_size/10