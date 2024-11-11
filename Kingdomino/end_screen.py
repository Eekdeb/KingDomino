import pygame
import config
import sys
from Player import Player

def draw_end_screen(screen:pygame.Surface,players:list[Player]):
    screen.fill(config.background_color)
    
    players_and_scores = [(player, player.board.get_all_points()) for player in players]
    players_and_scores.sort(key=lambda x: x[1], reverse=True)
    
    font = pygame.font.Font(None, 100)
    counter = 0
    spacer = 110
    for player,score in players_and_scores:

        name_font = font.render(player.name + ":", True, player.color)
        name_rect = name_font.get_rect(center=(screen.get_width()/3,2*screen.get_height()/8+spacer*counter))
        screen.blit(name_font, name_rect)

        score_font = font.render(str(score), True, player.color)
        score_rect = score_font.get_rect(center=((screen.get_width()*2)/3,2*screen.get_height()/8+spacer*counter))
        screen.blit(score_font, score_rect)
        counter += 1

    pygame.display.flip()
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return


    