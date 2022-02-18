# Wordle-Bot

This project will suggest different words to guess that will maximize the amount of information you gain in the game Wordle. It uses some information theory concepts similar to those discussed in the 3blue1brown video (https://www.youtube.com/watch?v=v68zYyaEmEA&t=0s). 

## How to Use

First you have to input the word that you used for your first wordle guess. The top five first guesses are as follows (in order of best to worst).
1. tares
2. lares
3. rales
4. rates
5. teras

After, the program will prompt you to enter the associated pattern. 0 corresponds to a grey square, 1 corresponds to a yellow square, and 2 corresponds to a green square. Your input for this pattern should consist of 5 digits all of which are either 0, 1, or 2. 

For example, if the pattern was all grey (all letters guessed are not in the answer word), you would input 00000 into the program.

If the pattern consisted of all yellow letters (all the letters are in the answer word but in the wrong spot), you would input 11111.

00022 would mean the first three letters are grey and the last two are green.

Once these two are the program will print how many possible words remain in the list of possible answers. Based on this reduced set of words, the program will calculate and print out the top five guesses and their associated "bit" values (discussed in more detail below).



