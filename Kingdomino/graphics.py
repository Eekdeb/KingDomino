import pygame 
from Actions import Actions
from Player import Player
import json
import time
from BrickStack import BrickStack

'''
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
	return'''

initchoosingBrickFace = False
def choosingBrickFace(playerQueue,brick4,pos,surface):
	global initchoosingBrickFace
	newQueue = [0,0,0,0]
	for player in playerQueue:
		placed = False
		selected = len(newQueue)-1
		selected = ac.jumpSelect(selected,False,newQueue)
		pile.draw4Choose(player,newQueue,brick4,selected,surface,pos,bricksize)
		pygame.display.flip()
		while(not placed):
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT: 
					running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						selected = ac.jumpSelect(selected,True,newQueue)
						pile.draw4Choose(player,newQueue,brick4,selected,surface,pos,bricksize)
					if event.key == pygame.K_s:
						selected = ac.jumpSelect(selected,False,newQueue)
						pile.draw4Choose(player,newQueue,brick4,selected,surface,pos,bricksize)
					if event.key == pygame.K_b:
						if(newQueue[selected] == 0):
							newQueue[selected] = player
							if(not initchoosingBrickFace):
								player.setPlacingBrick(brick4[selected])
							player.setBrick(brick4[selected])
							placed = True
			pygame.display.flip()

	#Take away the 0s and uppdate the queue
	newQueue = [i for i in newQueue if i!=0]
	if(not initchoosingBrickFace):
		initchoosingBrickFace = True
	return newQueue			

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
# Initialize Pygame
pygame.init()
#globals
bricksize = 60
spacerSize = 10

background_colour = (117, 115, 89) 
startBrickColor = (255,255,255)
wheatColor = (212, 204, 59)
forestColor = (25, 115, 49)
waterColor = (45, 116, 179)
fieldColor = (36, 201, 80)
desertColor = (144, 150, 123)
mineColor = (64, 69, 49)

allColors =  [background_colour,startBrickColor,wheatColor,forestColor,waterColor,fieldColor,desertColor,mineColor]

# Set the screen to fullscreen
size = pygame.display.get_desktop_sizes()
size = (size[0][0]-10, size[0][1]-50)
screen = pygame.display.set_mode(size)
chooseBrickPos = (screen.get_width()/2,100)
#Varables for text writing
font = pygame.font.SysFont('arial', 50)

pygame.display.update()
# Set the caption of the screen 
pygame.display.set_caption('Kingdomino') 
pygame.display.list_modes()

# Fill the background colour to the screen 
screen.fill(background_colour) 
pygame.display.flip()
#drawBoard(tmpBoard,screen,allColors,(size[0]/6,size[1]/6,400,400))
# Update the display using flip 
#pygame.display.flip()


#------------------------------------------------------------------------------------
#  								Start Game
#------------------------------------------------------------------------------------

#Initialis
ac = Actions()
pile = BrickStack()
pile.shuffle()

#create players
playerQueue = ac.createPlayers(screen,size,bricksize,4)
screen.fill(background_colour)
for player in playerQueue:
	player.board.drawBoard(screen,player.boardpos,player.color)
	pygame.display.flip()
#Start the game
##Payers Pick the first card
brick4 = pile.get4()
##First round of chosing
pygame.display.flip()
playerQueue = choosingBrickFace(playerQueue,brick4,chooseBrickPos,screen)

running = True
while running: 
	
	for i in range(0, 12):
		#Print selected bricks to remember them
		pile.drawPlayerBricks(playerQueue,screen,(chooseBrickPos[0],chooseBrickPos[1]+100+bricksize*4),bricksize)
		
		#Draw new bricks exept last round
		if(i != 11):
			brick4 = pile.get4()
			#Next round chosing bircks
			pile.take4(brick4,screen,chooseBrickPos,bricksize)
			#later to draw the names above the players text = font.render(str("Hello"), True, (0, 0, 0))
			pygame.display.flip()
			#chose bricks
			playerQueue = choosingBrickFace(playerQueue,brick4,chooseBrickPos,screen)
					
		#Place the bricks
		for player in playerQueue:
			#player.board.drawBoardPlacing(screen,(size[0]/6,size[1]/6,bricksize*5,bricksize*5),(0,0),(0,1),player.placingBrick)

			if not ac.initAndCheckBrickOK(player):
				player.nextBrick()
				continue
			ac.placeBrick(player,"§",screen,player.boardpos)
			placed = False
			while(not placed):
				tempBoard = []
				for event in pygame.event.get(): 
					if event.type == pygame.QUIT: 
						running = False
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_a:
							ac.placeBrick(player,"a",screen,player.boardpos)
							print("A")
						if event.key == pygame.K_s:
							ac.placeBrick(player,"s",screen,player.boardpos)
							print("S")
						if event.key == pygame.K_w:
							ac.placeBrick(player,"w",screen,player.boardpos)
							print("W")
						if event.key == pygame.K_d:
							ac.placeBrick(player,"d",screen,player.boardpos)
							print("d")
						if event.key == pygame.K_q:
							ac.placeBrick(player,"q",screen,player.boardpos)
							print("q")
						if event.key == pygame.K_b:
							ask = ac.placeBrick(player,"b",screen,player.boardpos)
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

