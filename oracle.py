# This program will guess Wordle five-letter words based on available inputs

import sys

my_dictionary = open('common.txt')
my_list = []
for lines in my_dictionary:
    for words in lines.split():
        my_list.append(words)


def filter_incorrect(guess, correctness, possibilities):
    incorrect_letters = []
    x = 0
    for letters in guess:
        if correctness[x] == 'incorrect':
            incorrect_letters.append(letters)
        x += 1

    if incorrect_letters:
        end = False
        for words in list(possibilities):
            for letters in incorrect_letters:
                if letters in list(words) and not end:
                    possibilities.remove(words)
                    end = True
            end = False

    return possibilities


def filter_position(guess, correctness, possibilities):
    position_letters = []
    x = 0
    for letters in guess:
        if correctness[x] == 'position':
            position_letters.append(letters)
            position_letters.append(x)
        x += 1

    if position_letters:
        for x in range(0, len(position_letters), 2):
            for words in list(possibilities):
                if position_letters[x] not in list(words):
                    possibilities.remove(words)
                if position_letters[x] == list(words)[position_letters[x + 1]]:
                    possibilities.remove(words)

    return possibilities

def weighting(possibilities):
    new_array = []
    mydict = {'a':2, 'b':0, 'c':0, 'd':0, 'e':2, 'f':0, 'g':0, 'h':0, 'i':2, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':2, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':2, 'v':0, 'w':0, 'x':0, 'y':1, 'z':0}
    for words in possibilities:
        x = 0
        for letter in list(words):
            x = x+mydict[letter]
        if x > 2:
            new_array.append(words)

    for words in new_array:
        if words in possibilities:
            possibilities.remove(words)

    new_array = new_array+possibilities

    for words in list(new_array):
        #find double letters in word
        for letters in list(words):
            if words.count(letters) > 1:
                new_array.append(new_array.pop(new_array.index(words)))

    return new_array



def filter_correct(guess, correctness, possibilities):
    correct_letters = []
    x = 0
    for letters in guess:
        if correctness[x] == 'correct':
            correct_letters.append(letters)
            correct_letters.append(x)
        x += 1

    if correct_letters:
        for x in range(0, len(correct_letters), 2):
            for words in list(possibilities):
                if correct_letters[x] != list(words)[correct_letters[x + 1]]:
                    possibilities.remove(words)

    return possibilities


possibilities = my_list

guess = ['a']

while guess!=['e','n','d']:

    guess = list(input('Enter a five-letter word: '))
    correctness = list(input('Enter the correctness of each letter: '))

    for y in range(0, len(correctness)):
        if correctness[y] == 'b':
            correctness[y] = 'incorrect'
        elif correctness[y] == 'y':
            correctness[y] = 'position'
        elif correctness[y] =='g':
            correctness[y] = 'correct'

    print(guess)
    print(correctness)

    skip_filter_incorrect = False
    x=0
    save_double_letters = []
    for letters in guess:
        #check double letters
        if guess.count(letters) > 1:
            save_double_letters.append(letters)
            save_double_letters.append(x) #save position of double letters
        x += 1
    if save_double_letters:
        for x in range(0, len(save_double_letters)-2, 2):
            if save_double_letters[x] in save_double_letters[x+2:]:
                if save_double_letters[x+1] != save_double_letters[x+3]:
                    if correctness[x+1] == 'incorrect' or correctness[x+3] == 'incorrect':
                        skip_filter_incorrect = True

    if not skip_filter_incorrect:
        possibilities = filter_incorrect(guess, correctness, possibilities)
    possibilities = filter_position(guess, correctness, possibilities)
    possibilities = filter_correct(guess, correctness, possibilities)
    possibilities = weighting(possibilities)

    print(possibilities)


