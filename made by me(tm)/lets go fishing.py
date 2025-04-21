# A pygame game about... well, fishing.
# Play type : Simulation
# (Still unfinished.)

import time, random
import pygame

pygame.init()

# Starting Vars ---------------

window = pygame.display.set_mode((500, 500))
window.fill((200, 200, 255))
clock = pygame.time.Clock()
run = True

# Fish class ------------------

class Fish():
    def __init__(self, boxCoor:tuple=(0, 0), size:tuple=(100, 100), nameText:str='Name', descText:str='Desc', percentage:float=100):
        if percentage < 1:
            percentCol = (200, 200, 0)
        elif percentage < 10:
            percentCol = (100, 0, 200)
        elif percentage < 25:
            percentCol = (200, 200, 255)
        elif percentage < 50:
            percentCol = (200, 255, 200)
        else:
            percentCol = (255, 255, 255)
        #---------------------------------------
        self.rect = pygame.Rect(boxCoor, size)
        self.nameText = pygame.font.Font(None, 30).render(nameText, True, (255, 255, 255))
        self.descText = pygame.font.Font(None, 30).render(descText, True, (200, 200, 200))
        self.percentText = pygame.font.Font(None, 30).render(percentage, True, percentCol)
    def update(self):
        window.blit()
    def isMouseHovering(self, coor:tuple=(0, 0)):
        return self.rect.collidepoint(coor)

# Load fishes -----------------

# ish1 = Fish()

# Some define functions -------

def pygameEvents():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            pass
        # elif event.type ==

def updateDisplay():
    pygame.display.update()
    clock.tick(30)

# Main loop -------------------

while run:
    # do stuff
    pygameEvents()
    updateDisplay()

pygame.quit()