
import random
number = random.randint(0,10)
tries = 5
while tries > 0:
  guess = int(input("Guess: "))
  if number > guess:
    print("Guess higher.")
    tries = tries - 1
    print("You got " + str(tries) + " tries left.")
  elif number < guess:
    print("Guess lower.")
    tries = tries - 1
    print("You got " + str(tries) + " tries left.")
  else:
    print("You got it!")
    break
