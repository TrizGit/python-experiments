# Rename batches of files easily.
# Though, it only works when you have filenames that looks like this: no. (#).mp3

import os, sys

def checkLength(text:str):
    return text[5:6+(len(text)-11)]
    
def checkLengthInt(text:str):
    return int(text[5:6+(len(text)-11)])
    
def numberCheck(text:str):
    if text.isdigit:
        return True
    else:
        return False
    
def cancelableInput(prompt:str, on_exit:str):
    try:
        input(prompt + ' || Ctrl+C to exit.\n')
    except KeyboardInterrupt:
        sys.exit(on_exit)
    
filepath = 'F:\\confidential evidance\\musicPL'

while True:
    listed_files = []
    files = os.listdir(filepath)
    for a in ['Playlists', 'desktop.ini', 'script']:
        files.remove(a)
    min_num = len(files)
    max_num = 0
    canContinue = False
    for file in files:
        if checkLengthInt(file) > max_num:
            max_num = checkLengthInt(file)
        if checkLengthInt(file) < min_num:
            min_num = checkLengthInt(file)

    # print(files)
    # print(f'{min_num} | {max_num}')

    try:
        num1 = int(input('Select the first range.\n> '))
        num2 = int(input('Select the second range.\n> '))
        spacing = int(input('How much would you like to move those range by?\n> '))
        canContinue = True
    except Exception as e:
        print(f'nope! [{e}] | Let\'s try that again.')
    
    if canContinue:
        if num2 > max_num:
            num2 = max_num
        elif num2 < min_num:
            num2 = min_num
        if num1 < min_num:
            num1 = min_num
        elif num1 > max_num:
            num1 = max_num
        if num1 > num2: # type: ignore
            num1 = num2
        
        for i in range(num1, num2 + 1):
            listed_files.append(f'no. ({i}).mp3')
            print(f'no. ({i}).mp3 -> no. ({i + spacing}).mp3')
        
        cancelableInput('Confirm?', 'Canceled')

        if spacing > 0:
            listed_files.reverse()
        for file in listed_files:
            try:
                os.rename(f'{filepath}\\{file}', f'{filepath}\\no. ({str(checkLengthInt(file) + spacing)}).mp3') # type: ignore
                print(f'{file} -> no. ({str(checkLengthInt(file) + spacing)}).mp3')
            except Exception as e:
                print(f'nope! [{e}] | Skipping...')
    
        cancelableInput('Again? || Enter to continue.', 'Exiting...')