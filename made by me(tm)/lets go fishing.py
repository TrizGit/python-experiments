# A pygame game about... well, fishing.
# (Still unfinished.)

import time, random
import pygame

pygame.init()

# Starting Vars ---------------

window = pygame.display.set_mode((500, 500))
window.fill((200, 200, 255))
clock = pygame.time.Clock()
run = True
isMouseHeld = False

# Fish class ------------------

class Text():
    def __init__(self, text:str='', fontSize:int=36, coor:tuple=(0, 0), color:tuple=(255, 255, 255)):
        self.text = text
        self.fontSize = fontSize
        self.textCoor = coor
        self.color = color
        self.font = pygame.font.Font(None, fontSize)
        self.visible_font = self.font.render(self.text, True, self.color)
        self.font_rect = self.visible_font.get_rect()
    def update(self):
        self.visible_font = self.font.render(self.text, True, self.color)
        self.font_rect = self.visible_font.get_rect()
        window.blit(self.visible_font, self.textCoor)
    def new_text(self, newText='hia'):
        self.text = newText
        self.update()

class Fish():
    def __init__(self, boxCoor:tuple=(0, 0), boxSize:tuple=(100, 100), nameText:str='Name', descText:str='Desc', percentage:float=0.9):
        self.x = boxCoor[0]
        self.y = boxCoor[1]
        self.w = boxSize[0]
        self.h = boxSize[1]
        #---------------------------------------
        if percentage < 0.01:
            percentCol = (200, 200, 0)
        elif percentage < 0.1:
            percentCol = (100, 0, 200)
        elif percentage < 0.25:
            percentCol = (200, 200, 255)
        elif percentage < 0.5:
            percentCol = (200, 255, 200)
        else:
            percentCol = (255, 255, 255)
        #---------------------------------------
        self.rect = pygame.draw.rect(window, (150, 150, 205), pygame.Rect(boxCoor, boxSize))
        self.nameText = Text(nameText, coor=(self.x + 5, self.y + 5))
        self.descText = Text(descText, 24, (self.x + 5, self.y + 30), (200, 200, 200))
        self.percentText = Text(str(percentage * 100) + '%', 20, (self.x + self.w - 40, self.y + 5), color=(percentCol))
    def update(self):
        self.nameText.update()
        self.descText.update()
        self.percentText.update()
    def isMouseHovering(self, coor:tuple=(0, 0)):
        return self.rect.collidepoint(coor)

# Load fishes -----------------

cod = Fish((10, 10), (480, 50), "Cod", "Your basic fish.")

# Some define functions -------

def pygameEvents():
    global run, mouseCoor, isMouseHeld
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseCoor = pygame.mouse.get_pos()
            isMouseHeld = True
            if event.button == 1: # left button
                # do stuff
                pass
        if event.type == pygame.MOUSEBUTTONUP:
            isMouseHeld = False
        if event.type == pygame.KEYDOWN:
            pass

def updateDisplay():
    cod.update()
    # ---------------------
    pygame.display.flip()
    clock.tick(30)

# Main loop -------------------

while run:
    # do stuff
    pygameEvents()
    updateDisplay()

pygame.quit()