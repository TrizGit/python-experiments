# A cli game about... well, gambling.
# (This script was heavily modified.)

from time import sleep as wait # i like it better when it's like lua
import random

symbols = [
    '!',
    '@',
    '#',
    '$',
    '%',
    '^',
    '&',
    '*'
]
symbol1 = ''
symbol2 = ''
symbol3 = ''

money = 2000
mult = 1
cost = -100
changes = 0
draws:int = 0

def newDraw():
    global draws, money
    draws += 1
    print('#' * 20, '\nDraw', draws, ' ' * 30)
    wait(3)
    print('\nMoney:', '$' + str(money), ' ' * 30, end='\r')
    wait(1)
    print('Money:', '$' + str(money), '($' + str(cost) + ')' ,' ' * 30, end='\r')
    wait(1)
    money += cost
    print('Money:', '$' + str(money), ' ' * 30)
    wait(1)

def spin():
    global symbol1, symbol2, symbol3, loop1, loop2, loop3
    loop1 = random.randint(2, 6) * 100
    loop2 = loop1 + 100
    loop3 = loop2 + 100
    
    print()
    while loop3 > 0:
        if loop1 > 0:
            symbol1 = random.choice(symbols)
            loop1 -= 1
        if loop2 > 0:
            symbol2 = random.choice(symbols)
            loop2 -= 1
        symbol3 = random.choice(symbols)
        loop3 -= 1

        print(f'|{symbol1}|{symbol2}|{symbol3}|', end='\r')
        wait(0.005)
    print()
    wait(2)

def change(counts:int):
    global money
    print('\nMoney:', '$' + str(money), ' ' * 30, end='\r')
    wait(1)
    print('Money:', '$' + str(money), '($' + str(counts) + ')' ,' ' * 30, end='\r')
    wait(1)
    money += counts
    print('Money:', '$' + str(money), ' ' * 30)
    wait(1)

def match():
    global cost, mult
    if symbol1 == symbol2 and symbol2 == symbol3 and symbol3 == symbol1:
        if symbol1 == '$':
            print('SUPER JACKPOT!!!1!1')
            wait(3)
            for i in range(160):
                jackpot = random.randint(1000000, 99999999) + (draws * 100 * mult)
                print(f'You got: ${jackpot}     ', end='\r')
                wait(0.005)
            cost -= jackpot % 100000
            mult += 2
        else:
            print('JACKPOT!')
            wait(3)
            for i in range(160):
                jackpot = random.randint(10000, 999999) + (draws * 10 * mult)
                print(f'You got: ${jackpot}     ', end='\r')
                wait(0.005)
            cost -= jackpot % 1000
            mult += 1
        wait(3)
        print()
        change(jackpot)
    elif symbol1 == symbol2 or symbol2 == symbol3 or symbol3 == symbol1:
        changes = random.randint(100, 999) + draws
        if symbol1 == '$' or symbol2 == '$':
            changes += random.randint(10, 100) * 10
        print(f'Two of a kind! (Get ${changes})     ')
        wait(3)
        change(changes)
    else:
        print('You get nothing :(')
        wait(3)

while money >= cost * -1:
    # draws = 4 # comment
    newDraw()
    spin()
    match()
    if money < cost * -1:
        break
    cost -= random.randint(20, 25) * mult
        
print('#' * 20,'\nno more gambling\nyou\'ve done it', draws, 'times')
wait(2)
print('Final machine cost: ', end='', flush=True)
wait(3)
print("$" + str(cost * -1), flush=True)
wait(1)
for i in range(11):
    print("Quitting in", 10 - i, 'seconds...    ', end='\r')
    wait(1)
print('Quitting...', " " * 20)
wait(random.random() * 3)