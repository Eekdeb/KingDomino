import pygame
number_of_players = 2

#colors
background_color = (117, 115, 89) 
startBrickColor = (255,255,255)
wheatColor = (212, 204, 59)
forestColor = (25, 115, 49)
waterColor = (45, 116, 179)
fieldColor = (36, 201, 80)
desertColor = (144, 150, 123)
mineColor = (64, 69, 49)
select_color = (255,255,255)
allColors =  [background_color,startBrickColor,wheatColor,forestColor,waterColor,fieldColor,desertColor,mineColor]

#Player settings
player1 = (106,17,173)
player2 = (217,33,33)
player3 = (4,99,7)
player4 = (255,225,64)

#key bindings
move_up = pygame.K_w
move_down = pygame.K_s
move_left = pygame.K_a
move_right = pygame.K_d
place = pygame.K_b
rotate = pygame.K_q

# Initialize constants
BRICK_SIZE = 60
SCREEN_MARGIN_X = 10
SCREEN_MARGIN_Y = 50
CHOOSE_BRICK_OFFSET_X = 2*BRICK_SIZE
CHOOSE_BRICK_OFFSET_Y = 100