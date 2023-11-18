# Import required modules / files
print("Importing modules / files. . .")
try:
    from pynput import keyboard
    from random import shuffle,random
    from time import sleep as sl
    longdictionary = open("longdictionary.txt", "rb")
    shortdictionary = open("shortdictionary.txt", "rb")
except ModuleNotFoundError:
    print("Missing modules!")
    quit()
print("Finished importing modules and files.\n")

#speed = int(input("Enter an average WPM to complete a word.\n"))

def chooseDictionary():
    selDictionary = input("Welcome! Please select the dictionary you would like to use.\n1. Long words (34 - 16 characters)\n2. Short(er) words (15 - 4)\n3. All words\n").lower()
    if selDictionary in ["1", "1.", "long", "l"] :
        return "long"
    elif selDictionary in ["2", "2.", "short", "s"]:
        return "short"
    elif selDictionary in ["3", "3.", "all", "a"]:
        return "all"
    else:
        print("\n")
        for i in range(3):
            print("Invalid option.")
        print("\n")
        sl(3)
        chooseDictionary()

def loadDict():
    wordlist = []
    dictionary = chooseDictionary()
    print("loading wordlists and building arrays. . .")
    if dictionary == "all":
        wordlist.append([i.lower().strip("\n") for i in open("longdictionary.txt", "r").readlines()])
        wordlist.append([i.lower().strip("\n") for i in open("shortdictionary.txt", "r").readlines()])
        wordlist = wordlist[0] + wordlist[1]
    elif dictionary == "short":
        wordlist.append([i.lower().strip("\n") for i in open("shortdictionary.txt", "r").readlines()])
        wordlist = wordlist[0]
    else:
        wordlist.append([i.lower().strip("\n") for i in open("longdictionary.txt", "r").readlines()])
        wordlist = wordlist[0]
    shuffle(wordlist)
    return wordlist

wordlist = loadDict()
blacklist = []

def inputLetters():
    words = []
    letters = input("Enter the letters required to complete your turn!\n").lower()
    for i in wordlist:
        if len(words) > 3:
            break
        if i.__contains__(letters) and not i in blacklist:
            words.append(i)
    return words

def findWords():
    wL = inputLetters()
    print("\n\nF10: Back to choose letters\n")
    for i in range(len(wL)):
        print(f"F{i+5}: {wL[i]}")
    return wL

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

keypress = -1

def on_release(key):
    global keypress
    print('{0} released'.format(
        key))
    if key == keyboard.Key.f10:
        # Stop listener
        keypress = -1
        return False
    elif key == keyboard.Key.f5:
        keypress = 0
        return False
    elif key == keyboard.Key.f6:
        keypress = 1
        return False
    elif key == keyboard.Key.f7:
        keypress = 2
        return False
    elif key == keyboard.Key.f8:
        keypress = 3
        return False

def printWord(w2p:str):
    kb = keyboard.Controller()
    for i in w2p:
        kb.press(f"{i}")
        sl(0.05)
        kb.release(f"{i}")
        rand = random()
        sl(0.1 * rand)
    kb.press(keyboard.Key.enter)
    
def activateType(wL:list = []):
    if len(wL) == 0:
        wL = findWords()
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    if not keypress == -1:
        blacklist.append(wL[keypress])
        printWord(wL[keypress])
        activateType(wL)
    else:
        wL = []
        activateType()

activateType()