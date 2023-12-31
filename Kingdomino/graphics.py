import pygame 
from Actions import Actions
from Player import Player
import json
import time
from BrickStack import BrickStack


def drawBoard(board,surface,colors,rect):
	posX = rect[0]
	posY = rect[1]
	width = rect[2]/5
	hight = rect[3]/5
	pygame.draw.rect(surface,colors[1],rect)
	for row in range(0,5):
		changY = posY + row * hight
		for column in range(0,5):
			changX = posX + column * width
			partRect = (changX,changY,width,hight)
			color = colors[board[row][column][0]]
			pygame.draw.rect(surface,color,partRect)
			pygame.draw.rect(surface,(0,0,0),partRect,1)
	return

tmpBoard = [[(3,0),(4,0),(5,0),(6,0),(7,0)],
            [(3,0),(4,0),(5,0),(6,0),(7,0)],
            [(3,0),(4,0),(2,0),(6,0),(7,0)],
            [(3,0),(4,0),(5,0),(6,0),(7,0)],
            [(3,0),(4,0),(5,0),(6,0),(7,0)]]

"""
1: starting brick   
2: wheat field      
3: forest      
4: water
5: grass field
6: desert
7: mine
"""
background_colour = (117, 115, 89) 
startBrickColor = (255,255,255)
wheatColor = (212, 204, 59)
forestColor = (25, 115, 49)
waterColor = (45, 116, 179)
fieldColor = (36, 201, 80)
desertColor = (144, 150, 123)
mineColor = (64, 69, 49)

allColors =  [background_colour,startBrickColor,wheatColor,forestColor,waterColor,fieldColor,desertColor,mineColor]
# Initialize Pygame
pygame.init()
# Set the screen to fullscreen
size = pygame.display.get_desktop_sizes()
size = (size[0][0]-10, size[0][1]-50)
bricksize = 80
spacerSize = 10
screen = pygame.display.set_mode(size)

#Varables for text writing
font = pygame.font.SysFont('arial', 50)

pygame.display.update()
# Set the caption of the screen 
pygame.display.set_caption('Kingdomino') 
pygame.display.list_modes()

# Fill the background colour to the screen 
screen.fill(background_colour) 

drawBoard(tmpBoard,screen,allColors,(size[0]/6,size[1]/6,400,400))
# Update the display using flip 
pygame.display.flip()


#Initialis
ac = Actions()
pile = BrickStack()
pile.shuffle()
#create players
playerQueue = ac.createPlayers()

#Start the game
##Payers Pick the first card
brick4 = pile.get4()
##First round of chosing
playerQueue = ac.firstRound(pile,brick4,playerQueue)

running = True
while running: 
# for loop through the event queue 
	for event in pygame.event.get(): 
		# Check for QUIT event	 
		if event.type == pygame.QUIT: 
			running = False
	
	for i in range(0, 12):
		#Draw new bricks exept last round
		if(i != 11):
			brick4 = pile.get4()
			#Next round chosing bircks
			#pile.draw(brick4[0],screen,(0,0,bricksize,bricksize))
			pile.draw4(brick4,screen,(0,0),bricksize)
			text = font.render(str("Hello"), True, (0, 0, 0))
			screen.blit(text, (200,100))
			pygame.display.flip()
			playerQueue = ac.nextRound(pile,brick4,playerQueue)
		
		#Place the bricks
		for player in playerQueue:
			player.board.drawBoardPlacing(screen,(size[0]/6,size[1]/6,bricksize*5,bricksize*5),(0,0),(0,1),player.placingBrick)
			if not ac.initAndCheckBrickOK(player):
				player.nextBrick()
				break
			placed = False
			while(not placed):
				tempBoard = []
				for event in pygame.event.get(): 
					if event.type == pygame.QUIT: 
						running = False
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_a:
							ac.placeBrick(player,"a",screen,(size[0]/6,size[1]/6,bricksize*5,bricksize*5))
							print("A")
						if event.key == pygame.K_s:
							ac.placeBrick(player,"s",screen,(size[0]/6,size[1]/6,bricksize*5,bricksize*5))
							print("S")
						if event.key == pygame.K_w:
							ac.placeBrick(player,"w",screen,(size[0]/6,size[1]/6,bricksize*5,bricksize*5))
							print("W")
						if event.key == pygame.K_d:
							ac.placeBrick(player,"d",screen,(size[0]/6,size[1]/6,bricksize*5,bricksize*5))
							print("d")
						if event.key == pygame.K_q:
							ac.placeBrick(player,"q",screen,(size[0]/6,size[1]/6,bricksize*5,bricksize*5))
							print("q")
						if event.key == pygame.K_b:
							ask = ac.placeBrick(player,"b",screen,(size[0]/6,size[1]/6,bricksize*5,bricksize*5))
							print(ask)
							if ask:
								placed = True
							print("b")
				#drawBoard(playerQueue[0].board.board,screen,allColors,(size[0]/6,size[1]/6,400,400))
				pygame.display.flip()
	#print out the points
	for p in playerQueue:
		print(p.name + ": " + str(p.board.getAllPoints()))
	running = False

