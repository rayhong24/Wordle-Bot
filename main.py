from class_game import Game
from class_wordle_bot import Wordle_bot

while True:
    print("Starting wordle game...")
  
    bot = Wordle_bot
  
    bot.play()
  
    cont = input("Enter 1 to play again. Enter 0 to end program.")
  
    if cont == '0':
        break
  
  
  
