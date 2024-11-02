import pygame
import config

def drawCrowns(surface, posX, posY, cellWidth, cellHeight, crownCount, crownColor=(0, 0, 0)):
    """
    Draws crowns in a specified cell, with automatic positioning and offset.
    
    Args:
        surface: The pygame surface to draw on.
        posX: X-coordinate of the cell's top-left corner.
        posY: Y-coordinate of the cell's top-left corner.
        cellWidth: Width of the cell.
        cellHeight: Height of the cell.
        crownCount: Number of crowns to draw in the cell.
        crownColor: Color of the crown(s), defaulting to black.
    """
    crownRect = pygame.Rect(posX + cellWidth / 10, posY + cellHeight / 10, cellWidth / 8, cellHeight / 8)
    offset = cellWidth / 7
    for _ in range(crownCount):
        pygame.draw.rect(surface, crownColor, crownRect)
        crownRect.left += offset

def choosingBricks(playerQueue, brick4, pos, surface, ac, pile, bricksize):
    newQueue = [0, 0, 0, 0]
    for player in playerQueue:
        placed = False
        selected = len(newQueue) - 1
        selected = ac.jump_Select(selected, False, newQueue)
        pile.draw4_choose(player, newQueue, brick4, selected, surface, pos, bricksize)
        pygame.display.flip()
        while not placed:
            if all(newQueue):
                return newQueue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return []
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        selected = ac.jump_Select(selected, True, newQueue)
                        pile.draw4_choose(player, newQueue, brick4, selected, surface, pos, bricksize)
                    elif event.key == pygame.K_s:
                        selected = ac.jump_Select(selected, False, newQueue)
                        pile.draw4_choose(player, newQueue, brick4, selected, surface, pos, bricksize)
                    elif event.key == pygame.K_b and newQueue[selected] == 0:
                        newQueue[selected] = player
                        player.setPlacingBrick(player.chosenBrick)
                        player.setBrick(brick4[selected])
                        placed = True
            pygame.display.flip()
    return [i for i in newQueue if i != 0]
