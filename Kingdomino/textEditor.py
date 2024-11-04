import pygame_textinput
import pygame

'''
This code is mostly written by AI with some changes to make it compatible to the game and is working
'''

def getName(screen,pos,playerNr):
    # But more customization possible: Pass your own font object
    font = pygame.font.SysFont("Consolas", 55)
    # Create own manager with custom input validator
    manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 6)
    # Pass these to constructor
    textinput_custom = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)
    # Customize much more
    textinput_custom.cursor_width = 0
    textinput_custom.cursor_blink_interval = 400 # blinking interval in ms
    textinput_custom.font_color = (0, 85, 170)

    clock = pygame.time.Clock()

    while True:
        #screen.fill((117, 115, 89))
        pygame.draw.rect(screen,(117, 115, 89),(pos[0],pos[1]+playerNr*55,500,55))
        events = pygame.event.get()

        # Feed it with events every frame
        textinput_custom.update(events)

        # Get its surface to blit onto the screen
        screen.blit(textinput_custom.surface, (pos[0],pos[1]+playerNr*55))

        # Check if user is exiting or pressed return
        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(f"User pressed enter! Input so far: {textinput_custom.value}")
                return textinput_custom.value

        pygame.display.update()
        clock.tick(30)