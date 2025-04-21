# on Module 6 Lesson 3-5
# (it's just a mix of english and indonesian, i regret picking bilingual.)

import pygame, time
from random import randint

# initialize
pygame.init()

# some pygame vars
bg = (200, 255, 255)
jendela = pygame.display.set_mode((500, 500))
jendela.fill(bg)
clock = pygame.time.Clock()

# classes
class Area():
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.fill_color = color
    def color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(jendela, self.fill_color, self.rect)
    def outline(self, frame_color, thickness):
        pygame.draw.rect(jendela, frame_color, self.rect, thickness)
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
class Label(Area):
    def setText(self, text, fSize, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fSize).render(text, True, text_color)
    def draw(self, shift_x, shift_y):
        self.fill()
        jendela.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

# more vars
cardList = []
numCards = 4
x = 70
for i in range(numCards):
    newCard = Label(x + (i * 100), 170, 70, 100, (255, 255, 0))
    newCard.outline((0, 0, 100), 10)
    newCard.setText("KLIK", 32)
    cardList.append(newCard)
wait = 0

# tulisan timer
timer_text = Label(0, 0, 50, 50, bg)
timer_text.setText('Timer:', 40, (0, 0, 100))
timer_text.draw(20, 20)
 
# angka timer
timer = Label(50, 55, 50, 40, bg)
timer.setText('0', 40, (0, 0, 100))
timer.draw(0, 0)
 
#tulisan score
score_text = Label(380, 0, 50, 50, bg)
score_text.setText('Score:', 40, (0, 0, 100))
score_text.draw(20, 20)
 
# angka score
score = Label(430, 55, 50, 50, bg)
score.setText('0', 40, (0, 0, 100))
score.draw(0, 0)

start_time = time.time()
cur_time = start_time
point = 0

while True:
    if wait == 0:
        wait = 20
        click = randint(0, numCards - 1)
        for i in range(numCards):
            cardList[i].color((255, 255, 0))
            if i == click:
                cardList[i].draw(10, 40)
            else:
                cardList[i].fill()
    else:
        wait -= 1
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(numCards):
                if cardList[i].collidepoint(x, y):
                    if i == click:
                        cardList[i].color((0, 255, 51))
                        point += 1
                    else:
                        cardList[i].color((255, 0, 0))
                        point -= 1
                    cardList[i].fill()
                    score.setText(str(point), 40, (0, 0, 100))
                    score.draw(0, 0)

    new_time = time.time()
    if new_time - start_time >= 11:
        lose = Label(0, 0, 500, 500, (255, 0, 0))
        lose.setText('WAKTU HABIS!!!', 60, (0, 0, 100))
        lose.draw(100, 100)
        break
    if int(new_time) - int(cur_time) == 1:
        timer.setText(str(int(new_time - start_time)), 40, (0, 0, 100))
        timer.draw(0, 0)
        cur_time = new_time
    if point >= 5:
        win = Label(0, 0, 500, 500, (200, 255, 200))
        win.setText('ANDA MENANG!!!', 60, (0, 0, 100))
        win.draw(100, 100)
        result = Label(90, 200, 250, 250, (200, 255, 200))
        result.setText('Waktu anda menyelesaikan permainan: ' + str(int(new_time - start_time)) + ' detik', 20, (0, 0, 100))
        result.draw(0, 0)
        break

    pygame.display.update()
    clock.tick(40)
pygame.display.update()