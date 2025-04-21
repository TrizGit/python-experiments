# A cli game about... well, gambling.
# Play type : Random Chance
# (This script was heavily modified.)

from time import sleep as wait # i like it better when it's like lua
from random import randint
from random import choice as randchoise # bad name choise

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
    print('Spinning...')
    wait(2)

def spin():
    global symbol1, symbol2, symbol3, loop1, loop2, loop3
    loop1 = randchoise([300, 400, 500, 600, 700])
    loop2 = loop1 + 100
    loop3 = loop2 + 100
    
    print()
    while loop3 > 0:
        if loop1 > 0:
            symbol1 = randchoise(symbols)
            loop1 -= 1
        if loop2 > 0:
            symbol2 = randchoise(symbols)
            loop2 -= 1
        symbol3 = randchoise(symbols)
        loop3 -= 1

        print(f'|{symbol1}|{symbol2}|{symbol3}|', end='\r')
        wait(0.05)
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
                jackpot = randint(100000, 10000000) + draws
                print(f'You got: ${jackpot}     ', end='\r')
                wait(0.005)
        else:
            print('JACKPOT!')
            wait(3)
            for i in range(160):
                jackpot = randint(10000, 100000) + draws
                print(f'You got: ${jackpot}     ', end='\r')
                wait(0.005)
        wait(3)
        print()
        change(jackpot)
        cost -= 1000
        mult += 1
    elif symbol1 == symbol2 or symbol2 == symbol3 or symbol3 == symbol1:
        changes = randint(100, 999) + draws
        if symbol1 == '$' or symbol2 == '$':
            changes += randint(10, 100) * 2
        print(f'Two of a kind! (Get ${changes})     ')
        wait(3)
        change(changes)
    else:
        print('You get nothing :(')
        wait(3)

print(f'Here\'s how it works:\n1. Machine usage starts at ${cost * -1}.\n2. When you draw, you have chance to win or lose.\n3. Everything is random.\n4. Any matches count as a win.\n5. Tax causes the machine to increase $25 after every spin.\n6. You start at ${money}.\n7. Be careful: after getting a jackpot, machine cost will raise by $1000 and the increments will double.\nAre you ready?')
wait(10)
print()
for i in range(4):
    if not i == 3:
        print(f'Too late! {3 - i}...', end='\r')
    else:
        print('Start!', ' ' * 30, end='\r')
    wait(1)

while money >= cost * -1:
    # draws = 4 # comment
    newDraw()
    spin()
    match()
    if money < cost * -1:
        break
    cost -= 25 * mult
        
print('#' * 20,'\nno more gambling\nyou\'ve done it', draws, 'times')
wait(2)
print('Final machine cost: ', end='', flush=True)
wait(4)
print("$" + str(cost * -1), flush=True)
wait(1)
for i in range(11):
    print("Quitting in", 10 - i, 'seconds...    ', end='\r')
    wait(1)
print('Quitting...', " " * 20)
wait(randint(1, 3))