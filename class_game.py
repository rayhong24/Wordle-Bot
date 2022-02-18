import numpy as np
from collections import Counter
import time


class Game:
    def __init__(self):
        self.all_words = set()
        
        all_words_file = open("wordle_list.txt", "r")
        possible_answers_file = open("possible_words.txt", "r")
        
        for line in all_words_file:
            self.all_words.add(str(line)[:-1])
            
        possible_answers = []
        for line in possible_answers_file:
            possible_answers.append(str(line)[:-1])
            
        
        self.guesses = 0
        
        self.winning_word = np.random.choice(possible_answers)
        
    def play(self):
        guesses = 0
        
        while True:
            letter_values = self.guess(input("Enter a five letter word. "))
            
            if not letter_values:
                print("That is not a word in the list. Try again")
            else:
                guesses += 1
                
                if sum(letter_values) == 10:
                    print("You win! The word was: ", self.winning_word)
                    return guesses
                elif guesses == 6:
                    print("You lose! The word was: ", self.winning_word)
                    return inf
                else:
                    print(letter_values)
                    
            
                    
                
                
    def guess(self, word):
        if word not in self.all_words:
            print("Not a word in the list")
            return []
        elif word == self.winning_word:
            print("You win!")
            return [2] * 5
        
        c = Counter(self.winning_word)
        letter_values = [0] * 5
        
        for i, letter in enumerate(word):
            if self.winning_word[i] == word[i]:
                letter_values[i] = 2
                c[letter] -= 1
                
        for i, letter in enumerate(word):
            if c[letter] > 0 and word[i] != self.winning_word[i]:
                letter_values[i] = 1
                c[letter] -= 1
                
                
        return letter_values