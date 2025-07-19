# mini balatro incoming.

import time
import random
import sys
import keyboard

# ♠♥♦♣
class HandType():
    def __init__(self, name:str, base_chip:float=10.0, base_mult:float=1.0):
        self.name = name
        self.base_chip = base_chip
        self.base_mult = base_mult

class Card():
    def __init__(self, name:str='Blank', code:int=0, score:float=0.0, mods:list=[]):
        self.name = name
        self.code = code
        self.score = score
        self.mods = mods
        self.pointed = False
        self.selected = False

# i have no idea how to do this, so enjoy this mess for now
# spades
spade_A = Card('♠ A', 0, 11.0)
spade_2 = Card('♠ 2', 1, 2.0)
spade_3 = Card('♠ 3', 2, 3.0)
spade_4 = Card('♠ 4', 3, 4.0)
spade_5 = Card('♠ 5', 4, 5.0)
spade_6 = Card('♠ 6', 5, 6.0)
spade_7 = Card('♠ 7', 6, 7.0)
spade_8 = Card('♠ 8', 7, 8.0)
spade_9 = Card('♠ 9', 8, 9.0)
spade_10 = Card('♠ 10', 9, 10.0)
spade_J = Card('♠ J', 10, 10.0)
spade_Q = Card('♠ Q', 11, 10.0)
spade_K = Card('♠ K', 12, 10.0)
# hearts
heart_A = Card('♥ A', 0, 11.0)
heart_2 = Card('♥ 2', 1, 2.0)
heart_3 = Card('♥ 3', 2, 3.0)
heart_4 = Card('♥ 4', 3, 4.0)
heart_5 = Card('♥ 5', 4, 5.0)
heart_6 = Card('♥ 6', 5, 6.0)
heart_7 = Card('♥ 7', 6, 7.0)
heart_8 = Card('♥ 8', 7, 8.0)
heart_9 = Card('♥ 9', 8, 9.0)
heart_10 = Card('♥ 10', 9, 10.0)
heart_J = Card('♥ J', 10, 10.0)
heart_Q = Card('♥ Q', 11, 10.0)
heart_K = Card('♥ K', 12, 10.0)
# diamonds
diamond_A = Card('♦ A', 0, 11.0)
diamond_2 = Card('♦ 2', 1, 2.0)
diamond_3 = Card('♦ 3', 2, 3.0)
diamond_4 = Card('♦ 4', 3, 4.0)
diamond_5 = Card('♦ 5', 4, 5.0)
diamond_6 = Card('♦ 6', 5, 6.0)
diamond_7 = Card('♦ 7', 6, 7.0)
diamond_8 = Card('♦ 8', 7, 8.0)
diamond_9 = Card('♦ 9', 8, 9.0)
diamond_10 = Card('♦ 10', 9, 10.0)
diamond_J = Card('♦ J', 10, 10.0)
diamond_Q = Card('♦ Q', 11, 10.0)
diamond_K = Card('♦ K', 12, 10.0)
# clubs
club_A = Card('♣ A', 0, 11.0)
club_2 = Card('♣ 2', 1, 2.0)
club_3 = Card('♣ 3', 2, 3.0)
club_4 = Card('♣ 4', 3, 4.0)
club_5 = Card('♣ 5', 4, 5.0)
club_6 = Card('♣ 6', 5, 6.0)
club_7 = Card('♣ 7', 6, 7.0)
club_8 = Card('♣ 8', 7, 8.0)
club_9 = Card('♣ 9', 8, 9.0)
club_10 = Card('♣ 10', 9, 10.0)
club_J = Card('♣ J', 10, 10.0)
club_Q = Card('♣ Q', 11, 10.0)
club_K = Card('♣ K', 12, 10.0)

# list every card as one giant list
spades = [spade_A, spade_2, spade_3, spade_4, spade_5, spade_6, spade_7, spade_8, spade_9, spade_10, spade_J, spade_Q, spade_K]
hearts = [heart_A, heart_2, heart_3, heart_4, heart_5, heart_6, heart_7, heart_8, heart_9, heart_10, heart_J, heart_Q, heart_K]
diamonds = [diamond_A, diamond_2, diamond_3, diamond_4, diamond_5, diamond_6, diamond_7, diamond_8, diamond_9, diamond_10, diamond_J, diamond_Q, diamond_K]
clubs = [club_A, club_2, club_3, club_4, club_5, club_6, club_7, club_8, club_9, club_10, club_J, club_Q, club_K]
all_suit = [spades, hearts, diamonds, clubs]

og_deck = [] # untouched unless a card was removed from the deck
cur_deck = []
cur_hand = []
selected = []
cur_pointed:Card
cur_pointed_index = 0
played = []

# list every hand type possible
High = HandType("High Card")
TwoPair = HandType("Two Pair", 20.0, 1.5)
Threes = HandType('Three of a Kind', 30.0, 2.0)
Fours = HandType('Four of a Kind', 40.0, 2.5)
Fives = HandType('Five of a Kind', 50.0, 2.5)
Straight = HandType('Straight', 60.0, 3.0)
Flush = HandType('Flush', 60.0, 3.0)
SFlush = HandType('Straight Flush', 100.0, 4.0)
RFlush = HandType('Royal Flush', 150.0, 5.0)

