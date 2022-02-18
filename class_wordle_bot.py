import numpy as np
from collections import Counter
import time
from math import log


class Wordle_bot:
    def __init__(self):
        self.allowed_guesses = set()
        self.possible_ans = set()
        
        words_file = open("wordle_list.txt", "r")
        
        for line in words_file:
            self.allowed_guesses.add(str(line)[:5])
            self.possible_ans.add(str(line)[:5])
            
        self.patterns_dict = {}
    
    def play(self):
        words_guessed = 0
    
        while True:
            words_guessed += 1
            
            guess = input("Enter your guess: ").lower()
            
            while guess not in self.allowed_guesses:
                print("Invalid word. Try again")
                guess = input("Enter your guess: ")
            
            values = input("Enter the values of your guess: ")
            
            while len(values) != 5 or not values.isnumeric():
                print("Invald values given. Try again")
                values = input("Enter the values of your guess: ")
                
            if (all(i == '2' for i in values)):
                print("You win! It took you %s guesses." % words_guessed)
                return words_guessed
                
            self.prune(guess, [int(i) for i in values])
            
            self.generate_guess_iter()
            
    # compares the run time of using a dictionary to store the patterns vs computing it every time.
    def test_times(self):
        while True:
            guess = input("Enter your guess: ").lower()
            
            while guess not in self.allowed_guesses:
                print("Invalid word. Try again")
                guess = input("Enter your guess")

            values = input("Enter the values of your guess: ")
            
            while len(values) != 5 or not values.isnumeric():
                print("Invald values given. Try again")
                values = input("Enter the values of your guess: ")
                
            self.prune(guess, [int(i) for i in values])
            
            start_time_f_set = time.time()
            self.generate_guess_f_set()
            print("f_set time: %s" % (time.time() - start_time_f_set))

            start_time_iter = time.time()
            self.generate_guess_iter()
            print("iter time: %s" % (time.time() - start_time_iter))

            
    def generate_guess_f_set(self):
        # Stores the expected bits of each possible guess word
        guess_bits = {}
        

        for guess_cand in self.allowed_guesses:
            letter_values_counts = Counter()

            for possible_answer in self.possible_ans:
                ans_letters = Counter(possible_answer)
                
                f_set = tuple([guess_cand, possible_answer])
                
                if f_set not in self.patterns_dict:
                    pattern = ['0'] * 5
                    
                    for i, letter in enumerate(guess_cand):
                        if possible_answer[i] == guess_cand[i]:
                            pattern[i] = '2'
                            ans_letters[letter] -= 1

                    for i, letter in enumerate(guess_cand):
                        if ans_letters[letter] > 0 and possible_answer[i] != guess_cand[i]:
                            pattern[i] = '1'
                            ans_letters[letter] -= 1
                    
                    self.patterns_dict[f_set] = "".join(pattern)
                
                letter_values_counts[self.patterns_dict[f_set]] += 1
            if flag:
                print()
                print(self.patterns_dict)
                print()
                print(guess_cand)
                l = [[key, val] for key, val in letter_values_counts.items()]
                l.sort(key=lambda x: -x[1])
                
                print(l)
                flag = False
            
            # sum of p * -log(p, 2) for the bits of info
            s = 0
            
            for val in letter_values_counts.values():
                p = val/len(self.possible_ans)
                s += p * (-log(p, 2))
                
            guess_bits[guess_cand] = s
            
        guess_list = [(key, value) for key, value in guess_bits.items()]
        
        guess_list.sort(key=lambda x:-guess_bits[x[0]])
        
        if len(self.possible_ans) <= 5:
            print(self.possible_ans)
        else:
            print(guess_list[:5])
            
        return guess_list[:5]
    
    def generate_guess_iter(self):
        guess_bits = {}

        for guess_cand in self.allowed_guesses:
            letter_values_counts = Counter()

            for possible_answer in self.possible_ans:
                ans_letters = Counter(possible_answer)
                
                pattern = ['0'] * 5
                
                for i, letter in enumerate(guess_cand):
                    if possible_answer[i] == guess_cand[i]:
                        pattern[i] = '2'
                        ans_letters[letter] -= 1

                    for i, letter in enumerate(guess_cand):
                        if ans_letters[letter] > 0 and possible_answer[i] != guess_cand[i]:
                            pattern[i] = '1'
                            ans_letters[letter] -= 1
                    
                
                letter_values_counts["".join(pattern)] += 1
                
            # sum of p * -log(p, 2) for the bits of info
            s = 0
            
            for val in letter_values_counts.values():
                p = val/len(self.possible_ans)
                s += p * (-log(p, 2))
                
            guess_bits[guess_cand] = s
            
        guess_list = [(key, value) for key, value in guess_bits.items()]
        
        guess_list.sort(key=lambda x:-guess_bits[x[0]])
        
        if len(self.possible_ans) <= 5:
            print(self.possible_ans)
        else:
            print(guess_list[:5])
            
        return guess_list[:5]
    
    def prune(self, guess, pattern):
        letters_not_in = set()
        
        green_inds = []
        yellow_letters = set()
        grey_letters = set()
        
        for i in range(len(pattern)):
            # Checks for letters in the right place
            if pattern[i] == 2:
                green_inds.append(i)
            # Checks for right letters in the wrong place
            elif pattern[i] == 1:
                yellow_letters.add(guess[i])
            
            # Checks for letters not in the answer.    
            if pattern[i] == 0 and guess.count(guess[i]) == 1:
                grey_letters.add(guess[i])
        
        new = set()
        
        # Eliminates words from possible answers set
        for word in self.possible_ans:
            valid_guess = True
            
            # Makes sure words have green letters in the right place
            for i in green_inds:
                if word[i] != guess[i]:
                    valid_guess = False
            
            # Makes sure words contain the yellow letters
            for letter in yellow_letters:
                if letter not in word:
                    valid_guess = False
                    
            # Makes sure words do not have yellow letters in the same place
            for i in range(len(pattern)):
                if pattern[i] == 1 and guess[i] == word[i]:
                    valid_guess = False
            
            # Makes sure words do not contain grey letters
            for letter in grey_letters:
                if letter in word:
                    valid_guess = False
                    
            if valid_guess:
                new.add(word)
        
        self.possible_ans = new
        
        print("There are %s possible words left." % len(self.possible_ans))
        
        if len(self.possible_ans) == 8:
            self.allowed_guesses = self.possilbe_ans
            
        
            
            
                
        