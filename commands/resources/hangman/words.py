import random


def getWord():
    with open('commands/resources/hangman/words.txt', 'r') as words:
        line = next(words)
        for num, aline in enumerate(words, 2):
            if random.randrange(num):
                continue
            line = aline
        return line