ante = 1
play = 1
required_score = 180
chip = 0.0
mult = 0.0
max_select = 5
max_hand = 8

answer:str = ''
additional_lines:int = 0

for suit in all_suit:
    for card in suit:
        og_deck.append(card)
        cur_deck.append(card)

def clear_line():
    """Clear lines"""
    print(' ' * 150, end='\r')

def flip_bool(bool:bool):
    """Flip a boolean"""
    if bool:
        return False
    elif not bool:
        return True

def cooldown(cd:float=1, cl:int=1):
    """Cooldown so no spammy"""
    print('\nCooldown...', end='\r')
    time.sleep(cd)
    for i in range(cl):
        clear_line()
        if i < cl - 1:
            print('\033[A', end='\r')

def move_pointer_up(num:int=1, ends:str='', clear_lines:bool=False, clear_curLine:bool=True):
    """Move the cursor up"""
    if clear_curLine:
        clear_line()
    for i in range(num):
        print('\033[A', end=ends)
        if clear_lines == True:
            clear_line()
def move_pointer_down(num:int=1, ends:str='', clear_lines:bool=False, clear_curLine:bool=True):
    """Move the cursor down"""
    if clear_curLine:
        clear_line()
    for i in range(num):
        print('\033[B', end=ends)
        if clear_lines == True:
            clear_line()
        
def awaitingInput(key:str, display:str='', delay:float=3.0):
    """Waiting for an input (uses keyboard module)"""
    global answer, detected_input
    if display == '':
        display = key.upper()
    if delay < 0.01:
        delay = 0.01
    if keyboard.is_pressed(key):
        for i in range(int(delay * 100)):
            if delay >= 0.1:
                print(f'Key pressed: {display} | Confirming in {round(delay - (i / 100), 2)}', end='\r')
            time.sleep(0.01)
            if not keyboard.is_pressed(key):
                move_pointer_up(num=0)
                break
            if i == int(delay * 100 - 1):
                answer = key
                detected_input = True

def move_pointed(index:int):
    """Change what card is currently pointed (indicated by > *card* <)"""
    global cur_pointed
    try:
        cur_pointed.pointed = False
    except Exception as E:
        pass
    cur_pointed = cur_hand[index]
    cur_pointed.pointed = True

    for num in range(len(cur_hand)):
        if cur_hand[num].pointed == True:
            print('> ', end='')
        print(cur_hand[num].name, end='')
        if cur_hand[num].pointed == True:
            print(' <', end='')

        if cur_hand[num].selected:
            print(' [X] ', end='')
        else:
            print(' ', end='')

        if num < len(cur_hand) - 1:
            print('| ', end='')

def check_deck():
    """Checks the current deck (unavailable yet)"""
    suit_lastshown = ''
    for card in cur_deck:
        suit_curshown = card.name[0]
        if suit_lastshown != suit_curshown:
            print()
        print(card.name, end=' ')
        suit_lastshown = card.name[0]

def modify_deck(add:Card, rem:Card):
    """Modifies the current deck (adding or removing card)"""
    global og_deck, cur_deck
    og_deck.append(add)
    cur_deck.append(add)
    og_deck.remove(rem)
    cur_deck.remove(rem)

def draw_card(card:Card):
    """Draw a card"""
    cur_deck.remove(card)
    cur_hand.append(card)

def new_round():
    """Start a new round"""
    while len(cur_hand) < max_hand:
        card_drawn = cur_deck[0]
        draw_card(card_drawn)

print(f'Round {play} | Ante {ante}\n')
time.sleep(3)
print(f'Required Score: {required_score}\n')
time.sleep(2)
random.shuffle(cur_deck)
print(f'Chips: {chip} | Mult: {mult}')
new_round()

move_pointed(cur_pointed_index)
print()
while True:
    detected_input = False
    awaitingInput('a', delay=0)
    awaitingInput('d', delay=0)
    awaitingInput('space', delay=0.5)
    awaitingInput('z')
    awaitingInput('x')
    if detected_input:
        move_pointer_up(1, clear_lines=True)

        if additional_lines >= 1:
            move_pointer_up(clear_lines=True)
            additional_lines = 0

        if answer == 'a':
            if cur_pointed_index == 0:
                cur_pointed_index = len(cur_hand) - 1
            else:
                cur_pointed_index -= 1
            move_pointed(cur_pointed_index)
            cooldown(0.5)
        elif answer == 'd':
            if cur_pointed_index == len(cur_hand) - 1:
                cur_pointed_index = 0
            else:
                cur_pointed_index += 1
            move_pointed(cur_pointed_index)
            cooldown(0.5)
        elif answer == 'space':
            if len(selected) >= max_select and cur_pointed.selected == False:
                move_pointed(cur_pointed_index)
                print("\nNope! You've reach the maximum cards selection.", end='')
                additional_lines = 1
            else:
                cur_pointed.selected = flip_bool(cur_pointed.selected)
                if cur_pointed.selected:
                    selected.append(cur_pointed)
                else:
                    selected.remove(cur_pointed)                
                move_pointed(cur_pointed_index)
            cooldown(1)